import asyncio
import time
from functools import cached_property
from typing import TYPE_CHECKING, Any, Awaitable, Callable, Dict, Mapping, Optional, TypeVar, Union

import httpx

from ._internal.api_client import MultipartFile
from ._internal.exceptions import BlindPayError
from ._internal.http import (
    DEFAULT_BASE_URL,
    DEFAULT_MAX_RETRIES,
    DEFAULT_TIMEOUT,
    HttpMethod,
    RequestOptions,
    api_root,
    body_read_failure,
    build_headers,
    encode_json,
    error_from_exception,
    error_from_response,
    exception_retry_delay,
    request_timeout,
    resolve_idempotency_key,
    response_retry_delay,
    success_from_response,
)
from ._version import __version__
from .resources.customers.customers import CustomersResource, CustomersResourceSync
from .resources.instances.instances import InstancesResource, InstancesResourceSync
from .resources.payins.payins import PayinsResource, PayinsResourceSync
from .types import BlindpayApiResponse
from .webhooks import DEFAULT_TOLERANCE_SECONDS, verify as verify_webhook

if TYPE_CHECKING:
    from blindpay.resources.available.available import AvailableResource, AvailableResourceSync
    from blindpay.resources.bank_accounts.bank_accounts import BankAccountsResource, BankAccountsResourceSync
    from blindpay.resources.custodial_wallets.custodial_wallets import (
        CustodialWalletsResource,
        CustodialWalletsResourceSync,
    )
    from blindpay.resources.fees.fees import FeesResource, FeesResourceSync
    from blindpay.resources.instances.onboarding import OnboardingResource, OnboardingResourceSync
    from blindpay.resources.limits.limits import LimitsResource, LimitsResourceSync
    from blindpay.resources.ownership.ownership import OwnershipResource, OwnershipResourceSync
    from blindpay.resources.partner_fees.partner_fees import PartnerFeesResource, PartnerFeesResourceSync
    from blindpay.resources.payables.payables import PayablesResource, PayablesResourceSync
    from blindpay.resources.payins.quotes import PayinQuotesResource, PayinQuotesResourceSync
    from blindpay.resources.payouts.payouts import PayoutsResource, PayoutsResourceSync
    from blindpay.resources.quotes.quotes import QuotesResource, QuotesResourceSync
    from blindpay.resources.rfi.rfi import (
        CustomerRfiResource,
        CustomerRfiResourceSync,
        InstanceRfiResource,
        InstanceRfiResourceSync,
    )
    from blindpay.resources.terms_of_service.terms_of_service import (
        TermsOfServiceResource,
        TermsOfServiceResourceSync,
    )
    from blindpay.resources.transfers.transfers import TransfersResource, TransfersResourceSync
    from blindpay.resources.upload.upload import UploadResource, UploadResourceSync
    from blindpay.resources.virtual_accounts.virtual_accounts import (
        VirtualAccountsResource,
        VirtualAccountsResourceSync,
    )
    from blindpay.resources.wallets.blockchain import BlockchainWalletsResource, BlockchainWalletsResourceSync
    from blindpay.resources.wallets.offramp import OfframpWalletsResource, OfframpWalletsResourceSync
    from blindpay.resources.webhooks.webhooks import WebhookEndpointsResource, WebhookEndpointsResourceSync

T = TypeVar("T")


def _options_kwarg(options: Optional[RequestOptions]) -> Dict[str, Any]:
    # Only pass options through when set, so _request keeps its (method, path, body) call shape.
    return {"options": options} if options else {}


def _with_legacy_v1_prefix(svix_signature: str) -> str:
    # Earlier versions of verify_webhook_signature only matched a bare base64 signature, so working integrations
    # strip the "v1," prefix themselves. Keep accepting that form here; blindpay.webhooks.verify stays strict.
    return svix_signature if "," in svix_signature else f"v1,{svix_signature}"


class ApiClientImpl:
    """Async HTTP layer: one shared ``httpx.AsyncClient``, retry rules from ``_internal/http.py``, ``asyncio.sleep``."""

    def __init__(
        self,
        base_url: str,
        headers: Dict[str, str],
        *,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout
        self.max_retries = max_retries
        self._owns_client = http_client is None
        self._client = http_client if http_client is not None else httpx.AsyncClient()
        self._sleep: Callable[[float], Awaitable[None]] = asyncio.sleep

    async def get(self, path: str) -> BlindpayApiResponse[T]:
        return await self._request("GET", path)

    async def post(
        self, path: str, body: Mapping[str, Any], options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[T]:
        return await self._request("POST", path, body, **_options_kwarg(options))

    async def put(
        self, path: str, body: Mapping[str, Any], options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[T]:
        return await self._request("PUT", path, body, **_options_kwarg(options))

    async def patch(
        self, path: str, body: Mapping[str, Any], options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[T]:
        return await self._request("PATCH", path, body, **_options_kwarg(options))

    async def delete(
        self, path: str, body: Optional[Mapping[str, Any]] = None, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[T]:
        return await self._request("DELETE", path, body, **_options_kwarg(options))

    async def post_multipart(
        self,
        path: str,
        data: Mapping[str, str],
        files: Mapping[str, MultipartFile],
        options: Optional[RequestOptions] = None,
    ) -> BlindpayApiResponse[T]:
        return await self._send("POST", path, data=data, files=files, options=options)

    async def _request(
        self,
        method: HttpMethod,
        path: str,
        body: Optional[Mapping[str, Any]] = None,
        options: Optional[RequestOptions] = None,
    ) -> BlindpayApiResponse[T]:
        return await self._send(method, path, json_body=body, options=options)

    async def _send(
        self,
        method: HttpMethod,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        data: Optional[Mapping[str, str]] = None,
        files: Optional[Mapping[str, MultipartFile]] = None,
        options: Optional[RequestOptions] = None,
    ) -> BlindpayApiResponse[T]:
        multipart = files is not None
        key = resolve_idempotency_key(method, options, multipart=multipart, max_retries=self.max_retries)
        content = encode_json(json_body) if json_body is not None else None
        request: Dict[str, Any] = {
            "headers": build_headers(self.headers, options, key, json_body=content is not None),
            "timeout": request_timeout(options, self.timeout),
        }
        if content is not None:
            request["content"] = content
        if multipart:
            request.update(data=data, files=files)
        url = f"{self.base_url}{path}"

        attempt = 0
        while True:
            try:
                built = self._client.build_request(method, url, **request)
            except Exception as error:  # a request that can't even be built is never retried
                return {"data": None, "error": error_from_exception(error, key, method)}
            try:
                response = await self._client.send(built, stream=True)
            except Exception as error:
                delay = exception_retry_delay(
                    error, method=method, idempotency_key=key, multipart=multipart, attempt=attempt
                )
                if delay is not None and attempt < self.max_retries:
                    await self._sleep(delay)
                    attempt += 1
                    continue
                return {"data": None, "error": error_from_exception(error, key, method)}

            try:
                await response.aread()
            except Exception as error:
                await response.aclose()
                delay, read_error = body_read_failure(
                    response, error, method=method, idempotency_key=key, multipart=multipart, attempt=attempt
                )
                if delay is not None and attempt < self.max_retries:
                    await self._sleep(delay)
                    attempt += 1
                    continue
                return {"data": None, "error": read_error}

            if response.is_success:
                return success_from_response(response, key)
            delay = response_retry_delay(
                response, method=method, idempotency_key=key, multipart=multipart, attempt=attempt
            )
            if delay is not None and attempt < self.max_retries:
                await self._sleep(delay)
                attempt += 1
                continue
            return {"data": None, "error": error_from_response(response, key, method)}

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()


class ApiClientImplSync:
    """Sync HTTP layer: one shared ``httpx.Client``, retries per ``_internal/http.py``, ``time.sleep`` backoff."""

    def __init__(
        self,
        base_url: str,
        headers: Dict[str, str],
        *,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.Client] = None,
    ):
        self.base_url = base_url
        self.headers = headers
        self.timeout = timeout
        self.max_retries = max_retries
        self._owns_client = http_client is None
        self.client = http_client if http_client is not None else httpx.Client()
        self._sleep: Callable[[float], None] = time.sleep

    def get(self, path: str) -> BlindpayApiResponse[T]:
        return self._request("GET", path)

    def post(
        self, path: str, body: Mapping[str, Any], options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[T]:
        return self._request("POST", path, body, **_options_kwarg(options))

    def put(
        self, path: str, body: Mapping[str, Any], options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[T]:
        return self._request("PUT", path, body, **_options_kwarg(options))

    def patch(
        self, path: str, body: Mapping[str, Any], options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[T]:
        return self._request("PATCH", path, body, **_options_kwarg(options))

    def delete(
        self, path: str, body: Optional[Mapping[str, Any]] = None, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[T]:
        return self._request("DELETE", path, body, **_options_kwarg(options))

    def post_multipart(
        self,
        path: str,
        data: Mapping[str, str],
        files: Mapping[str, MultipartFile],
        options: Optional[RequestOptions] = None,
    ) -> BlindpayApiResponse[T]:
        return self._send("POST", path, data=data, files=files, options=options)

    def _request(
        self,
        method: HttpMethod,
        path: str,
        body: Optional[Mapping[str, Any]] = None,
        options: Optional[RequestOptions] = None,
    ) -> BlindpayApiResponse[T]:
        return self._send(method, path, json_body=body, options=options)

    def _send(
        self,
        method: HttpMethod,
        path: str,
        *,
        json_body: Optional[Mapping[str, Any]] = None,
        data: Optional[Mapping[str, str]] = None,
        files: Optional[Mapping[str, MultipartFile]] = None,
        options: Optional[RequestOptions] = None,
    ) -> BlindpayApiResponse[T]:
        multipart = files is not None
        key = resolve_idempotency_key(method, options, multipart=multipart, max_retries=self.max_retries)
        content = encode_json(json_body) if json_body is not None else None
        request: Dict[str, Any] = {
            "headers": build_headers(self.headers, options, key, json_body=content is not None),
            "timeout": request_timeout(options, self.timeout),
        }
        if content is not None:
            request["content"] = content
        if multipart:
            request.update(data=data, files=files)
        url = f"{self.base_url}{path}"

        attempt = 0
        while True:
            try:
                built = self.client.build_request(method, url, **request)
            except Exception as error:  # a request that can't even be built is never retried
                return {"data": None, "error": error_from_exception(error, key, method)}
            try:
                response = self.client.send(built, stream=True)
            except Exception as error:
                delay = exception_retry_delay(
                    error, method=method, idempotency_key=key, multipart=multipart, attempt=attempt
                )
                if delay is not None and attempt < self.max_retries:
                    self._sleep(delay)
                    attempt += 1
                    continue
                return {"data": None, "error": error_from_exception(error, key, method)}

            try:
                response.read()
            except Exception as error:
                response.close()
                delay, read_error = body_read_failure(
                    response, error, method=method, idempotency_key=key, multipart=multipart, attempt=attempt
                )
                if delay is not None and attempt < self.max_retries:
                    self._sleep(delay)
                    attempt += 1
                    continue
                return {"data": None, "error": read_error}

            if response.is_success:
                return success_from_response(response, key)
            delay = response_retry_delay(
                response, method=method, idempotency_key=key, multipart=multipart, attempt=attempt
            )
            if delay is not None and attempt < self.max_retries:
                self._sleep(delay)
                attempt += 1
                continue
            return {"data": None, "error": error_from_response(response, key, method)}

    def close(self) -> None:
        if self._owns_client:
            self.client.close()


def _validate_settings(timeout: float, max_retries: int) -> None:
    if timeout <= 0:
        raise BlindPayError("timeout must be a positive number of seconds")
    if max_retries < 0:
        raise BlindPayError("max_retries must be 0 (no retries) or more")


class _InstancesNamespace(InstancesResource):
    """``InstancesResource`` plus its sub-resources, all visible to type checkers."""

    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        super().__init__(instance_id, api_client)
        self._api = api_client

    @cached_property
    def webhook_endpoints(self) -> "WebhookEndpointsResource":
        from blindpay.resources.webhooks.webhooks import create_webhook_endpoints_resource

        return create_webhook_endpoints_resource(self._instance_id, self._api)

    @cached_property
    def terms_of_service(self) -> "TermsOfServiceResource":
        from blindpay.resources.terms_of_service import create_terms_of_service_resource

        return create_terms_of_service_resource(self._instance_id, self._api)

    @cached_property
    def onboarding(self) -> "OnboardingResource":
        from blindpay.resources.instances.onboarding import create_onboarding_resource

        return create_onboarding_resource(self._instance_id, self._api)

    @cached_property
    def rfi(self) -> "InstanceRfiResource":
        from blindpay.resources.rfi.rfi import create_instance_rfi_resource

        return create_instance_rfi_resource(self._instance_id, self._api)


class _PayinsNamespace(PayinsResource):
    """``PayinsResource`` plus its sub-resources, all visible to type checkers."""

    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        super().__init__(instance_id, api_client)
        self._api = api_client

    @cached_property
    def quotes(self) -> "PayinQuotesResource":
        from blindpay.resources.payins.quotes import create_payin_quotes_resource

        return create_payin_quotes_resource(self._instance_id, self._api)


class _CustomersNamespace(CustomersResource):
    """``CustomersResource`` plus its sub-resources, all visible to type checkers."""

    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        super().__init__(instance_id, api_client)
        self._api = api_client

    @cached_property
    def bank_accounts(self) -> "BankAccountsResource":
        from blindpay.resources.bank_accounts.bank_accounts import create_bank_accounts_resource

        return create_bank_accounts_resource(self._instance_id, self._api)

    @cached_property
    def rfi(self) -> "CustomerRfiResource":
        from blindpay.resources.rfi.rfi import create_customer_rfi_resource

        return create_customer_rfi_resource(self._instance_id, self._api)


class _WalletsNamespace:
    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def blockchain(self) -> "BlockchainWalletsResource":
        from blindpay.resources.wallets.blockchain import create_blockchain_wallets_resource

        return create_blockchain_wallets_resource(self._instance_id, self._api)

    @cached_property
    def offramp(self) -> "OfframpWalletsResource":
        from blindpay.resources.wallets.offramp import create_offramp_wallets_resource

        return create_offramp_wallets_resource(self._instance_id, self._api)

    @cached_property
    def custodial(self) -> "CustodialWalletsResource":
        from blindpay.resources.custodial_wallets.custodial_wallets import create_custodial_wallets_resource

        return create_custodial_wallets_resource(self._instance_id, self._api)


class BlindPay:
    _api_key: str
    _instance_id: str
    _base_url: str

    def __init__(
        self,
        *,
        api_key: str,
        instance_id: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        if not api_key:
            raise BlindPayError("Api key not provided, get your api key on blindpay dashboard")

        if not instance_id:
            raise BlindPayError("Instance id not provided, get your instance id on blindpay dashboard")

        _validate_settings(timeout, max_retries)

        self._api_key = api_key
        self._instance_id = instance_id
        self._base_url = api_root(base_url)

        # No client-wide Content-Type: httpx sets application/json for JSON bodies and multipart/form-data
        # (with its boundary) for uploads. A fixed JSON Content-Type would break the multipart requests.
        self._headers = {
            "Accept": "application/json",
            "User-Agent": f"blindpay-python/{__version__}",
            "Authorization": f"Bearer {self._api_key}",
        }

        self._api = ApiClientImpl(
            self._base_url, self._headers, timeout=timeout, max_retries=max_retries, http_client=http_client
        )

    def __repr__(self) -> str:
        return f"BlindPay(instance_id={self._instance_id!r}, base_url={self._base_url!r}, api_key='***')"

    @cached_property
    def available(self) -> "AvailableResource":
        from blindpay.resources.available import create_available_resource

        return create_available_resource(self._api)

    @cached_property
    def instances(self) -> _InstancesNamespace:
        return _InstancesNamespace(self._instance_id, self._api)

    @cached_property
    def ownership(self) -> "OwnershipResource":
        from blindpay.resources.ownership import create_ownership_resource

        return create_ownership_resource(self._instance_id, self._api)

    @cached_property
    def partner_fees(self) -> "PartnerFeesResource":
        from blindpay.resources.partner_fees import create_partner_fees_resource

        return create_partner_fees_resource(self._instance_id, self._api)

    @cached_property
    def payins(self) -> _PayinsNamespace:
        return _PayinsNamespace(self._instance_id, self._api)

    @cached_property
    def quotes(self) -> "QuotesResource":
        from blindpay.resources.quotes import create_quotes_resource

        return create_quotes_resource(self._instance_id, self._api)

    @cached_property
    def payables(self) -> "PayablesResource":
        from blindpay.resources.payables import create_payables_resource

        return create_payables_resource(self._instance_id, self._api)

    @cached_property
    def payouts(self) -> "PayoutsResource":
        from blindpay.resources.payouts import create_payouts_resource

        return create_payouts_resource(self._instance_id, self._api)

    @cached_property
    def customers(self) -> _CustomersNamespace:
        return _CustomersNamespace(self._instance_id, self._api)

    @cached_property
    def virtual_accounts(self) -> "VirtualAccountsResource":
        from blindpay.resources.virtual_accounts import create_virtual_accounts_resource

        return create_virtual_accounts_resource(self._instance_id, self._api)

    @cached_property
    def wallets(self) -> _WalletsNamespace:
        return _WalletsNamespace(self._instance_id, self._api)

    @cached_property
    def transfers(self) -> "TransfersResource":
        from blindpay.resources.transfers import create_transfers_resource

        return create_transfers_resource(self._instance_id, self._api)

    @cached_property
    def fees(self) -> "FeesResource":
        from blindpay.resources.fees import create_fees_resource

        return create_fees_resource(self._instance_id, self._api)

    @cached_property
    def limits(self) -> "LimitsResource":
        from blindpay.resources.limits import create_limits_resource

        return create_limits_resource(self._instance_id, self._api)

    @cached_property
    def upload(self) -> "UploadResource":
        from blindpay.resources.upload import create_upload_resource

        return create_upload_resource(self._instance_id, self._api)

    @cached_property
    def terms_of_service(self) -> "TermsOfServiceResource":
        from blindpay.resources.terms_of_service import create_terms_of_service_resource

        return create_terms_of_service_resource(self._instance_id, self._api)

    def verify_webhook_signature(
        self,
        *,
        secret: str,
        id: str,
        timestamp: str,
        payload: Union[str, bytes],
        svix_signature: str,
        tolerance: int = DEFAULT_TOLERANCE_SECONDS,
    ) -> bool:
        """
        Verifies the BlindPay webhook signature.

        Deprecated: use ``blindpay.webhooks.verify``, which needs no client. Unlike it, this method also accepts the
        legacy bare signature form (no ``v1,`` prefix) that earlier versions of the SDK required.

        Args:
            secret: The webhook secret from BlindPay dashboard (``whsec_...``)
            id: The value of the `svix-id` header
            timestamp: The value of the `svix-timestamp` header
            payload: The raw request body, exactly as received
            svix_signature: The value of the `svix-signature` header (``v1,<signature>``, space-separated),
                or a bare signature
            tolerance: Maximum distance, in seconds, between `svix-timestamp` and now (default 300)

        Returns:
            True if a ``v1`` signature matches and the timestamp is within ``tolerance`` of now, False otherwise
        """
        return verify_webhook(
            payload,
            {"svix-id": id, "svix-timestamp": timestamp, "svix-signature": _with_legacy_v1_prefix(svix_signature)},
            secret,
            tolerance=tolerance,
        )

    async def aclose(self) -> None:
        """Closes the underlying HTTP client (unless you passed your own ``http_client``)."""
        await self._api.aclose()

    async def __aenter__(self) -> "BlindPay":
        return self

    async def __aexit__(
        self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]
    ) -> None:
        await self.aclose()


class _InstancesNamespaceSync(InstancesResourceSync):
    """``InstancesResourceSync`` plus its sub-resources, all visible to type checkers."""

    def __init__(self, instance_id: str, api_client: ApiClientImplSync) -> None:
        super().__init__(instance_id, api_client)
        self._api = api_client

    @cached_property
    def webhook_endpoints(self) -> "WebhookEndpointsResourceSync":
        from blindpay.resources.webhooks.webhooks import create_webhook_endpoints_resource_sync

        return create_webhook_endpoints_resource_sync(self._instance_id, self._api)

    @cached_property
    def terms_of_service(self) -> "TermsOfServiceResourceSync":
        from blindpay.resources.terms_of_service import create_terms_of_service_resource_sync

        return create_terms_of_service_resource_sync(self._instance_id, self._api)

    @cached_property
    def onboarding(self) -> "OnboardingResourceSync":
        from blindpay.resources.instances.onboarding import create_onboarding_resource_sync

        return create_onboarding_resource_sync(self._instance_id, self._api)

    @cached_property
    def rfi(self) -> "InstanceRfiResourceSync":
        from blindpay.resources.rfi.rfi import create_instance_rfi_resource_sync

        return create_instance_rfi_resource_sync(self._instance_id, self._api)


class _PayinsNamespaceSync(PayinsResourceSync):
    """``PayinsResourceSync`` plus its sub-resources, all visible to type checkers."""

    def __init__(self, instance_id: str, api_client: ApiClientImplSync) -> None:
        super().__init__(instance_id, api_client)
        self._api = api_client

    @cached_property
    def quotes(self) -> "PayinQuotesResourceSync":
        from blindpay.resources.payins.quotes import create_payin_quotes_resource_sync

        return create_payin_quotes_resource_sync(self._instance_id, self._api)


class _CustomersNamespaceSync(CustomersResourceSync):
    """``CustomersResourceSync`` plus its sub-resources, all visible to type checkers."""

    def __init__(self, instance_id: str, api_client: ApiClientImplSync) -> None:
        super().__init__(instance_id, api_client)
        self._api = api_client

    @cached_property
    def bank_accounts(self) -> "BankAccountsResourceSync":
        from blindpay.resources.bank_accounts.bank_accounts import create_bank_accounts_resource_sync

        return create_bank_accounts_resource_sync(self._instance_id, self._api)

    @cached_property
    def rfi(self) -> "CustomerRfiResourceSync":
        from blindpay.resources.rfi.rfi import create_customer_rfi_resource_sync

        return create_customer_rfi_resource_sync(self._instance_id, self._api)


class _WalletsNamespaceSync:
    def __init__(self, instance_id: str, api_client: ApiClientImplSync) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def blockchain(self) -> "BlockchainWalletsResourceSync":
        from blindpay.resources.wallets.blockchain import create_blockchain_wallets_resource_sync

        return create_blockchain_wallets_resource_sync(self._instance_id, self._api)

    @cached_property
    def offramp(self) -> "OfframpWalletsResourceSync":
        from blindpay.resources.wallets.offramp import create_offramp_wallets_resource_sync

        return create_offramp_wallets_resource_sync(self._instance_id, self._api)

    @cached_property
    def custodial(self) -> "CustodialWalletsResourceSync":
        from blindpay.resources.custodial_wallets.custodial_wallets import create_custodial_wallets_resource_sync

        return create_custodial_wallets_resource_sync(self._instance_id, self._api)


class BlindPaySync:
    _api_key: str
    _instance_id: str
    _base_url: str

    def __init__(
        self,
        *,
        api_key: str,
        instance_id: str,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = DEFAULT_MAX_RETRIES,
        http_client: Optional[httpx.Client] = None,
    ):
        if not api_key:
            raise BlindPayError("Api key not provided, get your api key on blindpay dashboard")

        if not instance_id:
            raise BlindPayError("Instance id not provided, get your instance id on blindpay dashboard")

        _validate_settings(timeout, max_retries)

        self._api_key = api_key
        self._instance_id = instance_id
        self._base_url = api_root(base_url)

        # No client-wide Content-Type: httpx sets application/json for JSON bodies and multipart/form-data
        # (with its boundary) for uploads. A fixed JSON Content-Type would break the multipart requests.
        self._headers = {
            "Accept": "application/json",
            "User-Agent": f"blindpay-python/{__version__}",
            "Authorization": f"Bearer {self._api_key}",
        }

        self._api = ApiClientImplSync(
            self._base_url, self._headers, timeout=timeout, max_retries=max_retries, http_client=http_client
        )

    def __repr__(self) -> str:
        return f"BlindPaySync(instance_id={self._instance_id!r}, base_url={self._base_url!r}, api_key='***')"

    @cached_property
    def available(self) -> "AvailableResourceSync":
        from blindpay.resources.available import create_available_resource_sync

        return create_available_resource_sync(self._api)

    @cached_property
    def instances(self) -> _InstancesNamespaceSync:
        return _InstancesNamespaceSync(self._instance_id, self._api)

    @cached_property
    def ownership(self) -> "OwnershipResourceSync":
        from blindpay.resources.ownership import create_ownership_resource_sync

        return create_ownership_resource_sync(self._instance_id, self._api)

    @cached_property
    def partner_fees(self) -> "PartnerFeesResourceSync":
        from blindpay.resources.partner_fees import create_partner_fees_resource_sync

        return create_partner_fees_resource_sync(self._instance_id, self._api)

    @cached_property
    def payins(self) -> _PayinsNamespaceSync:
        return _PayinsNamespaceSync(self._instance_id, self._api)

    @cached_property
    def quotes(self) -> "QuotesResourceSync":
        from blindpay.resources.quotes import create_quotes_resource_sync

        return create_quotes_resource_sync(self._instance_id, self._api)

    @cached_property
    def payables(self) -> "PayablesResourceSync":
        from blindpay.resources.payables import create_payables_resource_sync

        return create_payables_resource_sync(self._instance_id, self._api)

    @cached_property
    def payouts(self) -> "PayoutsResourceSync":
        from blindpay.resources.payouts import create_payouts_resource_sync

        return create_payouts_resource_sync(self._instance_id, self._api)

    @cached_property
    def customers(self) -> _CustomersNamespaceSync:
        return _CustomersNamespaceSync(self._instance_id, self._api)

    @cached_property
    def virtual_accounts(self) -> "VirtualAccountsResourceSync":
        from blindpay.resources.virtual_accounts import create_virtual_accounts_resource_sync

        return create_virtual_accounts_resource_sync(self._instance_id, self._api)

    @cached_property
    def wallets(self) -> _WalletsNamespaceSync:
        return _WalletsNamespaceSync(self._instance_id, self._api)

    @cached_property
    def transfers(self) -> "TransfersResourceSync":
        from blindpay.resources.transfers import create_transfers_resource_sync

        return create_transfers_resource_sync(self._instance_id, self._api)

    @cached_property
    def fees(self) -> "FeesResourceSync":
        from blindpay.resources.fees import create_fees_resource_sync

        return create_fees_resource_sync(self._instance_id, self._api)

    @cached_property
    def limits(self) -> "LimitsResourceSync":
        from blindpay.resources.limits import create_limits_resource_sync

        return create_limits_resource_sync(self._instance_id, self._api)

    @cached_property
    def upload(self) -> "UploadResourceSync":
        from blindpay.resources.upload import create_upload_resource_sync

        return create_upload_resource_sync(self._instance_id, self._api)

    @cached_property
    def terms_of_service(self) -> "TermsOfServiceResourceSync":
        from blindpay.resources.terms_of_service import create_terms_of_service_resource_sync

        return create_terms_of_service_resource_sync(self._instance_id, self._api)

    def verify_webhook_signature(
        self,
        *,
        secret: str,
        id: str,
        timestamp: str,
        payload: Union[str, bytes],
        svix_signature: str,
        tolerance: int = DEFAULT_TOLERANCE_SECONDS,
    ) -> bool:
        """
        Verifies the BlindPay webhook signature.

        Deprecated: use ``blindpay.webhooks.verify``, which needs no client. Unlike it, this method also accepts the
        legacy bare signature form (no ``v1,`` prefix) that earlier versions of the SDK required.

        Args:
            secret: The webhook secret from BlindPay dashboard (``whsec_...``)
            id: The value of the `svix-id` header
            timestamp: The value of the `svix-timestamp` header
            payload: The raw request body, exactly as received
            svix_signature: The value of the `svix-signature` header (``v1,<signature>``, space-separated),
                or a bare signature
            tolerance: Maximum distance, in seconds, between `svix-timestamp` and now (default 300)

        Returns:
            True if a ``v1`` signature matches and the timestamp is within ``tolerance`` of now, False otherwise
        """
        return verify_webhook(
            payload,
            {"svix-id": id, "svix-timestamp": timestamp, "svix-signature": _with_legacy_v1_prefix(svix_signature)},
            secret,
            tolerance=tolerance,
        )

    def close(self) -> None:
        if hasattr(self, "_api"):
            self._api.close()

    def __enter__(self) -> "BlindPaySync":
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        self.close()

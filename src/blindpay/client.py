import base64
import hashlib
import hmac
from functools import cached_property
from typing import TYPE_CHECKING, Any, Dict, Literal, Mapping, Optional, TypeVar

import httpx

from ._internal.exceptions import BlindPayError
from .types import BlindpayApiResponse

if TYPE_CHECKING:
    from blindpay.resources.api_keys.api_keys import ApiKeysResource, ApiKeysResourceSync
    from blindpay.resources.available.available import AvailableResource, AvailableResourceSync
    from blindpay.resources.bank_accounts.bank_accounts import BankAccountsResource, BankAccountsResourceSync
    from blindpay.resources.instances.instances import InstancesResource, InstancesResourceSync
    from blindpay.resources.partner_fees.partner_fees import PartnerFeesResource, PartnerFeesResourceSync
    from blindpay.resources.payins.payins import PayinsResource, PayinsResourceSync
    from blindpay.resources.payins.quotes import PayinQuotesResource, PayinQuotesResourceSync
    from blindpay.resources.payouts.payouts import PayoutsResource, PayoutsResourceSync
    from blindpay.resources.quotes.quotes import QuotesResource, QuotesResourceSync
    from blindpay.resources.receivers.receivers import ReceiversResource, ReceiversResourceSync
    from blindpay.resources.virtual_accounts.virtual_accounts import (
        VirtualAccountsResource,
        VirtualAccountsResourceSync,
    )
    from blindpay.resources.wallets.blockchain import BlockchainWalletsResource, BlockchainWalletsResourceSync
    from blindpay.resources.wallets.offramp import OfframpWalletsResource, OfframpWalletsResourceSync
    from blindpay.resources.webhooks.webhooks import WebhookEndpointsResource, WebhookEndpointsResourceSync

__version__ = "1.1.0"

T = TypeVar("T")


class ApiClientImpl:
    def __init__(self, base_url: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.headers = headers

    async def get(self, path: str) -> BlindpayApiResponse[T]:
        return await self._request("GET", path)

    async def post(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[T]:
        return await self._request("POST", path, body)

    async def put(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[T]:
        return await self._request("PUT", path, body)

    async def patch(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[T]:
        return await self._request("PATCH", path, body)

    async def delete(self, path: str, body: Optional[Mapping[str, Any]] = None) -> BlindpayApiResponse[T]:
        return await self._request("DELETE", path, body)

    async def _request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        path: str,
        body: Optional[Mapping[str, Any]] = None,
    ) -> BlindpayApiResponse[T]:
        url = f"{self.base_url}{path}"

        try:
            async with httpx.AsyncClient() as client:
                if body is not None:
                    response = await client.request(method=method, url=url, headers=self.headers, json=body)
                else:
                    response = await client.request(method=method, url=url, headers=self.headers)

                if response.status_code >= 400:
                    try:
                        error_data = response.json()
                        error_message = error_data.get("message", "Unknown error")
                    except Exception:
                        error_message = "Unknown error"

                    return {"data": None, "error": {"message": error_message}}

                data = response.json()
                return {"data": data, "error": None}

        except Exception as e:
            error_message = str(e) if str(e) else "Unknown error"
            return {"data": None, "error": {"message": error_message}}


class ApiClientImplSync:
    def __init__(self, base_url: str, headers: Dict[str, str]):
        self.base_url = base_url
        self.headers = headers
        self.client = httpx.Client(base_url=base_url, headers=headers)

    def get(self, path: str) -> BlindpayApiResponse[T]:
        return self._request("GET", path)

    def post(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[T]:
        return self._request("POST", path, body)

    def put(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[T]:
        return self._request("PUT", path, body)

    def patch(self, path: str, body: Mapping[str, Any]) -> BlindpayApiResponse[T]:
        return self._request("PATCH", path, body)

    def delete(self, path: str, body: Optional[Mapping[str, Any]] = None) -> BlindpayApiResponse[T]:
        return self._request("DELETE", path, body)

    def _request(
        self,
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        path: str,
        body: Optional[Mapping[str, Any]] = None,
    ) -> BlindpayApiResponse[T]:
        try:
            if body is not None:
                response = self.client.request(method=method, url=path, json=body)
            else:
                response = self.client.request(method=method, url=path)

            if response.status_code >= 400:
                try:
                    error_data = response.json()
                    error_message = error_data.get("message", "Unknown error")
                except Exception:
                    error_message = "Unknown error"

                return {"data": None, "error": {"message": error_message}}

            data = response.json()
            return {"data": data, "error": None}

        except Exception as e:
            error_message = str(e) if str(e) else "Unknown error"
            return {"data": None, "error": {"message": error_message}}

    def close(self) -> None:
        self.client.close()


class _InstancesNamespace:
    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def _base(self) -> "InstancesResource":
        from blindpay.resources.instances.instances import create_instances_resource

        return create_instances_resource(self._instance_id, self._api)

    @cached_property
    def api_keys(self) -> "ApiKeysResource":
        from blindpay.resources.api_keys.api_keys import create_api_keys_resource

        return create_api_keys_resource(self._instance_id, self._api)

    @cached_property
    def webhook_endpoints(self) -> "WebhookEndpointsResource":
        from blindpay.resources.webhooks.webhooks import create_webhook_endpoints_resource

        return create_webhook_endpoints_resource(self._instance_id, self._api)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)


class _PayinsNamespace:
    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def _base(self) -> "PayinsResource":
        from blindpay.resources.payins.payins import create_payins_resource

        return create_payins_resource(self._instance_id, self._api)

    @cached_property
    def quotes(self) -> "PayinQuotesResource":
        from blindpay.resources.payins.quotes import create_payin_quotes_resource

        return create_payin_quotes_resource(self._instance_id, self._api)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)


class _ReceiversNamespace:
    def __init__(self, instance_id: str, api_client: ApiClientImpl) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def _base(self) -> "ReceiversResource":
        from blindpay.resources.receivers.receivers import create_receivers_resource

        return create_receivers_resource(self._instance_id, self._api)

    @cached_property
    def bank_accounts(self) -> "BankAccountsResource":
        from blindpay.resources.bank_accounts.bank_accounts import create_bank_accounts_resource

        return create_bank_accounts_resource(self._instance_id, self._api)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)


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


class BlindPay:
    _api_key: str
    _instance_id: str
    _base_url: str

    def __init__(self, *, api_key: str, instance_id: str):
        if not api_key:
            raise BlindPayError("Api key not provided, get your api key on blindpay dashboard")

        if not instance_id:
            raise BlindPayError("Instance id not provided, get your instance id on blindpay dashboard")

        self._api_key = api_key
        self._instance_id = instance_id
        self._base_url = "https://api.blindpay.com/v1"

        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"blindpay-python/{__version__}",
            "Authorization": f"Bearer {self._api_key}",
        }

        self._api = ApiClientImpl(self._base_url, self._headers)

    @cached_property
    def available(self) -> "AvailableResource":
        from blindpay.resources.available import create_available_resource

        return create_available_resource(self._api)

    @cached_property
    def instances(self) -> _InstancesNamespace:
        return _InstancesNamespace(self._instance_id, self._api)

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
    def payouts(self) -> "PayoutsResource":
        from blindpay.resources.payouts import create_payouts_resource

        return create_payouts_resource(self._instance_id, self._api)

    @cached_property
    def receivers(self) -> _ReceiversNamespace:
        return _ReceiversNamespace(self._instance_id, self._api)

    @cached_property
    def virtual_accounts(self) -> "VirtualAccountsResource":
        from blindpay.resources.virtual_accounts import create_virtual_accounts_resource

        return create_virtual_accounts_resource(self._instance_id, self._api)

    @cached_property
    def wallets(self) -> _WalletsNamespace:
        return _WalletsNamespace(self._instance_id, self._api)

    def verify_webhook_signature(
        self, *, secret: str, id: str, timestamp: str, payload: str, svix_signature: str
    ) -> bool:
        """
        Verifies the BlindPay webhook signature

        Args:
            secret: The webhook secret from BlindPay dashboard
            id: The value of the `svix-id` header
            timestamp: The value of the `svix-timestamp` header
            payload: The raw request body
            svix_signature: The value of the `svix-signature` header

        Returns:
            True if the signature is valid, False otherwise
        """
        signed_content = f"{id}.{timestamp}.{payload}"

        secret_parts = secret.split("_")
        if len(secret_parts) < 2:
            return False

        try:
            secret_bytes = base64.b64decode(secret_parts[1])
        except Exception:
            return False

        expected_signature = base64.b64encode(
            hmac.new(secret_bytes, signed_content.encode(), hashlib.sha256).digest()
        ).decode()

        return len(svix_signature) == len(expected_signature) and hmac.compare_digest(
            svix_signature, expected_signature
        )


class _InstancesNamespaceSync:
    def __init__(self, instance_id: str, api_client: ApiClientImplSync) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def _base(self) -> "InstancesResourceSync":
        from blindpay.resources.instances.instances import create_instances_resource_sync

        return create_instances_resource_sync(self._instance_id, self._api)

    @cached_property
    def api_keys(self) -> "ApiKeysResourceSync":
        from blindpay.resources.api_keys.api_keys import create_api_keys_resource_sync

        return create_api_keys_resource_sync(self._instance_id, self._api)

    @cached_property
    def webhook_endpoints(self) -> "WebhookEndpointsResourceSync":
        from blindpay.resources.webhooks.webhooks import create_webhook_endpoints_resource_sync

        return create_webhook_endpoints_resource_sync(self._instance_id, self._api)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)


class _PayinsNamespaceSync:
    def __init__(self, instance_id: str, api_client: ApiClientImplSync) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def _base(self) -> "PayinsResourceSync":
        from blindpay.resources.payins.payins import create_payins_resource_sync

        return create_payins_resource_sync(self._instance_id, self._api)

    @cached_property
    def quotes(self) -> "PayinQuotesResourceSync":
        from blindpay.resources.payins.quotes import create_payin_quotes_resource_sync

        return create_payin_quotes_resource_sync(self._instance_id, self._api)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)


class _ReceiversNamespaceSync:
    def __init__(self, instance_id: str, api_client: ApiClientImplSync) -> None:
        self._instance_id = instance_id
        self._api = api_client

    @cached_property
    def _base(self) -> "ReceiversResourceSync":
        from blindpay.resources.receivers.receivers import create_receivers_resource_sync

        return create_receivers_resource_sync(self._instance_id, self._api)

    @cached_property
    def bank_accounts(self) -> "BankAccountsResourceSync":
        from blindpay.resources.bank_accounts.bank_accounts import create_bank_accounts_resource_sync

        return create_bank_accounts_resource_sync(self._instance_id, self._api)

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)


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


class BlindPaySync:
    _api_key: str
    _instance_id: str
    _base_url: str

    def __init__(self, *, api_key: str, instance_id: str):
        if not api_key:
            raise BlindPayError("Api key not provided, get your api key on blindpay dashboard")

        if not instance_id:
            raise BlindPayError("Instance id not provided, get your instance id on blindpay dashboard")

        self._api_key = api_key
        self._instance_id = instance_id
        self._base_url = "https://api.blindpay.com/v1"

        self._headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": f"blindpay-python/{__version__}",
            "Authorization": f"Bearer {self._api_key}",
        }

        self._api = ApiClientImplSync(self._base_url, self._headers)

    @cached_property
    def available(self) -> "AvailableResourceSync":
        from blindpay.resources.available import create_available_resource_sync

        return create_available_resource_sync(self._api)

    @cached_property
    def instances(self) -> _InstancesNamespaceSync:
        return _InstancesNamespaceSync(self._instance_id, self._api)

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
    def payouts(self) -> "PayoutsResourceSync":
        from blindpay.resources.payouts import create_payouts_resource_sync

        return create_payouts_resource_sync(self._instance_id, self._api)

    @cached_property
    def receivers(self) -> _ReceiversNamespaceSync:
        return _ReceiversNamespaceSync(self._instance_id, self._api)

    @cached_property
    def virtual_accounts(self) -> "VirtualAccountsResourceSync":
        from blindpay.resources.virtual_accounts import create_virtual_accounts_resource_sync

        return create_virtual_accounts_resource_sync(self._instance_id, self._api)

    @cached_property
    def wallets(self) -> _WalletsNamespaceSync:
        return _WalletsNamespaceSync(self._instance_id, self._api)

    def verify_webhook_signature(
        self, *, secret: str, id: str, timestamp: str, payload: str, svix_signature: str
    ) -> bool:
        """
        Verifies the BlindPay webhook signature

        Args:
            secret: The webhook secret from BlindPay dashboard
            id: The value of the `svix-id` header
            timestamp: The value of the `svix-timestamp` header
            payload: The raw request body
            svix_signature: The value of the `svix-signature` header

        Returns:
            True if the signature is valid, False otherwise
        """
        signed_content = f"{id}.{timestamp}.{payload}"

        secret_parts = secret.split("_")
        if len(secret_parts) < 2:
            return False

        try:
            secret_bytes = base64.b64decode(secret_parts[1])
        except Exception:
            return False

        expected_signature = base64.b64encode(
            hmac.new(secret_bytes, signed_content.encode(), hashlib.sha256).digest()
        ).decode()

        return len(svix_signature) == len(expected_signature) and hmac.compare_digest(
            svix_signature, expected_signature
        )

    def close(self) -> None:
        if hasattr(self, "_api"):
            self._api.close()

    def __enter__(self) -> "BlindPaySync":
        return self

    def __exit__(self, exc_type: Optional[type], exc_val: Optional[BaseException], exc_tb: Optional[Any]) -> None:
        self.close()

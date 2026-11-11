from typing import List, Literal, Optional, Union

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ..._internal.http import RequestOptions, path_param
from ...types import BlindpayApiResponse

InstanceMemberRole = Literal["owner", "admin", "finance", "checker", "operations", "developer", "viewer"]
InstanceType = Literal["production", "development"]
InstanceOnboardingStep = Literal[
    "initial", "business_details", "business_profile", "documents", "applicant", "completed", "blocked"
]


class Instance(TypedDict):
    """The client's own instance. ``type`` is ``development`` for sandbox instances (settlement is simulated)."""

    id: str
    name: str
    type: Union[InstanceType, str]
    onboarding_step: Union[InstanceOnboardingStep, str]


class InstanceMember(TypedDict):
    id: str
    email: str
    first_name: str
    middle_name: str
    last_name: str
    image_url: str
    created_at: str
    role: InstanceMemberRole


GetInstanceMembersResponse = List[InstanceMember]


class UpdateInstanceInput(TypedDict, total=False):
    name: str
    customer_invite_redirect_url: Optional[str]
    email_notifications: bool
    require_passkey: bool
    partner_tos_terms_accepted: Literal[True]
    accent_color: Optional[str]
    logo_url: Optional[str]
    partner_tos_link: Optional[str]
    partner_tos_screenshot: Optional[str]


class UpdateInstanceMemberRoleInput(TypedDict):
    member_id: str
    role: InstanceMemberRole


class MigrateInstanceOwnershipInput(TypedDict):
    user_id: str


class MigrateInstanceOwnershipResponse(TypedDict):
    success: bool


class InstancesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def get(self) -> BlindpayApiResponse[Instance]:
        return await self._client.get(f"/instances/{self._instance_id}")

    async def get_members(self) -> BlindpayApiResponse[GetInstanceMembersResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/members")

    async def update(
        self, data: UpdateInstanceInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return await self._client.put(f"/instances/{self._instance_id}", data, options=options)

    async def delete(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}", options=options)

    async def delete_member(
        self, member_id: str, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return await self._client.delete(
            f"/instances/{self._instance_id}/members/{path_param(member_id)}", options=options
        )

    async def update_member_role(
        self, member_id: str, role: InstanceMemberRole, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return await self._client.put(
            f"/instances/{self._instance_id}/members/{path_param(member_id)}", {"user_role": role}, options=options
        )

    async def migrate_ownership(
        self, data: MigrateInstanceOwnershipInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[MigrateInstanceOwnershipResponse]:
        return await self._client.post(f"/instances/{self._instance_id}/ownership", data, options=options)


class InstancesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def get(self) -> BlindpayApiResponse[Instance]:
        return self._client.get(f"/instances/{self._instance_id}")

    def get_members(self) -> BlindpayApiResponse[GetInstanceMembersResponse]:
        return self._client.get(f"/instances/{self._instance_id}/members")

    def update(self, data: UpdateInstanceInput, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return self._client.put(f"/instances/{self._instance_id}", data, options=options)

    def delete(self, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}", options=options)

    def delete_member(self, member_id: str, options: Optional[RequestOptions] = None) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/members/{path_param(member_id)}", options=options)

    def update_member_role(
        self, member_id: str, role: InstanceMemberRole, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[None]:
        return self._client.put(
            f"/instances/{self._instance_id}/members/{path_param(member_id)}", {"user_role": role}, options=options
        )

    def migrate_ownership(
        self, data: MigrateInstanceOwnershipInput, options: Optional[RequestOptions] = None
    ) -> BlindpayApiResponse[MigrateInstanceOwnershipResponse]:
        return self._client.post(f"/instances/{self._instance_id}/ownership", data, options=options)


def create_instances_resource(instance_id: str, client: InternalApiClient) -> InstancesResource:
    return InstancesResource(instance_id, client)


def create_instances_resource_sync(instance_id: str, client: InternalApiClientSync) -> InstancesResourceSync:
    return InstancesResourceSync(instance_id, client)

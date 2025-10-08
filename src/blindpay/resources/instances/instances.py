from typing import List, Literal, Optional

from typing_extensions import TypedDict

from ..._internal.api_client import InternalApiClient, InternalApiClientSync
from ...types import BlindpayApiResponse

InstanceMemberRole = Literal["owner", "admin", "finance", "checker", "operations", "developer", "viewer"]


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


class UpdateInstanceInput(TypedDict):
    name: str
    receiver_invite_redirect_url: Optional[str]


class UpdateInstanceMemberRoleInput(TypedDict):
    member_id: str
    role: InstanceMemberRole


class InstancesResource:
    def __init__(self, instance_id: str, client: InternalApiClient):
        self._instance_id = instance_id
        self._client = client

    async def get_members(self) -> BlindpayApiResponse[GetInstanceMembersResponse]:
        return await self._client.get(f"/instances/{self._instance_id}/members")

    async def update(self, data: UpdateInstanceInput) -> BlindpayApiResponse[None]:
        return await self._client.put(f"/instances/{self._instance_id}", data)

    async def delete(self) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}")

    async def delete_member(self, member_id: str) -> BlindpayApiResponse[None]:
        return await self._client.delete(f"/instances/{self._instance_id}/members/{member_id}")

    async def update_member_role(self, member_id: str, role: InstanceMemberRole) -> BlindpayApiResponse[None]:
        return await self._client.put(f"/instances/{self._instance_id}/members/{member_id}", {"role": role})


class InstancesResourceSync:
    def __init__(self, instance_id: str, client: InternalApiClientSync):
        self._instance_id = instance_id
        self._client = client

    def get_members(self) -> BlindpayApiResponse[GetInstanceMembersResponse]:
        return self._client.get(f"/instances/{self._instance_id}/members")

    def update(self, data: UpdateInstanceInput) -> BlindpayApiResponse[None]:
        return self._client.put(f"/instances/{self._instance_id}", data)

    def delete(self) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}")

    def delete_member(self, member_id: str) -> BlindpayApiResponse[None]:
        return self._client.delete(f"/instances/{self._instance_id}/members/{member_id}")

    def update_member_role(self, member_id: str, role: InstanceMemberRole) -> BlindpayApiResponse[None]:
        return self._client.put(f"/instances/{self._instance_id}/members/{member_id}", {"role": role})


def create_instances_resource(instance_id: str, client: InternalApiClient) -> InstancesResource:
    return InstancesResource(instance_id, client)


def create_instances_resource_sync(instance_id: str, client: InternalApiClientSync) -> InstancesResourceSync:
    return InstancesResourceSync(instance_id, client)

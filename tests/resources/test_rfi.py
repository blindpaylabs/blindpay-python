from typing import Any, Dict
from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync
from blindpay.resources.rfi import CustomerRfi, InstanceRfi, RfiResponseMap
from tests.spec_fixtures import assert_matches_spec, response_variants

CUSTOMER_RFI = response_variants("GET /v1/instances/{instance_id}/customers/{customer_id}/rfi")
INSTANCE_RFI = response_variants("GET /v1/instances/{instance_id}/rfi")
ANSWERS: RfiResponseMap = {"tax_id": "123", "docs": ["https://example.com/a.pdf"]}


def _object_variants(variants: Dict[str, Any]) -> Dict[str, Any]:
    # GET .../rfi may also answer null (no open RFI); the shape check needs the object variants.
    return {k.split(".")[0]: v for k, v in variants.items() if isinstance(v, dict)}


class TestRfi:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test_key", instance_id="in_000000000000")

    def test_rfi_types_match_the_spec(self):
        assert_matches_spec(CustomerRfi, _object_variants(CUSTOMER_RFI))
        assert_matches_spec(InstanceRfi, _object_variants(INSTANCE_RFI))

    @pytest.mark.asyncio
    async def test_instance_get_and_submit_send_the_answers_as_the_body(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": None, "error": None}

            assert (await self.blindpay.instances.rfi.get())["data"] is None
            await self.blindpay.instances.rfi.submit({"response": ANSWERS})

            assert mock_request.call_args_list[0].args == ("GET", "/instances/in_000000000000/rfi")
            assert mock_request.call_args_list[1].args == ("POST", "/instances/in_000000000000/rfi", ANSWERS)

    @pytest.mark.asyncio
    async def test_customer_submit(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"success": True}, "error": None}

            await self.blindpay.customers.rfi.submit({"customer_id": "cu_000000000000", "response": ANSWERS})

            mock_request.assert_called_once_with(
                "POST", "/instances/in_000000000000/customers/cu_000000000000/rfi", ANSWERS
            )


class TestRfiSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test_key", instance_id="in_000000000000")

    def test_customer_get(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": CUSTOMER_RFI["full"], "error": None}

            response = self.blindpay.customers.rfi.get("cu_000000000000")

            assert response["data"] == CUSTOMER_RFI["full"]
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/customers/cu_000000000000/rfi")

    def test_instance_submit(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"success": False, "reason": "no_pending_rfi"}, "error": None}

            response = self.blindpay.instances.rfi.submit({"response": ANSWERS})

            assert response["data"] == {"success": False, "reason": "no_pending_rfi"}
            mock_request.assert_called_once_with("POST", "/instances/in_000000000000/rfi", ANSWERS)

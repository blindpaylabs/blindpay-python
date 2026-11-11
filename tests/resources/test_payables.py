from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync
from blindpay.resources.payables import Payable
from tests.spec_fixtures import assert_matches_spec, response_variants

PAYABLE = response_variants("GET /v1/instances/{instance_id}/payables/{id}")
LIST = response_variants("GET /v1/instances/{instance_id}/payables")
CREATE_BODY = {"customer_id": "cu_000000000000", "currency": "BRL", "boleto_barcode": "0", "from": {"legal_name": "A"}}


class TestPayables:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test_key", instance_id="in_000000000000")

    def test_payable_type_matches_the_spec(self):
        assert_matches_spec(Payable, PAYABLE)

    @pytest.mark.asyncio
    async def test_create(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": PAYABLE["full"], "error": None}

            response = await self.blindpay.payables.create(CREATE_BODY)  # type: ignore[arg-type]

            assert response["data"] == PAYABLE["full"]
            mock_request.assert_called_once_with("POST", "/instances/in_000000000000/payables", CREATE_BODY)

    @pytest.mark.asyncio
    async def test_list_with_filters(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": LIST["full.b0"], "error": None}

            await self.blindpay.payables.list({"status": "draft", "limit": 10})

            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payables?status=draft&limit=10")

    @pytest.mark.asyncio
    async def test_get_and_delete(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": PAYABLE["full"], "error": None}

            await self.blindpay.payables.get("pa_000000000000")
            await self.blindpay.payables.delete("pa_000000000000")

            assert mock_request.call_args_list[0].args == ("GET", "/instances/in_000000000000/payables/pa_000000000000")
            assert mock_request.call_args_list[1].args == (
                "DELETE",
                "/instances/in_000000000000/payables/pa_000000000000",
                None,
            )


class TestPayablesSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test_key", instance_id="in_000000000000")

    def test_create(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": PAYABLE["full"], "error": None}

            response = self.blindpay.payables.create(CREATE_BODY)  # type: ignore[arg-type]

            assert response["data"] == PAYABLE["full"]
            mock_request.assert_called_once_with("POST", "/instances/in_000000000000/payables", CREATE_BODY)

    def test_list_without_params(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": LIST["full.b1"], "error": None}

            response = self.blindpay.payables.list()

            assert response["data"] == LIST["full.b1"]
            mock_request.assert_called_once_with("GET", "/instances/in_000000000000/payables")

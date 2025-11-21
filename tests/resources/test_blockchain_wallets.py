from unittest.mock import patch

import pytest

from blindpay import BlindPay, BlindPaySync


class TestBlockchainWallets:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPay(api_key="test-key", instance_id="in_000000000000")

    @pytest.mark.asyncio
    async def test_get_blockchain_wallet_message(self):
        mocked_message = {"message": "random"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_message, "error": None}

            response = await self.blindpay.wallets.blockchain.get_wallet_message("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_message
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets/sign-message"
            )

    @pytest.mark.asyncio
    async def test_list_blockchain_wallets(self):
        mocked_wallets = [
            {
                "id": "bw_000000000000",
                "name": "Wallet Display Name",
                "network": "polygon",
                "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
                "is_account_abstraction": False,
                "receiver_id": "re_000000000000",
            }
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallets, "error": None}

            response = await self.blindpay.wallets.blockchain.list("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_wallets
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets"
            )

    @pytest.mark.asyncio
    async def test_create_blockchain_wallet_with_address(self):
        mocked_wallet = {
            "id": "bw_000000000000",
            "name": "Wallet Display Name",
            "network": "polygon",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "signature_tx_hash": None,
            "is_account_abstraction": True,
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = await self.blindpay.wallets.blockchain.create_with_address(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Wallet Display Name",
                    "network": "polygon",
                    "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_wallet
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets",
                {
                    "name": "Wallet Display Name",
                    "network": "polygon",
                    "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                    "is_account_abstraction": True,
                },
            )

    @pytest.mark.asyncio
    async def test_create_blockchain_wallet_with_hash(self):
        mocked_wallet = {
            "id": "bw_000000000000",
            "name": "Wallet Display Name",
            "network": "polygon",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            "is_account_abstraction": False,
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = await self.blindpay.wallets.blockchain.create_with_hash(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Wallet Display Name",
                    "network": "polygon",
                    "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_wallet
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets",
                {
                    "name": "Wallet Display Name",
                    "network": "polygon",
                    "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
                    "is_account_abstraction": False,
                },
            )

    @pytest.mark.asyncio
    async def test_get_blockchain_wallet(self):
        mocked_wallet = {
            "id": "bw_000000000000",
            "name": "Wallet Display Name",
            "network": "polygon",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            "is_account_abstraction": False,
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = await self.blindpay.wallets.blockchain.get(
                {
                    "receiver_id": "re_000000000000",
                    "id": "bw_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_wallet
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets/bw_000000000000"
            )

    @pytest.mark.asyncio
    async def test_delete_blockchain_wallet(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = await self.blindpay.wallets.blockchain.delete(
                {
                    "receiver_id": "re_000000000000",
                    "id": "bw_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"data": None}
            mock_request.assert_called_once_with(
                "DELETE",
                "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets/bw_000000000000",
                None,
            )

    @pytest.mark.asyncio
    async def test_create_asset_trustline(self):
        mocked_response = {
            "xdr": (
                "AAAAAgAAAABqVFqpZzXx+KxRjXXFGO3sKwHCEYdHsWxDRrJTLGPDowAAAGQABVECAAAAAQAAAAEAAAAAAAAAAAAAAA"
                "BmWFbUAAAAAAAAAAEAAAAAAAAABgAAAAFVU0RCAAAAAABbjPEfrLNLCLjNQyaWWgTeFn4tnbFnNd9FTJ3HgkLUCwAAAAAAAAAAAAAAAAAAAAE="
            ),
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = await self.blindpay.wallets.blockchain.create_asset_trustline(
                "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B"
            )

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/create-asset-trustline",
                {"address": "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B"},
            )

    @pytest.mark.asyncio
    async def test_mint_usdb_stellar(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {}, "error": None}

            response = await self.blindpay.wallets.blockchain.mint_usdb_stellar(
                {
                    "address": "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B",
                    "amount": "1000000",
                    "signedXdr": (
                        "AAAAAgAAAABqVFqpZzXx+KxRjXXFGO3sKwHCEYdHsWxDRrJTLGPDowAAAGQABVECAAAAAQAAAAEAAAAAAAAAAAAA"
                        "AABmWFbUAAAAAAAAAAEAAAAAAAAABgAAAAFVU0RCAAAAAABbjPEfrLNLCLjNQyaWWgTeFn4tnbFnNd9FTJ3HgkLUCwAAAAAAAAAAAAAAAAAAAAE="
                    ),
                }
            )

            assert response["error"] is None
            assert response["data"] is not None
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/mint-usdb-stellar",
                {
                    "address": "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B",
                    "amount": "1000000",
                    "signedXdr": (
                        "AAAAAgAAAABqVFqpZzXx+KxRjXXFGO3sKwHCEYdHsWxDRrJTLGPDowAAAGQABVECAAAAAQAAAAEAAAAAAAAAAAAA"
                        "AABmWFbUAAAAAAAAAAEAAAAAAAAABgAAAAFVU0RCAAAAAABbjPEfrLNLCLjNQyaWWgTeFn4tnbFnNd9FTJ3HgkLUCwAAAAAAAAAAAAAAAAAAAAE="
                    ),
                },
            )

    @pytest.mark.asyncio
    async def test_mint_usdb_solana(self):
        mocked_response = {
            "success": True,
            "signature": "4wceVEQeJG4vpS4k2o1dHU5cFWeWTQU8iaCEpRaV5KkqSxPfbdAc8hzXa7nNYG6rvqgAmDkzBycbcXkKKAeK8Jtu",
            "error": "",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = await self.blindpay.wallets.blockchain.mint_usdb_solana(
                {
                    "address": "7YttLkHDoNj9wyDur5pM1ejNaAvT9X4eqaYcHQqtj2G5",
                    "amount": "1000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/mint-usdb-solana",
                {
                    "address": "7YttLkHDoNj9wyDur5pM1ejNaAvT9X4eqaYcHQqtj2G5",
                    "amount": "1000000",
                },
            )

    @pytest.mark.asyncio
    async def test_prepare_solana_delegation_transaction(self):
        mocked_response = {
            "success": True,
            "transaction": "AAGBf4K95Gp5i6f0BAEYAgABAgMEBQYHCAkKCwwNDg8QERITFBUWFxgZGhscHR4fICEiIw==",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = await self.blindpay.wallets.blockchain.prepare_solana_delegation_transaction(
                {
                    "token_address": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                    "amount": "1000000",
                    "owner_address": "7YttLkHDoNj9wyDur5pM1ejNaAvT9X4eqaYcHQqtj2G5",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/prepare-delegate-solana",
                {
                    "token_address": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA",
                    "amount": "1000000",
                    "owner_address": "7YttLkHDoNj9wyDur5pM1ejNaAvT9X4eqaYcHQqtj2G5",
                },
            )


class TestBlockchainWalletsSync:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.blindpay = BlindPaySync(api_key="test-key", instance_id="in_000000000000")

    def test_get_blockchain_wallet_message(self):
        mocked_message = {"message": "random"}

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_message, "error": None}

            response = self.blindpay.wallets.blockchain.get_wallet_message("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_message
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets/sign-message"
            )

    def test_list_blockchain_wallets(self):
        mocked_wallets = [
            {
                "id": "bw_000000000000",
                "name": "Wallet Display Name",
                "network": "polygon",
                "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
                "is_account_abstraction": False,
                "receiver_id": "re_000000000000",
            }
        ]

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallets, "error": None}

            response = self.blindpay.wallets.blockchain.list("re_000000000000")

            assert response["error"] is None
            assert response["data"] == mocked_wallets
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets"
            )

    def test_create_blockchain_wallet_with_address(self):
        mocked_wallet = {
            "id": "bw_000000000000",
            "name": "Wallet Display Name",
            "network": "polygon",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "signature_tx_hash": None,
            "is_account_abstraction": True,
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = self.blindpay.wallets.blockchain.create_with_address(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Wallet Display Name",
                    "network": "polygon",
                    "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_wallet
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets",
                {
                    "name": "Wallet Display Name",
                    "network": "polygon",
                    "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
                    "is_account_abstraction": True,
                },
            )

    def test_create_blockchain_wallet_with_hash(self):
        mocked_wallet = {
            "id": "bw_000000000000",
            "name": "Wallet Display Name",
            "network": "polygon",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            "is_account_abstraction": False,
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = self.blindpay.wallets.blockchain.create_with_hash(
                {
                    "receiver_id": "re_000000000000",
                    "name": "Wallet Display Name",
                    "network": "polygon",
                    "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_wallet
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets",
                {
                    "name": "Wallet Display Name",
                    "network": "polygon",
                    "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
                    "is_account_abstraction": False,
                },
            )

    def test_get_blockchain_wallet(self):
        mocked_wallet = {
            "id": "bw_000000000000",
            "name": "Wallet Display Name",
            "network": "polygon",
            "address": "0xDD6a3aD0949396e57C7738ba8FC1A46A5a1C372C",
            "signature_tx_hash": "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",
            "is_account_abstraction": False,
            "receiver_id": "re_000000000000",
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_wallet, "error": None}

            response = self.blindpay.wallets.blockchain.get(
                {
                    "receiver_id": "re_000000000000",
                    "id": "bw_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == mocked_wallet
            mock_request.assert_called_once_with(
                "GET", "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets/bw_000000000000"
            )

    def test_delete_blockchain_wallet(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {"data": None}, "error": None}

            response = self.blindpay.wallets.blockchain.delete(
                {
                    "receiver_id": "re_000000000000",
                    "id": "bw_000000000000",
                }
            )

            assert response["error"] is None
            assert response["data"] == {"data": None}
            mock_request.assert_called_once_with(
                "DELETE",
                "/instances/in_000000000000/receivers/re_000000000000/blockchain-wallets/bw_000000000000",
                None,
            )

    def test_create_asset_trustline(self):
        mocked_response = {
            "xdr": (
                "AAAAAgAAAABqVFqpZzXx+KxRjXXFGO3sKwHCEYdHsWxDRrJTLGPDowAAAGQABVECAAAAAQAAAAEAAAAAAAAAAAAAAA"
                "BmWFbUAAAAAAAAAAEAAAAAAAAABgAAAAFVU0RCAAAAAABbjPEfrLNLCLjNQyaWWgTeFn4tnbFnNd9FTJ3HgkLUCwAAAAAAAAAAAAAAAAAAAAE="
            ),
        }

        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": mocked_response, "error": None}

            response = self.blindpay.wallets.blockchain.create_asset_trustline(
                "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B"
            )

            assert response["error"] is None
            assert response["data"] == mocked_response
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/create-asset-trustline",
                {"address": "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B"},
            )

    def test_mint_usdb_stellar(self):
        with patch.object(self.blindpay._api, "_request") as mock_request:
            mock_request.return_value = {"data": {}, "error": None}

            response = self.blindpay.wallets.blockchain.mint_usdb_stellar(
                {
                    "address": "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B",
                    "amount": "1000000",
                    "signedXdr": (
                        "AAAAAgAAAABqVFqpZzXx+KxRjXXFGO3sKwHCEYdHsWxDRrJTLGPDowAAAGQABVECAAAAAQAAAAEAAAAAAAAAAAAA"
                        "AABmWFbUAAAAAAAAAAEAAAAAAAAABgAAAAFVU0RCAAAAAABbjPEfrLNLCLjNQyaWWgTeFn4tnbFnNd9FTJ3HgkLUCwAAAAAAAAAAAAAAAAAAAAE="
                    ),
                }
            )

            assert response["error"] is None
            assert response["data"] is not None
            mock_request.assert_called_once_with(
                "POST",
                "/instances/in_000000000000/mint-usdb-stellar",
                {
                    "address": "GCDNJUBQSX7AJWLJACMJ7I4BC3Z47BQUTMHEICZLE6MU4KQBRYG5JY6B",
                    "amount": "1000000",
                    "signedXdr": (
                        "AAAAAgAAAABqVFqpZzXx+KxRjXXFGO3sKwHCEYdHsWxDRrJTLGPDowAAAGQABVECAAAAAQAAAAEAAAAAAAAAAAAA"
                        "AABmWFbUAAAAAAAAAAEAAAAAAAAABgAAAAFVU0RCAAAAAABbjPEfrLNLCLjNQyaWWgTeFn4tnbFnNd9FTJ3HgkLUCwAAAAAAAAAAAAAAAAAAAAE="
                    ),
                },
            )

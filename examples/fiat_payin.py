"""Workflow: collect a fiat payin into a blockchain wallet (quote, then payin). Amounts are integer cents."""

import asyncio
import os

from _helpers import unwrap

from blindpay import BlindPay


async def collect(blindpay: BlindPay, blockchain_wallet_id: str, amount_cents: int) -> str:
    quote = await blindpay.payins.quotes.create(
        {
            "blockchain_wallet_id": blockchain_wallet_id,
            "currency_type": "sender",
            "payment_method": "pix",
            "request_amount": amount_cents,
            "token": "USDC",
        }
    )
    payin = unwrap(await blindpay.payins.create_evm(unwrap(quote)["id"]))
    return payin["id"]  # then wait for the payin.complete webhook


async def main() -> None:
    async with BlindPay(
        api_key=os.environ["BLINDPAY_API_KEY"], instance_id=os.environ["BLINDPAY_INSTANCE_ID"]
    ) as client:
        print(await collect(client, os.environ["BLOCKCHAIN_WALLET_ID"], 10000))


if __name__ == "__main__":
    asyncio.run(main())

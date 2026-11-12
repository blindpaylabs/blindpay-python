# BlindPay Python SDK - Examples

Each example reads `BLINDPAY_API_KEY` and `BLINDPAY_INSTANCE_ID` (plus the ids it needs) from the environment. Use a
development instance: settlement is simulated there. CI type-checks every file here (pyright strict and mypy), and
nothing here runs against the API in CI.

| File | Workflow |
|---|---|
| `webhook_endpoint.py` | Register a webhook endpoint, then verify deliveries against the raw body, dedupe on `svix-id`, and handle a failed payout on `payout.update` or `payout.complete` |
| `managed_wallet_payout.py` | Quote with `bank_account_id`, then `payouts.create_evm` with `wallet_id` and an explicit idempotency key; what to do after a 5xx |
| `managed_wallet_payin_payout.py` | Create a managed wallet, fund it with a payin quote (`wallet_id`) and `payins.create_evm`, then pay a bank account with `payouts.create_evm` and `wallet_id`; the dev sentinels `66600` (failed) and `77700` (refunded) |
| `fiat_payin.py` | Payin quote, then payin (async client) |
| `reconciliation.py` | Sum a customer's completed payouts with `list_auto_paging` and filters |
| `get_available_rails.py` | Rails and their bank-detail fields, async and sync |

`_helpers.unwrap` turns a `{data, error}` result into its data or raises with the API error's code and request id.

```bash
pip install blindpay
BLINDPAY_API_KEY=... BLINDPAY_INSTANCE_ID=... CUSTOMER_ID=... python examples/reconciliation.py
```

# Blindpay Python SDK

Official Python SDK for Blindpay API - Global payments infrastructure.

## Installation

```bash
pip install blindpay
```

## Requirements

- Python 3.12 or higher
- httpx
- pydantic

## Quick Start

```python
import asyncio
from blindpay import BlindPay

async def main():
    # Initialize the client
    client = BlindPay(
        api_key="your-api-key",
        instance_id="your-instance-id"
    )
    
    # List available countries
    response = await client.available["countries"]()
    if response["error"]:
        print(f"Error: {response['error']['message']}")
    else:
        print(f"Countries: {response['data']}")
    
    # Create a receiver
    response = await client.receivers["create"](
        type="individual",
        kyc_type="light",
        email="john.doe@example.com",
        first_name="John",
        last_name="Doe",
        # ... other fields
    )
    
    # Close the client when done
    await client.close()

# Run the async function
asyncio.run(main())
```

## Resources

The SDK provides access to the following resources:

### Available
```python
# Get available rails
await client.available["get_rails"]()

# Get bank details
await client.available["get_bank_details"]()
```

### Instances
```python
# Get instance details
await client.instances["get"]()

# Update instance
await client.instances["update"](name="New Name")

# API Keys
await client.instances["api_keys"]["list"]()
await client.instances["api_keys"]["create"](name="API Key Name", permission="full_access")
await client.instances["api_keys"]["get"]("api-key-id")
await client.instances["api_keys"]["delete"]("api-key-id")

# Webhook Endpoints
await client.instances["webhook_endpoints"]["list"]()
await client.instances["webhook_endpoints"]["create"](url="https://example.com/webhook")
await client.instances["webhook_endpoints"]["get"]("webhook-id")
await client.instances["webhook_endpoints"]["update"]("webhook-id", enabled=False)
await client.instances["webhook_endpoints"]["delete"]("webhook-id")
```

### Receivers
```python
# List receivers
await client.receivers["list"]()

# Create a receiver
await client.receivers["create"](
    type="individual",
    kyc_type="light",
    email="john.doe@example.com",
    first_name="John",
    last_name="Doe",
    # ... other fields
)

# Get a receiver
await client.receivers["get"]("receiver-id")

# Update a receiver
await client.receivers["update"]("receiver-id", email="new.email@example.com")

# Delete a receiver
await client.receivers["delete"]("receiver-id")

# Submit KYC
await client.receivers["submit_kyc"]("receiver-id")

# Bank Accounts
await client.receivers["bank_accounts"]["list"]("receiver-id")
await client.receivers["bank_accounts"]["create"]("receiver-id", type="pix", pix_key="key")
await client.receivers["bank_accounts"]["get"]("receiver-id", "bank-account-id")
await client.receivers["bank_accounts"]["update"]("receiver-id", "bank-account-id", name="New Name")
await client.receivers["bank_accounts"]["delete"]("receiver-id", "bank-account-id")
```

### Quotes
```python
# Create a quote
await client.quotes["create"](
    bank_account_id="bank-account-id",
    currency_type="receiver",
    request_amount=1000,
    cover_fees=False,
    # ... other fields
)

# Get FX rate
await client.quotes["get_fx_rate"](
    currency_type="sender",
    from_currency="USD",
    to="BRL",
    request_amount=1000
)
```

### Payins
```python
# List payins
await client.payins["list"]()

# Get a payin
await client.payins["get"]("payin-id")

# Get payin tracking
await client.payins["get_track"]("payin-id")

# Export payins
await client.payins["export"](status="completed")

# Create EVM payin
await client.payins["create_evm"]("payin-quote-id")

# Payin Quotes
await client.payins["quotes"]["create"](
    receiver_id="receiver-id",
    bank_account_id="bank-account-id",
    # ... other fields
)
await client.payins["quotes"]["get"]("quote-id")
```

### Payouts
```python
# List payouts
await client.payouts["list"]()

# Create a payout
await client.payouts["create"](
    bank_account_id="bank-account-id",
    amount=1000,
    # ... other fields
)

# Get a payout
await client.payouts["get"]("payout-id")

# Get payout tracking
await client.payouts["get_track"]("payout-id")

# Export payouts
await client.payouts["export"](status="completed")
```

### Virtual Accounts
```python
# List virtual accounts
await client.virtual_accounts["list"]()

# Create a virtual account
await client.virtual_accounts["create"](
    name="Account Name",
    # ... other fields
)

# Get a virtual account
await client.virtual_accounts["get"]("virtual-account-id")

# Get balance
await client.virtual_accounts["get_balance"]("virtual-account-id")

# List transactions
await client.virtual_accounts["list_transactions"]("virtual-account-id")

# Update a virtual account
await client.virtual_accounts["update"]("virtual-account-id", name="New Name")

# Delete a virtual account
await client.virtual_accounts["delete"]("virtual-account-id")
```

### Wallets

#### Blockchain Wallets
```python
# List blockchain wallets
await client.wallets["blockchain"]["list"]("receiver-id")

# Create with address
await client.wallets["blockchain"]["create_with_address"](
    receiver_id="receiver-id",
    name="Wallet Name",
    network="ethereum",
    address="0x..."
)

# Create with hash
await client.wallets["blockchain"]["create_with_hash"](
    receiver_id="receiver-id",
    name="Wallet Name",
    network="ethereum",
    signature_tx_hash="0x..."
)

# Get wallet message
await client.wallets["blockchain"]["get_wallet_message"]("receiver-id")

# Get a wallet
await client.wallets["blockchain"]["get"]("receiver-id", "wallet-id")

# Delete a wallet
await client.wallets["blockchain"]["delete"]("receiver-id", "wallet-id")
```

#### Offramp Wallets
```python
# List offramp wallets
await client.wallets["offramp"]["list"]("receiver-id")

# Create an offramp wallet
await client.wallets["offramp"]["create"](
    receiver_id="receiver-id",
    name="Wallet Name",
    network="ethereum",
    address="0x..."
)

# Get an offramp wallet
await client.wallets["offramp"]["get"]("receiver-id", "wallet-id")

# Delete an offramp wallet
await client.wallets["offramp"]["delete"]("receiver-id", "wallet-id")
```

### Partner Fees
```python
# List partner fees
await client.partner_fees["list"]()

# Create a partner fee
await client.partner_fees["create"](
    name="Fee Name",
    percentage=0.01,
    # ... other fields
)

# Get a partner fee
await client.partner_fees["get"]("partner-fee-id")

# Update a partner fee
await client.partner_fees["update"]("partner-fee-id", percentage=0.02)

# Delete a partner fee
await client.partner_fees["delete"]("partner-fee-id")
```

## Webhook Signature Verification

```python
from blindpay import BlindPay

client = BlindPay(
    api_key="your-api-key",
    instance_id="your-instance-id"
)

# Verify webhook signature
is_valid = client.verify_webhook_signature(
    secret="your-webhook-secret",
    id="svix-id-header-value",
    timestamp="svix-timestamp-header-value",
    payload="raw-request-body",
    svix_signature="svix-signature-header-value"
)

if is_valid:
    print("Webhook signature is valid")
else:
    print("Invalid webhook signature")
```

## Error Handling

All API methods return a response dictionary with either `data` or `error`:

```python
response = await client.receivers["get"]("receiver-id")

if response["error"]:
    print(f"Error: {response['error']['message']}")
else:
    receiver = response["data"]
    print(f"Receiver: {receiver}")
```

## Types

The SDK includes comprehensive type definitions for all API resources and parameters. These can be imported from the main package:

```python
from blindpay import (
    AccountClass,
    BankAccountType,
    Country,
    Currency,
    CurrencyType,
    Network,
    Rail,
    StablecoinToken,
    TransactionDocumentType,
    TransactionStatus,
    PaginationParams,
    PaginationMetadata,
    # ... and more
)
```

## Development

This SDK uses:
- `uv` for package management
- `httpx` for async HTTP requests
- `pydantic` for data validation

## License

MIT

## Support

For support, please contact gabriel@blindpay.com or visit [https://blindpay.com](https://blindpay.com)

# BlindPay Python SDK - Examples

This directory contains example code demonstrating how to use the BlindPay Python SDK.

## Prerequisites

Before running these examples, you need:

1. **API Credentials**: Get your API key and instance ID from the [BlindPay Dashboard](https://app.blindpay.com)
2. **Python 3.12+**: Ensure you have Python 3.12 or higher installed
3. **Install the SDK**: 
   ```bash
   pip install blindpay
   ```

## Examples

### 1. Get Available Rails (`get_available_rails.py`)

Demonstrates how to:
- Get list of available payment rails
- Get bank details required for specific rails
- Use both async and sync clients
- Handle errors properly
- Use context managers for automatic cleanup

**Run it:**
```bash
python examples/get_available_rails.py
```

## Quick Start

### Async Usage (Recommended)

```python
import asyncio
from blindpay import BlindPay

async def main():
    # Initialize the client
    client = BlindPay(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    )
    
    # Get available rails
    response = await client.available.get_rails()
    
    if response["error"]:
        print(f"Error: {response['error']['message']}")
        return
    
    # Success!
    rails = response["data"]
    for rail in rails:
        print(f"{rail['label']}: {rail['value']}")

asyncio.run(main())
```

### Sync Usage

```python
from blindpay import BlindPaySync

# Initialize the sync client
client = BlindPaySync(
    api_key="your_api_key_here",
    instance_id="your_instance_id_here",
)

# Get available rails
response = client.available.get_rails()

if response["error"]:
    print(f"Error: {response['error']['message']}")
else:
    rails = response["data"]
    for rail in rails:
        print(f"{rail['label']}: {rail['value']}")
```

### Context Manager (Auto-cleanup)

```python
from blindpay import BlindPaySync

with BlindPaySync(
    api_key="your_api_key_here",
    instance_id="your_instance_id_here",
) as client:
    response = client.available.get_rails()
    # Connection is automatically closed when exiting
```

## Response Format

All API methods return a response in this format:

```python
# Success response
{
    "data": {...},  # Your data here
    "error": None
}

# Error response
{
    "data": None,
    "error": {
        "message": "Error description"
    }
}
```

Always check for errors before accessing data:

```python
response = await client.available.get_rails()

if response["error"]:
    # Handle error
    print(f"Error: {response['error']['message']}")
else:
    # Use data
    data = response["data"]
```

## Available Resources

The SDK provides access to the following resources:

### Core Resources
- `client.available` - Available payment rails and bank details
- `client.instances` - Instance management and members
- `client.quotes` - Payment quotes management
- `client.partner_fees` - Partner fee management

### Receivers
- `client.receivers` - Receiver management
  - `client.receivers.bank_accounts` - Bank account management

### Payments
- `client.payins` - Payins management
  - `client.payins.quotes` - Payin quotes management
- `client.payouts` - Payouts management

### Virtual Accounts
- `client.virtual_accounts` - Virtual account management

### Wallets
- `client.wallets.blockchain` - Blockchain wallet operations
- `client.wallets.offramp` - Offramp wallet operations

### API Keys & Webhooks
- `client.instances.api_keys` - API key management
- `client.instances.webhook_endpoints` - Webhook configuration


## Error Handling Best Practices

```python
try:
    client = BlindPay(
        api_key="your_api_key",
        instance_id="your_instance_id",
    )
    
    response = await client.available.get_rails()
    
    if response["error"]:
        # API returned an error
        error_message = response["error"]["message"]
        logger.error(f"API error: {error_message}")
        # Handle the error appropriately
        return
    
    # Successful response
    data = response["data"]
    
except Exception as e:
    # Unexpected error (network, etc.)
    logger.exception("Unexpected error occurred")
    # Handle unexpected errors
```

## Environment Variables

For production use, store credentials as environment variables:

```python
import os
from blindpay import BlindPay

client = BlindPay(
    api_key=os.environ.get("BLINDPAY_API_KEY"),
    instance_id=os.environ.get("BLINDPAY_INSTANCE_ID"),
)
```

## Need Help?

- **Documentation**: [https://api.blindpay.com/reference](https://api.blindpay.com/reference)
- **Dashboard**: [https://app.blindpay.com](https://app.blindpay.com)
- **Support**: [gabriel@blindpay.com](mailto:gabriel@blindpay.com)


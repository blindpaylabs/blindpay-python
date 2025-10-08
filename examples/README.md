# BlindPay Python SDK - Examples

This directory contains example code demonstrating how to use the BlindPay Python SDK.

## Prerequisites

Before running these examples, you need:

1. **API Credentials**: Get your API key and instance ID from the [BlindPay dashboard](https://app.blindpay.com)
2. **Python 3.12+**: Ensure you have Python 3.12 or higher installed
3. **Install the SDK**: 
   ```bash
   pip install blindpay
   ```

## Examples

### 1. Get Available Rails (`examples/get_available_rails.py`)

Demonstrates how to:
- Get list of available payment rails
- Get bank details required for specific rails
- Use both async and sync clients
- Simple error handling (always remember to handle errors properly)

**Copy the code and run it:**
```bash
python3 your_file_name.py
```

## Quick Start

### Async Usage (Recommended)

```python
import asyncio
from blindpay import BlindPay

async def main():
    # Initialize the client
    blindpay = BlindPay(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    )
    
    # Get available rails
    response = await blindpay.available.get_rails()
    
    if response["error"]:
        print(f"Error: {response['error']['message']}")
        return
    
    rails = response["data"]
    for rail in rails:
        print(f"{rail['label']}: {rail['value']}")

asyncio.run(main())
```

### Sync Usage

```python
from blindpay import BlindPaySync

# Initialize the sync client
blindpay = BlindPaySync(
    api_key="your_api_key_here",
    instance_id="your_instance_id_here",
)

# Get available rails
response = blindpay.available.get_rails()

if response["error"]:
    print(f"Error: {response['error']['message']}")
else:
    rails = response["data"]
    for rail in rails:
        print(f"{rail['label']}: {rail['value']}")
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
response = await blindpay.available.get_rails()

if response["error"]:
    # Handle error
    print(f"Error: {response['error']['message']}")
else:
    # Use data
    data = response["data"]
```

## Environment Variables

For production use, store credentials as environment variables:

```python
import os
from blindpay import BlindPay

blindpay = BlindPay(
    api_key=os.environ.get("BLINDPAY_API_KEY"),
    instance_id=os.environ.get("BLINDPAY_INSTANCE_ID"),
)
```

## Need Help?

- **Documentation**: [https://api.blindpay.com/reference](https://api.blindpay.com/reference)
- **Dashboard**: [https://app.blindpay.com](https://app.blindpay.com)
- **Support**: [gabriel@blindpay.com](mailto:gabriel@blindpay.com)


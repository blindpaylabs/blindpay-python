# BlindPay Python SDK

The official Python SDK for Blindpay - Global payments infrastructure made simple.

## Installation

```bash
pip install blindpay
```

## Requirements

- Python 3.12 or higher

## Error Handling

All API methods return a response dictionary with either `data` or `error`:

```python
    blindpay = BlindPay(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here"
    )

    response = await blindpay.receivers.get("receiver-id")

    if response['error']:
        print(f"Error: {response['error']['message']}")
        return

    receiver = response['data']
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
- `typing_extensions` for typing

## License

MIT

## Support

For support, please contact gabriel@blindpay.com or visit [blindpay](https://blindpay.com)

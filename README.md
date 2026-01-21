<h1>BlindPay Python SDK <img src="https://github.com/user-attachments/assets/c42b121d-adf1-467c-88ce-6f5be1efa93c" align="right" width="102"/></h1>

[![chat on Discord](https://img.shields.io/discord/856971667393609759.svg?logo=discord)](https://discord.gg/x7ap6Gkbe9)
[![twitter](https://img.shields.io/twitter/follow/blindpaylabs?style=social)](https://twitter.com/intent/follow?screen_name=blindpaylabs)
[![Version](https://img.shields.io/github/v/release/blindpaylabs/blindpay-swift?include_prereleases)](https://github.com/blindpaylabs/blindpay-swift/releases)

The official Python SDK for [BlindPay](https://blindpay.com) - Stablecoin API for global payments.

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

# BlindPay Python SDK <img src="https://github.com/user-attachments/assets/c42b121d-adf1-467c-88ce-6f5be1efa93c" align="right" width="102"/>

[![chat on Discord](https://img.shields.io/discord/856971667393609759.svg?logo=discord)](https://discord.gg/x7ap6Gkbe9)
[![twitter](https://img.shields.io/twitter/follow/blindpaylabs?style=social)](https://twitter.com/intent/follow?screen_name=blindpaylabs)
[![Version](https://img.shields.io/github/v/release/blindpaylabs/blindpay-python?include_prereleases)](https://github.com/blindpaylabs/blindpay-python/releases)

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

    response = await blindpay.customers.get("customer-id")

    if response['error']:
        print(f"Error: {response['error']['message']}")
        return

    customer = response['data']
    print(f"Customer: {customer}")
```

## Webhooks

Verify every delivery against the **raw** request body, before parsing it. No client or API key is needed:

```python
from blindpay import webhooks

# Flask: request.get_data(); FastAPI/Starlette: await request.body()
raw_body = request.get_data()

if not webhooks.verify(raw_body, request.headers, secret):  # secret: "whsec_..."
    abort(400)
```

`verify` checks the Svix `v1` signatures in `svix-signature` and rejects timestamps more than 5 minutes from now
(`tolerance=` changes that). Deduplicate deliveries on the `svix-id` header, and never log the secret.

## Uploads

`upload.create` and `upload.analyze` send `multipart/form-data`. Pass bytes or a binary file object:

```python
with open("proof_of_address.pdf", "rb") as f:
    response = await blindpay.upload.create({"bucket": "onboarding", "file": f})

file_url = response["data"]["file_url"]
```

The API checks the file's MIME type, which the SDK guesses from the filename (or the file's first bytes). Pass
`filename` and `content_type` to set them explicitly.

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
- `typing_extensions` for typing

## License

MIT

## Support

For support, please contact alves@blindpay.com or visit [blindpay](https://blindpay.com)

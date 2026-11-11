"""
Example: Get Available Rails

This example demonstrates how to use the BlindPay SDK to fetch available
payment rails and their bank details
"""

import asyncio

from _helpers import unwrap

from blindpay import BlindPay, BlindPaySync


async def async_example() -> None:
    print("=== Async Example ===\n")

    async with BlindPay(api_key="your_api_key_here", instance_id="your_instance_id_here") as blindpay:
        rails = unwrap(await blindpay.available.get_rails())
        print(f"Found {len(rails)} available rails:\n")
        for rail in rails:
            print(f"  • {rail['label']} ({rail['value']}) - {rail['country']}")

        print("\n--- Getting bank details for PIX ---\n")
        bank_details = unwrap(await blindpay.available.get_bank_details("pix"))
        print(f"PIX requires {len(bank_details)} fields:\n")
        for detail in bank_details:
            required = "Required" if detail.get("required") else "Optional"
            print(f"  • {detail['label']} ({detail['key']}) - {required}")


def sync_example() -> None:
    print("\n\n=== Sync Example ===\n")

    with BlindPaySync(api_key="your_api_key_here", instance_id="your_instance_id_here") as blindpay:
        rails = unwrap(blindpay.available.get_rails())
        print(f"Found {len(rails)} available rails:\n")
        for rail in rails:
            print(f"  • {rail['label']} ({rail['value']}) - {rail['country']}")

        print("\n--- Getting bank details for ACH ---\n")
        bank_details = unwrap(blindpay.available.get_bank_details("ach"))
        print(f"ACH requires {len(bank_details)} fields:\n")
        for detail in bank_details:
            required = "Required" if detail.get("required") else "Optional"
            print(f"  • {detail['label']} ({detail['key']}) - {required}")


if __name__ == "__main__":
    asyncio.run(async_example())

    sync_example()

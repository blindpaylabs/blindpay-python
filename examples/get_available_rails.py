"""
Example: Get Available Rails

This example demonstrates how to use the BlindPay SDK to fetch available
payment rails and their bank details
"""

import asyncio

from blindpay import BlindPay, BlindPaySync


async def async_example() -> None:
    print("=== Async Example ===\n")

    blindpay = BlindPay(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    )

    # Get available rails
    rails_response = await blindpay.available.get_rails()

    if rails_response["error"]:
        print(f"Error: {rails_response['error']['message']}")
        return

    rails = rails_response["data"]
    if rails is None:
        print("No rails data returned")
        return

    print(f"Found {len(rails)} available rails:\n")

    for rail in rails:
        print(f"  • {rail['label']} ({rail['value']}) - {rail['country']}")

    # Get bank details for a specific rail (e.g., PIX)
    print("\n--- Getting bank details for PIX ---\n")
    bank_details_response = await blindpay.available.get_bank_details("pix")

    if bank_details_response["error"]:
        print(f"Error: {bank_details_response['error']['message']}")
        return

    bank_details = bank_details_response["data"]
    if bank_details is None:
        print("No bank details returned")
        return

    print(f"PIX requires {len(bank_details)} fields:\n")

    for detail in bank_details:
        required = "Required" if detail["required"] else "Optional"
        print(f"  • {detail['label']} ({detail['key']}) - {required}")


def sync_example() -> None:
    print("\n\n=== Sync Example ===\n")

    blindpay = BlindPaySync(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    )

    # Get available rails
    rails_response = blindpay.available.get_rails()

    if rails_response["error"]:
        print(f"Error: {rails_response['error']['message']}")
        return

    rails = rails_response["data"]
    if rails is None:
        print("No rails data returned")
        return

    print(f"Found {len(rails)} available rails:\n")

    for rail in rails:
        print(f"  • {rail['label']} ({rail['value']}) - {rail['country']}")

    # Get bank details for ACH
    print("\n--- Getting bank details for ACH ---\n")
    bank_details_response = blindpay.available.get_bank_details("ach")

    if bank_details_response["error"]:
        print(f"Error: {bank_details_response['error']['message']}")
        return

    bank_details = bank_details_response["data"]
    if bank_details is None:
        print("No bank details returned")
        return

    print(f"ACH requires {len(bank_details)} fields:\n")

    for detail in bank_details:
        required = "Required" if detail["required"] else "Optional"
        print(f"  • {detail['label']} ({detail['key']}) - {required}")


if __name__ == "__main__":
    asyncio.run(async_example())

    sync_example()

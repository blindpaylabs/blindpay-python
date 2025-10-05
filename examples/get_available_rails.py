"""
Example: Get Available Rails

This example demonstrates how to use the BlindPay SDK to fetch available
payment rails and their bank details
"""

import asyncio

from blindpay import BlindPay, BlindPaySync


async def async_example():
    print("=== Async Example ===\n")

    client = BlindPay(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    )

    # Get available rails
    rails_response = await client.available.get_rails()

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
    bank_details_response = await client.available.get_bank_details("pix")

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


def sync_example():
    print("\n\n=== Sync Example ===\n")

    client = BlindPaySync(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    )

    # Get available rails
    rails_response = client.available.get_rails()

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
    bank_details_response = client.available.get_bank_details("ach")

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


def context_manager_example():
    """Example using context manager (auto-closes connection)"""
    print("\n\n=== Context Manager Example ===\n")

    with BlindPaySync(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    ) as client:
        rails_response = client.available.get_rails()

        if rails_response["error"]:
            print(f"Error: {rails_response['error']['message']}")
        elif rails_response["data"]:
            rails = rails_response["data"]
            print(f"Available rails: {[r['value'] for r in rails]}")
        else:
            print("No data returned")

    # Connection is automatically closed when exiting the context


def error_handling_example():
    """Example with proper error handling"""
    print("\n\n=== Error Handling Example ===\n")

    try:
        client = BlindPaySync(
            api_key="your_api_key_here",
            instance_id="your_instance_id_here",
        )

        response = client.available.get_rails()

        # Check for errors
        if response["error"]:
            error_msg = response["error"]["message"]
            print(f"❌ API Error: {error_msg}")
            # Handle the error appropriately
            return

        # Process the successful response
        rails = response["data"]
        if rails is None:
            print("⚠️  No data returned")
            return

        print(f"✅ Success! Retrieved {len(rails)} rails")

        # Do something with the data
        for rail in rails:
            print(f"   - {rail['label']}: {rail['value']}")

    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        # Handle unexpected errors


if __name__ == "__main__":
    asyncio.run(async_example())

    sync_example()

    context_manager_example()

    error_handling_example()

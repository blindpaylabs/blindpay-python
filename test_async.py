import asyncio

from blindpay import BlindPay


async def main() -> None:
    # Initialize the async client
    client = BlindPay(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    )

    # Get available rails
    print("Fetching available rails...\n")
    response = await client.available.get_rails()

    # Check for errors
    if response["data"]:
        print(f"✅ Success! Found {len(response['data'])} available rails:\n")
        for rail in response["data"]:
            print(f"  • {rail['label']:25} {rail['value']:15} ({rail['country']})")


if __name__ == "__main__":
    asyncio.run(main())

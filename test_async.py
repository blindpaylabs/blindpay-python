import asyncio

from blindpay import BlindPay


async def main():
    # Initialize the async client
    client = BlindPay(
        api_key="your_api_key_here",
        instance_id="your_instance_id_here",
    )

    # Get available rails
    print("Fetching available rails...\n")
    response = await client.available.get_rails()

    # Check for errors
    if response["error"]:
        print(f"❌ Error: {response['error']['message']}")
    else:
        rails = response["data"]
        if rails is None:
            print("⚠️  No data returned")
        else:
            print(f"✅ Success! Found {len(rails)} available rails:\n")
            for rail in rails:
                print(f"  • {rail['label']:25} {rail['value']:15} ({rail['country']})")


if __name__ == "__main__":
    asyncio.run(main())

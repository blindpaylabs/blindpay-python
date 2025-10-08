from blindpay import BlindPaySync

# Initialize the sync client
client = BlindPaySync(
    api_key="your_api_key_here",
    instance_id="your_instance_id_here",
)

# Get available rails
print("Fetching available rails...\n")
response = client.available.get_rails()

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

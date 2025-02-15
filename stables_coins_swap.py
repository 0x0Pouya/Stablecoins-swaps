import time
import requests

# List of swap platforms and their respective API endpoints
PLATFORMS = [
    {'name': 'Platform A', 'api_url': 'https://platforma.com/api'},
    {'name': 'Platform B', 'api_url': 'https://platformb.com/api'},
    # Add more platforms as needed
]

# Fetch swap rates from a specific platform with error handling
def fetch_swap_rates(platform):
    api_url = platform['api_url'] + '/swap_rates'
    try:
        response = requests.get(api_url, timeout=5)
        response.raise_for_status()  # Raise an error for non-2xx status codes
        swap_rates = response.json()

        # Ensure required keys exist, fallback to a high value if missing
        return {
            'USDC': swap_rates.get('USDC', float('inf')),
            'USDT': swap_rates.get('USDT', float('inf')),
            'NativeUSD': swap_rates.get('NativeUSD', float('inf')),
        }
    except requests.RequestException as e:
        print(f"Error fetching data from {platform['name']}: {e}")
        return {'USDC': float('inf'), 'USDT': float('inf'), 'NativeUSD': float('inf')}

# Determine the cheapest option among swap platforms
def find_cheapest_option():
    cheapest_rate = float('inf')
    cheapest_platform = None

    for platform in PLATFORMS:
        stable_coin_rates = fetch_swap_rates(platform)
        min_rate = min(stable_coin_rates.values())

        if min_rate < cheapest_rate:
            cheapest_rate = min_rate
            cheapest_platform = platform

    return cheapest_platform, cheapest_rate

# Execute the swap on the cheapest platform
def execute_swap(platform, source_asset, destination_asset, amount):
    api_url = platform['api_url'] + '/execute_swap'
    payload = {
        'source_asset': source_asset,
        'destination_asset': destination_asset,
        'amount': amount,
    }
    
    try:
        response = requests.post(api_url, json=payload, timeout=5)
        response.raise_for_status()
        print(f'Swap executed successfully on {platform["name"]}!')
    except requests.RequestException as e:
        print(f'Failed to execute swap on {platform["name"]}: {e}')

# Terminal application
def main():
    print('Welcome to the Asset Swapping Terminal!')
    
    try:
        duration = int(input('Enter the duration in minutes: '))
        trigger_price = float(input('Enter the trigger price: '))
        source_asset = input('Enter the source asset: ').strip()
        destination_asset = input('Enter the destination asset: ').strip()
        amount = float(input('Enter the amount: '))
        interval = int(input('Enter the polling interval in seconds (default 10): ') or 10)
    except ValueError:
        print("Invalid input. Please enter numeric values where required.")
        return

    end_time = time.time() + duration * 60

    while time.time() < end_time:
        cheapest_platform, cheapest_rate = find_cheapest_option()

        if not cheapest_platform:
            print("No valid swap rates found. Retrying...")
            time.sleep(interval)
            continue

        print(f'\nBest price found: {cheapest_rate} on {cheapest_platform["name"]}')

        if cheapest_rate <= trigger_price:
            print(f'Trigger price reached! Executing swap on {cheapest_platform["name"]}...')
            execute_swap(cheapest_platform, source_asset, destination_asset, amount)
            break
        else:
            print('Trigger price not reached. Continuing to monitor...')

        time.sleep(interval)

    print('Duration expired. No swap executed.')

# Run the terminal application
if __name__ == '__main__':
    main()

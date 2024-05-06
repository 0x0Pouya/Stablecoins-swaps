import time
import requests

# List of swap platforms and their respective API endpoints
PLATFORMS = [
    {
        'name': 'Platform A',
        'api_url': 'https://platforma.com/api',
    },
    {
        'name': 'Platform B',
        'api_url': 'https://platformb.com/api',
    },
    # Add more platforms as needed
]

# Fetch swap rates from a specific platform
def fetch_swap_rates(platform):
    api_url = platform['api_url'] + '/swap_rates'
    response = requests.get(api_url)
    swap_rates = response.json()
    return swap_rates

# Determine the cheapest option among swap platforms
def find_cheapest_option():
    cheapest_rate = float('inf')
    cheapest_platform = None

    for platform in PLATFORMS:
        swap_rates = fetch_swap_rates(platform)
        # Consider only stable coin swap rates (USDC, USDT, native USD)
        stable_coin_rates = {
            'USDC': swap_rates['USDC'],
            'USDT': swap_rates['USDT'],
            'NativeUSD': swap_rates['NativeUSD'],
        }

        # Find the minimum swap rate among stable coins
        min_rate = min(stable_coin_rates.values())

        if min_rate < cheapest_rate:
            cheapest_rate = min_rate
            cheapest_platform = platform

    return cheapest_platform, cheapest_rate

# Execute the swap on the cheapest platform
def execute_swap(source_asset, destination_asset, amount):
    cheapest_platform, _ = find_cheapest_option()
    api_url = cheapest_platform['api_url'] + '/execute_swap'
    payload = {
        'source_asset': source_asset,
        'destination_asset': destination_asset,
        'amount': amount,
    }
    response = requests.post(api_url, json=payload)
    if response.status_code == 200:
        print('Swap executed successfully!')
    else:
        print('Failed to execute swap.')

# Terminal application
def main():
    print('Welcome to the Asset Swapping Terminal!')

    duration = int(input('Enter the duration in minutes: '))
    trigger_price = float(input('Enter the trigger price: '))
    source_asset = input('Enter the source asset: ')
    destination_asset = input('Enter the destination asset: ')
    amount = float(input('Enter the amount: '))

    end_time = time.time() + duration * 60

    while time.time() < end_time:
        cheapest_platform, cheapest_rate = find_cheapest_option()

        print(f'\nBest price found: {cheapest_rate} on {cheapest_platform["name"]}')

        if cheapest_rate >= trigger_price:
            print(f'Trigger price reached! Executing swap...')
            execute_swap(source_asset, destination_asset, amount)
            break
        else:
            print('Trigger price not reached. Continuing to monitor...')

        time.sleep(10)  # Wait for 10 seconds before checking again

    print('Duration expired. No swap executed.')

# Run the terminal application
if __name__ == '__main__':
    main()

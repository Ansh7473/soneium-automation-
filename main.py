import asyncio
from web3 import Web3
from src.utils import load_config, load_private_keys, load_proxies, init_web3
from src.tasks import run_task

async def main():
    # Load configuration, private keys, and proxies
    config = load_config()
    private_keys = load_private_keys()
    proxies = load_proxies()

    # Ensure there are enough proxies for all private keys
    if len(proxies) < len(private_keys):
        print("Error: Not enough proxies for private keys.")
        return

    # Process each wallet with its assigned proxy
    for i, key in enumerate(private_keys):
        account = Web3().eth.account.from_key(key)  # Create account object
        proxy = proxies[i]
        print(f"Processing {account.address} with proxy {proxy}")

        # Initialize Web3 instance with the specific proxy
        web3 = init_web3(config["rpc_url"], proxy)

        # Check the wallet's balance
        balance = web3.eth.get_balance(account.address) / 10**18
        if balance < config["minimum_balance"]:
            print(f"Skipping {account.address} - Low balance: {balance} {config['native_token']}")
            continue

        # Execute tasks for this wallet using the proxied Web3 instance
        for task in config["tasks"]:
            if "rotate_swaps" in task:
                await run_task("rotate_swaps", web3, account, task["rotate_swaps"], proxy)

if __name__ == "__main__":
    asyncio.run(main())

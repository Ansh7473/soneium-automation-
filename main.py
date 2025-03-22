# main.py
import asyncio
from web3 import Web3
from src.utils import load_config, load_private_keys, load_proxies, init_web3
from src.tasks import TASKS, run_task

async def main():
    # Load config and data
    config = load_config()
    private_keys = load_private_keys()
    proxies = load_proxies()

    # Initialize Web3 for Soneium
    web3 = init_web3(config["rpc_url"])
    web3.eth.default_account = web3.eth.accounts[0]  # Set a default for gas estimation

    # Validate proxies
    if len(proxies) < len(private_keys):
        print("Error: Not enough proxies for private keys.")
        return

    # Process each account
    for i, key in enumerate(private_keys):
        account = web3.eth.account.from_key(key)
        proxy = proxies[i]
        print(f"Processing {account.address} with proxy {proxy}")

        # Check balance
        balance = web3.eth.get_balance(account.address) / 10**18
        if balance < config["minimum_balance"]:
            print(f"Skipping {account.address} - Low balance: {balance} {config['native_token']}")
            continue

        # Execute tasks
        for task in config["tasks"]:
            if task in TASKS:
                await run_task(task, web3, account, config)
            else:
                print(f"Unknown task: {task}")

if __name__ == "__main__":
    asyncio.run(main())

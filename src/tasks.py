from src.dapp_modules.kyo_finance import execute_swap

async def rotate_swaps(web3, account, rotate_config, proxy):
    num_rotations = rotate_config["num_rotations"]
    eth_to_usdc_amount = rotate_config["eth_to_usdc_amount"]
    usdc_to_eth_amount = rotate_config["usdc_to_eth_amount"]
    
    for i in range(num_rotations):
        print(f"Starting rotation {i+1}/{num_rotations}")
        
        # Swap ETH to USDC
        await execute_swap(web3, account, {
            "token_in": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",  # ETH
            "token_out": "0xba9986d2381edf1da03b0b9c1f8b00dc4aacc369",  # USDC
            "swap_amount": eth_to_usdc_amount
        }, proxy)
        
        # Swap USDC back to ETH
        await execute_swap(web3, account, {
            "token_in": "0xba9986d2381edf1da03b0b9c1f8b00dc4aacc369",  # USDC
            "token_out": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",  # ETH
            "swap_amount": usdc_to_eth_amount
        }, proxy)

async def run_task(task_name, web3, account, config, proxy):
    if task_name == "rotate_swaps":
        await rotate_swaps(web3, account, config, proxy)

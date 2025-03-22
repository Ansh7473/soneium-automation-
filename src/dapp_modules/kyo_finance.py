from web3 import Web3

UNIVERSAL_ROUTER = "0x11feF46913EF8de4501e6B9452Ec77c26e736818"
ETH_ADDRESS = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"
USDC_ADDRESS = "0xba9986d2381edf1da03b0b9c1f8b00dc4aacc369"

# Simplified ABI for UniversalRouter (replace with full ABI if needed)
UNIVERSAL_ROUTER_ABI = [
    {
        "inputs": [
            {"name": "commands", "type": "bytes"},
            {"name": "inputs", "type": "bytes[]"},
            {"name": "deadline", "type": "uint256"}
        ],
        "name": "execute",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    }
]

def get_token_decimals(web3, token_address):
    if token_address == ETH_ADDRESS:
        return 18
    erc20_abi = [{"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}]
    token_contract = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=erc20_abi)
    return token_contract.functions.decimals().call()

def get_token_balance(web3, account, token_address):
    if token_address == ETH_ADDRESS:
        return web3.eth.get_balance(account.address)
    erc20_abi = [{"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"}]
    token_contract = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=erc20_abi)
    return token_contract.functions.balanceOf(account.address).call()

async def approve_token(web3, account, token_address, amount_wei):
    if token_address == ETH_ADDRESS:
        return
    erc20_abi = [
        {"constant": False, "inputs": [{"name": "spender", "type": "address"}, {"name": "value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
    ]
    token_contract = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=erc20_abi)
    tx = token_contract.functions.approve(UNIVERSAL_ROUTER, amount_wei).build_transaction({
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gas": 100000,
        "gasPrice": web3.to_wei("5", "gwei")
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approved {amount_wei} of token {token_address}: {tx_hash.hex()}")

async def execute_swap(web3, account, swap_config, proxy):
    universal_router = web3.to_checksum_address(UNIVERSAL_ROUTER)
    contract = web3.eth.contract(address=universal_router, abi=UNIVERSAL_ROUTER_ABI)
    
    token_in = swap_config["token_in"]
    token_out = swap_config["token_out"]
    amount = swap_config["swap_amount"]
    
    # Convert amount to wei based on token decimals
    decimals = get_token_decimals(web3, token_in)
    amount_in_wei = int(amount * 10**decimals)
    
    # Check balance
    balance = get_token_balance(web3, account, token_in)
    if balance < amount_in_wei:
        print(f"Insufficient {token_in} balance for {account.address}")
        return
    
    # Approve token if not ETH
    if token_in != ETH_ADDRESS:
        await approve_token(web3, account, token_in, amount_in_wei)
    
    # Swap logic
    commands = "0x00"  # V3_SWAP_EXACT_IN
    path = Web3.to_bytes(hexstr=token_in) + Web3.to_bytes(hexstr="0000fe68") + Web3.to_bytes(hexstr=token_out)  # 0.3% fee
    inputs = [web3.eth.abi.encode(["address", "uint256", "uint256", "bytes", "bool"], [account.address, amount_in_wei, 0, path, True])]
    deadline = int(web3.eth.get_block("latest")["timestamp"]) + 1000
    
    tx = contract.functions.execute(commands, inputs, deadline).build_transaction({
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gas": 300000,
        "gasPrice": web3.to_wei("5", "gwei"),
        "value": amount_in_wei if token_in == ETH_ADDRESS else 0
    })
    
    signed_tx = account.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    print(f"Swap completed: {tx_hash.hex()}")
    web3.eth.wait_for_transaction_receipt(tx_hash)

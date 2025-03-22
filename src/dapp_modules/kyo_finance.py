# src/dapp_modules/kyo_finance.py
from web3 import Web3

# Kyo Finance UniversalRouter address (Soneium Mainnet)
UNIVERSAL_ROUTER = "0x11feF46913EF8de4501e6B9452Ec77c26e736818"
ETH_ADDRESS = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"  # Native SONE
USDC_ADDRESS = "0xba9986d2381edf1da03b0b9c1f8b00dc4aacc369"  # USDC

# UniversalRouter ABI from Blockscout
UNIVERSAL_ROUTER_ABI = [
    {"inputs": [{"components": [{"internalType": "address", "name": "permit2", "type": "address"}, {"internalType": "address", "name": "weth9", "type": "address"}, {"internalType": "address", "name": "seaportV1_5", "type": "address"}, {"internalType": "address", "name": "seaportV1_4", "type": "address"}, {"internalType": "address", "name": "openseaConduit", "type": "address"}, {"internalType": "address", "name": "nftxZap", "type": "address"}, {"internalType": "address", "name": "x2y2", "type": "address"}, {"internalType": "address", "name": "foundation", "type": "address"}, {"internalType": "address", "name": "sudoswap", "type": "address"}, {"internalType": "address", "name": "elementMarket", "type": "address"}, {"internalType": "address", "name": "nft20Zap", "type": "address"}, {"internalType": "address", "name": "cryptopunks", "type": "address"}, {"internalType": "address", "name": "looksRareV2", "type": "address"}, {"internalType": "address", "name": "routerRewardsDistributor", "type": "address"}, {"internalType": "address", "name": "looksRareRewardsDistributor", "type": "address"}, {"internalType": "address", "name": "looksRareToken", "type": "address"}, {"internalType": "address", "name": "v2Factory", "type": "address"}, {"internalType": "address", "name": "v3Factory", "type": "address"}, {"internalType": "bytes32", "name": "pairInitCodeHash", "type": "bytes32"}, {"internalType": "bytes32", "name": "poolInitCodeHash", "type": "bytes32"}], "internalType": "struct RouterParameters", "name": "params", "type": "tuple"}], "stateMutability": "nonpayable", "type": "constructor"},
    {"inputs": [], "name": "BalanceTooLow", "type": "error"},
    {"inputs": [], "name": "BuyPunkFailed", "type": "error"},
    {"inputs": [], "name": "ContractLocked", "type": "error"},
    {"inputs": [], "name": "ETHNotAccepted", "type": "error"},
    {"inputs": [{"internalType": "uint256", "name": "commandIndex", "type": "uint256"}, {"internalType": "bytes", "name": "message", "type": "bytes"}], "name": "ExecutionFailed", "type": "error"},
    {"inputs": [], "name": "FromAddressIsNotOwner", "type": "error"},
    {"inputs": [], "name": "InsufficientETH", "type": "error"},
    {"inputs": [], "name": "InsufficientToken", "type": "error"},
    {"inputs": [], "name": "InvalidBips", "type": "error"},
    {"inputs": [{"internalType": "uint256", "name": "commandType", "type": "uint256"}], "name": "InvalidCommandType", "type": "error"},
    {"inputs": [], "name": "InvalidOwnerERC1155", "type": "error"},
    {"inputs": [], "name": "InvalidOwnerERC721", "type": "error"},
    {"inputs": [], "name": "InvalidPath", "type": "error"},
    {"inputs": [], "name": "InvalidReserves", "type": "error"},
    {"inputs": [], "name": "InvalidSpender", "type": "error"},
    {"inputs": [], "name": "LengthMismatch", "type": "error"},
    {"inputs": [], "name": "SliceOutOfBounds", "type": "error"},
    {"inputs": [], "name": "TransactionDeadlinePassed", "type": "error"},
    {"inputs": [], "name": "UnableToClaim", "type": "error"},
    {"inputs": [], "name": "UnsafeCast", "type": "error"},
    {"inputs": [], "name": "V2InvalidPath", "type": "error"},
    {"inputs": [], "name": "V2TooLittleReceived", "type": "error"},
    {"inputs": [], "name": "V2TooMuchRequested", "type": "error"},
    {"inputs": [], "name": "V3InvalidAmountOut", "type": "error"},
    {"inputs": [], "name": "V3InvalidCaller", "type": "error"},
    {"inputs": [], "name": "V3InvalidSwap", "type": "error"},
    {"inputs": [], "name": "V3TooLittleReceived", "type": "error"},
    {"inputs": [], "name": "V3TooMuchRequested", "type": "error"},
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "RewardsSent", "type": "event"},
    {"inputs": [{"internalType": "bytes", "name": "looksRareClaim", "type": "bytes"}], "name": "collectRewards", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "bytes", "name": "commands", "type": "bytes"}, {"internalType": "bytes[]", "name": "inputs", "type": "bytes[]"}], "name": "execute", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "bytes", "name": "commands", "type": "bytes"}, {"internalType": "bytes[]", "name": "inputs", "type": "bytes[]"}, {"internalType": "uint256", "name": "deadline", "type": "uint256"}], "name": "execute", "outputs": [], "stateMutability": "payable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256[]", "name": "", "type": "uint256[]"}, {"internalType": "uint256[]", "name": "", "type": "uint256[]"}, {"internalType": "bytes", "name": "", "type": "bytes"}], "name": "onERC1155BatchReceived", "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}], "stateMutability": "pure", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "bytes", "name": "", "type": "bytes"}], "name": "onERC1155Received", "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}], "stateMutability": "pure", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}, {"internalType": "address", "name": "", "type": "address"}, {"internalType": "uint256", "name": "", "type": "uint256"}, {"internalType": "bytes", "name": "", "type": "bytes"}], "name": "onERC721Received", "outputs": [{"internalType": "bytes4", "name": "", "type": "bytes4"}], "stateMutability": "pure", "type": "function"},
    {"inputs": [{"internalType": "bytes4", "name": "interfaceId", "type": "bytes4"}], "name": "supportsInterface", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "pure", "type": "function"},
    {"inputs": [{"internalType": "int256", "name": "amount0Delta", "type": "int256"}, {"internalType": "int256", "name": "amount1Delta", "type": "int256"}, {"internalType": "bytes", "name": "data", "type": "bytes"}], "name": "uniswapV3SwapCallback", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"stateMutability": "payable", "type": "receive"}
]

async def approve_token(web3, account, token_address, amount):
    if token_address == ETH_ADDRESS:
        return
    erc20_abi = [
        {"constant": False, "inputs": [{"name": "spender", "type": "address"}, {"name": "value", "type": "uint256"}],
         "name": "approve", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
    ]
    token_contract = web3.eth.contract(address=web3.to_checksum_address(token_address), abi=erc20_abi)
    tx = token_contract.functions.approve(UNIVERSAL_ROUTER, Web3.to_wei(amount, "ether")).build_transaction({
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gas": 100000,
        "gasPrice": web3.to_wei("5", "gwei")
    })
    signed_tx = account.sign_transaction(tx)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
    web3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approved {amount} of token {token_address} for UniversalRouter: {tx_hash.hex()}")

async def execute_swap(web3, account, config):
    universal_router = web3.to_checksum_address(UNIVERSAL_ROUTER)
    contract = web3.eth.contract(address=universal_router, abi=UNIVERSAL_ROUTER_ABI)
    
    token_in = web3.to_checksum_address(config["kyo_token_in"])
    token_out = web3.to_checksum_address(config["kyo_token_out"])
    amount = config["kyo_swap_amount"]
    num_swaps = config.get("kyo_num_swaps", 1)
    
    total_amount = amount * num_swaps
    await approve_token(web3, account, token_in, total_amount)
    
    for i in range(num_swaps):
        commands = "0x00"  # V3_SWAP_EXACT_IN
        path = Web3.to_bytes(hexstr=token_in) + Web3.to_bytes(hexstr="0000fe68") + Web3.to_bytes(hexstr=token_out)  # 0.3% fee
        inputs = [web3.eth.abi.encode(
            types=["address", "uint256", "uint256", "bytes", "bool"],
            values=[account.address, Web3.to_wei(amount, "ether"), 0, path, True]
        )]
        deadline = int(web3.eth.get_block("latest")["timestamp"]) + 1000
        
        tx = contract.functions.execute(commands, inputs, deadline).build_transaction({
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gas": 300000,
            "gasPrice": web3.to_wei("5", "gwei"),
            "value": Web3.to_wei(amount, "ether") if token_in == ETH_ADDRESS else 0
        })
        
        signed_tx = account.sign_transaction(tx)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Swap {i+1}/{num_swaps} ({token_in} to {token_out}) completed: {tx_hash.hex()}")
        web3.eth.wait_for_transaction_receipt(tx_hash)
    
    return tx_hash

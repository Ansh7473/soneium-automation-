import yaml
from web3 import Web3

def load_config(file_path="src/config.yaml"):
    with open(file_path, "r") as f:
        return yaml.safe_load(f)

def load_private_keys(file_path="data/private_keys.txt"):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def load_proxies(file_path="data/proxies.txt"):
    try:
        with open(file_path, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

def init_web3(rpc_url, proxy=None):
    if proxy:
        w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'proxies': {'http': proxy, 'https': proxy}}))
    else:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
    if not w3.is_connected():
        raise Exception("Failed to connect to RPC")
    return w3

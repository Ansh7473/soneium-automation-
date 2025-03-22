# src/tasks.py
from src.dapp_modules.kyo_finance import execute_swap

TASKS = [
    "kyo_swap"
]

async def kyo_swap(web3, account, config):
    await execute_swap(web3, account, config)

async def run_task(task_name, web3, account, config):
    tasks = {
        "kyo_swap": kyo_swap
    }
    if task_name in tasks:
        await tasks[task_name](web3, account, config)

from web3 import Web3
import asyncio
from flatlaunchpeg import FLATLAUNCHPEG_ABI

# add your blockchain connection information
infura_url = 'https://fabled-restless-valley.avalanche-testnet.discover.quiknode.pro/b9eee19d9197f6e3c1c5f71d2c5dad059d228e95/ext/bc/C/rpc'
web3 = Web3(Web3.HTTPProvider(infura_url))

contract_address = '0x2953Bc8814880bd9f4Eb530B244D44bf42F712F9'
launchpeg_abi = FLATLAUNCHPEG_ABI

contract = web3.eth.contract(address=contract_address, abi=launchpeg_abi)


# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    # and whatever

# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "PairCreated" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for Initialized in event_filter.get_all_entries():
            handle_event(Initialized)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "PairCreated" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.Initialized.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
    finally:
        loop.close()

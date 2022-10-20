import multiprocessing
import os
import collections
import asyncio
import textwrap

from multiprocessing import Process
from eth_account     import Account
from joepeg_abi      import JOEPEG_ABI
from colorama        import Fore, Back, Style
from dotenv          import load_dotenv
from utils           import print_banner, dim_text
from web3            import Web3

    ########################
    #   1. Initial Setup   #
    ########################

# NOTE: 
# This section accomplishes two tasks:
# 1. Retrieves the contract address of the JoePeg contract
# 2. Creates collections of RPC node addresses and private keys

# NOTE: 
# If you have more/less accounts/Nodes, you can adjust as needed
# Just add or remove the appropriate number of variables in LazyBoyz and Nodes
# EXAMPLE - ADDING AN ACCOUNT/NODE:
# LazyBoy:
# LazyBoy(private_key=os.getenv(<PRIVATE_KEY_NAME>))
# Nodes:
# Node(os.getenv(<NODE_ADDRESS_NAME>))

load_dotenv()

mint_address = os.getenv("JOEPEG_ADDRESS")

LazyBoy = collections.namedtuple('LazyBoy', [
    'private_key'
])

LazyBoyz = (
    LazyBoy(private_key=os.getenv("LAZY_BOY_ONE")),
    LazyBoy(private_key=os.getenv("LAZY_BOY_TWO")),
    LazyBoy(private_key=os.getenv("LAZY_BOY_THREE")),
)

Node = collections.namedtuple('Nodes', [
    'address'
])

Nodes = (
    Node(address=os.getenv("RPC_ONE")),
    Node(address=os.getenv("RPC_TWO")),
    Node(address=os.getenv("RPC_THREE")),
    # Node(address=os.getenv("RPC_FOUR")),
    # Node(address=os.getenv("RPC_FIVE")),
    Node(address=os.getenv("RPC_SIX")),
)

# NOTE:
# This function is only used to start the script by asking the user whether they want to mint or not
def start_script():
    print('Are you ready to mint? (Enter yes/no)')
    start = input()
    if start == 'no':
        print(Fore.DIM + ('Goodbye!'))
        exit()
    elif start == 'yes':
        print()
    else:
        print(Fore.DIM + ('Please enter "yes" or "no"'))
        start_script()

print_banner()
print()
start_script()

    ############################
    #   2. Connect to Web3     #
    ############################

print()
print(Fore.YELLOW + ('Starting to configure Lazy Boyz...'))
print()

# NOTE: 
# The following section accomplishes 2 things:
# 1. Each node is used to create seperate web3 connections and is stored in web3s
# 2. Each Private Key is used to create an account and is stored in accounts

# w3 = an instance of each web3 connection
w3 = [Web3(Web3.HTTPProvider(node.address)) for node in Nodes]
# accounts =  an in instance of each account
accounts = [Account.from_key(lazy.private_key) for lazy in LazyBoyz]
# signers  = an instance of each signer built using accounts & w3
signers = []

def get_signers():
    signer_count = 0
    for i in range(len(w3)):
        for i in range(len(accounts)):
            signers.append(w3[i].eth.account.signTransaction)
            signer_count = signer_count + 1
    print(Fore.GREEN + ('All Lazy Boyz Configured ✓'))
    print()
    print(Fore.BLUE + 'Configured ' + str(signer_count) + ' Signers Successfully ✓')
    print()
    print(Fore.YELLOW + ('Testing RPC Nodes...'))
    print()

get_signers()


# NOTE:
# This serves as a test to see that all of signers are configured correctly
# If isConnected() returns true, then we know that the signer is configured correctly

# FUNCTION WITHOUT ASCII TABLE:
# This is a lot easier to read than the actual function used-But it doesn't look as cool
# If you are trying to use this script as a guide, the following function is a lot easier to read
# 
def test_nodes():
    connected = 0
    disconnected = 0
    for i in range(len(Nodes)):
        if w3[i].isConnected():
            connected = connected + 1
        else:
            disconnected = disconnected + 1
    if disconnected > 0:
        print(Fore.RED + 'Disconnected Nodes: ' + str(disconnected))
    if connected == len(Nodes):
        print(Fore.GREEN + 'All Nodes Connected ✓')

test_nodes()

# NOTE:
# This function checks the balance of each Lazy Boy wallet and prints the results in an ASCII table
# If the balance is 0, then the user is prompted to add funds to the wallet then check again or continue
# (This is to prevent the user from accidentally minting with an empty wallet and useful for testing the script)

# FUNCTION WITHOUT ASCII TABLE:
# This is a lot easier to read than the actual function used-But it doesn't look as cool
# If you are trying to use this script as a guide, the following function is a lot easier to read

def print_wallet_balances():
    funded = 0
    unfunded = 0
    for i in range(len(accounts)):
        if w3[i].eth.getBalance(accounts[i].address) > 0:
            funded = funded + 1
        else:
            unfunded = unfunded + 1
    if unfunded > 0:
        print(Fore.RED + 'Unfunded Wallets: ' + str(unfunded))
        print(Fore.RED + ('Please add funds to your wallets or remove the unfunded wallets from the LazyBoyz list'))
        exit()
    if funded == len(accounts):
        print(Fore.GREEN + 'All Wallets Funded ✓')
        print()
        print(Fore.YELLOW + ('Starting to configure JoePeg Contract...'))
             
print_wallet_balances()

    ############################
    #  3. Connect to Contract  #
    ############################

# NOTE:
# This for function creates a unique contract object using all of the w3 instances
# This is done so that we can call the contract functions using each different Node + Signer

contract = []
def configure_contract():
    for i in range(len(w3)):
        contract.append(w3[i].eth.contract(address=mint_address, abi=JOEPEG_ABI))
        print(contract[i].address)
        print(contract[i].events)
    print()
    print(Fore.GREEN + ('JoePeg Contract Configured ✓'))
    print()
    print(Fore.BLUE + ('Created ' + str(len(w3) + 1) + ' Contract instances Successfully ✓'))
    print()

configure_contract()



    ############################
    #    4. Scan for Start     #
    ############################



#NOTE:
# This function is used to tell the script what to do once the 'Initialized' 
# event is found in the latest block. It notifies the user that the sale has started
# and then calls the mint function

# define function to handle events and print to the console
def handle_event(event):
    print(Web3.toJSON(event))
    # and whatever


# asynchronous defined function to loop
# this loop sets up an event filter and is looking for new entires for the "Initialized" event
# this loop runs on a poll interval
async def log_loop(event_filter, poll_interval):
    while True:
        for Initialized in event_filter.get_new_entries():
            handle_event(Initialized)
        await asyncio.sleep(poll_interval)


# when main is called
# create a filter for the latest block and look for the "Initialized" event for the uniswap factory contract
# run an async loop
# try to run the log_loop function above every 2 seconds
def main():
    event_filter = contract.events.Initialized.createFilter(fromBlock='latest')
    #block_filter = web3.eth.filter('latest')
    # tx_filter = web3.eth.filter('pending')
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 2)))
                # log_loop(block_filter, 2),
                # log_loop(tx_filter, 2)))
    finally:
        # close loop to free up system resources
        loop.close()

# NOTE:
# This function just asks the user if they want to start scanning for the start of the sale
# If the user enters "yes", then the script will continue and eventually mint using each Lazy Boy
# If the user enters "no", then the script will exit
# IMPORTANT: It is very easy to get rate limited if you start scanning too early
# I recommend waiting until the sale is about to begin to start scanning

def start_scan():
    print(Fore.WHITE + ('Would you like to start scanning for JoePegs? (Enter yes/no)'))
    continue_script = input()
    if continue_script == 'no':
        print('Goodbye!')
        exit()
    elif continue_script == 'yes':
        print()
        print(Fore.BLUE + ('Starting to scan for JoePegs...'))
        main()
    else:
        print('Please enter "yes" or "no"')
        start_scan()

start_scan()


    ######################
    #      5. Mint!      #
    ######################


# NOTE:
# Now that the sale has started, we can begin to mint using each Lazy Boy and signer
def mint():
    print(Fore.BLUE + ('Minting JoePegs...'))




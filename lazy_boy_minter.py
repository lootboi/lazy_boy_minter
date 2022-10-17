import os
import collections
import asyncio
import textwrap

from eth_account    import Account
from web3           import Web3
from dotenv         import load_dotenv
from joepeg_abi     import JOEPEG_ABI
from colorama       import Fore, Back, Style
from utils          import print_banner, dim_text
def dim(text):
     print(Fore.DIM + text)

load_dotenv()

    ########################
    #   Prompt Functions   #
    ########################

# NOTE:
# All of the following functions are simply to prompt te user for some type of input

# NOTE: 
# Function to prompt whether or not to start the script

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

# NOTE:


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
    Node(address=os.getenv("RPC_FOUR")),
    Node(address=os.getenv("RPC_FIVE")),
)

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

w3 = [Web3(Web3.HTTPProvider(node.address)) for node in Nodes]
accounts = [Account.from_key(lazy.private_key) for lazy in LazyBoyz]
signers = []

signer_count = 0

for i in range(len(w3)):
    for i in range(len(accounts)):
        signers.append(w3[i].eth.account.signTransaction)
        signer_count = signer_count + 1

print(Fore.BLUE + 'Configured ' + str(signer_count) + ' Signers Successfully ✓')
print()
print(Fore.YELLOW + ('Testing RPC Nodes...'))
print()


# NOTE:
# This serves as a test to see that all of signers are configured correctly
# We use each signer to call the current block of the network
# If isConnected() returns true, then we know that the signer is configured correctly

# NOTE:
# This function takes all of the nodes and tests to see if they are connected
# All of the nodes are then put into an ascii table along with their status
# If they are connected, then we know that the signer is configured correctly
# If they are not connected, then we know that the signer is not configured correctly

def test_nodes():
    connected = 0
    disconnected = 0
    print(Fore.YELLOW + ' ________________________________________________________')
    print(Fore.YELLOW + '|========================================================|')
    print(Fore.YELLOW + '|======================== ' + Fore.BLUE + 'Nodes' + Fore.YELLOW + ' =========================|')
    print(Fore.YELLOW + '|========================================================|')
    print(Fore.YELLOW + '|' + Fore.BLUE + '        Node Address' + Fore.YELLOW + '        |' + Fore.BLUE + '           Status' + Fore.YELLOW + '          |')
    print(Fore.YELLOW + '|========================================================|')
    for i in range(len(Nodes)):
        if(w3[i].isConnected()):
            connected = connected + 1
            print(Fore.YELLOW + '| ' + Style.RESET_ALL + '         Node #' + str(i + 1) + Fore.YELLOW + '           |' + Fore.GREEN + '         Connected' + Fore.YELLOW + '         |')
            print(Fore.YELLOW + '|========================================================|')
        if(w3[i].isConnected() == False):
            disconnected = disconnected + 1
            print(Fore.YELLOW + '| ' + Style.RESET_ALL + '         Node #' + str(i + 1) + Fore.YELLOW + '           |' + Fore.RED + '        Not Connected' + Fore.YELLOW + '      |')
            print(Fore.YELLOW + '|========================================================|')
    print(Fore.YELLOW + '|' + Fore.BLUE + ' Nodes Connected: ' + Fore.YELLOW + str(connected) + '                                     |')
    print(Fore.YELLOW + '|--------------------------------------------------------|')
    print(Fore.YELLOW + '|' + Fore.BLUE + ' Nodes Disconnected: ' + Fore.YELLOW + str(disconnected) + '                                  |')
    print(Fore.YELLOW + '|========================================================|')
    print()
    if disconnected > 0:
        print(Fore.RED + ('Please check your RPC Nodes and try again'))
        exit()
test_nodes()

print(Fore.BLUE + ('Testing RPC Nodes Successful ✓'))
print()
print(Fore.YELLOW + ('Checking Lazy Boy wallet balances...'))
print()

# NOTE:
# This function checks the balance of each Lazy Boy wallet and prints the results in an ASCII table
# If the balance is 0, then the user is prompted to add funds to the wallet then check again or continue
# (This is to prevent the user from accidentally minting with an empty wallet and useful for testing the script)

def print_wallet_balances():
    funded = 0
    unfunded = 0
    print(Fore.YELLOW + ' ______________________________________________________________')
    print('|==============================================================|')
    print('|====================== ' + Style.RESET_ALL + Fore.BLUE + 'Wallet Balances' + Style.RESET_ALL + Fore.YELLOW + ' =======================|')
    print('|==============================================================|')
    print('|               ' + Style.RESET_ALL + Fore.BLUE + 'Wallet Address' + Style.RESET_ALL + Fore.YELLOW + '               | ' + Style.RESET_ALL + Fore.BLUE + '    Balance' + Style.RESET_ALL + Fore.YELLOW + '     |')
    print('|==============================================================|')
    for i in range(len(accounts)):
        if w3[i].eth.get_balance(accounts[i].address) == 0:
            unfunded = unfunded + 1
            print('| ' + Style.RESET_ALL + Fore.WHITE + str(accounts[i].address) + Style.RESET_ALL + Fore.YELLOW + ' |     ' + Style.RESET_ALL + Fore.RED + str(w3[i].fromWei(w3[i].eth.get_balance(accounts[i].address), 'ether')) + ' AVAX' + Style.RESET_ALL + Fore.YELLOW + '      |')
            print('|==============================================================|')
        else:
            funded = funded + 1
            print('| ' + Style.RESET_ALL + Fore.WHITE + str(accounts[i].address) + Style.RESET_ALL + Fore.YELLOW + ' |     ' + Style.RESET_ALL + Fore.GREEN + str(w3[i].fromWei(w3[i].eth.get_balance(accounts[i].address), 'ether')) + ' AVAX' + Style.RESET_ALL + Fore.YELLOW + '      |')
            print('|==============================================================|')
    print(Fore.YELLOW + '| ' + Fore.BLUE + 'Funded Wallets: ' + Fore.YELLOW + str(funded) + '                                            |')
    print(Fore.YELLOW + '|--------------------------------------------------------------|')
    print(Fore.YELLOW + '| ' + Fore.BLUE + 'Unfunded Wallets: ' + Fore.YELLOW + (str(unfunded)) + '                                          |')
    print(Fore.YELLOW + '|==============================================================|')
    if unfunded > 0:
        print(Fore.RED + ('You have unfunded wallets!'))
        print(Fore.RED + ('Please add funds to your wallets or remove the unfunded wallets from the LazyBoyz list'))
        exit()
    if unfunded == 0:
        print()
        print(Fore.BLUE + ('All wallets are funded ✓'))  
             
print_wallet_balances()

print()
print(Fore.YELLOW + ('Starting to configure JoePeg Contract...'))
print()


    ############################
    #   3. Connect to Contract #
    ############################


# NOTE:
# This for function creates a unique contract object using all of the w3 instances
# This is done so that we can call the contract functions using each different Node + Signer

contract = []
def configure_contract():
    print(Fore.YELLOW + ' ________________________________________________')
    print(Fore.YELLOW + '|================================================|')
    print(Fore.YELLOW + '|================== ' + Fore.BLUE + 'Contracts' + Fore.YELLOW + ' ===================|')
    print(Fore.YELLOW + '|================================================|')
    print(Fore.YELLOW + '|   ' + Fore.BLUE + mint_address + Fore.YELLOW + '   |')
    print(Fore.YELLOW + '|================================================|')
    for i in range(len(w3)):
        contract.append(w3[i].eth.contract(address=mint_address, abi=JOEPEG_ABI))
        print(Fore.YELLOW + '|' + Fore.WHITE + ' Contract #' + str(i + 1) + Fore.YELLOW + ' | ' + Fore.GREEN + '           Configured ✓' + Fore.YELLOW + '          |')
        print(Fore.YELLOW + '|================================================|')

configure_contract()

print()
print(Fore.BLUE + ('JoePeg Contract Configured ✓'))
print()


    ############################
    #    4. Scan for Start     #
    ############################

#NOTE:
# This function is used to tell the script what to do once the 'Initialized' 
# event is found in the latest block. It notifies the user that the sale has started
# and then calls the mint function

def handle_event():
    print(Fore.BLUE + ('JoePeg Sale Started ✓'))
    # mint()

# NOTE:
# This function is used to scan for the 'Initialized' event in the latest block
# If the event is found, then the handle_event() function is called

async def log_loop(event_filter, poll_interval):
    while True:
        for Initialized in event_filter.get_new_entries():
            handle_event(Initialized)
        await asyncio.sleep(poll_interval)

# NOTE:
# This function is used to create a filter for the 'Initialized' event
# It then calls the log_loop() function to scan for the event

def scan():
    for i in range(len(contract)):
        event_filter = contract[i].events.Initialized.createFilter(fromBlock='latest')
        loop = asyncio.get_event_loop()
        try:
            loop.run_until_complete(
                asyncio.gather(
                    log_loop(event_filter, 0.1)))
        finally:
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
        scan()
    else:
        print('Please enter "yes" or "no"')
        start_scan()

start_scan()

print(Fore.YELLOW + ('Starting to scan for JoePegs...'))
print()

# NOTE:
# These next 3 functions are used to actually scan for the start of the sale


    ######################
    #      5. Mint!      #
    ######################


# NOTE:
# Now that the sale has started, we can begin to mint using each Lazy Boy and signer
def mint():
    print(Fore.BLUE + ('Minting JoePegs...'))



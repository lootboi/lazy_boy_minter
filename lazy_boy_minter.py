import click
import os
import collections
import multiprocessing
import time

from eth_account    import Account
from web3           import Web3
from dotenv         import load_dotenv
from joepeg_abi     import JOEPEG_ABI
from colorama       import Fore, Back, Style
from utils          import print_banner

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
    LazyBoy(private_key=os.getenv("LAZY_WALLET_ONE")),
    LazyBoy(private_key=os.getenv("LAZY_WALLET_TWO")),
    LazyBoy(private_key=os.getenv("LAZY_WALLET_THREE")),
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

print(Fore.BLUE + ('Configured Signers Successfully ✓'))
print(Fore.BLUE + ('Testing RPC Nodes...'))
print()


# NOTE:
# This serves as a test to see that all of signers are configured correctly
# We use each signer to call the current block of the network
# If isConnected() returns true, then we know that the signer is configured correctly
def test_nodes():
    for i in range(len(w3)):
        block = w3[i].eth.get_block_number
        print(Fore.YELLOW + ('Testing Node: #' + str(i + 1)))
        if(w3[i].isConnected()):
            print(Fore.GREEN + ('Node #' + str(i + 1) + ' is connected ✓'))
        if(w3[i].isConnected() == False):
            print(Fore.RED + ('Node #' + str(i + 1) + ' is not connected'))
            print(Fore.RED + ('Please check your RPC Node settings'))
            exit()
        print()

test_nodes()

print(Fore.BLUE + ('Testing RPC Nodes Successful ✓'))
print(Fore.BLUE + ('Checking Lazy Boy wallet balances...'))
print()

# NOTE:
# This function checks the balance of each Lazy Boy wallet and prints the results
# If the balance is 0, then the user is prompted to add funds to the wallet

def check_balances():
    unfunded = 0
    funded = 0
    for i in range(len(accounts)):
        balance = w3[i].eth.get_balance(accounts[i].address)
        print(Fore.YELLOW + ('Checking balance of Lazy Boy #' + str(i + 1) + ': '))
        if(balance == 0):
            print(Fore.RED + ('Wallet is empty'))
            unfunded = unfunded + 1
        if(balance > 0):
            funded = funded + 1
        if(balance == 0):
            unfunded = unfunded + 1
            print(Fore.RED + ('Lazy Boy #' + str(i + 1) + ' has a balance of 0'))
            print(Fore.RED + ('Please add funds to use this wallet'))
        if(balance != 0):
            funded = funded + 1
            print(Fore.GREEN + ('Lazy Boy #' + str(i + 1) + ' has a balance of ' + str(w3[i].fromWei(balance, 'ether')) + ' AVAX'))
            print()
    print(Fore.BLUE + ('Lazy Boy wallet balances checked ✓'))
    if(unfunded > 0):
        print(Fore.RED + (str(unfunded) + ' of your Lazy Boyz are unfunded, would you like to continue? (Enter yes/no)'))
        continue_script = input()
        if continue_script == 'no':
            print(Fore.DIM + ('Goodbye!'))
            exit()
        elif continue_script == 'yes':
            print()
        else:
            print(Fore.DIM + ('Please enter "yes" or "no"'))
            check_balances()
    if(unfunded == 0):
        print(Fore.BLUE + ('All of your Lazy Boyz are funded!'))

check_balances()

print()
print(Fore.YELLOW + ('Starting to configure JoePeg Contract...'))
print()
print(Fore.BLUE + ('JoePeg Contract Address: ' + mint_address))


    ############################
    #   3. Connect to Contract #
    ############################


# NOTE:
# This for function creates a unique contract object using all of the w3 instances
# This is done so that we can call the contract functions using each different Node + Signer

contract = []
def configure_contract():
    for i in range(len(w3)):
        contract.append(w3[i].eth.contract(address=mint_address, abi=JOEPEG_ABI))
        print(Fore.YELLOW + ('Contract with Node #' + str(i + 1) + ' configured ✓'))

configure_contract()

print()
print(Fore.BLUE + ('JoePeg Contract Configured ✓'))
print()


    ############################
    #    4. Scan for Start     #
    ############################

# NOTE:
# This function just asks the user if they want to start scanning for the start of the sale
# If the user enters "yes", then the script will continue and eventually mint using each Lazy Boy
# If the user enters "no", then the script will exit
# IMPORTANT: It is very easy to get rate limited if you start scanning too early
# I recommend waiting until the sale is about to start to start scanning

def start_scan():
    print(Fore.WHITE + ('Would you like to start scanning for JoePegs? (Enter yes/no)'))
    continue_script = input()
    if continue_script == 'no':
        print('Goodbye!')
        exit()
    elif continue_script == 'yes':
        print()
    else:
        print('Please enter "yes" or "no"')
        start_scan()

start_scan()

print(Fore.YELLOW + ('Starting to scan for JoePegs...'))
print()

# NOTE: THIS IS AI GENERATED CODE (MUST EDIT)
# This is how the script will scan for the start of the sale
# The script will continue to scan until until the sale has started
# Once the sale has started, the script will stop scanning and beginn to propogate transactions

def scan():
    while True:
        try:
            sale_status = contract[0].functions.saleIsActive().call()
            if(sale_status == True):
                print(Fore.GREEN + ('JoePeg Sale has started!'))
                print()
            if(sale_status == False):
                print(Fore.RED + ('JoePeg Sale has not started yet'))
                print()
                time.sleep(1)
        except:
            print(Fore.RED + ('JoePeg Sale has not started yet'))
            print()
            time.sleep(1)

scan()


    ######################
    #      5. Mint!      #
    ######################


# NOTE:
# Now that the sale has started, we can begin to mint using each Lazy Boy and signer




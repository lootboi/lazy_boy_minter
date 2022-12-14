import os
import collections
import asyncio
import concurrent.futures

from eth_account     import Account
from flatlaunchpeg   import FLATLAUNCHPEG_ABI
from colorama        import Fore, Style
from dotenv          import load_dotenv
from utils           import print_banner
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
    Node(address=os.getenv("RPC_FOUR")),
    Node(address=os.getenv("RPC_FIVE")),
    # Node(address=os.getenv("RPC_SIX")),
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

# NOTE:
# This serves as a test to see that all of signers are configured correctly
# If isConnected() returns true, then we know that the signer is configured correctly

# FUNCTION WITHOUT ASCII TABLE:
# This is a lot easier to read than the actual function used-But it doesn't look as cool
# If you are trying to use this script as a guide, the following function is a lot easier to read
# 
# def test_nodes():
#     connected = 0
#     disconnected = 0
#     for i in range(len(Nodes)):
#         if w3[i].isConnected():
#             connected = connected + 1
#         else:
#             disconnected = disconnected + 1
#     if disconnected > 0:
#         print(Fore.RED + 'Disconnected Nodes: ' + str(disconnected))
#     if connected == len(Nodes):
#         print(Fore.GREEN + 'All Nodes Connected ???')

def test_nodes():
    connected = 0
    disconnected = 0
    print(Fore.YELLOW + ' ________________________________________________________')
    print(Fore.YELLOW + '|========================================================|')
    print(Fore.YELLOW + '|======================== ' + Fore.BLUE + 'Nodes' + Fore.YELLOW + ' =========================|')
    print(Fore.YELLOW + '|========================================================|')
    print(Fore.YELLOW + '|' + Fore.BLUE + '        Node Address' + Fore.YELLOW + '        |' + Fore.BLUE + '           Status' + Fore.YELLOW + '          |')
    print(Fore.YELLOW + '|========================================================|')
    for i in range(len(w3)):
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
    if connected == len(Nodes):
        print(Fore.GREEN + 'All Nodes Connected ???')
        print()
        print(Fore.BLUE + ('Tested RPC Nodes Successfully ???'))
        print()
        print(Fore.YELLOW + ('Checking Lazy Boy wallet balances...'))
        print()


test_nodes()

# NOTE:
# This function checks the balance of each Lazy Boy wallet and prints the results in an ASCII table
# If the balance is 0, then the user is prompted to add funds to the wallet then check again or continue
# (This is to prevent the user from accidentally minting with an empty wallet and useful for testing the script)

# FUNCTION WITHOUT ASCII TABLE:
# This is a lot easier to read than the actual function used-But it doesn't look as cool
# If you are trying to use this script as a guide, the following function is a lot easier to read

# def print_wallet_balances():
#     funded = 0
#     unfunded = 0
#     for i in range(len(accounts)):
#         if w3[i].eth.getBalance(accounts[i].address) > 0:
#             funded = funded + 1
#         else:
#             unfunded = unfunded + 1
#     if unfunded > 0:
#         print(Fore.RED + 'Unfunded Wallets: ' + str(unfunded))
#         print(Fore.RED + ('Please add funds to your wallets or remove the unfunded wallets from the LazyBoyz list'))
#         exit()
#     if funded == len(accounts):
#         print(Fore.GREEN + 'All Wallets Funded ???')
#         print()
#         print(Fore.YELLOW + ('Starting to configure JoePeg Contract...'))

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
            print('| ' + Style.RESET_ALL + Fore.WHITE + str(accounts[i].address) + Style.RESET_ALL + Fore.YELLOW + ' |     ' + Style.RESET_ALL + Fore.RED + str(w3[i].fromWei(w3[i].eth.get_balance(accounts[i].address), 'ether')) + ' AVAX' + Style.RESET_ALL + Fore.YELLOW + '    |')
            print('|==============================================================|')
        else:
            funded = funded + 1
            print('| ' + Style.RESET_ALL + Fore.WHITE + str(accounts[i].address) + Style.RESET_ALL + Fore.YELLOW + ' |     ' + Style.RESET_ALL + Fore.GREEN + str(w3[i].fromWei(w3[i].eth.get_balance(accounts[i].address), 'ether')) + ' AVAX' + Style.RESET_ALL + Fore.YELLOW + '    |')
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
        print(Fore.GREEN + ('All wallets are funded ???'))  
        print()
        print(Fore.BLUE + 'Checked Balances Successfully ???')
        print()
        print(Fore.YELLOW + ('Starting to configure JoePeg Contract...'))
             
print_wallet_balances()


    ############################
    #  3. Connect to Contract  #
    ############################


# NOTE:
# This for function creates a unique contract object using all of the w3 instances
# This is done so that we can call the contract functions using each different Node + Signer

contracts = []
def configure_contract():
    for i in range(len(w3)):
        contracts.append(w3[i].eth.contract(address=mint_address, abi=FLATLAUNCHPEG_ABI))
    print()
    print(Fore.GREEN + ('JoePeg Contract Configured ???'))
    print()
    print(Fore.BLUE + ('Created ' + str(len(w3) + 1) + ' Contract instances Successfully ???'))
    print()

configure_contract()

    ######################
    #      5. Mint!      #
    ######################

# NOTE:
# This function uses two for loops to iterate through the Lazy boys list and the contract objects
# The function then calls the allowlistMint function for each contract object

def mint():
    gas_limit = 300_000
    max_gas_in_gwei = 300
    gas_tip_in_gwei = 50
    mint_amount = 1
    for i in range(len(contracts)):
        for j in range(len(accounts)):
            print('Attempting to mint with ' + str(accounts[j].address))
            contract_function = contracts[i].functions.allowlistMint(mint_amount)
            tx = contract_function.buildTransaction({
                'from': accounts[j].address,
                'type': 0x2,
                'chainId': w3[0].eth.chain_id,
                'gas': gas_limit,
                'maxFeePerGas': Web3.toWei(max_gas_in_gwei, 'gwei'),
                'maxPriorityFeePerGas': Web3.toWei(gas_tip_in_gwei, 'gwei'),
                'nonce': w3[i].eth.get_transaction_count(accounts[j].address),
                'value': 0
            })
            signed_tx = w3[i].eth.account.sign_transaction(tx, private_key=LazyBoyz[j].private_key)
            try:
                tx_hash = w3[i].eth.send_raw_transaction(signed_tx.rawTransaction)
                print(Fore.YELLOW + 'Transaction Hash: ' + str(tx_hash.hex()) + ' | ' + 'Node: ' + str(i) + ' | ' + 'Account: ' + str(j))
            except:
                print(Fore.RED + 'Transaction Failed')




    ############################
    #    4. Scan for Start     #
    ############################



#NOTE:
# These next few functions scan for the Initialized() event in the JoePeg Contract
# Once this event is found, we know to begin minting with our wallets

def handle_event(event):
    print(event)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        executor.map(mint(), contracts)

#NOTE:
# The listener function itself

async def log_loop(event_filter, poll_interval):
    while True:
        print("Polling...")
        for Initialized in event_filter.get_all_entries():
            handle_event(Initialized)
        # We also check the currentPhase in case the listener somehow gets derailed and misses the event
        phase = contracts[0].functions.currentPhase().call()
        if phase > 0:
            print(Fore.GREEN + 'Sale has started! Minting...')
            with concurrent.futures.ProcessPoolExecutor() as executor:
                executor.map(mint())
        await asyncio.sleep(poll_interval, contracts)

def listen_loop():
    event_filter = contracts[0].events.Initialized.createFilter(fromBlock='latest')
    loop = asyncio.get_event_loop()
    asyncio.set_event_loop(loop)
    try:
        print('Starting event loop')
        loop.run_until_complete(
            asyncio.gather(
                log_loop(event_filter, 0.5)))
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
        print(Fore.BLUE + ('Starting to scan:'))
        listen_loop()
    else:
        print('Please enter "yes" or "no"')
        start_scan()

start_scan()







from eth_account    import Account
from web3           import Web3
from dotenv         import load_dotenv
from joepeg_abi     import JOEPEG_ABI
import os

# NOTE: In order to perform any utility, we need to grab the .env file for use in the script
# Make sure that you have used the ENV_EXAMPLE file to create your own .env file
load_dotenv()

    ########################
    #   1. Initial Setup   #
    ########################

# NOTE: All of the following are wallets that have been created for minting purposes.
# These wallets are pre-generated and must be funded with AVAX to mint successfully.
# We need to create an instance of our wallets to use them in the script:
lazy_boy_one = w3.eth.account.privateKeyToAccount(os.getenv("LAZY_WALLET_ONE"))
lazy_boy_two = w3.eth.account.privateKeyToAccount(os.getenv("LAZY_WALLET_TWO"))
lazy_boy_three = w3.eth.account.privateKeyToAccount(os.getenv("LAZY_WALLET_THREE"))
# NOTE: w3 is not defined until the propagate_minting function is called-Must fix this

# Then, we need to create a list of our wallets to use in the script:
minters = [lazy_boy_one, lazy_boy_two, lazy_boy_three]

# We also need to create a list of all the RPC nodes that we want to propagate our transactions to:
rpcs = [os.getenv("RPC_ONE"), os.getenv("RPC_TWO"), os.getenv("RPC_THREE"), os.getenv("RPC_FOUR"), os.getenv("RPC_FIVE")]

    ########################
    # 2. Propagate Minting #
    ########################

# NOTE: We need to create a function that propogates each minters transactions to all of the RPC nodes
#This function will take in a list of RPC nodes and a list of minters, and will propagate each minters transactions to all of the RPC nodes
def propagate_minting(rpcs, minters):
    # We need to create a for loop that will iterate through each of the RPC nodes:
    for rpc in rpcs:
        # We need to create a for loop that will iterate through each of the minters:
        for minter in minters:
            # We need to create a variable that will hold the RPC node that we are currently iterating through:
            w3 = Web3(Web3.HTTPProvider(rpc))
            # We need to create a variable that will hold the minter that we are currently iterating through:
            minter = minter
            # We need to create a variable that will hold the nonce of the minter that we are currently iterating through:
            nonce = w3.eth.getTransactionCount(minter.address)
            # NOTE: We need to 
            # We need to create a variable that will hold the transaction that we are currently iterating through:
            tx = {
                'nonce': nonce,
                'to': os.getenv("CONTRACT_ADDRESS"),
                'value': 0,
                'gas': 2000000,
                'gasPrice': w3.toWei('20', 'gwei'),
                'data': os.getenv("CONTRACT_ABI").encode('utf-8')
            }
            # We need to create a variable that will hold the signed transaction that we are currently iterating through:
            signed_tx = minter.signTransaction(tx)
            # We need to create a variable that will hold the transaction hash that we are currently iterating through:
            tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            # We need to create a variable that will hold the transaction receipt that we are currently iterating through:
            tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            # We need to print the transaction receipt for each transaction that is propagated:
            print(tx_receipt)



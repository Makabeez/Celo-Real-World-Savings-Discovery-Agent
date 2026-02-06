import os
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RPC_URL = os.getenv("CELO_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Initialize Web3 with Sepolia RPC
w3 = Web3(Web3.HTTPProvider(RPC_URL))

def check_connection():
    try:
        if w3.is_connected():
            account = w3.eth.account.from_key(PRIVATE_KEY)
            balance_wei = w3.eth.get_balance(account.address)
            balance_eth = w3.from_wei(balance_wei, 'ether')
            chain_id = w3.eth.chain_id

            print(f"--- Connection Status ---")
            print(f"Network: Celo Sepolia")
            print(f"Chain ID: {chain_id}")
            print(f"Agent Address: {account.address}")
            print(f"Balance: {balance_eth} CELO")
            return True
        else:
            print("Error: Connection failed. Check RPC URL in .env")
            return False
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    check_connection()

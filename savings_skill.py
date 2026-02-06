import os
import json
import time
from web3 import Web3
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RPC_URL = os.getenv("CELO_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

# Mock Vault Address
SAVINGS_VAULT_ADDRESS = "0x000000000000000000000000000000000000dEaD"

class SavingsAgent:
    def __init__(self, threshold_eth=1.0):
        self.threshold = w3.to_wei(threshold_eth, 'ether')
        self.chain_id = 11142220

    def check_and_save(self):
        print(f"--- Checking Agent Balance for Automation ---")
        balance = w3.eth.get_balance(account.address)
        print(f"Current Balance: {w3.from_wei(balance, 'ether')} CELO")

        if balance > self.threshold:
            # Calculate amount to save (keep threshold, move the rest)
            savings_amount = balance - self.threshold
            print(f"Threshold exceeded. Moving {w3.from_wei(savings_amount, 'ether')} CELO to Savings Vault...")
            
            # Get latest gas price and nonce
            gas_price = w3.eth.gas_price
            nonce = w3.eth.get_transaction_count(account.address)
            
            tx = {
                'nonce': nonce,
                'to': SAVINGS_VAULT_ADDRESS,
                'value': savings_amount,
                'gas': 21000,
                'gasPrice': gas_price,
                'chainId': self.chain_id
            }
            
            signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
            
            # Fixed attribute: raw_transaction instead of rawTransaction
            tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
            
            print(f"✅ Automation Success! Hash: {w3.to_hex(tx_hash)}")
            return w3.to_hex(tx_hash)
        else:
            print("Balance below threshold. No action taken.")
            return None

if __name__ == "__main__":
    agent = SavingsAgent(threshold_eth=1.0)
    agent.check_and_save()

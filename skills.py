import os
import json
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

RPC_URL = os.getenv("CELO_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

class CeloAgentSkills:
    def __init__(self):
        self.agent_id = account.address
        self.reputation_standard = "ERC-8004"
        
    def get_agent_profile(self):
        """Returns the agent profile for ERC-8004 registration"""
        profile = {
            "address": self.agent_id,
            "name": "RealWorld_Celo_Agent",
            "capabilities": ["remittances", "yield_optimization", "savings"],
            "status": "active"
        }
        return profile

    def send_remittance(self, recipient_address, amount_celo):
        """Simulates a real-world remittance skill"""
        print(f"--- Executing Remittance Skill ---")
        nonce = w3.eth.get_transaction_count(account.address)
        
        tx = {
            'nonce': nonce,
            'to': recipient_address,
            'value': w3.to_wei(amount_celo, 'ether'),
            'gas': 21000,
            'gasPrice': w3.eth.gas_price,
            'chainId': 11142220
        }
        
        signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        print(f"Remittance sent! Hash: {w3.to_hex(tx_hash)}")
        return w3.to_hex(tx_hash)

if __name__ == "__main__":
    skills = CeloAgentSkills()
    profile = skills.get_agent_profile()
    print(f"Agent Profile Loaded: {json.dumps(profile, indent=2)}")

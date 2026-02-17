import os
import time
import json
from web3 import Web3
from eth_account.messages import encode_defunct
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RPC_URL = os.getenv("CELO_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
# We use the key to create the account object for signing
account = w3.eth.account.from_key(PRIVATE_KEY)

def register_reputation():
    print(f"--- ERC-8004 Reputation Registration ---")
    
    # In ERC-8004, an agent must sign its identity
    timestamp = int(time.time())
    message_text = f"ERC-8004 Agent Registration | Address: {account.address} | Time: {timestamp}"
    
    # Correct way to encode and sign a message in web3.py
    message_encoded = encode_defunct(text=message_text)
    signed_message = w3.eth.account.sign_message(message_encoded, private_key=PRIVATE_KEY)
    
    print(f"Agent Signature: {signed_message.signature.hex()}")
    print(f"Status: Ready for SelfProtocol verification")
    
    # Saving attestation for submission
    attestation_data = {
        "agent": account.address,
        "signature": signed_message.signature.hex(),
        "timestamp": timestamp,
        "standard": "ERC-8004",
        "message": message_text
    }
    
    with open("agent_attestation.json", "w") as f:
        json.dump(attestation_data, f, indent=4)
        
    print("✅ Attestation saved to agent_attestation.json")

if __name__ == "__main__":
    register_reputation()

import os
import json
import time
from web3 import Web3
from eth_account.messages import encode_defunct
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

RPC_URL = os.getenv("CELO_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

def generate_reputation_report():
    print(f"--- Generating ERC-8004 Reputation Score ---")
    
    # Get agent activity (transaction count)
    tx_count = w3.eth.get_transaction_count(account.address)
    balance = w3.eth.get_balance(account.address)
    
    # Reputation Logic: More transactions = Higher Score
    # For the hackathon, we link the "Savings" skill to the score
    reputation_score = min(100, tx_count * 10) 
    
    report_data = {
        "agent_address": account.address,
        "network": "Celo Sepolia",
        "tx_count": tx_count,
        "reputation_score": f"{reputation_score}/100",
        "timestamp": int(time.time()),
        "standard": "ERC-8004",
        "verified_skills": ["Savings Automation", "Transaction Signing"]
    }
    
    # Sign the reputation report
    message_text = json.dumps(report_data, sort_keys=True)
    message_encoded = encode_defunct(text=message_text)
    signed_report = w3.eth.account.sign_message(message_encoded, private_key=PRIVATE_KEY)
    
    final_payload = {
        "report": report_data,
        "signature": signed_report.signature.hex()
    }
    
    with open("final_reputation_score.json", "w") as f:
        json.dump(final_payload, f, indent=4)
        
    print(f"✅ Reputation Score Generated: {reputation_score}/100")
    print(f"✅ Proof saved to final_reputation_score.json")

if __name__ == "__main__":
    generate_reputation_report()

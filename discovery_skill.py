import os
import json
from eth_account.messages import encode_defunct
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

RPC_URL = os.getenv("CELO_RPC_URL")
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
w3 = Web3(Web3.HTTPProvider(RPC_URL))
account = w3.eth.account.from_key(PRIVATE_KEY)

class AgentDiscovery:
    def __init__(self):
        self.registry_info = {
            "agent_address": account.address,
            "discovery_protocol": "A2A",
            "supported_standards": ["ERC-8004", "AP2"]
        }

    def announce_presence(self):
        """Announces agent capabilities to the network"""
        print(f"--- Agent Discovery Announcement ---")
        
        # Metadata to be discovered by other agents
        announcement = {
            "address": account.address,
            "skills": ["savings", "remittances"],
            "endpoint": "https://github.com/your-repo-link", # Update this later
            "version": "1.0.0"
        }
        
        message_text = json.dumps(announcement, sort_keys=True)
        message_encoded = encode_defunct(text=message_text)
        signature = w3.eth.account.sign_message(message_encoded, private_key=PRIVATE_KEY)
        
        discovery_packet = {
            "data": announcement,
            "signature": signature.signature.hex()
        }
        
        with open("discovery_announcement.json", "w") as f:
            json.dump(discovery_packet, f, indent=4)
            
        print(f"✅ Discovery packet generated for {account.address}")
        print(f"✅ Packet saved to discovery_announcement.json")
        return discovery_packet

if __name__ == "__main__":
    discovery = AgentDiscovery()
    discovery.announce_presence()

import time
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# --- CONFIGURATION ---
CELO_RPC = "https://forno.celo.org"
PRIVATE_KEY=0x22515f02bce13d8f736c5afdd8b5a9664023ec78fd05b237856d9bb68f53af06 
TARGET_TX_COUNT = 10500 # Pushing past the 10k finish line for Citizenship

# Connect to Celo Mainnet
w3 = Web3(Web3.HTTPProvider(CELO_RPC))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0) 

if not w3.is_connected():
    print("❌ Failed to connect to Celo Mainnet")
    exit()

print("✅ Connected to Celo Mainnet")

account = w3.eth.account.from_key(PRIVATE_KEY)
wallet_address = account.address
print(f"🤖 Agent Identity: {wallet_address}")

def execute_micro_tx(nonce_val):
    tx = {
        'nonce': nonce_val,
        'to': wallet_address,
        'value': w3.to_wei(0.0001, 'ether'),
        'gas': 100000,
        'gasPrice': w3.eth.gas_price,
        'chainId': 42220
    }
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return w3.to_hex(tx_hash)

def farm_visa_transactions():
    print(f"🚀 Starting Citizenship Farming: Targeting {TARGET_TX_COUNT} TXs")
    current_nonce = w3.eth.get_transaction_count(wallet_address)
    
    while current_nonce < TARGET_TX_COUNT:
        try:
            print(f"⏳ Executing Tx {current_nonce + 1}/{TARGET_TX_COUNT}...")
            tx_hash = execute_micro_tx(current_nonce)
            print(f"✅ Tx Submitted! Hash: {tx_hash}")
            
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
            
            if receipt.status == 1:
                print(f"🎉 Tx {current_nonce + 1} Confirmed on Mainnet!")
                current_nonce += 1
            else:
                print("⚠️ Transaction failed on-chain. Retrying...")
            
            # Shorter sleep time since we are grinding the final stretch
            time.sleep(3) 
            
        except Exception as e:
            print(f"❌ Error during transaction: {e}")
            time.sleep(10)
            current_nonce = w3.eth.get_transaction_count(wallet_address)

if __name__ == "__main__":
    farm_visa_transactions()
    print("🏆 Celo Citizenship Goal Reached!")

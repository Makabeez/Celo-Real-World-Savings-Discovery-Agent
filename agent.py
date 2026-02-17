import os
import time
import logging
from web3 import Web3
from dotenv import load_dotenv
from decimal import Decimal

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
load_dotenv()

# --- CONFIGURATION ---
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
CELO_RPC = "https://forno.celo.org"
CHAIN_ID = 42220
THRESHOLD_CELO = Decimal("1.0")
CHECK_INTERVAL = 60

# Official Celo Mainnet Addresses
WCELO_ADDRESS = "0x471EcE3750Da237f93B8E339c536989b8978a438"
USDC_ADDRESS = "0xcebA9300f2b948710d2653dD7B07f33A8B32118C"
UBESWAP_ROUTER = "0xE3D8bd6Aed4F159bc8000a9cD47CffDb95F96121" 

w3 = Web3(Web3.HTTPProvider(CELO_RPC))
account = w3.eth.account.from_key(PRIVATE_KEY)
MY_ADDRESS = account.address

# ABIs
WCELO_ABI = [
    {"constant":False,"inputs":[],"name":"deposit","outputs":[],"payable":True,"stateMutability":"payable","type":"function"},
    {"constant":False,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":False,"stateMutability":"nonpayable","type":"function"}
]
ROUTER_ABI = [{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"address[]","name":"path","type":"address[]"},{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"deadline","type":"uint256"}],"name":"swapExactTokensForTokens","outputs":[{"internalType":"uint256[]","name":"amounts","type":"uint256[]"}],"stateMutability":"nonpayable","type":"function"}]

wcelo_contract = w3.eth.contract(address=WCELO_ADDRESS, abi=WCELO_ABI)
router_contract = w3.eth.contract(address=UBESWAP_ROUTER, abi=ROUTER_ABI)

def wrap_and_swap(amount_celo):
    try:
        amount_wei = w3.to_wei(amount_celo, 'ether')
        # Use 'pending' nonce to avoid 'already known' errors
        current_nonce = w3.eth.get_transaction_count(MY_ADDRESS, 'pending')

        # 1. WRAP NATIVE CELO
        logging.info(f"🎁 Step 1/3: Wrapping {amount_celo:.4f} CELO into WCELO...")
        tx1 = wcelo_contract.functions.deposit().build_transaction({
            'from': MY_ADDRESS, 'value': amount_wei, 'gas': 150000,
            'gasPrice': w3.eth.gas_price, 'nonce': current_nonce, 'chainId': CHAIN_ID
        })
        w3.eth.send_raw_transaction(w3.eth.account.sign_transaction(tx1, PRIVATE_KEY).raw_transaction)
        time.sleep(15) # Wait for blockchain confirmation

        # 2. APPROVE ROUTER
        logging.info("🔓 Step 2/3: Approving Ubeswap Router...")
        tx2 = wcelo_contract.functions.approve(UBESWAP_ROUTER, amount_wei).build_transaction({
            'from': MY_ADDRESS, 'gas': 100000, 'gasPrice': w3.eth.gas_price,
            'nonce': current_nonce + 1, 'chainId': CHAIN_ID
        })
        w3.eth.send_raw_transaction(w3.eth.account.sign_transaction(tx2, PRIVATE_KEY).raw_transaction)
        time.sleep(15)

        # 3. SWAP WCELO FOR USDC
        logging.info("🔄 Step 3/3: Swapping WCELO for USDC...")
        tx3 = router_contract.functions.swapExactTokensForTokens(
            amount_wei, 0, [WCELO_ADDRESS, USDC_ADDRESS], MY_ADDRESS, int(time.time()) + 600
        ).build_transaction({
            'from': MY_ADDRESS, 'gas': 350000, 'gasPrice': w3.eth.gas_price,
            'nonce': current_nonce + 2, 'chainId': CHAIN_ID
        })
        final_hash = w3.eth.send_raw_transaction(w3.eth.account.sign_transaction(tx3, PRIVATE_KEY).raw_transaction)
        logging.info(f"🚀 MISSION SUCCESS! Transaction Hash: {w3.to_hex(final_hash)}")
        
    except Exception as e:
        logging.error(f"❌ Transaction sequence failed: {e}")

# Main execution loop
logging.info(f"✅ Agent Operational on Mainnet: {MY_ADDRESS}")
while True:
    try:
        balance = Decimal(w3.from_wei(w3.eth.get_balance(MY_ADDRESS), "ether"))
        logging.info(f"💰 Monitoring Balance: {balance:.4f} CELO")
        
        if balance > THRESHOLD_CELO:
            amount_to_process = balance - THRESHOLD_CELO
            wrap_and_swap(amount_to_process)
            logging.info("Cycle complete. Stopping agent to prevent double-swaps.")
            break # Exit loop after success for clean submission data
            
        time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        break
    except Exception as e:
        logging.error(f"Unexpected Loop Error: {e}")
        time.sleep(10)

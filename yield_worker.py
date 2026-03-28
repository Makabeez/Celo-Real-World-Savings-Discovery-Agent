import time
from web3 import Web3
from web3.middleware import ExtraDataToPOAMiddleware

# --- CONFIGURATION ---
CELO_RPC = "https://forno.celo.org"
PRIVATE_KEY=0x22515f02bce13d8f736c5afdd8b5a9664023ec78fd05b237856d9bb68f53af06

USDC_ADDRESS = Web3.to_checksum_address("0xcebA9300f2b948710d2653dD7B07f33A8B32118C")
AAVE_POOL_ADDRESS = Web3.to_checksum_address("0x794a61358D6845594F94dc1DB02A252b5b4814aD")

w3 = Web3(Web3.HTTPProvider(CELO_RPC))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

account = w3.eth.account.from_key(PRIVATE_KEY)
wallet_address = account.address

ERC20_ABI = [
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
    {"constant": False, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}], "name": "approve", "outputs": [{"name": "", "type": "bool"}], "type": "function"}
]

AAVE_POOL_ABI = [
    {"inputs": [{"internalType": "address", "name": "asset", "type": "address"}, {"internalType": "uint256", "name": "amount", "type": "uint256"}, {"internalType": "address", "name": "onBehalfOf", "type": "address"}, {"internalType": "uint16", "name": "referralCode", "type": "uint16"}], "name": "supply", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

usdc_contract = w3.eth.contract(address=USDC_ADDRESS, abi=ERC20_ABI)
aave_pool = w3.eth.contract(address=AAVE_POOL_ADDRESS, abi=AAVE_POOL_ABI)

def approve_usdc(amount):
    print(f"🔐 Approving Aave Pool to handle {amount / 10**6} USDC...")
    # Request the pending nonce to avoid overlap
    nonce = w3.eth.get_transaction_count(wallet_address, 'pending')
    
    tx = usdc_contract.functions.approve(AAVE_POOL_ADDRESS, amount).build_transaction({
        'chainId': 42220, 'gas': 100000, 'gasPrice': w3.eth.gas_price, 'nonce': nonce,
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"⏳ Waiting for approval confirmation... Hash: {w3.to_hex(tx_hash)}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("✅ Approval complete.")
    
    # Give the RPC node 5 seconds to fully sync the new nonce
    time.sleep(5) 

def supply_to_aave(amount):
    print(f"🏦 Supplying {amount / 10**6} USDC to Aave Yield Pool...")
    nonce = w3.eth.get_transaction_count(wallet_address, 'pending')
    
    tx = aave_pool.functions.supply(USDC_ADDRESS, amount, wallet_address, 0).build_transaction({
        'chainId': 42220, 'gas': 250000, 'gasPrice': w3.eth.gas_price, 'nonce': nonce,
    })
    
    signed_tx = w3.eth.account.sign_transaction(tx, private_key=PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    
    print(f"⏳ Waiting for supply confirmation... Hash: {w3.to_hex(tx_hash)}")
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"💸 Success! Funds are now generating yield on Aave.")

def run_yield_strategy():
    print("🚀 Initiating Sweep-to-Save Strategy...")
    while True:
        try:
            tx_count = w3.eth.get_transaction_count(wallet_address)
            if tx_count < 1000:
                print(f"⏸️ Agent has {tx_count} TXs. Waiting for Work Visa...")
                time.sleep(60)
                continue

            usdc_balance = usdc_contract.functions.balanceOf(wallet_address).call()
            if usdc_balance > 1000000:
                print(f"💰 Detected surplus balance: {usdc_balance / 10**6} USDC.")
                approve_usdc(usdc_balance)
                supply_to_aave(usdc_balance)
            else:
                print("💤 No surplus USDC detected. Monitoring wallets...")

            time.sleep(3600)
        except Exception as e:
            print(f"❌ Error in yield loop: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_yield_strategy()

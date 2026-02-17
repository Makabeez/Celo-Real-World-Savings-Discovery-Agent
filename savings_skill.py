import os
import json
import time
from web3 import Web3
from dotenv import load_dotenv

load_dotenv()

# --- CONFIGURATION FORCE MAINNET ---
RPC_URL = "https://forno.celo.org"
CHAIN_ID = 42220

# Connexion Web3
w3 = Web3(Web3.HTTPProvider(RPC_URL))
PRIVATE_KEY = os.getenv("PRIVATE_KEY")
account = w3.eth.account.from_key(PRIVATE_KEY)

# Adresses Mainnet
CELO_ADDRESS = w3.to_checksum_address("0x471EcE3750Da237f93B8E339c536989b8978a438")
USDC_ADDRESS = w3.to_checksum_address("0xcebA9300f2b948710d2653dD7B07f33A8B32118C")
ROUTER_ADDRESS = w3.to_checksum_address("0x5615CDAb10dc425a742d643d949a7F474C01abc4")

# ABI Uniswap Router (Minimal)
ROUTER_ABI = [{"inputs":[{"components":[{"internalType":"address","name":"tokenIn","type":"address"},{"internalType":"address","name":"tokenOut","type":"address"},{"internalType":"uint24","name":"fee","type":"uint24"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMinimum","type":"uint256"},{"internalType":"uint160","name":"sqrtPriceLimitX96","type":"uint160"}],"internalType":"struct ISwapRouter.ExactInputSingleParams","name":"params","type":"tuple"}],"name":"exactInputSingle","outputs":[{"internalType":"uint256","name":"amountOut","type":"uint256"}],"stateMutability":"payable","type":"function"}]

class SavingsAgent:
    def __init__(self, threshold_celo=1.0):
        self.threshold = w3.to_wei(threshold_celo, 'ether')
        self.router = w3.eth.contract(address=ROUTER_ADDRESS, abi=ROUTER_ABI)

    def check_and_save(self):
        try:
            balance = w3.eth.get_balance(account.address)
            print(f"✅ [MAINNET] Solde actuel : {w3.from_wei(balance, 'ether')} CELO")

            if balance > self.threshold:
                amount_to_swap = balance - self.threshold
                print(f"🚀 SEUIL DÉPASSÉ ! Swap de {w3.from_wei(amount_to_swap, 'ether')} CELO en cours...")

                # Configuration du Swap
                params = {
                    "tokenIn": CELO_ADDRESS,
                    "tokenOut": USDC_ADDRESS,
                    "fee": 3000,
                    "recipient": account.address,
                    "amountIn": amount_to_swap,
                    "amountOutMinimum": 0,
                    "sqrtPriceLimitX96": 0
                }

                # Transaction
                tx = self.router.functions.exactInputSingle(params).build_transaction({
                    'from': account.address,
                    'value': amount_to_swap,
                    'gas': 350000,
                    'gasPrice': w3.eth.gas_price,
                    'nonce': w3.eth.get_transaction_count(account.address),
                    'chainId': CHAIN_ID
                })

                signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
                
                print(f"🎉 SUCCÈS ! Hash : {w3.to_hex(tx_hash)}")
                return w3.to_hex(tx_hash)
            else:
                print("💤 Solde insuffisant pour le swap (Min 1.0 CELO)")
                return None
        except Exception as e:
            print(f"❌ ERREUR : {str(e)}")
            return None

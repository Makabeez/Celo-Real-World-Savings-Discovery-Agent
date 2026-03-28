from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from datetime import datetime
import requests
import random
from web3 import Web3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

CELO_RPC = "https://forno.celo.org"
w3 = Web3(Web3.HTTPProvider(CELO_RPC))

def get_real_celo_price():
    try:
        res = requests.get("https://api.binance.com/api/v3/ticker/price?symbol=CELOUSDT", timeout=2)
        return float(res.json()["price"])
    except:
        return 0.82 

@app.get("/api/status")
async def get_status():
    current_price = get_real_celo_price()
    mock_celo = 11.32
    mock_usdc = 145.20
    agent_wallet = "0x42095A63f19567f862419b7c6c6FfB47bb63F39f" 
    
    try:
        tx_count = w3.eth.get_transaction_count(agent_wallet)
    except Exception:
        tx_count = 0
        
    if tx_count >= 10000:
        visa_status = "Celo Citizen: Ecosystem Master"
        reason = f"Citizenship secured. Agent has full ecosystem access. Executing Yield Routing."
        strategy = "Yield Routing: Supplying USDC to Aave (5.2% APY)"
    elif tx_count >= 1000:
        visa_status = "Work Visa: Active (Farming Citizenship)"
        reason = f"Work Visa secured. Market stable at ${current_price:.2f}. Grinding remaining TXs for Citizenship."
        strategy = "Visa Farming: Pushing for 10,000 TX Milestone"
    else:
        visa_status = "Tourist Visa: Eligible"
        reason = "Building initial on-chain reputation."
        strategy = "Visa Farming: Building on-chain reputation"

    return {
        "status": "Active",
        "celo_price": current_price,
        "active_strategy": strategy,
        "reasoning": reason,
        "balance_celo": mock_celo,
        "balance_usdc": mock_usdc,
        "visa_status": visa_status,
        "tx_count": tx_count,
        "timestamp": datetime.now().strftime("%H:%M:%S")
    }

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)

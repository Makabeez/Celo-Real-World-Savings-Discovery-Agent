import requests
from cryptography.hazmat.primitives.asymmetric import ed25519

# ==========================================
# ⚙️ CONFIGURATION - FILL THESE IN
# ==========================================

PRIVATE_KEY_HEX = "93e6363fbb5561d41ab1cb172d0c10c8805539710865d8cc32cb218516e9360d"
PUBLIC_KEY_HEX = "69f1298cd8438f96883c7abc8c92c58bdd803333c06eabb99e3700126996e0c4"
GUARDIAN_WALLET = "0x2f225F8A538e7fD613e8ba79DCDdC7D1422AEd1C"
# ==========================================

def automated_handshake():
    print("🤖 Initiating automated API handshake...")
    
    # 1. Ask the API for a fresh challenge hash directly
    challenge_url = "https://app.ai.self.xyz/api/agent/register/ed25519-challenge"
    challenge_payload = {
        "pubkey": PUBLIC_KEY_HEX,
        "network": "mainnet",
        "humanAddress": GUARDIAN_WALLET
    }
    
    print("🌐 Requesting fresh challenge hash...")
    chal_res = requests.post(challenge_url, json=challenge_payload)
    
    if chal_res.status_code != 200:
        print(f"❌ Failed to get challenge: {chal_res.text}")
        return
        
    challenge_data = chal_res.json()
    
    # Safely extract the hash, removing '0x' if the API included it
    raw_hash = challenge_data.get("challengeHash", "").replace("0x", "")
    print(f"✅ Received fresh hash: {raw_hash}")
    
    # 2. Sign the raw bytes of the hash
    try:
        private_bytes = bytes.fromhex(PRIVATE_KEY_HEX)
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(private_bytes)
        
        hash_bytes = bytes.fromhex(raw_hash)
        signature_hex = private_key.sign(hash_bytes).hex()
        print(f"🔐 Signature generated: {signature_hex[:16]}...{signature_hex[-16:]}")
    except Exception as e:
        print(f"❌ Cryptography Error: Ensure your private key is exactly 64 hex characters. Details: {e}")
        return
    
    # 3. Submit the final registration
    register_url = "https://app.ai.self.xyz/api/agent/register"
    register_payload = {
        "mode": "ed25519-linked",
        "network": "mainnet",
        "humanAddress": GUARDIAN_WALLET,
        "ed25519Pubkey": PUBLIC_KEY_HEX,
        "ed25519Signature": signature_hex,
        "disclosures": {
            "minimumAge": 21,
            "ofac": True,
            "nationality": True,
            "name": True, 
            "date_of_birth": True,
            "gender": True,
            "issuing_state": True
        }
    }
    
    print("🚀 Submitting Visa registration...")
    reg_res = requests.post(register_url, json=register_payload)
    
    if reg_res.status_code == 200:
        print("\n🎉 SUCCESS! Your agent is officially verified.")
        print("👉 Check your browser. The Work Visa should now be unlocked!")
    else:
        print(f"\n❌ Registration Failed: {reg_res.text}")

if __name__ == "__main__":
    automated_handshake()

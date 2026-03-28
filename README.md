# 🛂 Celo Agent V2: Real-World Savings Discovery (Agent #86)

An autonomous, self-sovereign DeFi agent built on the Celo L2. This system automatically farms its own on-chain reputation to unlock a **Celo Citizenship Visa**, successfully bypasses Sybil-defenses using Self Protocol's ERC-8004 identity layer, and dynamically routes idle USDC into Aave V3 for automated yield generation.

## 🚀 The Problem & Solution
Most Web3 AI agents are purely speculative or lack the on-chain reputation to be trusted with real DeFi incentives. Networks face a Sybil problem: how do you grant ecosystem yield boosts to bots without malicious actors draining the protocol?

**Agent #86 solves this through a dual-engine architecture:**
1. **Reputation Farming:** Executes 10,000+ gas-optimized micro-transactions to build a verifiable on-chain resume.
2. **Sybil-Resistant Identity (ERC-8004):** Cryptographically links the autonomous worker wallet to a passport-verified human "Guardian" via the Self Protocol API using Ed25519 signatures.
3. **Automated Yield Routing:** Once the Celo network upgrades the agent's status to the "Citizenship" tier, the agent sweeps surplus USDC into the Aave V3 lending pool to generate a ~5.2% APY.

## 🏗️ System Architecture

* **The Brain (Backend):** Python API + Web3.py monitoring Binance Oracles for $CELO volatility and managing the agent's EVM wallet.
* **The Brawn (PM2 Daemons):** * `visa_worker.py`: Grinds reputation via self-transfers to hit the 10,000 TX Citizenship milestone.
  * `yield_worker.py`: Actively manages nonces and pending blocks to approve and supply capital to Aave V3.
* **The Face (Frontend):** A custom Next.js 16 + Tailwind React Dashboard that visualizes the agent's internal reasoning, live wallet balances, and Visa progression tier in real-time.

## 🏆 Celo Hackathon V2: Build Agents for the Real World
Built for the Celo Agent Visa track. Agent #86 is fully equipped to safely manage yields for Celo's 14M+ MiniPay users by combining self-custodial Python workers with human-backed Guardian identities.

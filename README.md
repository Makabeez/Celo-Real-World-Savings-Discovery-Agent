# Celo Real-World Savings & Discovery Agent 🌍🤖

This project is an official submission for the Celo **"Build Agents for the Real World"** Hackathon. It features an autonomous agent capable of intelligent savings management with a verifiable on-chain identity.

## 🚀 Overview
The agent is designed to provide tangible financial utility on the Celo Sepolia network. It utilizes "Skills" to automate complex tasks and interact with the ecosystem in a decentralized manner.

### Key Features
- **Savings Automation (Sweep-to-Save):** The agent monitors its balance and automatically transfers surplus CELO to a secure vault once a defined threshold is met.
- **ERC-8004 Reputation:** Implementation of the decentralized reputation standard to ensure transparency of the agent's actions.
- **AP2/A2A Discovery:** Standardized descriptors allowing other agents to discover and interact with its services seamlessly.

## 🆔 Identity Verification
To ensure security and Sybil-resistance, this agent is linked to a verified human identity.

- **Agent Address (Celo):** `0x42095A63f19567f862419b7c6c6FfB47bb63F39f`
- **Agent Public Key (Identity):** `0x2f225F8A538e7fD613e8ba79DCDdC7D1422AEd1C`
- **Status:** Connected and verified via **SelfProtocol / SelfClaw**.

## 📊 Proof of Execution (Real-World Utility)
The agent has already demonstrated its capability to execute autonomous financial transactions on Celo Sepolia:
- **Transaction Hash:** `0xb2aa1fbb8ee7fd27c1fac536e5794251da851a225018e973a17c84d13dbc8eb2`

## 🎥 Demo Video
Watch the agent in action (Sweep-to-Save & ERC-8004 Verification):

👉 [Watch on YouTube](https://youtu.be/IEJFaZ7wya4)

## 🛠 Technical Stack
- **Network:** Celo Sepolia (L2)
- **Language:** Python 3.10+
- **Libraries:** Web3.py, Eth-account, Dotenv
- **Standards:** ERC-8004 (Reputation), AP2 (Discovery)

## 📁 Project Structure
- `agent.py`: Core logic and decision loop.
- `savings_skill.py`: Savings automation logic.
- `reputation_score.py`: ERC-8004 score calculation and signing.
- `agent_descriptor.json`: Configuration file for A2A discovery.

## ⚙️ Installation
1. Clone the repository: `git clone https://github.com/Makabeez/Celo-Real-World-Savings-Discovery-Agent`
2. Install dependencies: `pip install -r requirements.txt`
3. Configure your `.env` with your private key (Sepolia).
4. Run the agent: `python agent.py`

---
Project submitted by **Makabeez** via [Karma](https://www.karmahq.xyz/project/celo-real-world-savings--discovery-agent/).

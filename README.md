# Celo Real-World Agent (ERC-8004)

This project is an AI-driven agentic application built for the **Celo "Build Agents for the Real World" Hackathon**. It focuses on everyday utility through automated financial management and decentralized reputation.

## Features
- **Savings Automation**: Automatically monitors wallet balance and moves surplus funds to a secure savings vault when a threshold (1 CELO) is exceeded.
- **ERC-8004 Reputation**: Implements a verifiable reputation score based on on-chain activity, signed cryptographically by the agent.
- **Celo Sepolia Integration**: Fully functional on the Celo L2 testnet for fast and low-cost operations.

## Technical Stack
- **Network**: Celo Sepolia (Chain ID: 11142220)
- **Standard**: ERC-8004 (Reputation Score)
- **Language**: Python 3
- **Libraries**: Web3.py, Eth-account, python-dotenv

## Agent Identity
- **Agent Address**: 0x42095A63f19567f862419b7c6c6FfB47bb63F39f
- **Verification**: Linked to SelfProtocol for human-to-agent verification.

## How it Works
1. `agent.py`: Handles network connection and wallet status.
2. `savings_skill.py`: Executes the "Real World" utility (moving funds).
3. `reputation_score.py`: Generates the signed ERC-8004 report based on transaction history.

## Proof of Execution
- **Savings Transaction**: 0xb2aa1fbb8ee7fd27c1fac536e5794251da851a225018e973a17c84d13dbc8eb2
- **Standard**: ERC-8004 compliant metadata and signatures stored in `final_reputation_score.json`.

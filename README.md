# Celo "Sweep-to-Save" Autonomous Agent 🌍🤖

Official submission for the Celo "Build Agents for the Real World" Hackathon. This autonomous agent manages financial liquidity on the **Celo Mainnet**.

## 🚀 Mainnet Success & Proof of Execution
The agent has successfully transitioned from Testnet to live Mainnet operations. It autonomously monitors balances and executes "Sweep-to-Save" logic.

- **Mainnet Transaction Hash**: [0xb31cace093ef8ead7f122b803d781c59ac65819ac82d7acd19efbf62977a75f1](https://celoscan.io/tx/0xb31cace093ef8ead7f122b803d781c59ac65819ac82d7acd19efbf62977a75f1)
- **Status**: Operational
- **Network**: Celo Mainnet (Chain ID: 42220)

## 🛠 Technical Architecture
The agent uses a robust 3-step sequence to ensure reliable decentralized swaps:
1. **Wrap**: Converts Native CELO to ERC-20 WCELO.
2. **Approve**: Authorizes the Ubeswap Router to move WCELO.
3. **Swap**: Executes the trade to USDC while maintaining a 1.0 CELO gas buffer.

## 🆔 On-Chain Identity
- **Agent Address**: `0x42095A63f19567f862419b7c6c6FfB47bb63F39f`
- **Standards**: ERC-8004 (Reputation), AP2 (Discovery)

## ⚙️ Installation
```bash
git clone [https://github.com/Makabeez/Celo-Real-World-Savings-Discovery-Agent](https://github.com/Makabeez/Celo-Real-World-Savings-Discovery-Agent)
pip install web3 python-dotenv
pm2 start agent.py --name celo-agent

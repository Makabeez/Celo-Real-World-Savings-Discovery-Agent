# Celo "Sweep-to-Save" Autonomous Agent 🌍🤖

Official submission for the Celo "Build Agents for the Real World" Hackathon. This autonomous agent manages financial liquidity while maintaining a verifiable on-chain identity via the SelfProtocol ecosystem.

## 🚀 Mainnet & Testnet Proof of Execution
The agent has successfully transitioned from Testnet to live Mainnet operations, demonstrating its ability to execute real-world financial transactions autonomously.

- **Mainnet (Live Success)**: [0xb31cace093ef8ead7f122b803d781c59ac65819ac82d7acd19efbf62977a75f1](https://celoscan.io/tx/0xb31cace093ef8ead7f122b803d781c59ac65819ac82d7acd19efbf62977a75f1)
- **Sepolia (Development)**: [0xb2aa1fbb8ee7fd27c1fac536e5794251da851a225018e973a17c84d13dbc8eb2](https://sepolia.celoscan.io/tx/0xb2aa1fbb8ee7fd27c1fac536e5794251da851a225018e973a17c84d13dbc8eb2)

## 🆔 Identity & Verification
To ensure security and Sybil-resistance, this agent is linked to a verified human identity through the SelfProtocol stack.
- **Verification Method**: Connected and verified via **SelfProtocol / SelfClaw**.
- **Agent Address (Celo)**: `0x42095A63f19567f862419b7c6c6FfB47bb63F39f`
- **Agent Public Key**: `0x2f225F8A538e7fD613e8ba79DCDdC7D1422AEd1C`
- **Standards**: ERC-8004 (Reputation), AP2/A2A (Discovery)

## 🛠 Technical Architecture
The agent implements a robust 3-step sequence to handle Native CELO swaps reliably on decentralized exchanges:

1. **Wrap**: Converts Native CELO to ERC-20 WCELO.
2. **Approve**: Grants the Ubeswap/Uniswap Router permission to spend WCELO.
3. **Swap**: Executes the trade to USDC while maintaining a **1.0 CELO gas buffer** to ensure continuous operation.



## 🎥 Demo Video
Watch the agent in action (Sweep-to-Save logic & ERC-8004 Verification):
👉 [Watch the Demo on YouTube](https://www.youtube.com/watch?v=dQw4w9WgXcQ)

## 📁 Project Structure
- `agent.py`: Core autonomous logic and main decision loop.
- `savings_skill.py`: Specialized logic for the Sweep-to-Save automation.
- `reputation_score.py`: ERC-8004 calculation and attestation signing.
- `agent_descriptor.json`: Configuration for AP2 discovery services.

## ⚙️ Installation & Usage
1. **Clone the Repo**:
   ```bash
   git clone [https://github.com/Makabeez/Celo-Real-World-Savings-Discovery-Agent](https://github.com/Makabeez/Celo-Real-World-Savings-Discovery-Agent)
   cd celo-agent-hackathon

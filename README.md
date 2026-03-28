# Celo "Sweep-to-Save" Autonomous Agent 🌍🤖

**Official submission for the Celo "Build Agents for the Real World" Hackathon.**

This autonomous agent manages financial liquidity while maintaining a verifiable on-chain identity via the SelfProtocol ecosystem. It is now fully operational on the **Celo Mainnet**.

## 🚀 Mainnet Proof of Execution
The agent has successfully transitioned from development to live production, demonstrating real-world utility by autonomously managing CELO liquidity.

- **Mainnet Demo Video**: [![Watch the Mainnet Execution](https://img.youtube.com/vi/DFjHpG77Ljk/0.jpg)](https://youtu.be/DFjHpG77Ljk)
- **Verified Transaction**: [`0xb31cace093ef8ead7f122b803d781c59ac65819ac82d7acd19efbf62977a75f1`](https://celoscan.io/tx/0xb31cace093ef8ead7f122b803d781c59ac65819ac82d7acd19efbf62977a75f1)

## 🆔 Identity & Verification
To ensure security and Sybil-resistance, this agent is linked to a verified human identity through the SelfProtocol stack.
- **Verification Method**: Connected via **SelfProtocol / SelfClaw**.
- **Agent Address (Celo)**: `0x42095A63f19567f862419b7c6c6FfB47bb63F39f`
- **Identity Standard**: Verified compliant with **ERC-8004** (Reputation) and **AP2/A2A** (Discovery).

## 🛠 Technical Architecture
The agent implements a robust 3-step sequence to handle Native CELO swaps reliably on decentralized exchanges:

1. **Wrap**: Converts Native CELO to ERC-20 WCELO.
2. **Approve**: Grants the DEX Router (Ubeswap/Uniswap) permission to spend WCELO.
3. **Swap**: Executes the trade to USDC while maintaining a **1.0 CELO gas buffer** to ensure continuous operation.

## 📁 Project Structure
- `agent.py`: Core autonomous logic and main decision loop.
- `savings_skill.py`: Specialized logic for the Sweep-to-Save automation.
- `reputation_score.py`: ERC-8004 calculation and attestation signing.
- `agent_descriptor.json`: Configuration for AP2 discovery services.
- `requirements.txt`: Project dependencies for environment setup.

## ⚙️ Installation & Usage
1. **Clone the Repo**:
   ```bash
   git clone [https://github.com/Makabeez/Celo-Real-World-Savings-Discovery-Agent](https://github.com/Makabeez/Celo-Real-World-Savings-Discovery-Agent)
   cd celo-agent-hackathon

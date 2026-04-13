![withdraw_token](https://github.com/user-attachments/assets/4dbc1db5-c1b6-4051-8a95-e9e2c7833183)
![Miniapp](https://github.com/user-attachments/assets/e182f3fc-eacb-4676-b4af-aed126d19587)
![deposit_token](https://github.com/user-attachments/assets/dad5e3df-1bf0-42ec-bca5-ac880b46f7e6)
![celoscan_tx](https://github.com/user-attachments/assets/864ac8ca-2bb7-4b24-9514-13a765ebb3a5)
![approve_withdraw](https://github.com/user-attachments/assets/13825a57-6ecd-4888-a249-21f35ec0008b)
![approve_token](https://github.com/user-attachments/assets/d92f6dee-40e0-49ea-9b66-2bf13ca9801a)
# MiniYield 🏦

A one-click, self-custodial yield router for MiniPay users, featuring an autonomous background agent that automatically sweeps idle USDC into Aave V3 for maximum yield. 

Built for the Celo Hackathon.

## 🌟 Overview

MiniYield simplifies Decentralized Finance (DeFi) for everyday users. By acting as a secure gateway to Aave V3 on the Celo blockchain, it allows users to earn yield on their stablecoins without navigating complex lending protocols. 

The system consists of a mobile-optimized Next.js frontend (designed for MiniPay), a production-hardened Solidity smart contract router, and an autonomous Python agent that discovers savings opportunities.

## 🔗 Smart Contract (Celo Mainnet)

The core routing logic is handled by a custom, fully verified smart contract deployed on the **Celo Mainnet**.

* **Contract Address:** [`0xb9f75EF30953ab91a9CB727f799A1a6Bb1499f22`](https://celoscan.io/address/0xb9f75EF30953ab91a9CB727f799A1a6Bb1499f22)
* **Integration:** Aave V3 Celo Pool
* **Security Features:** * `SafeERC20` strict token transfers
  * `ReentrancyGuard` to prevent recursive attacks
  * `Ownable2Step` for safe ownership transfers
  * Immutable core addresses for gas optimization and security
  * Built-in Emergency Token Recovery

## 🛠️ System Architecture

### 1. The Frontend (`/celo-dashboard`)
A responsive, React-based dashboard built with **Next.js**, **Wagmi**, **Viem**, and **React Query**. It allows users to seamlessly deposit USDC and withdraw aUSDC with a single tap.

### 2. The Smart Contract (`/contracts/Agent86Router.sol`)
A decentralized router that takes user USDC, supplies it to Aave V3, and routes the aUSDC receipt tokens directly back to the user's wallet, taking a transparent 1% routing fee in the process.

### 3. The Autonomous Agent (Python)
A backend Python worker that monitors on-chain states and user balances to discover and execute optimal yield strategies automatically.

## 🚀 Getting Started

### Prerequisites
* Node.js & npm
* Python 3.10+
* PM2 (for production deployment)

### Running the Frontend Locally
```bash
# Navigate to the dashboard directory
cd celo-dashboard

# Install dependencies
npm install

# Run the development server
npm run dev

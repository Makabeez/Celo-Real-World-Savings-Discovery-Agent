# Celo Real-World Savings & Discovery Agent 🌍🤖

Ce projet est une soumission officielle pour le hackathon **"Build Agents for the Real World"** de Celo. Il présente un agent autonome capable de gérer intelligemment l'épargne tout en possédant une identité vérifiable on-chain.

## 🚀 Présentation
L'agent est conçu pour apporter une utilité financière concrète au quotidien sur le réseau Celo Sepolia. Il utilise des "Skills" (compétences) pour automatiser des tâches complexes et interagir avec l'écosystème de manière décentralisée.

### Fonctionnalités Clés
- **Automatisation de l'Épargne (Sweep-to-Save) :** L'agent surveille son solde et transfère automatiquement l'excédent de CELO vers un coffre-fort (Vault) sécurisé dès qu'un seuil est atteint.
- **Identité ERC-8004 :** Implémentation du standard de réputation décentralisée pour garantir la transparence des actions de l'agent.
- **Découverte AP2/A2A :** Utilisation de descripteurs standardisés pour permettre à d'autres agents de trouver et d'utiliser ses services.

## 🆔 Vérification d'Identité
Pour garantir la sécurité et la résistance aux attaques Sybil, cet agent est lié à une identité humaine vérifiée.

- **Agent Address (Celo) :** `0x42095A63f19567f862419b7c6c6FfB47bb63F39f`
- **Agent Public Key (Identity) :** `0x2f225F8A538e7fD613e8ba79DCDdC7D1422AEd1C`
- **Statut :** Connecté et vérifié via **SelfProtocol / SelfClaw**.

## 📊 Preuve d'Exécution (Utilité Réelle)
L'agent a déjà démontré sa capacité à exécuter des transactions financières autonomes sur Celo Sepolia :
- **Transaction Hash :** `0xb2aa1fbb8ee7fd27c1fac536e5794251da851a225018e973a17c84d13dbc8eb2`

## 🛠 Stack Technique
- **Réseau :** Celo Sepolia (L2)
- **Langage :** Python 3.10+
- **Bibliothèques :** Web3.py, Eth-account, Dotenv
- **Standards :** ERC-8004 (Reputation), AP2 (Discovery)

## 📁 Structure du Projet
- `agent.py` : Cœur de l'agent et boucle de décision.
- `savings_skill.py` : Logique d'automatisation de l'épargne.
- `reputation_score.py` : Calcul et signature du score ERC-8004.
- `agent_descriptor.json` : Fichier de configuration pour la découverte A2A.

## ⚙️ Installation
1. Clonez le répertoire : `git clone https://github.com/Makabeez/Celo-Real-World-Savings-Discovery-Agent`
2. Installez les dépendances : `pip install -r requirements.txt`
3. Configurez votre `.env` avec votre clé privée (Sepolia).
4. Lancez l'agent : `python agent.py`

---
Projet soumis par **Makabeez** via [Karma](https://www.karmahq.xyz/project/celo-real-world-savings--discovery-agent/).

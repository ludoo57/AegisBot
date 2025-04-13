<h1 align="center">🤖 AegisBOT</h1>
<p align="center">
Bot Discord de sécurité, modération et administration avancée.<br>
Créé avec ❤️ par <strong>ludoo57</strong>
</p>

<p align="center">
<img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/ludoo57/AegisBOT/main/.github/version-badge.json&style=flat-square" />
<img src="https://img.shields.io/badge/AegisBOT-v2.0.0-blue?style=flat-square" />
<img src="https://img.shields.io/badge/Python-3.10+-yellow?style=flat-square" />
<img src="https://img.shields.io/badge/RedBot-Compatible-brightgreen?style=flat-square" />
<img src="https://img.shields.io/github/license/ludoo57/AegisBOT?style=flat-square" />
</p>

---

## 📌 À propos

AegisBOT est un bot Discord conçu pour offrir une **modération avancée**, une **protection anti-nuke/anti-raid**, et des **outils d'administration intelligents**.  
Inspiré de bots populaires comme **Wick**, **Dyno**, et **Carl**, il propose une expérience moderne, interactive et hautement personnalisable.

---

## ⚙️ Fonctionnalités principales

- 🛡️ Anti-raid / Anti-nuke / Anti-webhook
- 💬 Automod (anti-lien, anti-spam, mots filtrés…)
- 👮 Système de `warn`, `mute`, `ban`, `kick`
- 📄 Commandes hybrides (prefix + slash)
- 📈 Logs détaillés, panneaux de configuration interactifs
- 🧩 Multi-guild support avec configuration par serveur
- 🧠 Interface intuitive avec embeds stylisés

---

## 🚀 Installation

```bash
git clone https://github.com/ludoo57/AegisBOT.git
cd AegisBOT
python -m venv venv
source venv/bin/activate  # ou .\\venv\\Scripts\\activate sur Windows
pip install -U pip
pip install -e .
redbot --dev MonBot

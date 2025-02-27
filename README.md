# 🕹️ **Serveur de Matchmaking**

## 📜 Présentation du projet

Ce projet consiste en un serveur de **matchmaking** pour un jeu de plateau au tour par tour. Il comprend trois composantes principales :  
- 🖥️ **Serveur de matchmaking**  
- 🎮 **Logiciel client**  
- 🗃️ **Base de données**

## ⚙️ Fonctionnalités

- **File d'attente** pour gérer les joueurs en attente
- **Matchs** avec communication entre les joueurs et gestion du plateau de jeu
- **Tours** pour enregistrer les coups joués

## 🛠️ **Stack technologique**

### 1️⃣ **Base de données**  
- 🗃️ **PostgreSQL** : Base de données relationnelle

### 2️⃣ **Serveur de matchmaking**  
- 🐍 **Python** avec **FastAPI** pour l'API  
- 💬 **WebSockets** pour la communication en temps réel  
- 🛠️ **SQLAlchemy** pour l'interaction avec PostgreSQL

### 3️⃣ **Logiciel client**  
- ⚛️ **React.js** avec **Next.js** pour l'interface web  

### 4️⃣ **Communication temps réel**  
- 💬 **WebSockets** pour les échanges en temps réel  
- 📡 **gRPC** pour des communications structurées (optionnel)

## 🚨 **Prérequis**

- Python 3.x  
- PostgreSQL  
- Node.js (si React est utilisé)  

---

uvicorn app.main:app --reload dans backend

wscat -c ws://127.0.0.1:8000/ws

deactivate sortir du venv
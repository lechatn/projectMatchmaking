# 🕹️ Serveur de Matchmaking
## 📜 Présentation du projet

Ce projet consiste en un serveur de **matchmaking** pour un jeu de morpion. Il comprend trois composantes principales :  
- 🖥️ **Serveur de matchmaking**  
- 🎮 **Logiciel client**  
- 🗃️ **Base de données**

## ⚙️ Fonctionnalités

- **File d'attente** pour gérer les joueurs en attente
- **Matchs** avec communication entre les joueurs et gestion du plateau de jeu

## 🛠️ Stack technologique

### 1️⃣ Base de données  
- 🗃️ **PostgreSQL** : Base de données relationnelle

### 2️⃣ Serveur de matchmaking  
- 🐍 **Python** avec **FastAPI** pour l'API  
- 💬 **WebSockets** pour la communication en temps réel  
- 🛠️ **SQLAlchemy** pour l'interaction avec PostgreSQL

### 3️⃣ Logiciel client  
- ⚛️ **React.js** avec **Next.js** pour l'interface web  

### 4️⃣ Communication temps réel  
- 💬 **WebSockets** pour les échanges en temps réel  

## 🚨 Prérequis

- Python 3.x  
- PostgreSQL  
- Node.js

## 🚀 Mise en place du projet

### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/lechatn/projectMatchmaking.git
cd projectMatchmaking
```


### 2️⃣ Configurer la base de données PostgreSQL

1. **Installer PostgreSQL**: Suivez les instructions sur le site officiel de PostgreSQL pour installer PostgreSQL sur votre machine.

2. **Créer une base de données**: Connectez-vous à PostgreSQL et créez une nouvelle base de données en utilisant la commande SQL suivante:

```bash
CREATE DATABASE nom_base;
```


3. **Configurer les variables d'environnement**: Créez un fichier `.env` à la racine du projet et ajoutez les informations de connexion à la base de données.

PS : Si la création de la bdd ne marche pas, le fichier backupMatchmaking.sql peut vous aider à la créer (ressources/backupMatchmaking.sql)

### 3️⃣ Configurer le serveur de matchmaking

1. **Créer et activer un environnement virtuel**:

```bash
python -m venv venv
source venv/Scripts/activate
```

2. **Installer les dépendances**:

```bash
cd backend
pip install -r requirements.txt
```

3. **Créer les tables de la base de données**: Utilisez SQLAlchemy pour créer les tables nécessaires dans la base de données PostgreSQL.

4. **Lancer le serveur**:

```bash
uvicorn app.main:app --reload
```

### 4️⃣ Configurer le logiciel client

1. **Installer les dépendances**:

Dans un autre terminal :
```bash
cd frontend/projectmatchmaking/
npm install
```

2. **Lancer le serveur de développement**:

```bash
npm start
```

### 5️⃣ Tester la communication WebSocket

Utilisez `wscat` si vous voulez tester la connexion WebSocket:

```bash
wscat -c ws://127.0.0.1:8000/ws
```

### 6️⃣ Désactiver l'environnement virtuel

Pour sortir de l'environnement virtuel, utilisez la commande:

```bash
deactivate
```


## 📚 Documentation

Pour plus d'informations, veuillez consulter la documentation officielle de chaque technologie utilisée dans ce projet:

- [FastAPI](https://fastapi.tiangolo.com/)
- [React.js](https://reactjs.org/docs/getting-started.html)
- [PostgreSQL](https://www.postgresql.org/docs/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [WebSockets](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API)











# 🚀 FreelanceAI Assistant

Application d'accompagnement des freelances avec système multi-agent basé sur CrewAI et Streamlit.

## 📋 Description

FreelanceAI Assistant est un MVP qui utilise l'intelligence artificielle pour accompagner les freelances dans leur lancement et développement. L'application propose 3 agents IA spécialisés :

- **🎯 Agent Positionnement & Offre** : Aide à clarifier le positionnement et créer une offre différenciante
- **💼 Agent Fiscalité & Trésorerie** : Guide sur le choix du statut et la gestion financière
- **📢 Agent Visibilité & Prospection** : Accompagne dans la stratégie marketing et l'acquisition clients

## 🛠️ Installation

### Prérequis
- Python 3.8 ou supérieur
- Clés API OpenAI et Serper

### Étapes d'installation

1. **Cloner le projet** (ou créer le dossier)
```bash
cd freelance-ai-assistant
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les clés API**

Modifiez le fichier `.env` avec vos clés :
```
OPENAI_API_KEY=votre_cle_openai
SERPER_API_KEY=votre_cle_serper
```

## 🚀 Lancement

```bash
streamlit run app.py
```

L'application s'ouvrira automatiquement dans votre navigateur à l'adresse : http://localhost:8501

## 💡 Utilisation

1. **Remplir votre profil** dans la barre latérale (ou utiliser le mode démo)
2. **Choisir un agent** ou lancer tous les agents
3. **Consulter les résultats** dans les onglets dédiés
4. **Télécharger** vos résultats pour les conserver

### Mode Démo

Activez le "Mode Démo" dans la sidebar pour tester rapidement avec des données pré-remplies.

## 📁 Structure du Projet

```
freelance-ai-assistant/
├── app.py              # Interface Streamlit
├── agents_crew.py      # Backend CrewAI
├── requirements.txt    # Dépendances
├── .env               # Variables d'environnement
└── .streamlit/
    └── config.toml    # Configuration Streamlit
```

## ⚙️ Architecture

- **Frontend** : Streamlit pour l'interface utilisateur
- **Backend** : CrewAI pour l'orchestration des agents
- **IA** : OpenAI GPT pour le traitement du langage
- **Recherche** : Serper API pour les recherches web

## 🔑 Obtenir les clés API

- **OpenAI** : https://platform.openai.com/api-keys
- **Serper** : https://serper.dev

## ⚠️ Notes importantes

- Les analyses peuvent prendre 1-2 minutes par agent
- Les résultats sont sauvegardés dans la session (non persistants)
- Assurez-vous d'avoir suffisamment de crédits sur vos comptes API

## 📝 Licence

Projet MVP à des fins de démonstration.

## 🤝 Support

Pour toute question ou problème, créez une issue sur le repository.
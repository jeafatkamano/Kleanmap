# KleanMap 🌍

**Plateforme IA de signalement et prédiction de la pollution urbaine en Afrique**

Tech Hub Africa Hackathon 2026 — Piste : Reducing Public Pollution

## Installation

```bash
pip install -r requirements.txt
python app.py
```

Ouvrir : http://localhost:5000

## Fonctionnalités

- 📍 Signalement citoyen sans inscription
- 🗺️ Carte interactive temps réel (Leaflet + OpenStreetMap)
- 🤖 Agent IA prédictif (zones à risque)
- 📊 Dashboard autorités + export CSV
- 📄 Rapport IA automatique

## Stack

- Backend : Python / Flask + SQLAlchemy
- Frontend : Bootstrap 5 + Leaflet.js + Chart.js
- Base de données : SQLite (développement) / PostgreSQL (production)
- IA : Moteur prédictif Python natif + Claude API (optionnel)

## Déploiement AWS

```bash
# Utiliser les prompts Terraform du projet AWS Prompt the Planet
terraform init && terraform apply
```

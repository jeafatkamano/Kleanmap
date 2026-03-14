# Kleanmap
KleanMap is an AI-powered pollution monitoring platform for African cities. Citizens report waste, water, air &amp; noise pollution on an interactive map. An AI engine predicts high-risk zones before they become critical. Built with Python/Flask + Leaflet.js.

# 🌍 KleanMap — AI-Powered Urban Pollution Monitoring Platform

[![Tech Hub Africa 2026](https://img.shields.io/badge/Tech%20Hub%20Africa-Hackathon%202026-green)](https://dorahacks.io)
[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0-lightgrey)](https://flask.palletsprojects.com)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Piste : Reducing Public Pollution** — Tech Hub Africa Hackathon 2026

KleanMap is a citizen-powered AI platform that enables African communities to report, visualize, and **predict** urban pollution zones in real time — before they become critical.

---

## 🎯 The Problem

African cities face a silent crisis:
- **2M+** unmanaged waste dump sites across West Africa
- **40%** of environmental disputes are preventable with early detection
- Municipal authorities have **no centralized data** to prioritize interventions
- Citizens have **no simple tool** to report pollution without bureaucracy

---

## 💡 The Solution

KleanMap applies **industrial AI principles** (predictive maintenance, digital twins, process optimization) to urban pollution management:

| Industrial AI Concept | KleanMap Application |
|---|---|
| Predictive maintenance | Predict pollution hotspots before they become critical |
| Digital twin | Dynamic trust profile for each reported zone |
| Process optimization | Automate municipal intervention prioritization |
| IoT sensor data | Citizen behavioral signals → real-time risk score |

---

## ✨ Features

### 📍 Citizen Reporting
- Report pollution in **30 seconds** — no account required
- GPS location picker on interactive map
- 4 pollution types: Waste, Water, Air, Noise
- Severity levels 1–3

### 🗺️ Real-Time Map
- Live markers color-coded by severity
- Filter by pollution type
- Auto-refresh every 30 seconds
- Built with **Leaflet.js + OpenStreetMap** (free, no API key)

### 🤖 AI Prediction Engine
- Distance-weighted density scoring algorithm
- Identifies high-risk zones **before** reports accumulate
- Visual overlay of predicted hotspots on map
- Pure Python — no external ML API required

### 📊 Authority Dashboard
- Priority queue sorted by criticality
- Status management (pending / in progress / resolved)
- AI-generated analytical report
- Chart.js visualization by pollution type
- **One-click CSV export** for NGO reporting

### 🔌 REST API
```
GET  /api/reports          → All reports as JSON
GET  /api/predictions      → AI-predicted risk zones
GET  /api/stats            → Aggregated statistics
POST /api/report/:id/status → Update report status
POST /report               → Submit new report
```

---

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/kleanmap.git
cd kleanmap

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Open **http://localhost:5000** — demo data loads automatically for Conakry, Guinea.

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11 + Flask 3.0 + SQLAlchemy |
| Database | SQLite (dev) / PostgreSQL (prod) |
| Frontend | Bootstrap 5 + Jinja2 templates |
| Maps | Leaflet.js 1.9 + OpenStreetMap |
| Charts | Chart.js 4.4 |
| AI Engine | Pure Python (distance-weighted scoring) |
| Deployment | AWS EC2 + RDS + ALB (Terraform-ready) |

---

## 📁 Project Structure

```
kleanmap/
├── app.py                  # Main Flask application + AI engine
├── requirements.txt        # Python dependencies
├── README.md
└── templates/
    ├── base.html           # Navbar + layout
    ├── index.html          # Homepage with live stats
    ├── map.html            # Interactive Leaflet map
    ├── report.html         # Citizen reporting form
    └── dashboard.html      # Authority dashboard
```

---

## 🤖 AI Prediction Algorithm

The prediction engine uses a **distance-weighted density scoring** approach:

```python
def compute_risk_score(lat, lng, reports):
    radius_deg = 0.05  # ~5km radius
    score = 0.0
    for report in nearby_reports(lat, lng, radius_deg):
        distance = euclidean_distance(lat, lng, report)
        weight = 1 / (1 + 10 * distance)
        score += report.severity * weight
    return min(1.0, score / 5.0)
```

Zones with a risk score **> 0.3** are flagged and displayed on the map.

---

## ☁️ AWS Deployment

This project is designed to deploy on AWS using Terraform:

```bash
# Uses the production-ready Terraform prompts
# from AWS Prompt the Planet Hackathon 2026
terraform init
terraform apply
```

Infrastructure includes: EC2 + ALB + Auto Scaling + RDS PostgreSQL + S3 + CloudWatch + IAM.

---

## 🌍 Impact

KleanMap targets **African cities** where pollution monitoring infrastructure is minimal:

- **Conakry, Guinea** — primary target city (demo data)
- **Dakar, Senegal** — expansion target
- **Abidjan, Côte d'Ivoire** — expansion target
- **Accra, Ghana** — expansion target

The platform is fully **open source**, works on **3G networks**, requires **no smartphone app installation**, and is accessible **without account creation**.

---

## 📸 Screenshots

| Homepage | Map | Report Form | Dashboard |
|---|---|---|---|
| Live stats | Leaflet markers | GPS picker | Priority queue |

---

## 🏆 Hackathon

**Tech Hub Africa — Hackathon 2026 Challenge**
- Track: **Reducing Public Pollution**
- Platform: DoraHacks
- Prize: $1,000 USD

---

## 📄 License

MIT License — free to use, modify and deploy.

---

## 👤 Author

Built by **Kamano** — Python/Flask developer and founder of [Tcheyna](https://github.com/YOUR_USERNAME/tcheyna), a trust-based real estate matching platform.

---

*KleanMap — Because clean cities start with informed citizens.* 🌿

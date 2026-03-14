from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
import os
import math

app = Flask(__name__)
app.config['SECRET_KEY'] = 'kleanmap-secret-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///kleanmap.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ── MODELS ──
class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    pollution_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    severity = db.Column(db.Integer, default=1)  # 1-3
    city = db.Column(db.String(100), default='Conakry')
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    upvotes = db.Column(db.Integer, default=0)

    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'pollution_type': self.pollution_type,
            'description': self.description,
            'severity': self.severity,
            'city': self.city,
            'status': self.status,
            'created_at': self.created_at.strftime('%d/%m/%Y %H:%M'),
            'upvotes': self.upvotes,
        }

class PredictionZone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    risk_score = db.Column(db.Float, default=0.0)  # 0-1
    zone_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'risk_score': self.risk_score,
            'zone_name': self.zone_name,
        }

# ── PREDICTION ENGINE (ML simplifié sans scikit-learn) ──
def compute_risk_score(lat, lng, reports):
    """Calcule un score de risque basé sur la densité et sévérité des signalements proches."""
    score = 0.0
    radius_deg = 0.05  # ~5km
    nearby = []
    for r in reports:
        dist = math.sqrt((r.latitude - lat)**2 + (r.longitude - lng)**2)
        if dist <= radius_deg:
            nearby.append(r)
    if not nearby:
        return 0.0
    total = sum(r.severity * (1 / (1 + 10 * math.sqrt(
        (r.latitude - lat)**2 + (r.longitude - lng)**2
    ))) for r in nearby)
    score = min(1.0, total / 5.0)
    return round(score, 2)

def generate_prediction_zones():
    """Génère des zones de prédiction basées sur les signalements existants."""
    reports = Report.query.filter_by(status='pending').all()
    if not reports:
        return []
    zones = []
    grid_size = 0.03
    lat_min = min(r.latitude for r in reports) - 0.05
    lat_max = max(r.latitude for r in reports) + 0.05
    lng_min = min(r.longitude for r in reports) - 0.05
    lng_max = max(r.longitude for r in reports) + 0.05
    lat = lat_min
    while lat <= lat_max:
        lng = lng_min
        while lng <= lng_max:
            score = compute_risk_score(lat, lng, reports)
            if score > 0.3:
                zones.append({'lat': round(lat, 4), 'lng': round(lng, 4), 'score': score})
            lng += grid_size
        lat += grid_size
    return zones

# ── AI REPORT GENERATOR ──
def generate_ai_report(reports):
    """Génère un rapport analytique basé sur les signalements."""
    if not reports:
        return "Aucun signalement actif pour le moment."
    total = len(reports)
    by_type = {}
    by_severity = {1: 0, 2: 0, 3: 0}
    for r in reports:
        by_type[r.pollution_type] = by_type.get(r.pollution_type, 0) + 1
        by_severity[r.severity] = by_severity.get(r.severity, 0) + 1
    top_type = max(by_type, key=by_type.get)
    critical = by_severity[3]
    report_text = f"""RAPPORT KleanMap — {datetime.now().strftime('%d/%m/%Y')}

RÉSUMÉ EXÉCUTIF
{total} signalement(s) actif(s) recensé(s) sur la zone surveillée.
Type de pollution dominant : {top_type} ({by_type[top_type]} signalement(s)).
Signalements critiques (niveau 3) : {critical}.

RÉPARTITION PAR TYPE
""" + "\n".join(f"  • {k} : {v} signalement(s)" for k, v in by_type.items()) + f"""

NIVEAUX DE SÉVÉRITÉ
  • Faible (niveau 1) : {by_severity[1]} signalement(s)
  • Moyen (niveau 2) : {by_severity[2]} signalement(s)
  • Critique (niveau 3) : {by_severity[3]} signalement(s)

RECOMMANDATIONS IA
  1. Prioriser l'intervention sur les zones de niveau 3 en premier.
  2. Surveiller les zones à risque élevé identifiées par le modèle prédictif.
  3. Mobiliser les équipes municipales sur les foyers de type '{top_type}'.
  4. Mettre à jour le statut des signalements après intervention.

Rapport généré automatiquement par KleanMap AI — Tech Hub Africa 2026
"""
    return report_text

# ── SEED DATA ──
def seed_data():
    if Report.query.count() == 0:
        samples = [
            Report(latitude=9.5370, longitude=-13.6773, pollution_type='Déchets sauvages',
                   description='Grande décharge sauvage près du marché', severity=3, city='Conakry'),
            Report(latitude=9.5450, longitude=-13.6850, pollution_type='Eau contaminée',
                   description='Eau stagnante et malodorante dans le quartier', severity=2, city='Conakry'),
            Report(latitude=9.5290, longitude=-13.6700, pollution_type='Air pollué',
                   description='Fumées noires d\'un générateur industriel', severity=2, city='Conakry'),
            Report(latitude=9.5500, longitude=-13.6600, pollution_type='Déchets sauvages',
                   description='Dépôt illégal de déchets plastiques', severity=1, city='Conakry'),
            Report(latitude=9.5600, longitude=-13.6900, pollution_type='Pollution sonore',
                   description='Bruit excessif 24h/24 près de l\'école', severity=1, city='Conakry'),
            Report(latitude=9.5200, longitude=-13.6800, pollution_type='Eau contaminée',
                   description='Déversement chimique visible dans le canal', severity=3,
                   city='Conakry', status='in_progress'),
            Report(latitude=9.5650, longitude=-13.6650, pollution_type='Déchets sauvages',
                   description='Déchets hospitaliers abandonnés', severity=3, city='Conakry'),
            Report(latitude=9.5100, longitude=-13.6950, pollution_type='Air pollué',
                   description='Brûlage de plastiques à ciel ouvert', severity=2, city='Conakry'),
        ]
        db.session.add_all(samples)
        db.session.commit()

# ── ROUTES ──
@app.route('/')
def index():
    total = Report.query.count()
    pending = Report.query.filter_by(status='pending').count()
    critical = Report.query.filter_by(severity=3).count()
    resolved = Report.query.filter_by(status='resolved').count()
    stats = {'total': total, 'pending': pending, 'critical': critical, 'resolved': resolved}
    return render_template('index.html', stats=stats)

@app.route('/map')
def map_view():
    return render_template('map.html')

@app.route('/report', methods=['GET', 'POST'])
def report():
    if request.method == 'POST':
        data = request.get_json()
        r = Report(
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            pollution_type=data['pollution_type'],
            description=data.get('description', ''),
            severity=int(data.get('severity', 1)),
            city=data.get('city', 'Conakry'),
        )
        db.session.add(r)
        db.session.commit()
        return jsonify({'success': True, 'id': r.id, 'message': 'Signalement enregistré !'})
    return render_template('report.html')

@app.route('/dashboard')
def dashboard():
    reports = Report.query.order_by(Report.created_at.desc()).all()
    ai_report = generate_ai_report(Report.query.filter_by(status='pending').all())
    return render_template('dashboard.html', reports=reports, ai_report=ai_report)

@app.route('/api/reports')
def api_reports():
    reports = Report.query.all()
    return jsonify([r.to_dict() for r in reports])

@app.route('/api/predictions')
def api_predictions():
    zones = generate_prediction_zones()
    return jsonify(zones)

@app.route('/api/report/<int:id>/upvote', methods=['POST'])
def upvote(id):
    r = Report.query.get_or_404(id)
    r.upvotes += 1
    db.session.commit()
    return jsonify({'upvotes': r.upvotes})

@app.route('/api/report/<int:id>/status', methods=['POST'])
def update_status(id):
    r = Report.query.get_or_404(id)
    data = request.get_json()
    r.status = data.get('status', r.status)
    db.session.commit()
    return jsonify({'success': True})

@app.route('/api/stats')
def api_stats():
    from sqlalchemy import func
    by_type = db.session.query(Report.pollution_type, func.count(Report.id))\
        .group_by(Report.pollution_type).all()
    by_severity = db.session.query(Report.severity, func.count(Report.id))\
        .group_by(Report.severity).all()
    return jsonify({
        'by_type': [{'type': t, 'count': c} for t, c in by_type],
        'by_severity': [{'severity': s, 'count': c} for s, c in by_severity],
        'total': Report.query.count(),
        'pending': Report.query.filter_by(status='pending').count(),
        'resolved': Report.query.filter_by(status='resolved').count(),
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_data()
    app.run(debug=True, port=5000)

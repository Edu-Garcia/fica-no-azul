from flask import jsonify
from .models import Investment, Category
from .extensions import db

def recommend_by_profile(profile: str):
    """Retorna lista de investments recomendados (simples heurística)."""
    q = Investment.query
    if profile == "conservador":
        return q.filter(Investment.risk.in_(["baixo", "medio"])).all()
    if profile == "moderado":
        return q.filter(Investment.risk.in_(["medio", "alto"])).all()
    if profile == "arrojado":
        return q.filter(Investment.risk == "alto").all()
    return q.all()
from flask import Blueprint, request, jsonify
from ..models import Category, User
from ..extensions import db

categories_bp = Blueprint("categories", __name__)

@categories_bp.route("/", methods=["GET"])
def list_categories():
    """Retorna categorias padrão + do usuário"""
    data = request.json or {}
    print("data", data)
    user_id = data.get("user_id")
    globals_q = Category.query.filter(Category.user_id == None).all()
    user_q = Category.query.filter_by(user_id=user_id).all()
    result = [c.to_dict() for c in globals_q + user_q]
    return jsonify(result)

@categories_bp.route("/", methods=["POST"])
def create_category():
    data = request.json or {}
    name = data.get("name")
    tipo = data.get("type", "gasto")
    user_id = data.get("user_id")
    if not name:
        return {"msg": "name é obrigatório"}, 400

    exists = Category.query.filter_by(user_id=user_id, name=name, type=tipo).first()
    if exists:
        return {"msg": "Categoria já existe para este usuário"}, 400

    c = Category(name=name, type=tipo, user_id=user_id)
    db.session.add(c)
    db.session.commit()
    return c.to_dict(), 201

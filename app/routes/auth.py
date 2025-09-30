from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import User

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json or {}
    print("data", data)
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    if not (name and email and password):
        return {"msg": "name, email e password são obrigatórios"}, 400
    if User.query.filter_by(email=email).first():
        return {"msg": "Usuário já existe"}, 400
    u = User(name=name, email=email)
    u.set_password(password)
    db.session.add(u)
    db.session.commit()
    return {"msg": "Usuário criado", "user": u.to_dict()}, 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")
    if not (email and password):
        return {"msg": "email e password são obrigatórios"}, 400
    u = User.query.filter_by(email=email).first()
    if not u or not u.check_password(password):
        return {"msg": "Credenciais inválidas"}, 401
    return {"user": u.to_dict()}

@auth_bp.route("/me", methods=["GET"])
def me():
    data = request.json or {}
    user_id = data.get("user_id")
    u = User.query.get(user_id)
    return {"user": u.to_dict()}
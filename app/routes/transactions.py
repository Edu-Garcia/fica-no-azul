from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Transaction, User, Category
from datetime import datetime

transactions_bp = Blueprint("transactions", __name__)

@transactions_bp.route("/", methods=["POST"])
def add_transaction():
    data = request.json or {}
    user_id = data.get("user_id")
    amount = data.get("amount")
    ttype = data.get("type")
    category_id = data.get("category_id")
    description = data.get("description", "")
    if amount is None or ttype not in ("entrada", "saida"):
        return {"msg": "amount e type (entrada/saida) obrigatórios"}, 400

    # Optional: verify category belongs to user or is global
    if category_id:
        cat = Category.query.get(category_id)
        if not cat:
            return {"msg": "Categoria não encontrada"}, 404

    t = Transaction(user_id=user_id, amount=float(amount), type=ttype,
                    category_id=category_id, description=description, date=datetime.utcnow())
    db.session.add(t)
    db.session.commit()
    return t.to_dict(), 201

@transactions_bp.route("/", methods=["GET"])
def list_transactions():
    data = request.json or {}
    user_id = data.get("user_id")
    # filtros opcionais: start_date, end_date, category_id, type
    q = Transaction.query.filter_by(user_id=user_id).order_by(Transaction.date.desc())
    results = [t.to_dict() for t in q.limit(500).all()]
    return jsonify(results)

@transactions_bp.route("/<int:tx_id>/undo", methods=["POST"])
def undo_transaction(tx_id):
    data = request.json or {}
    user_id = data.get("user_id")
    t = Transaction.query.get(tx_id)
    if not t or t.user_id != user_id:
        return {"msg": "Transacao nao encontrada"}, 404
    if t.reversed:
        return {"msg": "Transacao ja estornada"}, 400
    rev = t.create_reversal()
    db.session.add(rev)
    db.session.commit()
    return {"msg": "Transacao estornada", "reversal": rev.to_dict()}
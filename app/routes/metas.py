from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Meta, Investment, Category, User
from datetime import datetime

metas_bp = Blueprint("metas", __name__)

@metas_bp.route("/", methods=["POST"])
def create_meta():
    data = request.json or {}
    user_id = data.get("user_id")
    description = data.get("description")
    target_amount = data.get("target_amount")
    deadline = data.get("deadline")  # ISO date string optional
    kind = data.get("kind", "caixinha")  # caixinha ou investimento
    investment_id = data.get("investment_id")

    if not description or target_amount is None:
        return {"msg": "description e target_amount obrigatorios"}, 400

    inst_id = None
    if kind == "investimento":
        if not investment_id:
            return {"msg": "investment_id obrigatorio para metas do tipo investimento"}, 400
        inst = Investment.query.get(investment_id)
        if not inst:
            return {"msg": "investment_id invalido"}, 404
        inst_id = investment_id

    deadline_date = None
    if deadline:
        try:
            deadline_date = datetime.fromisoformat(deadline).date()
        except Exception:
            return {"msg": "deadline formato invalido. Use YYYY-MM-DD"}, 400

    m = Meta(user_id=user_id, description=description, target_amount=float(target_amount),
             deadline=deadline_date, kind=kind, investment_id=inst_id)
    db.session.add(m)
    db.session.commit()
    return m.to_dict(), 201

@metas_bp.route("/", methods=["GET"])
def list_metas():
    data = request.json or {}
    user_id = data.get("user_id")
    metas = Meta.query.filter_by(user_id=user_id).all()
    return jsonify([m.to_dict() for m in metas])

@metas_bp.route("/<int:meta_id>/deposit", methods=["POST"])
def deposit_to_meta(meta_id):
    user_id = data.get("user_id")
    data = request.json or {}
    amount = data.get("amount")
    if amount is None:
        return {"msg": "amount obrigatorio"}, 400
    m = Meta.query.get(meta_id)
    if not m or m.user_id != user_id:
        return {"msg": "Meta nao encontrada"}, 404

    if m.kind == "caixinha":
        m.deposit(float(amount))
        db.session.commit()
        return m.to_dict()
    else:
        # para metas de investimento, precisa fornecer meses
        months = int(data.get("months", 0))
        if months <= 0:
            return {"msg": "months obrigatorio e > 0 para aplicar em investimento"}, 400
        applied = m.apply_investment(float(amount), months)
        db.session.commit()
        return {"meta": m.to_dict(), "applied_result": applied}

@metas_bp.route("/<int:meta_id>/progress", methods=["GET"])
def meta_progress(meta_id):
    data = request.json or {}
    user_id = data.get("user_id")
    m = Meta.query.get(meta_id)
    if not m or m.user_id != user_id:
        return {"msg": "Meta nao encontrada"}, 404
    return {"progress": m.progress(), "meta": m.to_dict()}
from flask import Blueprint, request, jsonify
from ..extensions import db
from ..models import Investment

investments_bp = Blueprint("investments", __name__)

@investments_bp.route("/", methods=["GET"])
def list_investments():
    invs = Investment.query.all()
    return jsonify([i.to_dict() for i in invs])

@investments_bp.route("/simulate", methods=["POST"])
def simulate():
    data = request.json or {}
    inv_id = data.get("investment_id")
    value = data.get("value")
    months = int(data.get("months", 0))
    if not inv_id or value is None:
        return {"msg": "investment_id e value obrigatorios"}, 400
    i = Investment.query.get(inv_id)
    if not i:
        return {"msg": "Investment not found"}, 404
    result = i.simulate(float(value), months)
    return {"result": result, "investment": i.to_dict()}
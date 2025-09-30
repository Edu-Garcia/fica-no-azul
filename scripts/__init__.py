"""
Seed script: populates default categories and investments.
Run: FLASK_APP=run.py flask shell
> from scripts.init_db import seed; seed()
or run as python scripts/init_db.py (with proper env)
"""
from app import create_app
from app.extensions import db
from app.models import Category, Investment, User
import os

def seed():
    app = create_app()
    with app.app_context():
        # create tables
        db.create_all()

        # default categories (global = user_id NULL)
        defaults = [
            ("Alimentação", "gasto"),
            ("Transporte", "gasto"),
            ("Moradia", "gasto"),
            ("Lazer", "gasto"),
            ("Saúde", "gasto"),
            ("Salário", "entrada"),
            ("Freelance", "entrada")
        ]
        for name, tipo in defaults:
            if not Category.query.filter_by(name=name, user_id=None).first():
                db.session.add(Category(name=name, type=tipo, user_id=None))

        # default investments
        invs = [
            ("Poupança", 0.005, "baixo"),
            ("CDB", 0.01, "medio"),
            ("Ações", 0.03, "alto")
        ]
        for name, rate, risk in invs:
            if not Investment.query.filter_by(name=name).first():
                db.session.add(Investment(name=name, monthly_rate=rate, risk=risk))

        # optional: create demo user
        if not User.query.filter_by(email="demo@local").first():
            u = User(name="Demo", email="demo@local")
            u.set_password("demo123")
            db.session.add(u)

        db.session.commit()
        print("Seed completed.")

if __name__ == "__main__":
    seed()
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
from sqlalchemy.orm import relationship

# Association note: Category.user_id NULL == global/padrão

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    profile = db.Column(db.String(20), default="moderado")  # conservador/moderado/arrojado

    categories = relationship("Category", backref="owner", lazy="dynamic")  # user-specific categories
    transactions = relationship("Transaction", backref="user", lazy="dynamic")
    metas = relationship("Meta", backref="user", lazy="dynamic")

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def balance(self) -> float:
        # calcula saldo baseando-se nas transações (inclui estornos e reversões)
        total = 0.0
        for t in self.transactions.filter_by(is_reversal=False).all():
            if t.type == "entrada":
                total += t.amount
            else:
                total -= t.amount
        # Note: reversals are stored as transactions too; is_reversal=True mark them as reversal transactions
        # The above line ignores original transactions being reversed — we mark original.reversed=True when reversing.
        return total

    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email, "profile": self.profile}


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    type = db.Column(db.String(20), default="gasto")  # gasto ou entrada
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)  # null -> global

    def to_dict(self):
        return {"id": self.id, "name": self.name, "type": self.type, "user_id": self.user_id}


class Transaction(db.Model):
    __tablename__ = "transactions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'entrada' ou 'saida'
    category_id = db.Column(db.Integer, db.ForeignKey("categories.id"), nullable=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.String(256), nullable=True)
    reversed = db.Column(db.Boolean, default=False)  # original transaction flag
    is_reversal = db.Column(db.Boolean, default=False)  # if this transaction is a reversal transaction
    reversal_of_id = db.Column(db.Integer, db.ForeignKey("transactions.id"), nullable=True)

    category = relationship("Category", foreign_keys=[category_id])

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "amount": self.amount,
            "type": self.type,
            "category": self.category.name if self.category else None,
            "category_id": self.category_id,
            "date": self.date.isoformat(),
            "description": self.description,
            "reversed": self.reversed,
            "is_reversal": self.is_reversal,
            "reversal_of_id": self.reversal_of_id
        }

    def create_reversal(self):
        if self.reversed:
            raise ValueError("Transação já foi estornada.")
        # cria transação inversa
        inverse_type = "entrada" if self.type == "saida" else "saida"
        rev = Transaction(
            user_id=self.user_id,
            amount=self.amount,
            type=inverse_type,
            category_id=self.category_id,
            description=f"Estorno de transação {self.id}",
            is_reversal=True,
            reversal_of_id=self.id
        )
        # marca original como reversa (reversed True)
        self.reversed = True
        return rev


class Investment(db.Model):
    __tablename__ = "investments"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    monthly_rate = db.Column(db.Float, nullable=False)  # ex: 0.01 = 1% ao mês
    risk = db.Column(db.String(20), default="medio")  # baixo/medio/alto

    def simulate(self, initial_value: float, months: int) -> float:
        return initial_value * ((1 + self.monthly_rate) ** months)

    def to_dict(self):
        return {"id": self.id, "name": self.name, "monthly_rate": self.monthly_rate, "risk": self.risk}


class Meta(db.Model):
    __tablename__ = "metas"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    target_amount = db.Column(db.Float, nullable=False)
    deadline = db.Column(db.Date, nullable=True)
    current_amount = db.Column(db.Float, default=0.0)
    kind = db.Column(db.String(20), default="caixinha")  # caixinha ou investimento
    investment_id = db.Column(db.Integer, db.ForeignKey("investments.id"), nullable=True)
    months_applied = db.Column(db.Integer, default=0)

    investment = relationship("Investment")

    def deposit(self, amount: float):
        self.current_amount += amount

    def apply_investment(self, amount: float, months: int):
        if not self.investment:
            raise ValueError("Meta não possui investimento associado.")
        result = self.investment.simulate(amount, months)
        self.current_amount += result
        self.months_applied += months
        return result

    def progress(self):
        if self.target_amount <= 0:
            return 0.0
        return min(100.0, (self.current_amount / self.target_amount) * 100.0)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "description": self.description,
            "target_amount": self.target_amount,
            "deadline": self.deadline.isoformat() if self.deadline else None,
            "current_amount": self.current_amount,
            "kind": self.kind,
            "investment": self.investment.to_dict() if self.investment else None,
            "months_applied": self.months_applied,
            "progress": self.progress()
        }

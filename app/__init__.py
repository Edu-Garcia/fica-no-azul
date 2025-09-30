from flask import Flask
from .config import Config
from .extensions import db, migrate, cors
from .routes.categories import categories_bp
from .routes.transactions import transactions_bp
from .routes.metas import metas_bp
from .routes.investments import investments_bp
from .routes.auth import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cors.init_app(app)

    # register blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(categories_bp, url_prefix="/categories")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(metas_bp, url_prefix="/metas")
    app.register_blueprint(investments_bp, url_prefix="/investments")

    @app.get("/")
    def index():
        return {"msg": "Dashboard Financeiro API - OK"}

    return app
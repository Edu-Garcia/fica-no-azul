# Dashboard Financeiro (Backend) - Flask + SQLite

API em Flask para um projeto de disciplina POO: dashboard financeiro com suporte a
- usuários (registro / login)
- transações (entrada / saída) com estorno/reversão (mantendo histórico)
- categorias (padrão global + categorias individuais por usuário)
- metas financeiras (caixinha ou vinculada a investimento)
- investimentos e simulações
- recomendações de investimento por perfil (conservador, moderado, arrojado)

---

## Requisitos
- Python 3.9+
- pip
- (opcional) virtualenv

---

## Instalação (local)

1. Clone o repositório:
```bash
git clone <repo-url> dashboard_financeiro
cd dashboard_financeiro


Crie e ative um virtualenv (recomendado):

python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows (Powershell)
.\\.venv\\Scripts\\Activate


Instale dependências:

pip install -r requirements.txt


Config (opcional)

Você pode setar variáveis de ambiente: DATABASE_URL, SECRET_KEY.

Por padrão será criado dashboard.db no diretório raiz.

Criar banco e rodar seed:

Usando Flask-Migrate:

export FLASK_APP=run.py
flask db init           # somente na primeira vez
flask db migrate -m "Initial"
flask db upgrade


Alternativa rápida (sem migrations):

python -c "from app import create_app; app=create_app(); from app.extensions import db; \
with app.app_context(): db.create_all()"


Popular dados iniciais (categorias padrão, investimentos, demo user):

python scripts/init_db.py
# ou via shell:
# FLASK_APP=run.py flask shell
# from scripts.init_db import seed; seed()


Rodar a API:
python run.py

A API estará em http://127.0.0.1:5000/.

Endpoints principais (resumo)
POST /auth/register - {name,email,password}
POST /auth/login - {email, password} -> {access_token}
GET /auth/me - (JWT) retorna dados do usuário
GET /categories/ - lista categorias (globais + do usuário)
POST /categories/ - cria categoria do usuário
POST /transactions/ - cria transação {amount,type,category_id,description}
GET /transactions/ - lista transações do usuário
POST /transactions/<id>/undo - estorna transação
GET /investments/ - lista investimentos
POST /investments/simulate - {investment_id, value, months}
POST /metas/ - cria meta {description,target_amount,deadline,kind,investment_id?}
GET /metas/ - lista metas do usuário
POST /metas/<id>/deposit - {amount, months?}
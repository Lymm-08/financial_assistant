from src.models.db import init_db

db_uri = "postgresql://postgres:nina2024@localhost:5432/bot_financeiro"

try:
    db = init_db(db_uri)
    print("Conexão OK, tabelas criadas!")
except Exception as e:
    print(f"Erro ao conectar/criar tabelas: {e}")

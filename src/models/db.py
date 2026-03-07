# ==========================
# ARQUIVO: src/models/db.py
# CONFIGURAÇÃO E MODELOS DO BANCO DE DADOS
# Suporta: SQLite, PostgreSQL, MySQL
# ==========================

# ==========================
# IMPORTAÇÕES
# ==========================

from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# ==========================
# CONFIGURAÇÃO BASE DO SQLALCHEMY
# ==========================

Base = declarative_base()

# ==========================
# MODELOS DE DADOS
# ==========================

# ==========================
# MODELO: ENTRY (LANÇAMENTOS)
# ==========================

class Entry(Base):
    __tablename__ = 'entries'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False)
    type = Column(String(20))  # 'despesa' ou 'receita'
    amount = Column(Float, nullable=False)
    category = Column(String(100))
    description = Column(String(500))
    date = Column(DateTime, default=datetime.now)
    is_encrypted = Column(Boolean, default=False)

    def __repr__(self):
        return f'<Entry {self.id}: {self.type} R${self.amount} - {self.category}>'

# ==========================
# MODELO: BANK (SALDO DO USUÁRIO)
# ==========================

class Bank(Base):
    __tablename__ = 'banks'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, unique=True)
    total_balance = Column(Float, default=0)
    currency = Column(String(10), default='BRL')
    last_updated = Column(DateTime, default=datetime.now)
    last_month = Column(Integer, default=0)  # Para controlar reset mensal

    def __repr__(self):
        return f'<Bank {self.user_id}: R${self.total_balance}>'

# ==========================
# FUNÇÕES DE INICIALIZAÇÃO
# ==========================

# ==========================
# INICIALIZAÇÃO DO BANCO DE DADOS
# ==========================

def init_db(db_uri='postgresql://postgres:nina2024@localhost:5432/bot_financeiro'):
    """
    Inicializa o banco de dados PostgreSQL

    Exemplos de URIs suportadas:
    - PostgreSQL: postgresql://user:password@localhost/dbname
    - PostgreSQL (local): postgresql://postgres:senha@localhost:5432/bot_financeiro
    - SQLite: sqlite:///bot_financeiro.db
    - MySQL: mysql://user:password@localhost/dbname
    """
    print(f'Conectando ao banco: {db_uri}')

    # SUBSEÇÃO: Criar engine do SQLAlchemy
    engine = create_engine(db_uri, echo=False)

    # SUBSEÇÃO: Criar todas as tabelas definidas nos modelos
    Base.metadata.create_all(engine)

    # SUBSEÇÃO: Criar factory de sessões
    Session = sessionmaker(bind=engine)

    print('Banco de dados inicializado com sucesso')

    return {
        'engine': engine,
        'Session': Session,
        'Entry': Entry,
        'Bank': Bank,
    }

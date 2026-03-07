# ==========================
# ARQUIVO: src/models/db.py
# CONFIGURAÇÃO E MODELO DO BANCO DE DADOS
# Suporta: SQLite, PostgreSQL, MySQL
# ==========================

from datetime import datetime
from sqlalchemy import create_engine, Column, String, Float, DateTime, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# ============ MODELO DE LANÇAMENTO ============
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

# ============ MODELO DE BANCO ============
class Bank(Base):
    __tablename__ = 'banks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), nullable=False, unique=True)
    total_balance = Column(Float, default=0)
    currency = Column(String(10), default='BRL')
    last_updated = Column(DateTime, default=datetime.now)
    last_month = Column(Integer, default=0)
    
    def __repr__(self):
        return f'<Bank {self.user_id}: R${self.total_balance}>'

# ============ FUNÇÃO PARA INICIALIZAR DB ============
def init_db(db_uri='postgresql://postgres:nina2024@localhost:5432/bot_financeiro'):
    """
    Inicializa o banco de dados PostgreSQL
    
    Exemplo de URIs:
    - PostgreSQL: postgresql://user:password@localhost/dbname
    - PostgreSQL (local): postgresql://postgres:senha@localhost:5432/bot_financeiro
    """
    print(f'Conectando ao banco: {db_uri}')
    
    # Criar engine
    engine = create_engine(db_uri, echo=False)
    
    # Criar tabelas
    Base.metadata.create_all(engine)
    
    # Criar session factory
    Session = sessionmaker(bind=engine)
    
    print('Banco de dados inicializado')
    
    return {
        'engine': engine,
        'Session': Session,
        'Entry': Entry,
        'Bank': Bank,
    }

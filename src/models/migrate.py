# ==========================
# ARQUIVO: src/models/migrate.py
# SCRIPT DE MIGRAÇÃO DO BANCO DE DADOS
# ==========================

from sqlalchemy import text, inspect
from datetime import datetime

def migrate_db(engine):
    """Executa migrações necessárias no banco de dados"""
    
    inspector = inspect(engine)
    
    # Verificar se a tabela 'banks' existe
    if 'banks' not in inspector.get_table_names():
        print("ℹ️ Tabela 'banks' não existe - será criada automaticamente")
        return True
    
    # Obter colunas da tabela 'banks'
    columns = {col['name'] for col in inspector.get_columns('banks')}
    
    # Lista de migrações necessárias
    migrações = [
        {
            'nome': 'Adicionar coluna last_month',
            'coluna': 'last_month',
            'sql': "ALTER TABLE banks ADD COLUMN last_month INTEGER DEFAULT 0",
            'verificar': lambda cols: 'last_month' not in cols
        }
    ]
    
    # Executar migrações
    with engine.connect() as conn:
        for migracao in migrações:
            if migracao['verificar'](columns):
                try:
                    print(f"🔄 Executando: {migracao['nome']}...")
                    conn.execute(text(migracao['sql']))
                    conn.commit()
                    print(f"✅ {migracao['nome']} concluído!")
                    columns.add(migracao['coluna'])
                except Exception as e:
                    print(f"⚠️ Erro ao executar {migracao['nome']}: {e}")
                    # Alguns bancos podem dar erro se a coluna já existe
                    if 'already exists' in str(e) or 'duplicate' in str(e).lower():
                        print(f"ℹ️ Coluna já existe, continuando...")
                    else:
                        raise
            else:
                print(f"✓ {migracao['nome']} já existe")
    
    print("✅ Migrações concluídas com sucesso!")
    return True

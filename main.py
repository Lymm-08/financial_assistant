# ==========================
# ARQUIVO: main.py
# PONTO DE ENTRADA DO BOT FINANCEIRO (VERSAO MODULAR)
# ==========================

import os
import sys
from dotenv import load_dotenv

# Carregar variaveis de ambiente
load_dotenv()

# Importar modulos
from src.config.config import config
from src.models.db import init_db

# ============ VALIDACAO DE TOKEN ============
if not config.get('BOT_TOKEN'):
    print('ERRO: Por favor defina a variavel BOT_TOKEN no arquivo .env')
    sys.exit(1)

# ============ INICIALIZAR BANCO DE DADOS ============
try:
    db_config = init_db(config.get('DB_URI', 'postgresql://postgres:nina2024@localhost:5432/bot_financeiro'))
    print('Banco PostgreSQL inicializado com sucesso')
except Exception as e:
    print(f'ERRO ao inicializar banco: {e}')
    sys.exit(1)

# ============ IMPORTAR BOT TELEGRAM ============
try:
    from telegram.ext import Application
    from src.commands.handlers import register_commands
except ImportError as e:
    print(f'ERRO: Dependencia faltando - {e}')
    print('Execute: pip install -r requirements.txt')
    sys.exit(1)

# ============ FUNCAO PRINCIPAL ============
def main():
    try:
        # Criar aplicacao
        app = Application.builder().token(config.get('BOT_TOKEN')).build()
        
        # Registrar comandos
        register_commands(app, db_config)
        
        # Iniciar bot
        print('Bot Financeiro iniciado!')
        print(f'Banco de dados: {config.get("DB_URI", "SQLite")}')
        print('Pronto para receber mensagens...')
        print('(Pressione Ctrl+C para parar)')
        
        from telegram import Update
        app.run_polling(allowed_updates=Update.ALL_TYPES)
    except KeyboardInterrupt:
        print('\nBot parado pelo usuario')
    except Exception as e:
        print(f'ERRO ao iniciar bot: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()

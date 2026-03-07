# ==========================
# ARQUIVO: main.py
# PONTO DE ENTRADA DO BOT FINANCEIRO (VERSÃO MODULAR)
# ==========================

# ==========================
# IMPORTAÇÕES E CONFIGURAÇÃO INICIAL
# ==========================

import os
import sys
from dotenv import load_dotenv

# SUBSEÇÃO: Carregar variáveis de ambiente
load_dotenv()

# SUBSEÇÃO: Importar módulos do projeto
from src.config.config import config
from src.models.db import init_db

# ==========================
# VALIDAÇÃO DE CONFIGURAÇÕES CRÍTICAS
# ==========================

# SUBSEÇÃO: Validar token do bot
if not config.get('BOT_TOKEN'):
    print('❌ ERRO: Por favor defina a variável BOT_TOKEN no arquivo .env')
    sys.exit(1)

# ==========================
# INICIALIZAÇÃO DO BANCO DE DADOS
# ==========================

# SUBSEÇÃO: Inicializar conexão com banco PostgreSQL
try:
    db_config = init_db(config.get('DB_URI', 'postgresql://postgres:nina2024@localhost:5432/bot_financeiro'))
    print('✅ Banco PostgreSQL inicializado com sucesso')
except Exception as e:
    print(f'❌ ERRO ao inicializar banco: {e}')
    sys.exit(1)

# ==========================
# IMPORTAÇÃO DO BOT TELEGRAM
# ==========================

# SUBSEÇÃO: Importar dependências do Telegram
try:
    from telegram.ext import Application
    from src.commands.handlers import register_commands
except ImportError as e:
    print(f'❌ ERRO: Dependência faltando - {e}')
    print('💡 Execute: pip install -r requirements.txt')
    sys.exit(1)

# ==========================
# FUNÇÃO PRINCIPAL
# ==========================

def main():
    """Função principal que inicializa e executa o bot"""
    try:
        # SUBSEÇÃO: Criar aplicação do Telegram
        app = Application.builder().token(config.get('BOT_TOKEN')).build()

        # SUBSEÇÃO: Registrar todos os comandos do bot
        register_commands(app, db_config)

        # SUBSEÇÃO: Iniciar bot com polling
        print('🚀 Bot Financeiro iniciado!')
        print(f'📊 Banco de dados: {config.get("DB_URI", "SQLite")}')
        print('📱 Pronto para receber mensagens...')
        print('(Pressione Ctrl+C para parar)')

        from telegram import Update
        app.run_polling(allowed_updates=Update.ALL_TYPES)

    except KeyboardInterrupt:
        print('\n⏹️  Bot parado pelo usuário')
    except Exception as e:
        print(f'❌ ERRO ao iniciar bot: {e}')
        import traceback
        traceback.print_exc()
        sys.exit(1)

# ==========================
# EXECUÇÃO DO PROGRAMA
# ==========================

if __name__ == '__main__':
    main()

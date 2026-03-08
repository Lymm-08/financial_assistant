# ==========================
# ARQUIVO: main.py
# PONTO DE ENTRADA DO BOT FINANCEIRO (VERSÃO MODULAR)
# ==========================

# ==========================
# IMPORTAÇÕES E CONFIGURAÇÃO INICIAL
# ==========================

import os
import sys
import subprocess
from dotenv import load_dotenv

# SUBSEÇÃO: Carregar variáveis de ambiente
load_dotenv()

# SUBSEÇÃO: Importar módulos do projeto
from src.config.config import config
from src.models.db import init_db
from src.models.migrate import migrate_db

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
    
    # SUBSEÇÃO: Executar migrações
    migrate_db(db_config['engine'])
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
# FUNÇÕES AUXILIARES
# ==========================

def kill_existing_python_processes():
    """Tenta matar processos Python existentes para evitar conflitos"""
    try:
        # Usar taskkill para forçar parada de todos os processos python.exe
        result = subprocess.run(['taskkill', '/F', '/IM', 'python.exe', '/T'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print('✅ Processos Python existentes foram terminados')
        else:
            print('ℹ️  Nenhum processo Python encontrado ou não foi possível terminar')
    except Exception as e:
        print(f'⚠️  Não foi possível verificar processos Python: {e}')

# ==========================
# FUNÇÃO PRINCIPAL
# ==========================

def main():
    """Função principal que inicializa e executa o bot"""
    try:
        # SUBSEÇÃO: Tentar parar processos Python existentes
        kill_existing_python_processes()

        # Pequena pausa para garantir que os processos foram terminados
        import time
        time.sleep(2)

        # SUBSEÇÃO: Criar aplicação do Telegram
        app = Application.builder().token(config.get('BOT_TOKEN')).build()

        # SUBSEÇÃO: Registrar todos os comandos do bot
        register_commands(app, db_config)

        # SUBSEÇÃO: Iniciar bot com polling e tratamento de conflitos
        print('🚀 Bot Financeiro iniciado!')
        print(f'📊 Banco de dados: {config.get("DB_URI", "SQLite")}')
        print('📱 Pronto para receber mensagens...')
        print('(Pressione Ctrl+C para parar)')

        from telegram import Update
        from telegram.error import Conflict

        # Tentar iniciar polling com tratamento de conflitos
        max_retries = 3
        retry_count = 0

        while retry_count < max_retries:
            try:
                app.run_polling(allowed_updates=Update.ALL_TYPES)
                break  # Sai do loop se conseguiu iniciar
            except Conflict as e:
                retry_count += 1
                print(f'⚠️  Conflito detectado (tentativa {retry_count}/{max_retries}): {e}')
                if retry_count < max_retries:
                    print('🔄 Aguardando 10 segundos para tentar novamente...')
                    time.sleep(10)
                    # Tentar matar processos novamente
                    kill_existing_python_processes()
                    time.sleep(2)
                else:
                    print('❌ Muitas tentativas falharam. Verifique se há outra instância rodando.')
                    sys.exit(1)
            except Exception as e:
                print(f'❌ ERRO ao iniciar bot: {e}')
                import traceback
                traceback.print_exc()
                sys.exit(1)

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

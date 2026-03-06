# ==========================
# ARQUIVO: src/config/config.py
# CONFIGURAÇÕES DO BOT
# ==========================

import os
from dotenv import load_dotenv
from pathlib import Path

# Carregar arquivo .env
dotenv_path = Path(__file__).parent.parent.parent / '.env'
load_dotenv(dotenv_path)

# IMPORTANTE: Ler valores APENAS do arquivo .env, ignorar variáveis de ambiente do sistema
env_values = {}
if dotenv_path.exists():
    with open(dotenv_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                env_values[key.strip()] = value.strip()

config = {
    'BOT_TOKEN': env_values.get('BOT_TOKEN', ''),
    'DB_URI': env_values.get('DB_URI', 'postgresql://postgres:nina2024@localhost:5432/bot_financeiro'),
    'DEBUG': env_values.get('DEBUG', 'False').lower() == 'true',
    'ENCRYPTION_KEY': env_values.get('ENCRYPTION_KEY', 'default_key_change_me'),
}

# Validação
if not config['BOT_TOKEN']:
    print('Aviso: BOT_TOKEN não configurado no .env')

print(f'Configuracao carregada:')
print(f'   - BOT_TOKEN: {config["BOT_TOKEN"][:10] + "..." if config["BOT_TOKEN"] else "NAO DEFINIDO"}')
print(f'   - DB_URI: {config["DB_URI"]}')
print(f'   - DEBUG: {config["DEBUG"]}')

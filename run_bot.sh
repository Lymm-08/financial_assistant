#!/bin/bash
# ==========================
# ARQUIVO: run_bot.sh
# Script para executar o Bot Financeiro em background
# Plataformas: Linux e macOS
# ==========================

echo "=================================================="
echo "  Bot Financeiro - Inicializando em Background"
echo "=================================================="
echo ""

# Detectar diretório do script
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"

# Verificar se está no diretório correto
if [ ! -f "main.py" ]; then
    echo "❌ ERRO: main.py não encontrado!"
    echo "Por favor, execute este script a partir do diretório raiz do projeto."
    exit 1
fi

# Criar venv se não existir
if [ ! -d ".venv" ]; then
    echo "📦 Criando ambiente virtual..."
    python3 -m venv .venv
    if [ $? -ne 0 ]; then
        echo "❌ ERRO ao criar venv!"
        exit 1
    fi
fi

# Ativar venv
echo "🔄 Ativando ambiente virtual..."
source .venv/bin/activate

# Instalar dependências
echo "📦 Verificando dependências..."
pip install -q -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ ERRO ao instalar dependências!"
    exit 1
fi

# Executar bot em background
echo ""
echo "🚀 Iniciando Bot Financeiro em background..."
echo ""

# Executar em background com nohup
nohup python main.py > bot_financeiro.log 2>&1 &
BOT_PID=$!

echo "✅ Bot iniciado em background!"
echo "📊 Process ID: $BOT_PID"
echo ""
echo "💡 PRÓXIMOS PASSOS:"
echo "   1. Abra seu Telegram"
echo "   2. Procure por seu bot"
echo "   3. Envie /start"
echo ""
echo "📋 Para verificar se está rodando:"
echo "   • Use: ps aux | grep main.py"
echo "   • Ou: pgrep -f 'main.py'"
echo "   • Ou: jobs -l"
echo ""
echo "📋 Ver logs em tempo real:"
echo "   • Use: tail -f bot_financeiro.log"
echo ""
echo "⏹️  Para parar o bot:"
echo "   • Use: pkill -f 'main.py'"
echo "   • Ou: kill $BOT_PID"
echo "   • Ou: kill %1 (se for job)"
echo ""

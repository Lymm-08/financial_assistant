# ==========================
# ARQUIVO: src/commands/handlers.py
# REGISTRADOR DE COMANDOS DO BOT
# ==========================

from telegram import Update
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
from datetime import datetime, timedelta
import re
from functools import partial

from src.ai.categorizer import categorize
from src.utils.formatter import format_money, format_date
from src.services.reports import generate_report

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /iniciar - Menu principal"""
    user = update.effective_user
    text = f"""
🤖 Bot Financeiro - Olá, {user.first_name}!

💰 O que você pode fazer:
• Registrar despesas/receitas digitando valores
• Gerar relatórios financeiros
• Acompanhar seu saldo automaticamente

📝 Como usar:
Digite mensagens como:
"50 pizza" ou "R$ 25 transporte"
"salario 3000" (para receitas)

📊 Comandos disponíveis:
/relatorio simples - Resumo geral
/relatorio completo - Detalhes completos  
/relatorio semanal - Últimos 7 dias
/relatorio mensal - Últimos 30 dias

💡 Dica: Qualquer mensagem com valor + descrição é registrada automaticamente!
"""
    await update.message.reply_text(text)

async def cmd_relatorio(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Comando /relatorio [tipo] - Gerar relatorios"""
    args = context.args
    user_id = str(update.effective_user.id)
    
    tipo = args[0].lower() if args else 'simples'
    
    # Gerar relatorio
    relatorio = generate_report(user_id, tipo, db)
    
    await update.message.reply_text(relatorio)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, db):

    """Processa mensagens para registrar gastos/receitas"""

    text = update.message.text
    user_id = str(update.effective_user.id)
    
    # Padrao: "valor descricao" ou "descricao valor"
    match = re.search(r'(\d+(?:[.,]\d{2})?)\s+(.+)|(.+)\s+(\d+(?:[.,]\d{2})?)', text)
    
    if not match:
        return
    
    # Extrair valor e descricao
    if match.group(1):
        valor = float(match.group(1).replace(',', '.'))
        descricao = match.group(2)
    else:
        descricao = match.group(3)
        valor = float(match.group(4).replace(',', '.'))
    
    # Categorizar
    categoria = categorize(descricao)
    
    # Detectar tipo com melhor confiança
    desc_lower = descricao.lower()
    palavras_receita = ['recebi', 'salario', 'bônus', 'ganho', 'renda', 'pagamento', 'depósito', 'bonificação']
    palavras_despesa = ['pago', 'comprei', 'gastei', 'transferência']
    
    eh_receita = any(p in desc_lower for p in palavras_receita)
    eh_despesa = any(p in desc_lower for p in palavras_despesa)
    
    # Se não tiver certeza, pedir confirmação
    if not eh_receita and not eh_despesa:
        mensagem = f"❓ Não consegui identificar se é despesa ou receita.\n\n💰 Valor: R$ {valor:.2f}\n📝 Descrição: {descricao}\n\n📌 Responda com:\n/receita - Se é uma entrada de dinheiro\n/despesa - Se é um gasto"
        await update.message.reply_text(mensagem)
        # Salvar contexto para a próxima mensagem
        context.user_data['pending_transaction'] = {
            'valor': valor,
            'descricao': descricao,
            'categoria': categoria,
            'user_id': user_id
        }
        return
    
    tipo = 'receita' if eh_receita else 'despesa'
    
    # Salvar no banco
    try:
        session = db['Session']()
        
        # Criar entrada
        entry = db['Entry'](
            user_id=user_id,
            type=tipo,
            amount=valor,
            category=categoria,
            description=descricao
        )
        session.add(entry)
        
        # Atualizar saldo bancario
        bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
        if not bank:
            bank = db['Bank'](user_id=user_id, total_balance=0)
            session.add(bank)
        
        if tipo == 'receita':
            bank.total_balance += valor
        else:
            bank.total_balance -= valor
        
        session.commit()
        
        # Salvar o saldo ANTES de fechar a sessão
        saldo_atual = bank.total_balance
        session.close()
        
        resposta = f"""
✅ Registrado com sucesso!

💰 Valor: {format_money(valor)}
📂 Categoria: {categoria}
📝 Descrição: {descricao}
🔄 Tipo: {tipo.capitalize()}
📅 Data: {format_date(datetime.now())}
🏦 Saldo Atual: {format_money(saldo_atual)}
"""
    except Exception as e:
        resposta = f"❌ Erro ao salvar: {str(e)}"
    
    await update.message.reply_text(resposta)

async def cmd_confirma_receita(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Confirma que a transação pendente é uma receita"""
    if 'pending_transaction' not in context.user_data:
        await update.message.reply_text("Nenhuma transação pendente de confirmação.")
        return
    
    trans = context.user_data.pop('pending_transaction')
    
    try:
        session = db['Session']()
        entry = db['Entry'](
            user_id=trans['user_id'],
            type='receita',
            amount=trans['valor'],
            category=trans['categoria'],
            description=trans['descricao']
        )
        session.add(entry)
        
        bank = session.query(db['Bank']).filter_by(user_id=trans['user_id']).first()
        if not bank:
            bank = db['Bank'](user_id=trans['user_id'], total_balance=0)
            session.add(bank)
        
        bank.total_balance += trans['valor']
        session.commit()
        saldo = bank.total_balance
        session.close()
        
        resposta = f"✅ Registrado como RECEITA!\n\n💚 +{format_money(trans['valor'])}\n🏦 Saldo: {format_money(saldo)}"
    except Exception as e:
        resposta = f"❌ Erro: {str(e)}"
    
    await update.message.reply_text(resposta)

async def cmd_confirma_despesa(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Confirma que a transação pendente é uma despesa"""
    if 'pending_transaction' not in context.user_data:
        await update.message.reply_text("Nenhuma transação pendente de confirmação.")
        return
    
    trans = context.user_data.pop('pending_transaction')
    
    try:
        session = db['Session']()
        entry = db['Entry'](
            user_id=trans['user_id'],
            type='despesa',
            amount=trans['valor'],
            category=trans['categoria'],
            description=trans['descricao']
        )
        session.add(entry)
        
        bank = session.query(db['Bank']).filter_by(user_id=trans['user_id']).first()
        if not bank:
            bank = db['Bank'](user_id=trans['user_id'], total_balance=0)
            session.add(bank)
        
        bank.total_balance -= trans['valor']
        session.commit()
        saldo = bank.total_balance
        session.close()
        
        resposta = f"✅ Registrado como DESPESA!\n\n❤️ -{format_money(trans['valor'])}\n🏦 Saldo: {format_money(saldo)}"
    except Exception as e:
        resposta = f"❌ Erro: {str(e)}"
    
    await update.message.reply_text(resposta)

def register_commands(app, db):
    """Registra todos os comandos e handlers no bot"""
    
    # Comandos
    app.add_handler(CommandHandler('start', cmd_start))
    app.add_handler(CommandHandler('iniciar', cmd_start))
    app.add_handler(CommandHandler('relatorio', partial(cmd_relatorio, db=db)))
    app.add_handler(CommandHandler('receita', partial(cmd_confirma_receita, db=db)))
    app.add_handler(CommandHandler('despesa', partial(cmd_confirma_despesa, db=db)))
    
    # Handler de mensagens
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, partial(handle_message, db=db)))
    
    print('Comandos registrados com sucesso')
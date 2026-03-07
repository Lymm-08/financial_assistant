# ==========================
# IMPORTAÇÕES
# ==========================

from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from functools import partial
from datetime import datetime
import re

from src.ai.categorizer import categorize
from src.utils.formatter import format_money, format_date
from src.services.reports import generate_report


# ==========================
# COMANDO /start e /iniciar
# ==========================

async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Comando /iniciar - Menu principal"""
    user = update.effective_user
    user_id = str(user.id)
    
    # Verificar se é usuário novo
    session = db['Session']()
    entries_count = session.query(db['Entry']).filter_by(user_id=user_id).count()
    bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
    session.close()
    
    is_new_user = entries_count == 0 and (not bank or bank.total_balance == 0)
    
    text = f"""
🤖 Bot Financeiro - Olá, {user.first_name}!

💰 O que você pode fazer:
• Registrar despesas/receitas digitando valores
• Gerar relatórios financeiros
• Acompanhar seu saldo automaticamente
"""

    keyboard = []
    if is_new_user:
        keyboard.append([InlineKeyboardButton("➕ Inserir saldo inicial", callback_data='inserir_saldo')])
    keyboard.append([InlineKeyboardButton("🔄 Reset", callback_data='reset')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text, reply_markup=reply_markup)

# ==========================
# HANDLER DE MENSAGENS LIVRES
# ==========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    text = update.message.text
    user_id = str(update.effective_user.id)

    # Verificar se está esperando saldo inicial
    if 'waiting_saldo' in context.user_data:
        try:
            valor = float(text.replace(',', '.'))
            session = db['Session']()
            bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
            if not bank:
                bank = db['Bank'](user_id=user_id, total_balance=0, last_month=datetime.now().month)
                session.add(bank)
            bank.total_balance = valor
            session.commit()
            session.close()
            del context.user_data['waiting_saldo']
            await update.message.reply_text(f"✅ Saldo inicial definido: {format_money(valor)}")
            return
        except ValueError:
            await update.message.reply_text("❌ Valor inválido. Digite apenas o número do saldo.")
            return

    match = re.search(r'(\d+(?:[.,]\d+)?)\s+(.+)|(.+)\s+(\d+(?:[.,]\d+)?)', text)
    if not match:
        return

    if match.group(1):
        valor = float(match.group(1).replace(',', '.'))
        descricao = match.group(2)
    else:
        descricao = match.group(3)
        valor = float(match.group(4).replace(',', '.'))

    categoria = categorize(descricao)

    desc_lower = descricao.lower()
    palavras_receita = ['recebi', 'salario', 'bônus', 'ganho', 'renda', 'pagamento', 'depósito', 'bonificação', 'salário', 'prêmio', 'reembolso', 'devolução', 'receita', 'entrada']
    palavras_despesa = ['pago', 'comprei', 'gastei', 'transferência', 'gasto', 'paguei', 'transferi', 'saque', 'débito', 'crédito', 'despesa', 'saída']

    eh_receita = any(p in desc_lower for p in palavras_receita)
    eh_despesa = any(p in desc_lower for p in palavras_despesa)

    if not eh_receita and not eh_despesa and categoria == 'Outros':
        mensagem = f"❓ Não consegui identificar se é despesa ou receita.\n\n💰 Valor: R$ {valor:.2f}\n📝 Descrição: {descricao}\n\n📌 Responda com:\n/receita ou /despesa"
        await update.message.reply_text(mensagem)
        context.user_data['pending_transaction'] = {
            'valor': valor,
            'descricao': descricao,
            'categoria': categoria,
            'user_id': user_id
        }
        return

    tipo = 'receita' if eh_receita else 'despesa'
    
    # Verificar mudança de mês
    session = db['Session']()
    current_month = datetime.now().month
    bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
    if bank and bank.last_month != 0 and bank.last_month != current_month:
        # Zerar transações do mês anterior
        session.query(db['Entry']).filter_by(user_id=user_id).delete()
        bank.last_month = current_month
        session.commit()
    
    # Salvar no banco
    try:
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
        if not bank:
            bank = db['Bank'](user_id=user_id, total_balance=0, last_month=current_month)
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

# ==========================
# CONFIRMAÇÕES DE TRANSAÇÕES
# ==========================

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

# ==========================
# NOVOS COMANDOS ADICIONADOS
# ==========================

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
    
# ==========================
# COMANDO /reset
# ==========================

async def cmd_reset(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Reseta todas as transações e saldo do usuário"""
    user_id = str(update.effective_user.id)

    try:
        session = db['Session']()

        # Apagar todas as transações do usuário
        session.query(db['Entry']).filter_by(user_id=user_id).delete()

        # Resetar saldo bancário
        bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
        if bank:
            bank.total_balance = 0

        session.commit()
        session.close()

        resposta = "🔄 Reset realizado!\nTodas as transações foram apagadas e o saldo voltou para R$ 0,00."
    except Exception as e:
        resposta = f"❌ Erro ao resetar: {str(e)}"

    await update.message.reply_text(resposta)

# ==========================
# COMANDO /ajustar_saldo
# ==========================

async def cmd_ajustar_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Ajusta manualmente o saldo do usuário"""
    user_id = str(update.effective_user.id)
    args = context.args

    if not args:
        await update.message.reply_text("⚠️ Use assim: /ajustar_saldo 1000")
        return

    try:
        novo_saldo = float(args[0].replace(',', '.'))
        session = db['Session']()

        bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
        if not bank:
            bank = db['Bank'](user_id=user_id, total_balance=0)
            session.add(bank)

        bank.total_balance = novo_saldo
        session.commit()
        session.close()

        resposta = f"✅ Saldo ajustado!\n🏦 Novo saldo: R$ {novo_saldo:.2f}"
    except Exception as e:
        resposta = f"❌ Erro ao ajustar saldo: {str(e)}"

    await update.message.reply_text(resposta)

# ==========================
# COMANDO /relatorio
# ==========================

async def cmd_relatorio(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Gera relatório financeiro"""
    user_id = str(update.effective_user.id)
    report = generate_report(user_id, db=db)
    await update.message.reply_text(report)

# ==========================
# HANDLER DE CALLBACKS
# ==========================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    query = update.callback_query
    await query.answer()
    data = query.data
    user_id = str(update.effective_user.id)

    if data == 'reset':
        # Chamar reset
        try:
            session = db['Session']()
            session.query(db['Entry']).filter_by(user_id=user_id).delete()
            bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
            if bank:
                bank.total_balance = 0
            session.commit()
            session.close()
            resposta = "🔄 Reset realizado!\nTodas as transações foram apagadas e o saldo voltou para R$ 0,00."
        except Exception as e:
            resposta = f"❌ Erro ao resetar: {str(e)}"
        await query.edit_message_text(resposta)
    
    elif data == 'inserir_saldo':
        context.user_data['waiting_saldo'] = True
        await query.edit_message_text("Digite o valor do seu saldo inicial (ex: 1000 ou 1000,50):")

def register_commands(app, db):
    """Registra todos os comandos e handlers no bot"""
    
    # Comandos
    app.add_handler(CommandHandler('start', partial(cmd_start, db=db)))
    app.add_handler(CommandHandler('iniciar', partial(cmd_start, db=db)))
    app.add_handler(CommandHandler('relatorio', partial(cmd_relatorio, db=db)))
    app.add_handler(CommandHandler('receita', partial(cmd_confirma_receita, db=db)))
    app.add_handler(CommandHandler('despesa', partial(cmd_confirma_despesa, db=db)))
    app.add_handler(CommandHandler('reset', partial(cmd_reset, db=db)))              # <-- novo
    app.add_handler(CommandHandler('ajustar_saldo', partial(cmd_ajustar_saldo, db=db)))  # <-- novo
    
    # Callbacks
    app.add_handler(CallbackQueryHandler(partial(handle_callback, db=db)))
    
    # Handler de mensagens
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, partial(handle_message, db=db)))
    
    print('Comandos registrados com sucesso')

    
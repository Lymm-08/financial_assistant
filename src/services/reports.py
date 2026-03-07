# ==========================
# ARQUIVO: src/services/reports.py
# GERACAO DE RELATORIOS
# ==========================

from datetime import datetime, timedelta
from sqlalchemy import func
from src.utils.formatter import format_money, format_date

def generate_report(user_id, report_type='simples', db=None):
    """
    Gera relatorio financeiro
    
    Tipos disponiveis:
    - simples: resumo rapido
    - completo: detalhes completos
    - semanal: ultimos 7 dias
    - mensal: ultimos 30 dias
    """
    
    if not db:
        return "❌ Erro: Banco de dados não configurado"
    
    if report_type == 'simples':
        return generate_simple_report(user_id, db)
    elif report_type == 'completo':
        return generate_detailed_report(user_id, db)
    elif report_type == 'semanal':
        return generate_weekly_report(user_id, db)
    elif report_type == 'mensal':
        return generate_monthly_report(user_id, db)
    else:
        return generate_simple_report(user_id, db)

def generate_simple_report(user_id, db):
    """Relatorio simples com resumo do mês atual"""
    try:
        session = db['Session']()
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Buscar transacoes do mês atual
        entries = session.query(db['Entry']).filter_by(user_id=user_id).filter(
            db['Entry'].date >= datetime(current_year, current_month, 1)
        ).all()
        
        # Calcular totais do mês
        receitas = sum(e.amount for e in entries if e.type == 'receita')
        despesas = sum(e.amount for e in entries if e.type == 'despesa')
        
        # Buscar saldo bancario atual
        bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
        saldo_banco = bank.total_balance if bank else 0
        
        session.close()
        
        # calcular porcentagem de economia (savings)
        economia = receitas - despesas
        if receitas > 0:
            pct = economia / receitas * 100
        else:
            pct = 0.0
        
        report = f"""


📊 RELATÓRIO SIMPLES (MÊS ATUAL)

👤 Usuário: {user_id}
📅 Mês Atual: {datetime.now().strftime('%B %Y')}
💰 Saldo Atual: {format_money(saldo_banco)}
💚 Receitas do Mês: {format_money(receitas)}
❤️ Despesas do Mês: {format_money(despesas)}
💡 Economia: ({pct:.1f}% das receitas)

📈 Transações Este Mês: {len(entries)}
"""
        return report
        return report
    except Exception as e:
        return f"❌ Erro ao gerar relatório: {str(e)}"

def generate_detailed_report(user_id, db):
    """Relatorio detalhado com categorias"""
    try:
        session = db['Session']()
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        # Buscar transacoes do mês atual
        entries = session.query(db['Entry']).filter_by(user_id=user_id).filter(
            db['Entry'].date >= datetime(current_year, current_month, 1)
        ).all()
        
        # Calcular totais do mês
        receitas = sum(e.amount for e in entries if e.type == 'receita')
        despesas = sum(e.amount for e in entries if e.type == 'despesa')
        
        # Agrupar por categoria
        categorias = {}
        for e in entries:
            cat = e.category
            if cat not in categorias:
                categorias[cat] = {'receitas': 0, 'despesas': 0, 'count': 0}
            if e.type == 'receita':
                categorias[cat]['receitas'] += e.amount
            else:
                categorias[cat]['despesas'] += e.amount
            categorias[cat]['count'] += 1
        
        # Buscar saldo bancario atual
        bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
        saldo_banco = bank.total_balance if bank else 0
        
        session.close()
        
        # Montar relatorio de categorias
        categorias_text = ""
        for cat, data in sorted(categorias.items()):
            total_cat = data['receitas'] - data['despesas']
            categorias_text += f"📂 {cat}: {format_money(total_cat)} ({data['count']} transações)\n"
        
        if not categorias_text:
            categorias_text = "Nenhuma transação registrada ainda.\n"
        
        # Ultimas 5 transacoes
        ultimas = entries[-5:] if entries else []
        ultimas_text = ""
        for e in reversed(ultimas):
            ultimas_text += f"• {format_date(e.date)}: {e.type} {format_money(e.amount)} - {e.description}\n"
        
        if not ultimas_text:
            ultimas_text = "Nenhuma transação registrada ainda."
        
        # porcentagem de economia
        economia = receitas - despesas
        pct = economia / receitas * 100 if receitas > 0 else 0.0
        
        report = f"""


📊 RELATÓRIO COMPLETO (MÊS ATUAL)

👤 Usuário: {user_id}
📅 Mês Atual: {datetime.now().strftime('%B %Y')}

💰 Saldo Atual: {format_money(saldo_banco)}
💚 Receitas do Mês: {format_money(receitas)}
❤️ Despesas do Mês: {format_money(despesas)}
💡 Economia: ({pct:.1f}% das receitas)

📂 Por Categoria:
{categorias_text}

📝 Últimas Transações:
{ultimas_text}
"""
        return report
    except Exception as e:
        return f"❌ Erro ao gerar relatório: {str(e)}"

def generate_weekly_report(user_id, db):
    """Relatorio dos ultimos 7 dias"""
    try:
        session = db['Session']()
        
        week_ago = datetime.now() - timedelta(days=7)
        
        # Buscar transacoes da semana
        entries = session.query(db['Entry']).filter(
            db['Entry'].user_id == user_id,
            db['Entry'].date >= week_ago
        ).all()
        
        # Calcular totais
        receitas = sum(e.amount for e in entries if e.type == 'receita')
        despesas = sum(e.amount for e in entries if e.type == 'despesa')
        saldo = receitas - despesas
        
        session.close()
        
        report = f"""


📊 RELATÓRIO SEMANAL (Últimos 7 dias)

👤 Usuário: {user_id}
📅 Período: {format_date(week_ago)} até {format_date(datetime.now())}

💰 Total: {format_money(saldo)}
💚 Receitas: {format_money(receitas)}
❤️ Despesas: {format_money(despesas)}

📈 Transações neste período: {len(entries)}
"""
        return report
    except Exception as e:
        return f"❌ Erro ao gerar relatório: {str(e)}"

def generate_monthly_report(user_id, db):
    """Relatorio dos ultimos 30 dias"""
    try:
        session = db['Session']()
        
        month_ago = datetime.now() - timedelta(days=30)
        
        # Buscar transacoes do mes
        entries = session.query(db['Entry']).filter(
            db['Entry'].user_id == user_id,
            db['Entry'].date >= month_ago
        ).all()
        
        # Calcular totais
        receitas = sum(e.amount for e in entries if e.type == 'receita')
        despesas = sum(e.amount for e in entries if e.type == 'despesa')
        saldo = receitas - despesas
        
        session.close()
        
        report = f"""

        
📊 RELATÓRIO MENSAL (Últimos 30 dias)

👤 Usuário: {user_id}
📅 Período: {format_date(month_ago)} até {format_date(datetime.now())}

💰 Total: {format_money(saldo)}
💚 Receitas: {format_money(receitas)}
❤️ Despesas: {format_money(despesas)}

📈 Transações neste período: {len(entries)}
"""
        return report
    except Exception as e:
        return f"❌ Erro ao gerar relatório: {str(e)}"

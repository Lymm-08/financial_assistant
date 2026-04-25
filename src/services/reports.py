# ==========================
# ARQUIVO: src/services/reports.py
# SISTEMA DE GERAÇÃO DE RELATÓRIOS FINANCEIROS
# ==========================

# ==========================
# IMPORTAÇÕES
# ==========================

from datetime import datetime, timedelta
from sqlalchemy import func
from src.utils.formatter import format_money, format_date

# ==========================
# FUNÇÕES AUXILIARES
# ==========================

# ==========================
# CALCULAR TOTAIS E DIVIDIR POR CATEGORIA
# ==========================

def _calcular_totais_e_categorias(entries):
    """Calcula receitas, despesas e agrupa por categoria

    Returns:
        tuple: (receitas, despesas, categorias_dict)
    """
    receitas = sum(e.amount for e in entries if e.type == 'receita')
    despesas = sum(e.amount for e in entries if e.type == 'despesa')

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

    return receitas, despesas, categorias


def _formatar_categorias_text(categorias):
    """Formata dicionário de categorias em texto

    Returns:
        str: Texto formatado com categorias
    """
    if not categorias:
        return "Nenhuma transação registrada.\n"

    categorias_text = ""
    for cat, data in sorted(categorias.items()):
        total_cat = data['receitas'] - data['despesas']
        categorias_text += f"📂 {cat}: {format_money(total_cat)} ({data['count']} transações)\n"

    return categorias_text


def _calcular_economia(receitas, despesas):
    """Retorna economia em valor e percentual."""
    economia = receitas - despesas
    pct = economia / receitas * 100 if receitas > 0 else 0.0
    return economia, pct


def _formatar_economia_text(receitas, despesas):
    """Formata a economia como valor em reais e percentual."""
    economia, pct = _calcular_economia(receitas, despesas)
    
    if receitas == 0:
        if despesas == 0:
            return f"{format_money(0)} (0.0%)"
        else:
            return f"Déficit: {format_money(abs(economia))} (sem receitas)"
    
    if economia < 0:
        return f"Déficit: {format_money(abs(economia))} ({abs(pct):.1f}%)"
    
    return f"{format_money(economia)} ({pct:.1f}%)"

# ==========================
# FUNÇÃO PRINCIPAL DE RELATÓRIOS
# ==========================

def generate_report(user_id, report_type='simples', db=None):
    """
    Gera relatório financeiro baseado no tipo solicitado

    Tipos disponíveis:
    - simples: resumo rápido do mês atual
    - completo: detalhes completos com categorias
    - semanal: últimos 7 dias
    - mensal: últimos 30 dias
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

# ==========================
# RELATÓRIOS PADRÃO
# ==========================

# ==========================
# RELATÓRIO SIMPLES
# ==========================

def generate_simple_report(user_id, db):
    """Relatório simples com resumo do mês atual"""
    try:
        session = db['Session']()
        current_month = datetime.now().month
        current_year = datetime.now().year

        # SUBSEÇÃO: Buscar transações do mês atual
        entries = session.query(db['Entry']).filter_by(user_id=user_id).filter(
            db['Entry'].date >= datetime(current_year, current_month, 1)
        ).all()

        # SUBSEÇÃO: Calcular totais
        receitas, despesas, _ = _calcular_totais_e_categorias(entries)
        economia_text = _formatar_economia_text(receitas, despesas)

        # SUBSEÇÃO: Buscar saldo bancário atual
        bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
        saldo_banco = bank.total_balance if bank else 0

        session.close()

        report = f"""


📊 RELATÓRIO SIMPLES (MÊS ATUAL)

👤 Usuário: {user_id}
📅 Mês Atual: {datetime.now().strftime('%B %Y')}
💰 Saldo Atual: {format_money(saldo_banco)}
💚 Receitas do Mês: {format_money(receitas)}
❤️ Despesas do Mês: {format_money(despesas)}
💡 Economia: {economia_text}

📈 Transações Este Mês: {len(entries)}
"""
        return report
    except Exception as e:
        return f"❌ Erro ao gerar relatório: {str(e)}"

# ==========================
# RELATÓRIO DETALHADO
# ==========================

def generate_detailed_report(user_id, db):
    """Relatório detalhado com categorias e últimas transações"""
    try:
        session = db['Session']()
        current_month = datetime.now().month
        current_year = datetime.now().year

        # SUBSEÇÃO: Buscar transações do mês atual
        entries = session.query(db['Entry']).filter_by(user_id=user_id).filter(
            db['Entry'].date >= datetime(current_year, current_month, 1)
        ).all()

        # SUBSEÇÃO: Calcular totais e categorias
        receitas, despesas, categorias = _calcular_totais_e_categorias(entries)
        economia_text = _formatar_economia_text(receitas, despesas)
        categorias_text = _formatar_categorias_text(categorias)

        # SUBSEÇÃO: Buscar saldo bancário atual
        bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
        saldo_banco = bank.total_balance if bank else 0

        # SUBSEÇÃO: Últimas 5 transações
        ultimas = entries[-5:] if entries else []
        ultimas_text = ""
        for e in reversed(ultimas):
            ultimas_text += f"• {format_date(e.date)}: {e.type} {format_money(e.amount)} - {e.description}\n"

        if not ultimas_text:
            ultimas_text = "Nenhuma transação registrada ainda."

        session.close()

        report = f"""


📊 RELATÓRIO COMPLETO (MÊS ATUAL)

👤 Usuário: {user_id}
📅 Mês Atual: {datetime.now().strftime('%B %Y')}

💰 Saldo Atual: {format_money(saldo_banco)}
💚 Receitas do Mês: {format_money(receitas)}
❤️ Despesas do Mês: {format_money(despesas)}
💡 Economia: {economia_text}

📂 Por Categoria:
{categorias_text}

📝 Últimas Transações:
{ultimas_text}
"""
        return report
    except Exception as e:
        return f"❌ Erro ao gerar relatório: {str(e)}"

def _gerar_relatorio_periodo(user_id, data_inicio, data_fim, titulo, db):
    """Função auxiliar para gerar relatórios de período

    Args:
        user_id: ID do usuário
        data_inicio: Data inicial do período
        data_fim: Data final do período
        titulo: Título do relatório
        db: Conexão do banco

    Returns:
        str: Relatório formatado
    """
    try:
        session = db['Session']()

        # SUBSEÇÃO: Buscar transações do período
        entries = session.query(db['Entry']).filter(
            db['Entry'].user_id == user_id,
            db['Entry'].date >= data_inicio,
            db['Entry'].date <= data_fim
        ).all()

        # SUBSEÇÃO: Calcular totais
        receitas, despesas, _ = _calcular_totais_e_categorias(entries)
        saldo = receitas - despesas

        session.close()

        report = f"""


📊 {titulo}

👤 Usuário: {user_id}
📅 Período: {format_date(data_inicio)} até {format_date(data_fim)}

💰 Total: {format_money(saldo)}
💚 Receitas: {format_money(receitas)}
❤️ Despesas: {format_money(despesas)}

📈 Transações neste período: {len(entries)}
"""
        return report
    except Exception as e:
        return f"❌ Erro ao gerar relatório: {str(e)}"


def generate_weekly_report(user_id, db):
    """Relatório dos últimos 7 dias"""
    week_ago = datetime.now() - timedelta(days=7)
    return _gerar_relatorio_periodo(
        user_id,
        week_ago,
        datetime.now(),
        "RELATÓRIO SEMANAL (Últimos 7 dias)",
        db
    )


def generate_monthly_report(user_id, db):
    """Relatório dos últimos 30 dias"""
    month_ago = datetime.now() - timedelta(days=30)
    return _gerar_relatorio_periodo(
        user_id,
        month_ago,
        datetime.now(),
        "RELATÓRIO MENSAL (Últimos 30 dias)",
        db
    )

# ==========================
# RELATÓRIOS ESPECIAIS
# ==========================

def generate_month_specific_report(user_id, month_number, db):
    """Gera relatório de um mês específico do ano atual"""
    try:
        session = db['Session']()
        current_year = datetime.now().year

        # SUBSEÇÃO: Mapeamento de nomes dos meses
        month_names = {
            1: 'Janeiro', 2: 'Fevereiro', 3: 'Março', 4: 'Abril',
            5: 'Maio', 6: 'Junho', 7: 'Julho', 8: 'Agosto',
            9: 'Setembro', 10: 'Outubro', 11: 'Novembro', 12: 'Dezembro'
        }

        month_name = month_names.get(month_number, f'Mês {month_number}')

        # SUBSEÇÃO: Definir período do mês
        start_date = datetime(current_year, month_number, 1)
        if month_number == 12:
            end_date = datetime(current_year + 1, 1, 1)
        else:
            end_date = datetime(current_year, month_number + 1, 1)

        # SUBSEÇÃO: Buscar transações do mês específico
        entries = session.query(db['Entry']).filter_by(user_id=user_id).filter(
            db['Entry'].date >= start_date,
            db['Entry'].date < end_date
        ).all()

        # SUBSEÇÃO: Calcular totais e categorias
        receitas, despesas, categorias = _calcular_totais_e_categorias(entries)
        economia_text = _formatar_economia_text(receitas, despesas)
        categorias_text = _formatar_categorias_text(categorias)

        # SUBSEÇÃO: Buscar saldo atual
        bank = session.query(db['Bank']).filter_by(user_id=user_id).first()
        saldo_atual = bank.total_balance if bank else 0

        # SUBSEÇÃO: Últimas transações do mês
        ultimas = entries[-5:] if entries else []
        ultimas_text = ""
        for e in reversed(ultimas):
            ultimas_text += f"• {format_date(e.date)}: {e.type} {format_money(e.amount)} - {e.description}\n"

        if not ultimas_text:
            ultimas_text = "Nenhuma transação registrada neste mês."

        session.close()

        report = f"""


📊 RELATÓRIO DE {month_name.upper()} {current_year}

👤 Usuário: {user_id}
📅 Mês: {month_name} {current_year}
🏦 Saldo Atual: {format_money(saldo_atual)}

💚 Receitas do Mês: {format_money(receitas)}
❤️ Despesas do Mês: {format_money(despesas)}
💡 Economia: {economia_text}

📂 Por Categoria:
{categorias_text}

📝 Últimas Transações:
{ultimas_text}

📈 Total de Transações: {len(entries)}
"""
        return report
    except Exception as e:
        return f"❌ Erro ao gerar relatório do mês: {str(e)}"
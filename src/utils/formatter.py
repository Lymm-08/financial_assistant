# ==========================
# ARQUIVO: src/utils/formatter.py
# FORMATACAO DE DADOS
# ==========================

from datetime import datetime

def format_money(value):
    """Formata valor para moeda brasileira"""
    try:
        return f'R$ {value:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
    except:
        return f'R$ {value}'

def format_date(date):
    """Formata data para formato brasileiro"""
    if isinstance(date, datetime):
        return date.strftime('%d/%m/%Y %H:%M')
    return str(date)

def format_percentage(value):
    """Formata percentual"""
    return f'{value:.1f}%'

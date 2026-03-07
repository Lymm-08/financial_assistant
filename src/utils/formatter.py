# ==========================
# ARQUIVO: src/utils/formatter.py
# UTILITÁRIOS DE FORMATAÇÃO DE DADOS
# ==========================

# ==========================
# IMPORTAÇÕES
# ==========================

from datetime import datetime

# ==========================
# FORMATAÇÃO DE MOEDA
# ==========================

def format_money(value):
    """Formata valor numérico para moeda brasileira (R$)

    Args:
        value: Valor numérico a ser formatado

    Returns:
        String formatada como moeda brasileira
    """
    try:
        return f'R$ {value:,.2f}'.replace(',', '_').replace('.', ',').replace('_', '.')
    except:
        return f'R$ {value}'

# ==========================
# FORMATAÇÃO DE DATA/HORA
# ==========================

def format_date(date):
    """Formata data/hora para formato brasileiro

    Args:
        date: Objeto datetime ou string de data

    Returns:
        String formatada como dd/mm/yyyy hh:mm
    """
    if isinstance(date, datetime):
        return date.strftime('%d/%m/%Y %H:%M')
    return str(date)

# ==========================
# FORMATAÇÃO DE PERCENTUAIS
# ==========================

# Nota: format_percentage foi removida por não ser utilizada
# Se precisar, use: f'{valor:.1f}%'

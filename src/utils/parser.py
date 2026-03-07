# ==========================
# ARQUIVO: src/utils/parser.py
# PARSER DE DADOS
# ==========================

import re
from datetime import datetime

def parse_money(text):
    """
    Extrai valor monetário do texto
    🔧 Correção: regex aceita números com vírgula/ponto sem truncar
    """
    clean = re.sub(r'[R$\s]', '', text)
    clean = clean.replace(',', '.')
    try:
        match = re.search(r'\d+(?:\.\d+)?', clean)  # corrigido
        if match:
            return float(match.group())
    except:
        pass
    return None

def parse_date(text):
    """
    Extrai data do texto
    
    Formatos suportados:
    - "01/01/2024"
    - "2024-01-01"
    - "hoje"
    - "ontem"
    """
    # Implementar parsing de datas
    return datetime.now()

def parse_category(text):
    """
    Sugere categoria baseado em palavras-chave
    """
    keywords = {
        'alimentação': ['pizza', 'restaurante', 'café', 'comida'],
        'transporte': ['uber', 'taxi', 'ônibus', 'gasolina'],
        'saúde': ['farmácia', 'médico', 'hospital'],
        'educação': ['curso', 'livro', 'escola'],
    }
    
    text_lower = text.lower()
    for category, words in keywords.items():
        if any(word in text_lower for word in words):
            return category
    
    return 'outros'

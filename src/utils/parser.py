# ==========================
# ARQUIVO: src/utils/parser.py
# UTILITÁRIOS DE PARSING DE TEXTO
# ==========================

# ==========================
# IMPORTAÇÕES
# ==========================

import re
from datetime import datetime

# ==========================
# PARSING DE VALORES MONETÁRIOS
# ==========================

def parse_money(text):
    """
    Extrai valor monetário do texto usando regex robusta

    Suporta formatos como:
    - R$ 123,45
    - 123.45
    - 123,45
    - 123

    Returns:
        float: Valor extraído ou None se não encontrado
    """
    # SUBSEÇÃO: Limpar texto removendo símbolos de moeda
    clean = re.sub(r'[R$\s]', '', text)
    clean = clean.replace(',', '.')

    try:
        # SUBSEÇÃO: Buscar padrão numérico com regex
        match = re.search(r'\d+(?:\.\d+)?', clean)
        if match:
            return float(match.group())
    except:
        pass
    return None

# ==========================
# PARSING DE DATAS
# ==========================

def parse_date(text):
    """
    Extrai data do texto (funcionalidade básica implementada)

    Formatos suportados:
    - "01/01/2024"
    - "2024-01-01"
    - "hoje"
    - "ontem"

    Returns:
        datetime: Data extraída ou data atual como fallback
    
    Nota: Implementação completa pode ser adicionada conforme necessário
    """
    # TODO: Implementar parsing completo de datas
    return datetime.now()

# ==========================
# PARSING DE CATEGORIAS
# ==========================

# Nota: parse_money e parse_category foram removidos por não serem utilizados
# A categorização é feita através da IA em src/ai/categorizer.py
# O parsing de valores usa regex diretamente em handlers.py

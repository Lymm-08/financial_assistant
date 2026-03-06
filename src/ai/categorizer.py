# ==========================
# ARQUIVO: src/ai/categorizer.py
# CATEGORIZAÇÃO INTELIGENTE COM FALLBACK
# ==========================

import requests
import os
import time

# ==========================================
# CONFIGURAÇÃO DA API HUGGING FACE
# ==========================================
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_TOKEN = os.getenv('HF_API_TOKEN', '')

# ==========================================
# REGRAS DE FALLBACK (PALAVRAS-CHAVE)
# ==========================================
FALLBACK_RULES = {
    'Transporte': ['uber', 'taxi', 'ônibus', 'metrô', 'combustível', 'gasolina', 'passagem', 'trem', 'voo', 'avião'],
    'Alimentação': ['pizza', 'restaurante', 'comida', 'café', 'almoço', 'jantar', 'lanche', 'padaria', 'açaí', 'hamburger', 'sorvete', 'adega'],
    'Compras': ['compra', 'market', 'supermercado', 'loja', 'shopping', 'produto', 'mercado'],
    'Lazer': ['cinema', 'jogo', 'filme', 'diversão', 'show', 'museu', 'teatro', 'shopping', 'viagem', 'hotel'],
    'Saúde': ['farmácia', 'médico', 'hospital', 'dentista', 'remédio', 'medicamento', 'academia'],
    'Contas': ['conta', 'água', 'luz', 'internet', 'gás', 'telefone', 'energia'],
    'Educação': ['curso', 'livro', 'escola', 'aula', 'universidade', 'faculdade'],
    'Moda': ['roupa', 'sapato', 'blusa', 'calça', 'tênis', 'jaqueta'],
}

# ==========================================
# FUNÇÃO PARA CONSULTAR A API HF
# ==========================================
def query_hf(prompt: str) -> str:
    headers = {}
    if HF_TOKEN:
        headers['Authorization'] = f'Bearer {HF_TOKEN}'
    tries = 3
    for attempt in range(tries):
        try:
            resp = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt}, timeout=15)
            if resp.ok:
                data = resp.json()
                if isinstance(data, dict) and 'error' in data:
                    time.sleep(2)
                    continue
                if isinstance(data, list) and 'generated_text' in data[0]:
                    return data[0]['generated_text']
                if isinstance(data, str):
                    return data
        except Exception as e:
            print("Exceção HF:", e)
        time.sleep(1)
    return ''

# ==========================================
# FALLBACK LOCAL (PALAVRAS-CHAVE)
# ==========================================
def fallback_categorize(description: str) -> str:
    desc_lower = description.lower()
    for category, keywords in FALLBACK_RULES.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    return 'Outros'

# ==========================================
# CATEGORIZAÇÃO PRINCIPAL
# ==========================================
def categorize(description: str) -> str:
    if not description:
        return 'Outros'
    prompt = (
        f"Classifique a seguinte descrição de transação financeira em uma única categoria."
        f"\nDescrição: {description}\nCategoria:"    
    )
    result = query_hf(prompt)
    if result:
        parts = result.split('Categoria:')
        cat = parts[-1].strip().split('\n')[0].strip()
        if cat and len(cat) > 1:
            return cat
    return fallback_categorize(description)

# ==========================================
# CATEGORIZAÇÃO COM CONFIANÇA
# ==========================================
def categorize_with_confidence(description: str):
    """
    Categoriza uma transação baseado na descrição usando API ou fallback.
    Retorna: (categoria, confiança)
    """
    if not description:
        return ('Outros', 0.0)

    # Primeiro tenta via API
    result = query_hf(
        f"Classifique a seguinte descrição de transação financeira em uma única categoria.\nDescrição: {description}\nCategoria:"
    )
    if result:
        parts = result.split('Categoria:')
        cat = parts[-1].strip().split('\n')[0].strip()
        if cat and len(cat) > 1:
            # Se veio da API, confiança alta
            return (cat, 0.9)

    # Se não conseguiu via API, tenta fallback
    cat = fallback_categorize(description)
    if cat != 'Outros':
        # Fallback encontrou palavra-chave → confiança média
        return (cat, 0.7)

    # Nada encontrado → confiança baixa
    return ('Outros', 0.2)

# ==========================================
# DEBUG
# ==========================================
print("HF_TOKEN:", HF_TOKEN[:10], "...")

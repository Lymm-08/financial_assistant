# ==========================
# ARQUIVO: src/ai/categorizer.py
# CATEGORIZAÇÃO INTELIGENTE COM FALLBACK
# ==========================

import requests
import os

# usa API gratuita do Hugging Face para geração de texto
HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_TOKEN = os.getenv('HF_API_TOKEN', '')

# Regras de fallback baseadas em palavras-chave para quando API falhar
FALLBACK_RULES = {
    'Transporte': ['uber', 'taxi', 'ônibus', 'metrô', 'combustível', 'gasolina', 'passagem', 'trem', 'voo', 'avião'],
    'Alimentação': ['pizza', 'restaurante', 'comida', 'café', 'almoço', 'jantar', 'lanche', 'padaria', 'açaí', 'hamburger', 'sorvete', 'adega'],
    'Compras': ['compra', 'market', 'supermercado', 'loja', 'shopping', 'produto'],
    'Lazer': ['cinema', 'jogo', 'filme', 'diversão', 'show', 'museu', 'teatro', 'shopping', 'viagem', 'hotel'],
    'Saúde': ['farmácia', 'médico', 'hospital', 'dentista', 'remédio', 'medicamento', 'academia'],
    'Contas': ['conta', 'água', 'luz', 'internet', 'gás', 'telefone', 'energia'],
    'Educação': ['curso', 'livro', 'escola', 'aula', 'universidade', 'faculdade'],
    'Moda': ['roupa', 'sapato', 'blusa', 'calça', 'tênis', 'jaqueta'],
}

def query_hf(prompt: str) -> str:
    headers = {}
    if HF_TOKEN:
        headers['Authorization'] = f'Bearer {HF_TOKEN}'
    try:
        resp = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt}, timeout=10)
        if resp.ok:
            data = resp.json()
            if isinstance(data, dict) and 'error' in data:
                return ''
            text = data[0].get('generated_text') if isinstance(data, list) else ''
            return text or ''
    except Exception:
        pass
    return ''

def fallback_categorize(description: str) -> str:
    """Fallback inteligente: busca palavras-chave na descrição"""
    desc_lower = description.lower()
    for category, keywords in FALLBACK_RULES.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    return 'Outros'

def categorize(description: str) -> str:
    """Chama a API para classificar a descrição em uma categoria"""
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
        if cat and len(cat) > 1:  # evitar caracteres únicos
            return cat
    # Usar fallback inteligente baseado em keywords
    return fallback_categorize(description)

def categorize_with_confidence(description):
    """
    Categoriza uma transação baseado na descrição usando API
    
    Retorna: (categoria, confiança)
    """
    if not description:
        return ('Outros', 0.0)
    cat = categorize(description)
    return (cat, 0.5)

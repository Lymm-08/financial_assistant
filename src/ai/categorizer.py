# ==========================
# ARQUIVO: src/ai/categorizer.py
# CATEGORIZAÇÃO INTELIGENTE COM FALLBACK
# ==========================

import requests
import os
import time

HF_API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-base"
HF_TOKEN = os.getenv('HF_API_TOKEN', '')

# 🔧 Correção: adicionei "mercado" em Compras
FALLBACK_RULES = {
    'Transporte': ['uber', 'taxi', 'ônibus', 'metrô', 'combustível', 'gasolina', 'passagem', 'trem', 'voo', 'avião'],
    'Alimentação': ['pizza', 'restaurante', 'comida', 'café', 'almoço', 'jantar', 'lanche', 'padaria', 'açaí', 'hamburger', 'sorvete', 'adega'],
    'Compras': ['compra', 'market', 'supermercado', 'mercado', 'loja', 'shopping', 'produto'],
    'Lazer': ['cinema', 'jogo', 'filme', 'diversão', 'show', 'museu', 'teatro', 'viagem', 'hotel'],
    'Saúde': ['farmácia', 'médico', 'hospital', 'dentista', 'remédio', 'medicamento', 'academia'],
    'Contas': ['conta', 'água', 'luz', 'internet', 'gás', 'telefone', 'energia'],
    'Educação': ['curso', 'livro', 'escola', 'aula', 'universidade', 'faculdade'],
    'Moda': ['roupa', 'sapato', 'blusa', 'calça', 'tênis', 'jaqueta'],
}


def query_hf(prompt: str) -> str:
    headers = {}
    if HF_TOKEN:
        headers['Authorization'] = f'Bearer {HF_TOKEN}'
    tries = 3
    for attempt in range(tries):
        try:
            resp = requests.post(HF_API_URL, headers=headers, json={"inputs": prompt}, timeout=15)
            print("HF resposta:", resp.status_code, resp.text)  # log para debug
            if resp.ok:
                data = resp.json()
                # Caso de erro (modelo carregando ou indisponível)
                if isinstance(data, dict) and 'error' in data:
                    time.sleep(2)  # espera e tenta de novo
                    continue
                # Caso padrão: lista com generated_text
                if isinstance(data, list) and 'generated_text' in data[0]:
                    return data[0]['generated_text']
                # Alguns modelos retornam string direta
                if isinstance(data, str):
                    return data
            else:
                print("Erro HF:", resp.status_code)
        except Exception as e:
            print("Exceção HF:", e)
        time.sleep(1)
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


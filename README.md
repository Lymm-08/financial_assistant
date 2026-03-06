# 🤖 Bot Financeiro Telegram - TCC

> **Bot inteligente para gerenciamento financeiro pessoal via Telegram** — desenvolvido em Python.

`https://img.shields.io/badge/Status-Pronto%20para%20Produ%C3%A7%C3%A3o-green` `https://img.shields.io/badge/Python-3.10%2B-blue` `https://img.shields.io/badge/License-Educational-informational`

---

## ✨ O Que É

Um **bot chatbot financeiro** que permite:

✅ **Registrar transações** via Telegram  
✅ **Categorização automática** com IA (Hugging Face)
✅ **Relatórios financeiros** em múltiplos formatos  
✅ **Armazenamento seguro** em PostgreSQL  
✅ **Rodar 24/7** em background  

---


### 🚀 Quick Start

1. **Clonar**
```bash
git clone <seu-repo>
cd bot-financeiro
```

2. **Instalar dependências**
```bash
pip install -r requirements.txt
```

3. **Criar arquivo `.env`**  
Use `.env.example` como template e preencha as variáveis essenciais:
```env
BOT_TOKEN=seu_token_aqui
DB_URI=postgresql://postgres:senha@localhost:5432/bot_financeiro
ENCRYPTION_KEY=chave_secreta
HF_API_TOKEN=hf_seu_token
DEBUG=False
```

4. **Rodar**
```bash
python main.py
```

---

### ✨ Uso rápido

- **/iniciar** — menu inicial  
- **/relatorio simples** — ver resumo  
- **20 pizza** — registrar despesa  
- **recebi 1000 salario** — registrar receita

---

### 📚 Documentação completa

A documentação técnica detalhada (arquitetura, modelos de dados, fluxos, testes) está em:  
**`[Parece que o resultado não era seguro para exibição. Vamos mudar as coisas e tentar outra opção!]`**

Para um guia de instalação passo a passo, veja: **`[Parece que o resultado não era seguro para exibição. Vamos mudar as coisas e tentar outra opção!]`**

---

### 🔒 Segurança essencial

- **NÃO** commite o arquivo `.env`.  
- Verifique que `.gitignore` inclui:
```
.env
.venv/
__pycache__/
*.pyc
```
- **Criptografia** está implementada; ative em produção conforme instruções no TCC.

---

### 📦 Tecnologias principais

**Python 3.10+**, **python-telegram-bot 20.3**, **PostgreSQL + SQLAlchemy**, **Hugging Face API**, **cryptography**.

---

### 📜 Licença

**Educational Use Only - TCC 2026**

---

### 🎓 Info do TCC

**Título:** Bot Financeiro Inteligente com IA  
**Data:** 06/03/2026  
**Status:** Pronto para Apresentação

---

**Made with 💚 for Education**
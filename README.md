# 🤖 Bot Financeiro Telegram - TCC

> **Bot inteligente para gerenciamento financeiro pessoal via Telegram** — desenvolvido em Python.

![Status](https://img.shields.io/badge/Status-Pronto%20para%20Produ%C3%A7%C3%A3o-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Educational-informational)


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

**Comandos principais:**
- **/start** — Menu inicial com botões  
- **/relatorio simples** — Resumo do mês atual
- **/relatorio completo** — Detalhes com categorias
- **/relatorio semanal** — Últimos 7 dias
- **/relatorio mensal** — Últimos 30 dias
- **/relatorio mes 1** — Relatório de janeiro (1-12 para qualquer mês)
- **/reset** — Zerar todas as transações e saldo
- **/ajustar_saldo 1500** — Ajustar saldo manualmente

**Transações naturais:**
- **20 pizza** — Registrar despesa de R$ 20 em Alimentação
- **recebi 1000 salario** — Registrar receita de R$ 1.000

---

### 🏗️ Código bem organizado

Todo o código está estruturado com **seções claras**, comentários e documentação:
- **config/** — Configurações e variáveis de ambiente
- **models/** — Modelos de banco de dados
- **commands/** — Handlers dos comandos Telegram
- **ai/** — Categorização automática com IA + fallback
- **utils/** — Formatação, parsing, criptografia
- **services/** — Geração de relatórios

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
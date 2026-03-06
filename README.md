# 🤖 Bot Financeiro Telegram - TCC

> Um bot inteligente para gerenciamento financeiro pessoal desenvolvido em Python

![Status](https://img.shields.io/badge/Status-Pronto%20para%20Produção-green)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-Educational-informational)

---

## 📚 Documentação Completa do TCC

Este projeto inclui **documentação técnica profissional** para fins educacionais:

### 📖 Arquivos de Documentação

| Documento | Conteúdo |
|-----------|----------|
| **[GUIA_PROJETO.md](GUIA_PROJETO.md)** | Guia de usuário e instalação |
| **[TCC_DOCUMENTACAO.md](TCC_DOCUMENTACAO.md)** | Documentação técnica completa (★ LEIA ISSO) |
| **[DOCUMENTACAO_EXTENSAO.md](DOCUMENTACAO_EXTENSAO.md)** | Como estender o projeto |
| **[TESTES_TROUBLESHOOTING.md](TESTES_TROUBLESHOOTING.md)** | Testes e resolução de problemas |
| **[README.md](README.md)** | Este arquivo |

---

## ✨ O Que É

Um **bot chatbot financeiro** que permite:

✅ **Registrar transações** via Telegram  
✅ **Categorização automática** com IA (Hugging Face)
✅ **Relatórios financeiros** em múltiplos formatos  
✅ **Armazenamento seguro** em PostgreSQL  
✅ **Rodar 24/7** em background  

---

## 🚀 Quick Start

### 1. Clonar/Baixar o Projeto

```bash
cd bot-financeiro
```

### 2. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar `.env`

```env
BOT_TOKEN=seu_token_aqui
DB_URI=postgresql://postgres:senha@localhost:5432/bot_financeiro
ENCRYPTION_KEY=chave_secreta
HF_API_TOKEN=hf_seu_token
DEBUG=False
```

### 4. Iniciar o Bot

```bash
python main.py
```

### 5. Usar no Telegram

```
/iniciar              - Menu inicial
/relatorio simples    - Ver resumo
20 pizza             - Registrar gasto
recebi 1000 salario  - Registrar receita
```

---

## 🏗️ Arquitetura

```
┌─────────────────┐
│   Telegram      │
└────────┬────────┘
         │ (mensagens)
         ▼
┌─────────────────────────────┐
│  Commands Layer             │
│  (handlers.py)              │
└────────┬────────────────────┘
         │
    ┌────┴────┬─────────┬──────────┐
    ▼         ▼         ▼          ▼
┌────────┐ ┌──────┐ ┌────────┐ ┌────────┐
│Parser  │ │ Cate │ │Services│ │ Models │
│        │ │gorizer         │         │
└────────┘ └──────┘ └────────┘ └───┬────┘
                                    │
                                    ▼
                        ┌───────────────────┐
                        │  PostgreSQL DB    │
                        └───────────────────┘
```

---

## 📊 Stack Tecnológico

| Camada | Tecnologia |
|--------|------------|
| **Bot** | python-telegram-bot 20.3 |
| **Backend** | Python 3.10+ |
| **Database** | PostgreSQL + SQLAlchemy |
| **IA** | Hugging Face API |
| **Segurança** | Cryptography, python-dotenv |

---

## 🎯 Recursos

### Comandos Implementados

| Comando | Função |
|---------|--------|
| `/iniciar` | Menu de boas-vindas |
| `/relatorio` | Gerar 4 tipos de relatórios |
| `/receita` | Confirmar entrada |
| `/despesa` | Confirmar gasto |
| Texto livre | Registrar transação |

### Tipos de Relatórios

- 📊 **Simples:** Receitas, despesas, saldo, economia%
- 📈 **Detalhado:** Com breakdown por categoria
- 📅 **Semanal:** Últimos 7 dias
- 📆 **Mensal:** Últimos 30 dias

### Categorias de Transações

```
Alimentação    Transporte      Saúde
Educação       Lazer           Vestiário
Compras        Contas/Utilities Renda
Presentes      Outros
```

---

## 🔒 Segurança

✅ Variáveis de ambiente (.env)  
✅ SQLAlchemy ORM (previne SQL injection)  
✅ Criptografia de dados (Fernet)  
✅ Isolamento por usuário  
✅ Validação de entrada  

---

## 📁 Estrutura

```
bot-financeiro/
├── main.py                      # Entry point
├── requirements.txt             # Dependências
├── .env                        # Config (não commitar)
├── GUIA_PROJETO.md             # Guia de usuário
├── TCC_DOCUMENTACAO.md         # ⭐ DOCUMENTAÇÃO TÉCNICA
├── DOCUMENTACAO_EXTENSAO.md    # Como estender
├── TESTES_TROUBLESHOOTING.md   # Testes
│
└── src/
    ├── config/                 # ⚙️ Configurações
    ├── models/                 # 🗄️ Banco de dados
    ├── commands/               # 🤖 Handlers
    ├── ai/                     # 🧠 IA
    ├── services/               # 📊 Relatórios
    └── utils/                  # 🛠️ Utilitários
```

---

## 🧪 Testes

```bash
# Teste de conexão DB
python teste_db.py

# Rodar bot em modo debug
DEBUG=True python main.py

# Ver o arquivo de testes completo
cat TESTES_TROUBLESHOOTING.md
```

---

## 📈 Performance

| Operação | Tempo |
|----------|-------|
| Registrar transação | < 1s |
| Gerar relatório | < 5s |
| Buscar 100 registros | < 2s |
| Categorizar com IA | 1-3s |

---

## 🚀 Deploy em Produção

### Opção 1: Windows Task Scheduler (Recomendado)

Ver [GUIA_PROJETO.md](GUIA_PROJETO.md) → Seção "Rodar 24/7"

### Opção 2: VPS (DigitalOcean, AWS)

```bash
# No servidor:
git clone seu-repo
cd bot-financeiro
pip install -r requirements.txt
nohup python main.py &
```

### Opção 3: Docker

```bash
docker build -t bot-financeiro .
docker run -d --env-file .env bot-financeiro
```

---

## 🤝 Contribuindo

Este é um projeto educacional de TCC.  
Sinta-se à vontade para estender e melhorar!

**Como estender:**
1. Leia [DOCUMENTACAO_EXTENSAO.md](DOCUMENTACAO_EXTENSAO.md)
2. Adicione novo recurso
3. Teste conforme [TESTES_TROUBLESHOOTING.md](TESTES_TROUBLESHOOTING.md)

---

## ❓ Dúvidas Frequentes

**P: Preciso de PostgreSQL?**  
A: Sim, mas pode trocar por SQLite editando `config.py`

**P: Como gerar chave de encriptação?**  
A: Veja [TESTES_TROUBLESHOOTING.md](TESTES_TROUBLESHOOTING.md)

**P: O bot funciona em Android/iPhone?**  
A: Sim! Via Telegram em qualquer aparelho

**P: Posso usar com meu banco real?**  
A: Sim! Todos os dados são criptografados

**Para mais dúvidas:**  
👉 Consulte a [TCC_DOCUMENTACAO.md](TCC_DOCUMENTACAO.md)

---

## 📜 Licença

Educational Use Only - TCC 2026

---

## 🎓 Info do TCC

**Título:** Bot Financeiro Inteligente com IA  
**Data:** 06/03/2026  
**Status:** 🟢 Pronto para Apresentação  
**Linhas de Código:** ~2000 LOC  
**Domínios:** Backend, IA, Segurança, DevOps  

---

## 📚 Leitura Recomendada

1. Start → [GUIA_PROJETO.md](GUIA_PROJETO.md)
2. Técnico → [TCC_DOCUMENTACAO.md](TCC_DOCUMENTACAO.md) (★ ESSENCIAL)
3. Extensão → [DOCUMENTACAO_EXTENSAO.md](DOCUMENTACAO_EXTENSAO.md)
4. Testes → [TESTES_TROUBLESHOOTING.md](TESTES_TROUBLESHOOTING.md)

---

**Made with 💚 for Education**  
**Pronto para seu TCC** ✅

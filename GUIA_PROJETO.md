# 🤖 BOT FINANCEIRO TELEGRAM - DOCUMENTAÇÃO COMPLETA (TCC)

---

## 📚 ÍNDICE RÁPIDO
1. [O Que É](#o-que-é)
2. [Instalação](#instalação--setup)
3. [Configuração](#configuração)
-  [Token Hugging Face](#token-hugging-face)
4. [Como Usar](#como-usar)
5. [Estrutura do Projeto](#estrutura-do-projeto)
6. [Modificar / Adicionar Recursos](#modificar--adicionar-recursos)
7. [Deploy](#deploy)
8. [commits]

---

# ✨ O QUE É

Um **BOT FINANCEIRO** completamente desenvolvido em **Python** para o **Telegram** que permite:

- ✅ Registrar **despesas e receitas** via chat
- ✅ **Categorizar automaticamente** as transações (usando API de IA externa, sem listas codificadas)
- ✅ Gerar **relatórios financeiros** (simples, semanal, mensal)
- ✅ **Criptografar** dados sensíveis
- ✅ **Armazenar** em banco PostgreSQL

**Stack Tecnológico:**
- 🐍 Python 3.10+
- 🤖 python-telegram-bot (Telegram API)
- 🗄️ PostgreSQL + SQLAlchemy (Banco de Dados)
- 🔐 Cryptography (Criptografia)
- 📦 python-dotenv (Variáveis de Ambiente)

---

# 🚀 INSTALAÇÃO & SETUP
### Token Hugging Face
Para categorizar automaticamente sem listas, o bot usa a API gratuita do Hugging Face.
- Crie uma conta em https://huggingface.co
- Vá em **Settings → Access Tokens** e gere um token (tipo `hf_xxx`)
- Adicione ao `.env`:
```dotenv
HF_API_TOKEN=seu_token_aqui
```

Se você não fornecer o token, o bot usará categorias de fallback genéricas.

## 🚀 INSTALAÇÃO & SETUP
## PASSO 1: INSTALAR PYTHON       ===feito===

### Windows:
```powershell
# Opção 1: Download direto
https://www.python.org/downloads/

# Opção 2: Winget
winget install Python.Python.3.11
```

**Após instalar, abra terminal e verifique:**
```bash
python --version
```

## PASSO 2: INSTALAR POSTGRESQL   ===feito===

### Windows:
```powershell
# Opção 1: Download direto
https://www.postgresql.org/download/windows/

# Opção 2: Winget
winget install PostgreSQL.PostgreSQL
```

**Durante instalação:**
- Escolha uma **senha** para o usuário `postgres`
- Mantenha porta padrão: **5432**
- Anote a senha! Você vai precisar.

### Criar Banco de Dados:  
1. Abra **pgAdmin 4** (vem com PostgreSQL)
2. Clique em **Servers** → **PostgreSQL**
3. Clique direito em **Databases**
4. **Create** → **Database**
5. Nome: `bot_financeiro`
6. Clique **Save**

**Pronto! Você tem:**
- Username: `postgres`
- Password: A senha que você escolheu
- Database: `bot_financeiro`
- Host: `localhost`
- Port: `5432`

## PASSO 3: INSTALAR DEPENDÊNCIAS  ===feito===

Abra terminal na pasta do projeto:

```bash
# Instalar todas as dependências
pip install -r requirements.txt
```

**Pacotes instalados:**
- python-telegram-bot==20.3 (Bot Telegram)
- sqlalchemy==2.0.23 (ORM Banco)
- psycopg2-binary==2.9.9 (Driver PostgreSQL)
- cryptography==41.0.7 (Criptografia)
- python-dotenv==1.0.0 (Variáveis)

---

# ⚙️ CONFIGURAÇÃO

## PASSO 4: CONFIGURAR .env     ===feito===

Abra o arquivo `.env` e preencha EXATAMENTE assim:

```env
BOT_TOKEN=seu_token_do_botfather_aqui
DB_URI=postgresql://postgres:sua_senha_postgres@localhost:5432/bot_financeiro
ENCRYPTION_KEY=uma_chave_criptografica_qualquer_123
DEBUG=False
```

### Obter BOT_TOKEN:            ===feito===

1. Abra **Telegram**
2. Procure: **@BotFather**
3. Envie: `/newbot`
4. Escolha um nome para o bot
   - Exemplo: "Meu Bot Financeiro TCC"
5. Escolha um username (@usuario_bot)
   - Exemplo: @bot_financeiro_tcc_emily_123
6. BotFather responde com o token:
   ```
   Token: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh (exemplo)
   ```
7. **Copie e cole no BOT_TOKEN do .env**

### Exemplo COMPLETO de .env:

```env
BOT_TOKEN=1234567890:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefgh

DB_URI=postgresql://postgres:senha123@localhost:5432/bot_financeiro

ENCRYPTION_KEY=chave_super_secreta_para_tcc_2026

DEBUG=False
```

**IMPORTANTE:**
- Nunca compartilhe o BOT_TOKEN
- Nunca faça commit do .env no git
- A senha do .env é a mesma do PostgreSQL que você escolheu

---

# 💬 COMO USAR

## Iniciar o Bot

### Opção 1: Desenvolvimento (Simples)

Abra terminal na pasta do projeto:

```bash
python main.py
```

**Você vai ver:**
```
Configuracao carregada:
   - BOT_TOKEN: ****
   - DB_URI: postgresql://postgres:...
   - DEBUG: False
Banco PostgreSQL inicializado com sucesso
Bot Financeiro iniciado!
Pronto para receber mensagens...
(Pressione Ctrl+C para parar)
```

---

### Opção 2: Rodar 24/7 com Task Scheduler (Produção)

Para testar o bot **por meses continuamente** sem perder a conexão, configure para rodar automaticamente no startup do Windows.

#### ⚙️ PASSO A PASSO:

**PASSO 1: Abrir Task Scheduler**
1. Clique no ícone **Windows** (canto esquerdo inferior)
2. Digite: `Task Scheduler`
3. Clique para abrir

**PASSO 2: Criar Nova Tarefa**
1. No lado direito, clique em **"Create Basic Task"**
2. Nome: `Bot Financeiro`
3. Descrição: `Executa o bot financeiro 24/7`
4. Clique em **"Next"**

**PASSO 3: Definir Quando Iniciar**
1. Selecione: **"When the computer starts"**
2. Clique em **"Next"**

**PASSO 4: Definir Ação**
1. Selecione: **"Start a program"**
2. Clique em **"Next"**

**PASSO 5: Configurar Programa**
1. **Program/script:** Cole o caminho do python:
   ```
   C:\Users\emily\OneDrive\Documentos\bot financeiro\.venv\Scripts\pythonw.exe
   ```
   
2. **Arguments:** Digite:
   ```
   main.py
   ```
   
3. **Start in (optional):** Cole:
   ```
   C:\Users\emily\OneDrive\Documentos\bot financeiro
   ```

4. Clique em **"Next"**

**PASSO 6: Revisar e Finalizar**
1. Revise as configurações
2. ✅ Marque: **"Open the Properties dialog for this task when I click Finish"**
3. Clique em **"Finish"**

**PASSO 7: Configurações Avançadas**
Uma janela abre com propriedades. Vá em:

- **General / Geral:**
  - ✅ Marque "Run whether user is logged in or not"
  - ✅ Marque "Run with highest privileges"

- **Triggers / Acionadores:**
  - Clique em "Startup"
  - Marque ✅ "Enabled"

- **Actions / Ações:**
  - Verifique se está correto
  - Marque ✅ "Enabled"

- **Settings / Configurações:**
  - ✅ "Run the task as soon as possible after a scheduled start is missed"
  - ✅ "If the task fails, restart every: 1 minute"

- Clique em **"OK"**

**PASSO 8: Testar**
1. Reinicie o computador
2. Abra Telegram
3. Procure seu bot
4. Digite: `/iniciar`
5. Se responder, funcionou! ✅

---

#### ✅ O que você consegue fazer agora:

- ✅ Bot inicia automaticamente quando liga o PC
- ✅ Roda em **background** (sem abrir janela)
- ✅ Funciona **24/7**
- ✅ Pode testar por **meses**
- ✅ Funciona em **múltiplos aparelhos** via Telegram
- ✅ Persiste dados no PostgreSQL

## Comandos no Telegram

Abra Telegram, procure seu bot e envie:

```
/iniciar                    - Menu principal
/relatorio simples          - Resumo rápido
/relatorio completo         - Detalhes com categorias
/relatorio semanal          - Últimos 7 dias
/relatorio mensal           - Últimos 30 dias

20 reais pizza              - Registrar despesa de R$20
50 pizza                    - Mesmo acima (simplificado)
recebi 1000 salário         - Registrar receita
```

## Exemplos de Uso

**Registrar Pizza:**
- Digite: `20 pizza`
- Bot responde:
  ```
  Registrado!
  Valor: R$ 20,00
  Categoria: Alimentação
  Tipo: despesa
  Data: 05/03/2026 19:30
  ```

**Ver Relatório:**
- Digite: `/relatorio simples`
- Bot responde:
  ```
  RELATORIO SIMPLES
  
  Saldo Total: R$ 0,00
  Receitas: R$ 0,00
  Despesas: R$ 20,00
  ```

---

# 📁 ESTRUTURA DO PROJETO

```
bot-financeiro/
│
├── 📄 main.py              ← ARQUIVO PRINCIPAL (execute isto!)
├── 📄 requirements.txt      ← Dependências Python
├── 📄 .env                 ← Suas configurações (não commitar!)
├── 📄 .env.example         ← Exemplo de configuração
├── 📄 SETUP_POSTGRESQL.md  ← Guia PostgreSQL
├── 📄 LEIA-ME-PRIMEIRO.md  ← Este arquivo
│
└── 📁 src/                 ← CÓDIGO-FONTE
    │
    ├── 📁 config/          ← ⚙️ CONFIGURAÇÕES
    │   ├── __init__.py
    │   └── config.py       [Carrega .env]
    │
    ├── 📁 models/          ← 🗄️ BANCO DE DADOS
    │   ├── __init__.py
    │   └── db.py           [Modelos Entry e Bank]
    │
    ├── 📁 commands/        ← 🎮 COMANDOS TELEGRAM
    │   ├── __init__.py
    │   └── handlers.py     [/iniciar, /relatorio]
    │
    ├── 📁 ai/              ← 🤖 INTELIGÊNCIA ARTIFICIAL
    │   ├── __init__.py
    │   └── categorizer.py  [Categoriza despesas]
    │
    ├── 📁 utils/           ← 🛠️ UTILITÁRIOS
    │   ├── __init__.py
    │   ├── formatter.py    [Formata R$, datas]
    │   ├── parser.py       [Extrai valores]
    │   └── encryption.py   [Criptografa dados]
    │
    └── 📁 services/        ← 📊 SERVIÇOS
        ├── __init__.py
        └── reports.py      [Gera relatórios]
```

---

## 🎯 O QUE FAZ CADA PASTA

### `config/` - CONFIGURAÇÕES
**Arquivo:** `config.py`

Lê o arquivo `.env` e carrega todas as configurações:
- BOT_TOKEN
- DB_URI (banco de dados)
- ENCRYPTION_KEY
- DEBUG mode

```python
# Usar em qualquer lugar:
from src.config.config import config

print(config['BOT_TOKEN'])
print(config['DB_URI'])
```

---

### `models/` - BANCO DE DADOS
**Arquivo:** `db.py`

Define a estrutura das tabelas usando SQLAlchemy:

**Tabela `entries` (Transações):**
```
id           → ID único
user_id      → Quem registrou
type         → "despesa" ou "receita"
amount       → Valor (R$)
category     → Categoria (Alimentação, Transporte, etc)
description  → Descrição
date         → Data/hora
is_encrypted → Dado criptografado?
```

**Tabela `banks` (Saldo por usuário):**
```
id            → ID único
user_id       → Usuário
total_balance → Saldo total
currency      → Moeda (BRL)
last_updated  → Última atualização
```

**Usar:**
```python
from src.models.db import init_db, Entry, Bank

db = init_db()
Session = db['Session']
session = Session()

# Criar entrada
nova = Entry(user_id='12345', type='despesa', amount=50.0, category='Alimentação')
session.add(nova)
session.commit()
```

---

### `commands/` - COMANDOS TELEGRAM
**Arquivo:** `handlers.py`

Processa todos os comandos e mensagens:

**Funções:**
- `cmd_start()` → Responde `/iniciar`
- `cmd_relatorio()` → Responde `/relatorio [tipo]`
- `handle_message()` → Processa mensagens com valores
- `register_commands()` → Registra tudo no bot

**Exemplo:** Quando usuário digita "20 pizza":
1. Handler recebe a mensagem
2. Parser extrai: valor=20, descrição="pizza"
3. Categorizer sugere: "Alimentação"
4. Salva no banco de dados
5. Retorna confirmação

---

### `ai/` - CATEGORIZAÇÃO
**Arquivo:** `categorizer.py`

Inteligência artificial para categorizar automaticamente:

**Categorias disponíveis:**
```
Alimentação      (pizza, restaurante, café)
Transporte       (uber, ônibus, gasolina)
Saúde            (farmácia, médico)
Educação         (curso, livro, escola)
Lazer            (cinema, jogo, show)
Vestiário        (roupa, sapato)
Compras          (supermercado, loja)
Contas/Utilidades (água, luz, internet)
Renda            (salário, freelance)
Presentes        (presente, aniversário)
```

**Como funciona:**
```python
from src.ai.categorizer import categorize

resultado = categorize("pizza no fornecedor")
# Retorna: "Alimentação"

resultado = categorize("passagem de ônibus")
# Retorna: "Transporte"
```

**Modificar categorias:**
Abra `src/ai/categorizer.py` e edite `CATEGORY_RULES`

---

### `utils/` - UTILITÁRIOS

#### `formatter.py` - Formatação
```python
from src.utils.formatter import format_money, format_date

# Formatar dinheiro
format_money(50.5)           # "R$ 50,50"
format_money(1234.56)        # "R$ 1.234,56"

# Formatar data
from datetime import datetime
format_date(datetime.now())  # "05/03/2026 19:30"
```

#### `parser.py` - Extração de Dados
```python
from src.utils.parser import parse_money

# Extrair valores de textos
parse_money("R$ 50,00")      # 50.0
parse_money("100.50")        # 100.5
parse_money("25 reais")      # 25.0
```

#### `encryption.py` - Criptografia
```python
from src.utils.encryption import Encryptor

# Criptografar dados sensíveis
enc = Encryptor("minha_chave_secreta")

texto_criptografado = enc.encrypt("dado_sensivel")
texto_normal = enc.decrypt(texto_criptografado)
```

---

### `services/` - SERVIÇOS

#### `reports.py` - Relatórios
```python
from src.services.reports import generate_report

# Tipos disponíveis:
generate_report(user_id, 'simples')    # Resumo
generate_report(user_id, 'completo')   # Completo
generate_report(user_id, 'semanal')    # 7 dias
generate_report(user_id, 'mensal')     # 30 dias
```

---

# 🛠️ MODIFICAR / ADICIONAR RECURSOS

## Adicionar Novo Comando

**Exemplo:** Adicionar comando `/meu_comando`

### Passo 1: Criar função em `src/commands/handlers.py`

Abra `src/commands/handlers.py` e adicione:

```python
async def cmd_meu_comando(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Meu novo comando"""
    mensagem = "Olá! Este é meu novo comando!"
    await update.message.reply_text(mensagem)
```

### Passo 2: Registrar em `register_commands()`

Encontre a função `register_commands()` no mesmo arquivo e adicione:

```python
def register_commands(app, db):
    """Registra todos os comandos"""
    
    # Adicionar esta linha:
    app.add_handler(CommandHandler('meu_comando', cmd_meu_comando))
    
    # ... outros handlers ...
```

### Passo 3: Testar

Reinicie o bot:
```bash
python main.py
```

Digite no Telegram: `/meu_comando`

---

## Adicionar Nova Categoria

Abra `src/ai/categorizer.py` e encontre `CATEGORY_RULES`:

```python
CATEGORY_RULES = {
    'Alimentação': [
        r'(?:pizza|restaurante|café)',
    ],
    'Minha Categoria': [        # ← ADICIONE AQUI
        r'(?:palavra1|palavra2|palavra3)',
    ],
    # ... outras categorias ...
}
```

**Exemplo:** Adicionar categoria "Viagem"

```python
'Viagem': [
    r'(?:hotel|passagem aérea|viagem|turismo|avião|hospedagem)',
],
```

---

## Modificar Mensagens do Bot

As mensagens estão em `src/commands/handlers.py`:

**Encontre `cmd_start()`:**
```python
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = f"""
Bot Financeiro - Bem-vindo, {user.first_name}!
... edite aqui ...
"""
    await update.message.reply_text(text)
```

Edite o `text` como quiser!

---

## Conectar com Banco de Dados

Para salvar/ler dados do PostgreSQL:

```python
from src.models.db import init_db, Entry, Bank

# Inicializar
db = init_db()
Session = db['Session']
session = Session()

# Criar nova entrada
nova_transacao = Entry(
    user_id='12345',
    type='despesa',
    amount=50.0,
    category='Alimentação',
    description='Pizza',
)
session.add(nova_transacao)
session.commit()

# Buscar dados
todas = session.query(Entry).filter_by(user_id='12345').all()
for t in todas:
    print(f"{t.category}: R$ {t.amount}")
```

---

# 🚀 DEPLOY

## Local (seu computador)

```bash
python main.py
```

## Online (Servidor)

### Opção 1: Render (Gratuito)

1. Acesse: https://render.com
2. Conecte sua conta GitHub
3. Deploy Python App
4. Defina comando: `python main.py`
5. Variáveis de ambiente: BOT_TOKEN, DB_URI, etc

### Opção 2: Heroku (Pago)

1. Heroku CLI: https://devcenter.heroku.com/articles/heroku-cli
2. No terminal:
```bash
heroku login
heroku create seu-app-name
git push heroku main
```

### Opção 3: VPS (AWS, DigitalOcean, etc)

1. SSH para o servidor
2. Clone o projeto
3. Instale Python e PostgreSQL
4. Configure .env
5. Execute: `python main.py` (de preferência com supervisor/systemd)

---

# ❓ DÚVIDAS FREQUENTES

**P: Esqueci a senha do PostgreSQL?**
A: Reinstale o PostgreSQL e escolha uma nova senha.

**P: Posso usar SQLite em vez de PostgreSQL?**
A: Sim! Mude em `.env`: `DB_URI=sqlite:///finance.db`

**P: O bot está fora do ar?**
A: Verifique se:
- BOT_TOKEN está correto no .env
- PostgreSQL está rodando
- Python estão instalados
- Não há erros no terminal

**P: Como salvo os dados no banco?**
A: Já está implementado! Basta digitar "20 pizza" que automaticamente salva.

**P: Posso modificar o código?**
A: Claro! É seu projeto. Qualquer mudança em `src/` é refletida quando reinicia.

**P: Como faço backup?**
A: PostgreSQL:
```bash
pg_dump -U postgres bot_financeiro > backup.sql
```

---

# 📝 RESUMO - COMECE AQUI!

**1️⃣ INSTALAR:**
```bash
pip install -r requirements.txt
```

**2️⃣ CONFIGURAR:**
- Instale PostgreSQL
- Crie banco `bot_financeiro`
- Preencha `.env` com suas credenciais

**3️⃣ RODAR:**
```bash
python main.py
```

**4️⃣ USAR:**
- Telegram: `/iniciar`
- Adicionar gasto: `20 pizza`
- Relatório: `/relatorio simples`

---

# 📚 PARA SEU TCC

**Este projeto demonstra:**

✅ **Backend** - Python, SQLAlchemy, PostgreSQL
✅ **API Telegram** - python-telegram-bot
✅ **Mecanismos de IA** - Categorização automática
✅ **Criptografia** - Dado seguro
✅ **Modularização** - Arquitetura limpa
✅ **Tratamento de erros** - Robustez
✅ **Banco de dados** - CRUD completo
✅ **Relatórios** - Processamento de dados

---

**Documento criado:** 05/03/2026
**Versão:** 1.0
**Linguagem:** Python 100%
**Status:** 🟢 Pronto para Produção

**Se tiver dúvidas, releia este documento. Tudo está aqui!**


# commit (🔄 Como recuperar versões antigas) 

1. Veja o histórico:

```powershell
git log
```

2. Copie o hash (aquele código longo do commit).

3. Volte para essa versão:

```powershell
git checkout <hash>
```

4. Isso coloca os arquivos no estado daquele commit.

**Se quiser apenas ver as diferenças sem voltar:**

```powershell
git diff
```

# commit (☁️ E se eu perder o código no PC?) backup seguro

- Se você só usa Git local, os commits ficam guardados na pasta .git do projeto.

- Se o computador quebrar ou a pasta for apagada, você perde tudo.

- Por isso, é fortemente recomendado ter um repositório remoto (GitHub, GitLab, Bitbucket).
Assim, mesmo que o PC seja perdido, você pode clonar o projeto de volta:

```powershell
git clone https://github.com/seuusuario/seuprojeto.git
```
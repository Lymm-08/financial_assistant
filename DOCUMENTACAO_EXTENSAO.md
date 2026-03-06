# 📖 DOCUMENTAÇÃO DE EXTENSÃO DO PROJETO

**Para TCC - Demonstração de Extensibilidade**

---

## Índice

1. [API de Handlers](#api-de-handlers)
2. [Como Adicionar Novo Comando](#como-adicionar-novo-comando)
3. [Como Adicionar Nova Categoria](#como-adicionar-nova-categoria)
4. [Como Customizar Fallback](#como-customizar-fallback)
5. [Como Adicionar Novo Tipo de Relatório](#como-adicionar-novo-tipo-de-relatório)
6. [Como Integrar Novo Banco de Dados](#como-integrar-novo-banco-de-dados)
7. [Como Adicionar Criptografia](#como-adicionar-criptografia)
8. [Padrões de Design Utilizados](#padrões-de-design-utilizados)

---

## 1. API de Handlers

### Estrutura de um Handler

```python
from telegram import Update
from telegram.ext import ContextTypes

async def seu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Descrição do que faz"""
    
    # Acessar informações do usuário
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name
    
    # Acessar a mensagem
    message_text = update.message.text
    
    # Responder
    await update.message.reply_text("Sua resposta aqui")
```

### Exemplo Completo: Handler de Saudação

```python
async def cmd_oi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Responde com uma saudação personalizada"""
    
    user = update.effective_user
    greeting = f"Olá {user.first_name}! 👋"
    
    await update.message.reply_text(greeting)

# Registrar no main.py
app.add_handler(CommandHandler('oi', cmd_oi))
```

---

## 2. Como Adicionar Novo Comando

### Passo a Passo

#### Passo 1: Criar a função em `src/commands/handlers.py`

```python
async def cmd_configuracao(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Abre menu de configurações"""
    
    user_id = update.effective_user.id
    
    # Lógica aqui
    mensagem = """
⚙️ MENU DE CONFIGURAÇÕES

1️⃣ /moeda - Mudar moeda (BRL, USD, EUR)
2️⃣ /categoria_nova - Adicionar categoria customizada
3️⃣ /notificacao - Ativar/desativar notificações
"""
    
    await update.message.reply_text(mensagem)
```

#### Passo 2: Registrar em `register_commands()`

```python
def register_commands(app, db):
    """Registra todos os comandos"""
    
    # Comandos existentes...
    
    # Seu novo comando (COM db parameter)
    app.add_handler(CommandHandler('configuracao', partial(cmd_configuracao, db=db)))
    
    # OU SEM db parameter (se não precisar)
    app.add_handler(CommandHandler('help', cmd_help))
```

#### Passo 3: Testar no Telegram

```
Digite: /configuracao
Esperado: Menu de confiturações aparece
```

### Comandos Comuns Úteis

```python
# Teclado customizado (ainda não implementado)
from telegram import ReplyKeyboardMarkup, KeyboardButton

reply_markup = ReplyKeyboardMarkup([
    [KeyboardButton('/receita'), KeyboardButton('/despesa')],
    [KeyboardButton('/relatorio')]
])

await update.message.reply_text(
    "Escolha uma opção:",
    reply_markup=reply_markup
)

# Editar mensagem anterior
await context.bot.edit_message_text(
    chat_id=update.effective_chat.id,
    message_id=update.message.message_id,
    text="Mensagem editada!"
)

# Excluir mensagem
await context.bot.delete_message(
    chat_id=update.effective_chat.id,
    message_id=update.message.message_id
)
```

---

## 3. Como Adicionar Nova Categoria

### Opção 1: Via Fallback Rules (Fácil)

**Arquivo:** `src/ai/categorizer.py`

```python
FALLBACK_RULES = {
    # Categorias existentes...
    
    # Adicione aqui:
    'Viagem': [
        'hotel', 'hostel', 'passagem aérea', 'avião', 
        'viagem', 'turismo', 'hospedagem', 'resort'
    ],
    
    'Assinatura': [
        'netflix', 'spotify', 'subscription', 'mensalidade',
        'plano', 'premium', 'assinatura'
    ],
}
```

**Efeito:** Quando fallback ativa, reconhece essas palavras automaticamente.

### Opção 2: Treinar Modelo Customizado (Avançado)

Para realmente treinar um modelo:

```python
# Criar dataset
import json

dataset = [
    {"text": "hotel em SP", "category": "Viagem"},
    {"text": "passagem aérea", "category": "Viagem"},
    {"text": "netflix subscription", "category": "Assinatura"},
    # ... mais exemplos
]

with open('custom_dataset.json', 'w') as f:
    json.dump(dataset, f)

# Upload para Hugging Face e fine-tune do modelo
# (Requer conta Hugging Face paga)
```

---

## 4. Como Customizar Fallback

**Arquivo:** `src/ai/categorizer.py`

```python
def fallback_categorize(description):
    """Busca por keywords na descrição"""
    
    desc_lower = description.lower()
    
    # Iterar pelas categorias
    for category, keywords in FALLBACK_RULES.items():
        for keyword in keywords:
            if keyword in desc_lower:
                return category
    
    # Se nenhuma categoria encontrada
    return 'Outros'
```

**Para modificar o comportamento:**

```python
# Opção 1: Aumentar prioridade de certas categorias
FALLBACK_RULES = {
    'Alimentação': ['pizza', 'restaurante', ...],  # Busca primeiro
    'Transporte': ['uber', ...],                    # Depois
}

# Opção 2: Usar regex mais complexo
import re

def fallback_categorize_regex(description):
    if re.search(r'\b(hotel|hospedagem|viagem)\b', description):
        return 'Viagem'
    # ... mais padrões

# Opção 3: Usar similaridade de texto
from difflib import SequenceMatcher

def fallback_categorize_similarity(description):
    best_match = None
    highest_ratio = 0
    
    for category, keywords in FALLBACK_RULES.items():
        for keyword in keywords:
            ratio = SequenceMatcher(None, description, keyword).ratio()
            if ratio > highest_ratio:
                highest_ratio = ratio
                best_match = category
    
    return best_match or 'Outros'
```

---

## 5. Como Adicionar Novo Tipo de Relatório

**Arquivo:** `src/services/reports.py`

### Template Básico

```python
def generate_custom_report(db, user_id):
    """Seu novo tipo de relatório"""
    
    session = db['Session']()
    Entry = db['Entry']
    Bank = db['Bank']
    
    # Query personalizada
    entries = session.query(Entry).filter_by(user_id=user_id).all()
    
    # Calcular o que você quiser
    total = sum(e.amount for e in entries)
    
    # Formatar resposta
    resposta = f"""
📊 SEU RELATÓRIO

Total: R$ {total:.2f}
"""
    
    session.close()
    return resposta
```

### Exemplo: Relatório por Tag

```python
def generate_tag_report(db, user_id, tag):
    """Relatório filtrado por tag"""
    
    session = db['Session']()
    Entry = db['Entry']
    
    # Buscar transações com tag
    entries = session.query(Entry).filter(
        Entry.user_id == user_id,
        Entry.description.contains(tag)
    ).all()
    
    receitas = sum(e.amount for e in entries if e.type == 'receita')
    despesas = sum(e.amount for e in entries if e.type == 'despesa')
    
    resposta = f"""
🏷️ RELATÓRIO - TAG: {tag}

💚 Receitas: R$ {receitas:.2f}
❤️  Despesas: R$ {despesas:.2f}
🔄 Saldo: R$ {receitas - despesas:.2f}

Total de transações: {len(entries)}
"""
    
    session.close()
    return resposta

# Registrar comando
async def cmd_tag_report(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    """Pede tag e mostra relatório"""
    
    if len(context.args) < 1:
        await update.message.reply_text("Use: /tag_report palavra")
        return
    
    tag = context.args[0]
    user_id = str(update.effective_user.id)
    
    report = generate_tag_report(db, user_id, tag)
    await update.message.reply_text(report)

# Em main.py:
# app.add_handler(CommandHandler('tag_report', partial(cmd_tag_report, db=db)))
```

---

## 6. Como Integrar Novo Banco de Dados

### Exemplo: Migrar de PostgreSQL para SQLite

**Novo arquivo:** `src/models/db_sqlite.py`

```python
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

class Entry(Base):
    __tablename__ = 'entries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    type = Column(String(20))  # 'receita' ou 'despesa'
    amount = Column(Float)
    category = Column(String(50))
    description = Column(String(255))
    date = Column(DateTime, default=datetime.now)
    is_encrypted = Column(Boolean, default=False)

class Bank(Base):
    __tablename__ = 'banks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50), unique=True)
    total_balance = Column(Float, default=0)
    currency = Column(String(3), default='BRL')
    last_updated = Column(DateTime, default=datetime.now)

def init_db_sqlite():
    """Inicializar SQLite"""
    
    # SQLite usa arquivo local
    engine = create_engine('sqlite:///finance.db')
    
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    
    return {
        'engine': engine,
        'Session': Session,
        'Entry': Entry,
        'Bank': Bank
    }

# Em config.py, use:
# if config['DATABASE'] == 'sqlite':
#     db = init_db_sqlite()
# else:
#     db = init_db_postgres()
```

### Exemplo: Integrar MongoDB (NoSQL)

```python
from pymongo import MongoClient

def init_db_mongodb():
    """Inicializar MongoDB"""
    
    client = MongoClient('mongodb://localhost:27017')
    db = client['bot_financeiro']
    
    # Coleções (equivalentes a tabelas)
    entries = db['entries']
    banks = db['banks']
    
    # Índices
    entries.create_index('user_id')
    entries.create_index('date')
    
    return {
        'client': client,
        'db': db,
        'entries': entries,
        'banks': banks
    }

# Uso:
# mongodb = init_db_mongodb()
# mongodb['entries'].insert_one({
#     'user_id': '12345',
#     'type': 'despesa',
#     'amount': 50.0,
#     'category': 'Alimentação'
# })
```

---

## 7. Como Adicionar Criptografia

**Arquivo:** `src/utils/encryption.py` (já existe)

### Ativar Criptografia em Production

```python
# Em src/commands/handlers.py

from src.utils.encryption import Encryptor

# Inicializar
ENCRYPTION_KEY = config['ENCRYPTION_KEY']
encryptor = Encryptor(ENCRYPTION_KEY)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE, db):
    # ... código existente ...
    
    # Antes de salvar no banco
    description_encrypted = encryptor.encrypt(descricao)
    
    entry = db['Entry'](
        user_id=user_id,
        type=tipo,
        amount=valor,
        category=categoria,
        description=description_encrypted,  # CRIPTOGRAFADO
        is_encrypted=True
    )
    
    session.add(entry)
    session.commit()

# Ao recuperar do banco
entry = session.query(db['Entry']).first()
if entry.is_encrypted:
    description = encryptor.decrypt(entry.description)
else:
    description = entry.description
```

### Criptografia mais Forte

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
import os
import base64

def generate_strong_key(password: str):
    """Gera chave forte a partir de senha"""
    
    salt = os.urandom(16)
    
    kdf = PBKDF2(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

# Usar com Fernet
key = generate_strong_key("minha_senha_super_secreta")
cipher = Fernet(key)

encrypted = cipher.encrypt(b"dados sensíveis")
decrypted = cipher.decrypt(encrypted)
```

---

## 8. Padrões de Design Utilizados

### 1. **Injeção de Dependência**

```python
from functools import partial

# Como funciona:
def cmd_relatorio(update, context, db):
    # 'db' é injetado
    pass

# Registrar:
app.add_handler(
    CommandHandler('relatorio', partial(cmd_relatorio, db=db))
)
```

**Vantagem:** Facilita testes, permite mock de `db`

### 2. **Padrão Builder**

```python
# Construir mensagens complexas
class MessageBuilder:
    def __init__(self):
        self.lines = []
    
    def add_header(self, text):
        self.lines.append(f"📊 {text}")
        return self
    
    def add_section(self, title, value):
        self.lines.append(f"\n{title}: {value}")
        return self
    
    def build(self):
        return '\n'.join(self.lines)

# Uso:
msg = MessageBuilder() \
    .add_header("RELATÓRIO") \
    .add_section("Receitas", "R$ 1000") \
    .add_section("Despesas", "R$ 500") \
    .build()
```

### 3. **Strategy Pattern**

```python
# Diferentes estratégias de categorização

class Categorizer:
    def __init__(self, strategy):
        self.strategy = strategy
    
    def categorize(self, description):
        return self.strategy.categorize(description)

class HFStrategy:
    def categorize(self, description):
        # Usar API Hugging Face
        pass

class FallbackStrategy:
    def categorize(self, description):
        # Usar keywords
        pass

# Usar:
categorizer = Categorizer(HFStrategy())
# Ou trocar facilmente:
categorizer = Categorizer(FallbackStrategy())
```

### 4. **Repository Pattern**

```python
# Abstração de acesso a dados

class EntryRepository:
    def __init__(self, session, Entry):
        self.session = session
        self.Entry = Entry
    
    def save(self, entry):
        self.session.add(entry)
        self.session.commit()
    
    def find_by_user(self, user_id):
        return self.session.query(self.Entry) \
            .filter_by(user_id=user_id).all()
    
    def find_by_category(self, user_id, category):
        return self.session.query(self.Entry) \
            .filter_by(user_id=user_id, category=category).all()

# Usar:
repo = EntryRepository(session, Entry)
entries = repo.find_by_user('12345')
```

### 5. **Singleton Pattern**

```python
# Uma única instância da configuração

class Config:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
        return cls._instance
    
    def load_config(self):
        # Carregar do .env
        pass

# Usar em qualquer lugar:
config = Config()  # Sempre a mesma instância
```

---

## Resumo de Extensibilidade

| Recurso | Dificuldade | Arquivo | Exemplo |
|---------|------------|---------|---------|
| Novo Comando | ⭐ Fácil | handlers.py | `/help` |
| Nova Categoria | ⭐ Fácil | categorizer.py | "Viagem" |
| Novo Relatório | ⭐⭐ Médio | reports.py | Relatório por tag |
| Novo Banco | ⭐⭐⭐ Difícil | db_*.py | MongoDB |
| Criptografia | ⭐⭐⭐ Difícil | encryption.py | AES-256 |

---

**Documento de extensão criado para fins educacionais de TCC**  
**Demonstra arquitetura extensível e boas práticas de design**

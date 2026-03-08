# 📚 ESTUDOS - Bot Financeiro Telegram

## O que você precisa saber para criar esse bot

---

## 1️⃣ **FUNDAMENTOS PYTHON**

### Conceitos Essenciais:
- **Variáveis e Tipos de Dados**: int, str, float, bool, dict, list
- **Estruturas de Controle**: if/elif/else, for, while
- **Funções**: def, parâmetros, return, *args, **kwargs
- **Orientação a Objetos**: classes, herança, métodos, atributos
- **Módulos e Imports**: create_engine, Session, etc.
- **Tratamento de Erros**: try/except/finally
- **Async/Await**: programação assíncrona (importante para bots)

### Recursos de Estudo:
- [Python Official Docs](https://docs.python.org/3/)
- [Real Python Tutorials](https://realpython.com/)
- Livro: "Automate the Boring Stuff with Python"

---

## 2️⃣ **BANCO DE DADOS (SQL e SQLAlchemy)**

### Conceitos Essenciais:
- **SQL Básico**: SELECT, INSERT, UPDATE, DELETE, WHERE, JOIN
- **Relationships**: Uma para Muitos (One-to-Many), Muitos para Muitos (Many-to-Many)
- **ACID**: Atomicidade, Consistência, Isolamento, Durabilidade
- **ORM (SQLAlchemy)**:
  - `create_engine()`: conectar ao banco
  - `declarative_base()`: criar modelos
  - `sessionmaker()`: gerenciar transações
  - `Column()`, `String`, `Integer`, `DateTime`: definir colunas
  - `Relationship()`: relacionamentos entre tabelas

### Bancos Suportados:
- PostgreSQL: banco robusto para produção
- SQLite: banco simples para desenvolvimento
- MySQL: alternativa comum

### O que você precisa entender:
- Como criar tabelas (modelos)
- Como inserir, ler, atualizar e deletar dados
- Como fazer consultas complexas com filtros
- Transactions (commit/rollback)
- Migrações de schema

### Recursos:
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial.html)
- [SQL Tutorial (W3Schools)](https://www.w3schools.com/sql/)

---

## 3️⃣ **API TELEGRAM (python-telegram-bot)**

### Conceitos Essenciais:
- **Bots Telegram**: como funcionam, o que são
- **Polling vs Webhooks**: duas formas de trazer mensagens
- **Updates**: eventos (mensagens, cliques em botões, etc.)
- **Handlers**: como processar diferentes tipos de atualizações
- **MessageHandler**: capturar mensagens de texto
- **CommandHandler**: processar comandos (/start, /help, etc.)
- **CallbackQueryHandler**: processar cliques em botões
- **InlineKeyboardButton e InlineKeyboardMarkup**: criar botões interativos

### Estrutura Básica de um Bot:
```python
from telegram.ext import Application, CommandHandler, MessageHandler, filters

async def start(update, context):
    await update.message.reply_text("Olá!")

app = Application.builder().token("SEU_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()
```

### O que você precisa aprender:
- Como criar um bot no BotFather
- Usar tokens de forma segura
- Processar diferentes tipos de mensagens
- Respond com texto, fotos, documentos
- Criar menus interativos com botões
- Persistir estado do usuário (context.user_data)

### Recursos:
- [python-telegram-bot Documentation](https://python-telegram-bot.readthedocs.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [Telegram Developer Documentation](https://core.telegram.org/)

---

## 4️⃣ **ARQUITETURA E PADRÕES DE PROJETO**

### Padrões Usados Neste Bot:
- **MVC (Model-View-Controller)**: 
  - Models: `src/models/db.py` (Entry, Bank)
  - Views: handlers do Telegram
  - Controller: `src/commands/handlers.py`

- **Factory Pattern**: `db['Session']` cria novas sessões do banco

- **Async/Await Pattern**: bots precisam ser não-bloqueantes

### Conceitos:
- **Separação de Responsabilidades**: cada arquivo tem um propósito
- **DRY (Don't Repeat Yourself)**: reutiliza funções comuns
- **Configuration Management**: usar `.env` para senhas/tokens
- **Logging**: rastreamento de erros e eventos

---

## 5️⃣ **VARIÁVEIS DE AMBIENTE (.env)**

### Por que usar:
- Nunca colocar senhas/tokens no código
- Permite diferentes configs para dev/production
- Segurança: arquivos .env não são commitados no git

### Ferramentas:
- `python-dotenv`: carrega `.env` em `os.environ`

### Exemplo:
```python
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("BOT_TOKEN")  # lê de .env
```

---

## 6️⃣ **CRIPTOGRAFIA (cryptography)**

### Conceitos:
- **Criptografia Simétrica**: mesma chave para encriptar/decriptar
- **Hashing**: transformação unilateral (não pode voltar)
- **Salting**: adicionar randomicidade ao hash

### Por que neste bot:
- Proteger dados financeiros sensíveis
- Garantir privacidade do usuário

### O que aprender:
- Como encriptar/decriptar dados
- Como fazer hash de senhas
- Boas práticas de segurança

### Recursos:
- [Cryptography Library](https://cryptography.io/)

---

## 7️⃣ **DEPLOYMENT E EXECUÇÃO EM BACKGROUND**

### Windows:
- **Task Scheduler**: agendar tarefas
- **VBS Scripts**: executar sem janela
- **batch files (.bat)**: scripts simples

### Linux/Mac:
- **systemd**: gerenciar serviços
- **cron**: agendar tarefas
- **nohup/screen/tmux**: manter processos rodando

### Cloud:
- **Docker**: containerização
- **AWS/Azure/GCP**: hospedagem
- **Heroku/Railway**: serviços simplificados

### O que você precisa:
- Entender como processos rodam em background
- Como manter um bot sempre online
- Como gerenciar logs
- Como atualizar sem derrubar o bot

---

## 8️⃣ **GIT E VERSIONAMENTO**

### Conceitos:
- **Commits**: salvar mudanças com mensagens
- **Branches**: linhas de desenvolvimento separadas
- **.gitignore**: o que NÃO versionar
- **Push/Pull**: sincronizar com repositório remoto

### Boas Práticas:
- Commit pequenos e focados
- Mensagens descritivas
- Não commitar senhas/tokens
- Teste antes de fazer commit

### Ferramentas:
- `git`: controle de versão
- GitHub/GitLab: repositórios remotos

---

## 9️⃣ **REGULAR EXPRESSIONS (Regex)**

### Conceitos:
- **Padrões de texto**: buscar, validar, extrair dados
- **Grupos de captura**: `()`
- **Quantificadores**: `*`, `+`, `?`, `{n}`
- **Character classes**: `[]`, `\d`, `\w`, `\s`

### Exemplo neste bot:
```python
import re
match = re.search(r'(\d+(?:[.,]\d+)?)\s+(.+)', "50 pizza")
# Captura: "50" e "pizza"
```

### Recursos:
- [Regex101.com](https://regex101.com/) - playground online
- [Python re module](https://docs.python.org/3/library/re.html)

---

## 🔟 **CONCEITOS FINANCEIROS**

### Básicos:
- **Receita**: dinheiro entrando
- **Despesa**: dinheiro saindo
- **Saldo/Balanço**: total atual
- **Categoria**: agrupamento de transações
- **Relatório**: resumo de dados

### Para este bot:
- Rastreamento de transações
- Cálculo de saldo
- Categorização automática
- Geração de relatórios

---

## 📋 **ROADMAP DE ESTUDO RECOMENDADO**

### Semana 1-2: Python Básico
- [ ] Variáveis e tipos
- [ ] Estruturas de controle
- [ ] Funções
- [ ] Listas e dicts
- [ ] Tratamento de erros

### Semana 3-4: Banco de Dados
- [ ] SQL básico
- [ ] SQLAlchemy ORM
- [ ] Criar e gerenciar tabelas
- [ ] Consultas com filtros

### Semana 5: Telegram API
- [ ] Criar bot no BotFather
- [ ] Handlers básicos
- [ ] Processar mensagens
- [ ] Botões interativos

### Semana 6: Integração
- [ ] Conectar bot com banco
- [ ] Criptografia básica
- [ ] Variáveis de ambiente
- [ ] Regex para parsing

### Semana 7: Deployment
- [ ] Executar em background
- [ ] Task Scheduler/systemd
- [ ] Docker basics
- [ ] Deploy em servidor

### Semana 8: Melhorias e Polish
- [ ] Testes
- [ ] Logging
- [ ] Tratamento de erros melhorado
- [ ] Documentação

---

## 🛠️ **FERRAMENTAS ESSENCIAIS**

### Desenvolvimento:
- **VS Code**: editor de código
- **Python 3.9+**: linguagem
- **pip/venv**: gerenciador de pacotes

### Banco de Dados:
- **PostgreSQL**: banco principal
- **pgAdmin**: interface gráfica
- **DBeaver**: cliente universal

### Debugging:
- **pdb**: debugger do Python
- **print statements**: logging simples
- **logging module**: logging profissional

### Versionamento:
- **Git**: controle de versão
- **GitHub**: repositório remoto

---

## 📚 **RECURSOS COMPLEMENTARES**

### YouTube Channels:
- [Corey Schafer Python Tutorials](https://www.youtube.com/@coreyms)
- [Traversy Media](https://www.youtube.com/@TraversyMedia)
- [Real Python](https://www.youtube.com/@realpython)

### Comunidades:
- Stack Overflow
- Reddit: r/learnprogramming, r/Python
- Discord: comunidades de programação

### Cursos Online:
- [Udemy Python Courses](https://www.udemy.com/courses/search/?q=python)
- [Codecademy](https://www.codecademy.com/)
- [freeCodeCamp](https://www.freecodecamp.org/)

---

## ✅ **CHECKLIST: Você está pronto quando consegue:**

- [ ] Escrever funções e usar orientação a objetos
- [ ] Criar modelos SQLAlchemy e fazer queries
- [ ] Criar um bot simples que responde mensagens
- [ ] Conectar bot com banco de dados
- [ ] Fazer deploy em outro computador/servidor
- [ ] Entender e explicar todo o código do projeto
- [ ] Modificar e estender o bot com novas funcionalidades

---

**Boa sorte nos estudos! 🚀**


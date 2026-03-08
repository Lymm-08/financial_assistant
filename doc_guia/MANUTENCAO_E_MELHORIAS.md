# 🔧 MANUTENÇÃO E MELHORIAS - Bot Financeiro

## 📋 TUTORIAIS PRÁTICOS DE MANUTENÇÃO

---

## 🔄 MANUTENÇÃO SEMANAL - PASSO A PASSO

### 1️⃣ **Verificar logs de erro** 🔍

**Objetivo:** Identificar problemas no bot antes que afetem usuários

**Como fazer:**

```bash
# 📂 Navegar para pasta do projeto
cd c:\bot_financeiro

# 📄 Abrir arquivo de logs (se existir)
type logs\bot_financeiro.log

# 🔍 Procurar por erros críticos nos últimos 7 dias
# (Use PowerShell ou Command Prompt)
Get-Content logs\bot_financeiro.log | Select-String "ERROR|CRITICAL" | Select-Object -Last 20
```

**O que verificar:**
- ❌ Erros de API do Telegram
- ❌ Falhas de conexão com banco
- ❌ Timeouts de resposta
- ❌ Problemas de categorização

**Ação se encontrar erros:**
- 📧 Anotar data/hora do erro
- 🔧 Verificar se problema persiste
- 📝 Documentar para correção

---

### 2️⃣ **Verificar status do banco de dados** 🗄️

**Objetivo:** Garantir que o banco está saudável e não está crescendo demais

**Como fazer:**

```bash
# 🐘 Abrir PostgreSQL (se tiver pgAdmin ou similar)
# Ou usar linha de comando:

# 📊 Ver tamanho do banco
psql postgresql://postgres:nina2024@localhost:5432/bot_financeiro -c "SELECT pg_size_pretty(pg_database_size('bot_financeiro'));"

# 📈 Contar registros
psql postgresql://postgres:nina2024@localhost:5432/bot_financeiro -c "SELECT COUNT(*) FROM entries;"
psql postgresql://postgres:nina2024@localhost:5432/bot_financeiro -c "SELECT COUNT(*) FROM banks;"

# 👥 Ver usuários ativos (última transação nos últimos 30 dias)
psql postgresql://postgres:nina2024@localhost:5432/bot_financeiro -c "SELECT user_id, COUNT(*) as transacoes FROM entries WHERE date >= CURRENT_DATE - INTERVAL '30 days' GROUP BY user_id ORDER BY transacoes DESC;"
```

**O que fazer se banco estiver grande:**
- 📦 Considerar arquivar dados antigos (> 2 anos)
- 🔄 Criar tabelas de histórico separadas
- 📊 Otimizar queries se necessário

---

## 🗓️ MANUTENÇÃO MENSAL - TUTORIAL COMPLETO

### 1️⃣ **Limpar cache e arquivos temporários** 🧹

**Por que fazer:** Python cria arquivos .pyc que podem causar conflitos

**Como fazer:**

```bash
# 📂 Ir para pasta do projeto
cd c:\bot_financeiro

# 🗑️ Remover cache do Python (Windows PowerShell)
Remove-Item -Path "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\commands\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\models\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\services\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "src\utils\__pycache__" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "*.pyc" -Force -ErrorAction SilentlyContinue

# ✅ Verificar se limpou
dir __pycache__ 2>nul || echo "Cache limpo com sucesso!"
```

---

### 2️⃣ **Fazer backup do banco de dados** 💾

**Por que fazer:** Proteger dados contra perdas

**Como fazer:**

```powershell
# 📅 Pegar data atual
$data = Get-Date -Format "yyyy-MM-dd_HH-mm"

# 💾 Criar backup
pg_dump postgresql://postgres:nina2024@localhost:5432/bot_financeiro > "backup_$data.sql"

# 📂 Mover para pasta segura
if (!(Test-Path "backups")) { New-Item -ItemType Directory -Path "backups" }
Move-Item "backup_$data.sql" "backups\"

# 📋 Listar backups existentes
Get-ChildItem backups\*.sql | Sort-Object LastWriteTime -Descending | Select-Object Name, LastWriteTime
```

**Dicas:**
- 📦 Manter últimos 12 backups
- ☁️ Upload para Google Drive/Dropbox
- 📱 Backup automático com script

---

### 3️⃣ **Atualizar dependências** 📦

**Por que fazer:** Correções de segurança e novos recursos

**Como fazer:**

```bash
# 📋 Verificar atualizações disponíveis
pip list --outdated

# 🔄 Atualizar requirements.txt (com cuidado!)
pip install --upgrade pip
pip install --upgrade -r requirements.txt

# 🧪 Testar se bot ainda funciona
python -c "import telegram; import sqlalchemy; print('✅ Dependências OK')"

# 🔄 Reiniciar bot se tudo estiver funcionando
# (matar processo antigo e iniciar novo)
```

**Cuidado:** Algumas atualizações podem quebrar compatibilidade!

---

### 4️⃣ **Analisar uso da API Hugging Face** 🤖

**Por que fazer:** Controlar custos da IA

**Como fazer:**

```bash
# 📊 Contar chamadas da API nos logs
Get-Content logs\bot_financeiro.log | Select-String "Query Hugging Face" | Measure-Object | Select-Object Count

# 📈 Ver uso por dia
Get-Content logs\bot_financeiro.log | Select-String "Query Hugging Face" | ForEach-Object {
    $date = $_.Line -replace '.*(\d{4}-\d{2}-\d{2}).*', '$1'
    [PSCustomObject]@{Date=$date; Count=1}
} | Group-Object Date | Select-Object Name, Count | Sort-Object Name -Descending

# 💰 Calcular custo aproximado (HF tem quota gratuita)
# Se > 1000 chamadas/mês, considerar plano pago
```

---

## 📅 MANUTENÇÃO TRIMESTRAL - GUIA DETALHADO

### 1️⃣ **Revisar e atualizar .env** 🔐

**Como fazer:**

```bash
# 📄 Abrir arquivo .env
notepad .env

# 🔍 Verificar cada linha:
# BOT_TOKEN: Ainda válido? (testar no Telegram)
# DB_URI: Credenciais corretas?
# HF_API_TOKEN: Ainda funciona?

# 🔄 Se necessário, gerar novos tokens:
# - BotFather (@BotFather) para BOT_TOKEN
# - huggingface.co/settings/tokens para HF_API_TOKEN

# 💾 Salvar e testar
python -c "from dotenv import load_dotenv; load_dotenv(); print('✅ .env carregado')"
```

---

### 2️⃣ **Testar todas as funcionalidades** 🧪

**Como fazer:**

```bash
# 🆕 Criar usuário de teste no Telegram
# (conta separada ou pedir para alguém testar)

# ✅ Testes a fazer:
# 1. /start - Mensagem de boas-vindas aparece?
# 2. Registrar transação: "50 pizza" - Funciona?
# 3. /relatorio simples - Gera relatório?
# 4. /relatorio completo - Detalhado funciona?
# 5. /reset - Limpa dados?
# 6. Reset mensal - Muda mês automaticamente?

# 📝 Documentar problemas encontrados
```

---

### 3️⃣ **Revisar requisitos de segurança** 🔒

**Como fazer:**

```bash
# 🔍 Verificar se .env não foi commitado
git log --oneline --all -- ".env"

# 🛡️ Verificar criptografia de dados
python -c "
from src.models.db import Entry
# Verificar se campos sensíveis estão criptografados
print('✅ Segurança básica verificada')
"

# 🔐 Testar tokens
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
print('BOT_TOKEN:', '***' + os.getenv('BOT_TOKEN')[-10:] if os.getenv('BOT_TOKEN') else '❌ FALTANDO')
print('HF_TOKEN:', '***' + os.getenv('HF_API_TOKEN')[-10:] if os.getenv('HF_API_TOKEN') else '❌ FALTANDO')
"
```

---

## 🐛 MANUTENÇÃO CORRETIVA - SOLUÇÃO DE PROBLEMAS

### ❌ **Bot não responde**

**Sintomas:** Usuários reclamam que bot não funciona

**Como diagnosticar:**

```bash
# 🔍 1. Verificar se processo está rodando
Get-Process python -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*main.py*"}

# 📊 2. Ver logs recentes
Get-Content logs\bot_financeiro.log -Tail 20

# 🔄 3. Reiniciar bot
# Matar processos antigos
Stop-Process -Name python -ErrorAction SilentlyContinue

# Iniciar novo
python main.py
```

---

### ❌ **Erro ao conectar ao banco de dados**

**Sintomas:** Bot funciona mas não salva dados

**Como resolver:**

```bash
# 🐘 1. Verificar se PostgreSQL está rodando
# Windows: services.msc > procurar "postgresql"
# Ou: pg_isready -h localhost -p 5432

# 🔑 2. Testar conexão
psql postgresql://postgres:nina2024@localhost:5432/bot_financeiro -c "SELECT 1;"

# 📄 3. Verificar .env
type .env | findstr "DB_URI"

# 🔧 4. Se erro de autenticação, resetar senha PostgreSQL
```

---

### ❌ **Categorização falhando**

**Sintomas:** Transações aparecem como "Outros"

**Como resolver:**

```bash
# 🤖 1. Verificar token Hugging Face
python -c "
import os
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('HF_API_TOKEN')
print('Token existe:', bool(token))
"

# 🌐 2. Testar conectividade
curl -H "Authorization: Bearer $HF_TOKEN" https://api-inference.huggingface.co/models/google/flan-t5-base

# 🔄 3. Bot usa fallback automático (OK!)
# Se IA falhar, usa regras por palavras-chave
```

---

## 💡 IDEIAS DE MELHORIA - IMPLEMENTAÇÃO PRÁTICA

### 🎯 CURTO PRAZO (1-2 meses)

#### 1️⃣ **Gráficos de gastos** 📊

**Como implementar:**

```python
# 📁 Editar src/services/reports.py
# Adicionar função gerar_grafico()

def gerar_grafico(user_id, tipo='mes'):
    # Usar matplotlib para criar gráfico
    import matplotlib.pyplot as plt

    # Buscar dados do usuário
    session = db['Session']()
    entries = session.query(db['Entry']).filter_by(user_id=user_id).all()

    # Criar gráfico de pizza por categoria
    categorias = {}
    for entry in entries:
        categorias[entry.category] = categorias.get(entry.category, 0) + entry.amount

    plt.pie(categorias.values(), labels=categorias.keys())
    plt.savefig('grafico.png')

    # Enviar no Telegram
    # await update.message.reply_photo(open('grafico.png', 'rb'))

# 📝 Comando: /graficos mes
```

---

#### 2️⃣ **Orçamento mensal** 💳

**Como implementar:**

```python
# 📁 Adicionar em src/models/db.py
class Orcamento(Base):
    __tablename__ = 'orcamentos'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    categoria = Column(String(100))
    limite = Column(Float)
    mes = Column(Integer)
    ano = Column(Integer)

# 📝 Comando: /orcamento Alimentacao 800
# Bot: "Orçamento definido: R$ 800 para Alimentação"
# Quando atingir 80%: "⚠️ Você já gastou 80% do orçamento de Alimentação!"
```

---

#### 3️⃣ **Exportar dados** 📥

**Como implementar:**

```python
# 📁 Adicionar em src/services/reports.py
import csv

def exportar_dados(user_id, formato='csv'):
    session = db['Session']()
    entries = session.query(db['Entry']).filter_by(user_id=user_id).all()

    with open(f'dados_{user_id}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Data', 'Tipo', 'Valor', 'Categoria', 'Descrição'])

        for entry in entries:
            writer.writerow([
                entry.date.strftime('%Y-%m-%d'),
                entry.type,
                entry.amount,
                entry.category,
                entry.description
            ])

    # Enviar arquivo via Telegram
    # await update.message.reply_document(open(f'dados_{user_id}.csv', 'rb'))

# 📝 Comando: /exportar mes
```

---

### 🎯 MÉDIO PRAZO (3-6 meses)

#### 4️⃣ **Categorias customizadas** 🏷️

**Como implementar:**

```python
# 📁 Adicionar tabela em src/models/db.py
class CustomCategory(Base):
    __tablename__ = 'custom_categories'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    nome = Column(String(100))
    emoji = Column(String(10))

# 📝 Comandos:
# /categorias add Streaming 📺
# /categorias list
# /categorias remove Streaming
```

---

#### 5️⃣ **Metas e objetivos** 🎯

**Como implementar:**

```python
# 📁 Adicionar em src/models/db.py
class Meta(Base):
    __tablename__ = 'metas'
    id = Column(Integer, primary_key=True)
    user_id = Column(String(50))
    descricao = Column(String(200))
    valor_total = Column(Float)
    valor_atual = Column(Float)
    data_limite = Column(DateTime)

# 📝 Comando: /meta "Viagem para praia" 2000 2024-12-31
# Bot responde progresso semanalmente
```

---

### 🎯 LONGO PRAZO (6-12 meses)

#### 6️⃣ **IA mais inteligente** 🤖

**Como implementar:**

```python
# 📁 Melhorar src/ai/categorizer.py
# Adicionar aprendizado com histórico do usuário

def aprender_padroes(user_id):
    # Analisar histórico do usuário
    # Criar regras personalizadas
    # Fine-tuning do modelo com dados do usuário
    pass

# 📝 Resultado: Bot aprende que "pizza" = Lazer para usuário X
# Sugere: "Gastou R$ 150 em lazer este mês, 20% acima da média"
```

---

## 📋 CHECKLIST DE MANUTENÇÃO

### 🔄 Semanal
- [ ] Verificar logs de erro
- [ ] Status do banco de dados

### 🗓️ Mensal
- [ ] Limpar cache Python
- [ ] Backup do banco
- [ ] Atualizar dependências
- [ ] Analisar uso da API

### 📅 Trimestral
- [ ] Revisar .env e tokens
- [ ] Testar funcionalidades
- [ ] Verificar segurança

### 🐛 Quando der erro
- [ ] Diagnosticar problema
- [ ] Aplicar solução específica
- [ ] Testar correção
- [ ] Documentar para futuro

---

**🚀 Mantenha seu bot sempre saudável!**

#### 8. **Integração com bancos** 🏦
```python
# Conectar com API do seu banco
# Importar transações automaticamente
# Conciliar com dados manuais
```

#### 9. **App web/mobile** 💻📱
```python
# Dashboard web (Flask/FastAPI)
# App mobile (React Native)
# Sincronizar com Telegram bot
```

#### 10. **Notificações inteligentes** 🔔
```python
# Avisos: "Você gastou 50 com streaming'
# Lembretes: "Falta registrar despesa de segunda"
# Resumos: "Economizou 200 em relação mês passado"
```

---

## 🛠️ PROCEDIMENTO DE MANUTENÇÃO PASSO A PASSO

### **Passo 1: Parar o bot com segurança**
```bash
# No Terminal onde bot está rodando:
Ctrl + C

# Aguardar: "Bot Financeiro encerrado"
```

### **Passo 2: Ativar backup**
```bash
# Fazer backup do banco
$data = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
pg_dump postgresql://user:pass@localhost/bot_financeiro > "backup_$data.sql"
```

### **Passo 3: Aplicar mudanças**
```bash
# Se alterou código:
git add .
git commit -m "manutencao: descrição das mudanças"

# Se atualizou dependências:
pip install --upgrade -r requirements.txt
```

### **Passo 4: Testar mudanças**
```bash
# Rodar testes
python -m pytest  # se tiver testes

# Ou rodar manual
python teste_db.py
```

### **Passo 5: Reiniciar bot**
```bash
python main.py
# Verificar se inicializou: "🚀 Bot Financeiro iniciado!"
```

### **Passo 6: Monitorar**
```bash
# Deixar rodando por 10-15 minutos
# Enviar mensagem teste no Telegram
# Verificar se logs limparam normalmente
```

---

## 📊 CHECKLIST DE SAÚDE DO BOT

Use semanalmente:

```
[ ] Bot respondendo aos comandos
[ ] Banco de dados conectado
[ ] Categorização funcionando
[ ] Relatórios gerando corretamente
[ ] Sem erros críticos nos logs
[ ] Nenhuma mensagem fica "travada"
[ ] Novo usuário consegue inserir saldo
[ ] Pode fazer registros normalmente
[ ] Reset mensal funcionando
[ ] API Hugging Face respondendo

Adicione data: ___/___/_____
```

---

## 🚨 QUANDO CHAMAR DESENVOLVEDOR

- ❌ Bot não inicia mesmo após reiniciar
- ❌ Banco de dados corrompido
- ❌ Falha de segurança (Token vazado)
- ❌ Mais de 5 erros críticos/dia
- ❌ Performance caiu drasticamente
- ❌ Comportamento estranho não documentado

---

## 📚 REFERÊNCIAS ÚTEIS

- PostgreSQL Docs: [postgresql.org/docs](https://www.postgresql.org/docs/)
- python-telegram-bot: [ptbdocs.readthedocs.io](https://docs.python-telegram-bot.org/)
- Hugging Face API: [huggingface.co/docs/api](https://huggingface.co/docs/api-inference)

---

**Última atualização:** 07/03/2026 ✅ 
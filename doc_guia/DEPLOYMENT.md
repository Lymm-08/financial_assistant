# 🚀 DEPLOYMENT - Bot Financeiro

## Como instalar e rodar o bot em qualquer lugar

---

## 📋 REQUISITOS MÍNIMOS

Antes de começar, você precisa de:

- **Python 3.9+** instalado
- **PostgreSQL** instalado e rodando
- **Token do Telegram Bot** (do @BotFather)
- **Acesso a terminal/CMD**

### Verificar versões:
```bash
python --version
psql --version
```

---

## 🔧 INSTALAÇÃO (Primeira Vez)

### 1️⃣ Clonar ou baixar o projeto

```bash
# Se estiver no Git
git clone <seu-repositorio-url>
cd bot_financeiro

# Ou extrair o arquivo ZIP
unzip bot_financeiro.zip
cd bot_financeiro
```

### 2️⃣ Configurar variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```bash
# Linux/Mac
touch .env
nano .env

# Windows (PowerShell)
New-Item -Path ".env" -ItemType File
notepad .env
```

**Conteúdo do `.env`:**

```ini
# Token do seu Bot Telegram
BOT_TOKEN=seu_token_aqui_do_botfather

# String de conexão PostgreSQL
DB_URI=postgresql://usuario:senha@localhost:5432/bot_financeiro

# Debug (True/False)
DEBUG=False
```

### 3️⃣ Criar banco de dados PostgreSQL

```bash
# Conectar ao PostgreSQL
psql -U postgres

# Dentro do PostgreSQL
CREATE DATABASE bot_financeiro;
EXIT;
```

### 4️⃣ Instalar Python dependencies

```bash
# Criar virtual environment
python -m venv .venv

# Ativar (Windows - Command Prompt)
.venv\Scripts\activate

# Ativar (Windows - PowerShell)
.venv\Scripts\Activate.ps1

# Ativar (Linux/Mac)
source .venv/bin/activate

# Instalar packages
pip install -r requirements.txt
```

---

## ⚡ EXECUTAR O BOT

### Opção 1: Modo de Desenvolvimento (com terminal visível)

```bash
python main.py
```

Você verá os logs em tempo real. Pressione `Ctrl+C` para parar.

---

### Opção 2: Modo Background (sem terminal visível) - Recomendado para Produção

#### **Windows:**

```bash
# Opção A: Usar run_bot.bat (mais simples)
run_bot.bat

# Opção B: Usar script Python (universalista)
python run_bot_background.py
```

**Para verificar se está rodando:**
1. Pressione `Ctrl+Shift+Esc` (Task Manager)
2. Procure por `python.exe`
3. Se estiver lá, o bot está rodando!

**Para parar:**
```bash
taskkill /IM python.exe
# Ou use Task Manager e finalize
```

---

#### **Linux / macOS:**

```bash
# Dar permissão ao script
chmod +x run_bot.sh

# Executar em background
./run_bot.sh
```

**Para verificar se está rodando:**
```bash
ps aux | grep main.py
# Ou
pgrep -f "main.py"
```

**Ver logs:**
```bash
tail -f bot_financeiro.log
```

**Para parar:**
```bash
pkill -f "main.py"
```

---

## 🌍 DEPLOYMENT EM SERVIDOR (Linux/Cloud)

### Opção 1: Systemd (Recomendado para servidores Linux)

Criar um serviço que inicia automaticamente:

```bash
# Criar arquivo de serviço
sudo nano /etc/systemd/system/bot-financeiro.service
```

**Cole este conteúdo:**

```ini
[Unit]
Description=Bot Financeiro Telegram
After=network.target postgresql.service

[Service]
Type=simple
User=seu_usuario_aqui
WorkingDirectory=/home/seu_usuario/bot_financeiro
ExecStart=/home/seu_usuario/bot_financeiro/.venv/bin/python main.py
Restart=always
RestartSec=10
Environment="PATH=/home/seu_usuario/bot_financeiro/.venv/bin"

[Install]
WantedBy=multi-user.target
```

**Ativar o serviço:**

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Ativar para iniciar na boot
sudo systemctl enable bot-financeiro

# Iniciar agora
sudo systemctl start bot-financeiro

# Ver status
sudo systemctl status bot-financeiro

# Ver logs
sudo journalctl -u bot-financeiro -f
```

---

### Opção 2: Cron (Agendador de tarefas)

Iniciar bot automaticamente na reinicialização:

```bash
# Editar crontab
crontab -e

# Adicionar esta linha:
@reboot cd /home/seu_usuario/bot_financeiro && source .venv/bin/activate && nohup python main.py &
```

---

### Opção 3: Docker (Containerização)

Criar arquivo `Dockerfile` na raiz:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
```

**Construir e rodar:**

```bash
# Build da imagem
docker build -t bot-financeiro .

# Rodar container
docker run -d \
  --name bot_financeiro \
  --env-file .env \
  bot-financeiro
```

---

## 📊 MONITORAMENTO

### Ver se o bot está rodando

**Windows:**
```bash
tasklist | findstr python
```

**Linux/Mac:**
```bash
ps aux | grep main.py
pgrep -f "main.py" | wc -l  # Conta quantos estão rodando
```

### Verificar conectividade com banco de dados

```bash
# Windows
psql -U postgres -d bot_financeiro -c "SELECT * FROM banks LIMIT 1;"

# Linux/Mac
psql -U postgres -d bot_financeiro -c "SELECT * FROM banks LIMIT 1;"
```

### Ver logs em tempo real

**Linux/Mac:**
```bash
tail -f bot_financeiro.log
```

**Windows (PowerShell):**
```powershell
Get-Content bot_financeiro.log -Wait
```

---

## 🔧 TROUBLESHOOTING

### ❌ "ModuleNotFoundError: No module named 'telegram'"

**Solução:**
```bash
# Certifique-se que o venv está ativado
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Reinstale dependências
pip install -r requirements.txt
```

---

### ❌ "Erro ao conectar ao banco: connection refused"

**Solução:**
```bash
# Verifique se PostgreSQL está rodando
psql -U postgres

# Verifique credenciais em .env
# Certifique-se que o banco existe
psql -U postgres -c "SELECT datname FROM pg_database WHERE datname='bot_financeiro';"
```

---

### ❌ "ERRO: BOT_TOKEN não definido"

**Solução:**
```bash
# Verifique se arquivo .env existe
ls -la .env

# Verifique se tem BOT_TOKEN
cat .env | grep BOT_TOKEN

# Obtém token novo do @BotFather no Telegram
```

---

### ❌ "Error while getting Updates: Conflict: terminated by other getUpdates request"

**Solução:**
Está rodando dois bots com o mesmo token. Feche todas as instâncias:

```bash
# Windows
taskkill /F /IM python.exe

# Linux/Mac
pkill -f "main.py"

# Aguarde 10 segundos e inicie novamente
```

---

## 🔐 SEGURANÇA

### Nunca commitar .env

Verificar `.gitignore`:
```bash
cat .gitignore | grep ".env"
```

Se não tiver, adicione:
```bash
echo ".env" >> .gitignore
```

### Usar senhas fortes

No `DB_URI`:
- ✅ `postgresql://user:SenhaForte123!@localhost:5432/bot`
- ❌ `postgresql://user:123@localhost:5432/bot`

### Variáveis de ambiente em servidor

Não colocar `.env` no repositório. Em produção, definir variáveis:

**Linux/Systemd:**
```ini
Environment="BOT_TOKEN=seu_token"
Environment="DB_URI=postgresql://..."
```

**Docker:**
```bash
docker run -e BOT_TOKEN=token -e DB_URI=uri ...
```

---

## 📈 ESCALABILIDADE

Para múltiplos bots ou instâncias:

1. **Usar database pool**: SQLAlchemy com pool_size configurado
2. **Load balancer**: nginx/HAProxy para distribuir carga
3. **Kubernetes**: orquestração avançada de containers
4. **Redis**: cache e fila de mensagens

---

## ✅ CHECKLIST DE DEPLOYMENT

- [ ] Python 3.9+ instalado
- [ ] PostgreSQL instalado e rodando
- [ ] Clone/download do projeto
- [ ] Arquivo `.env` criado com credenciais
- [ ] `pip install -r requirements.txt` executado
- [ ] Bot token obtido do @BotFather
- [ ] Banco de dados criado
- [ ] Bot funciona em modo desenvolvimento (`python main.py`)
- [ ] Bot testado em modo background
- [ ] Logs são visualizáveis
- [ ] Sistema de parada/reinício configurado

---

## 📞 SUPORTE

Para reportar problemas:
1. Verifique os logs: `tail -f bot_financeiro.log`
2. Confirme variáveis: `.env` correto
3. Teste conectividade: `psql -U postgres`
4. Reinicie o serviço

---

**Deployment bem-sucedido! 🎉**


# 🔧 MANUTENÇÃO E MELHORIAS - Bot Financeiro

## 📋 MANUTENÇÕES NECESSÁRIAS

### 🔄 MANUTENÇÃO SEMANAL

#### 1. Verificar logs de erro
```bash
# Abrir arquivo de logs
cat logs/bot_financeiro.log

# Procurar por erros críticos
grep "ERROR\|CRITICAL" logs/bot_financeiro.log
```
**O que verificar:** Erros de API, falhas de banco de dados, timeouts

---

#### 2. Verificar status do banco de dados
```bash
# Conectar ao PostgreSQL via psql
psql postgresql://seu_usuario:sua_senha@localhost:5432/bot_financeiro

# Ver tamanho do banco
SELECT pg_size_pretty(pg_database_size('bot_financeiro'));

# Contar transações
SELECT COUNT(*) FROM entries;
SELECT COUNT(*) FROM banks;
```
**O que fazer:** Se crescer muito, considerar arquivar dados antigos

---


### 🗓️ MANUTENÇÃO MENSAL

#### 1. Limpar cache e arquivos temporários
```bash
cd c:\bot_financeiro
Remove-Item __pycache__ -Recurse -Force
Remove-Item src\__pycache__ -Recurse -Force
Remove-Item *.pyc -Force
```

#### 2. Fazer backup do banco de dados
```bash
# Windows PowerShell
$data = Get-Date -Format "yyyy-MM-dd"
pg_dump postgresql://user:pass@localhost:5432/bot_financeiro > "backup_$data.sql"
```

#### 3. Atualizar dependências
```bash
# Ver quais pacotes precisam atualização
pip list --outdated

# Atualizar tudo (com cuidado!)
pip install --upgrade -r requirements.txt
```

---

#### 4. Analisar uso da API Hugging Face
```bash
# Contar quantas vezes a API foi chamada (ver logs)
grep "Query Hugging Face" logs/bot_financeiro.log | wc -l

# Se > 1000/mês, considerar plano pago
```

---

### 📅 MANUTENÇÃO TRIMESTRAL

#### 1. Revisar e atualizar `.env`
```bash
# Verificar se tokens ainda são válidos
# Regenerar BOT_TOKEN se suspeitar comprometimento
# Verificar API_KEY da Hugging Face
```

#### 2. Testar todas as funcionalidades
```bash
# Criar novo usuário de teste
# Registrar receita/despesa
# Gerar relatórios
# Testar reset mensal
# Testar categorização
```

#### 3. Revisar requisitos de segurança
```python
# Verificar se senhas estão criptografadas
# Validar que .env não foi commitado no Git
# Confirmar que dados sensíveis estão protegidos
```

---

### 🐛 MANUTENÇÃO CORRETIVA (quando der erro)

#### Erro: "Bot não responde"
```bash
# 1. Verificar se o bot está rodando
Get-Process python | Where-Object {$_.Name -like "*main*"}

# 2. Reiniciar o bot
# Fechar terminal e rodar novamente:
python main.py

# 3. Ver logs de erro
tail -20 logs/bot_financeiro.log
```

#### Erro: "Erro ao conectar ao banco de dados"
```bash
# 1. Verificar se PostgreSQL está rodando
pg_isready -h localhost -p 5432

# 2. Conferir credenciais em .env
# 3. Testar conexão direta
psql postgresql://seu_usuario:sua_senha@localhost:5432/bot_financeiro
```

#### Erro: "Categorização falhando"
```bash
# 1. Verificar se API_KEY da Hugging Face está válida
# 2. Checar quota de requisições (status.huggingface.co)
# 3. Bot usa fallback automático por palavras-chave (está protegido!)
```

---

## 💡 IDEIAS DE MELHORIA

### 🎯 CURTO PRAZO (1-2 meses)

#### 1. **Gráficos de gastos** 📊
```python
# Adicionar em src/services/reports.py
# Usar biblioteca matplotlib ou plotly
# Gerar gráficos por categoria, mês, semana
# Enviar como imagem no Telegram

# Comando: /graficos mes
# Resposta: Imagem com pizza/barras de despesas
```

#### 2. **Orçamento mensal** 💳
```python
# Adicionar recurso de definir limite de gastos
# Avisar quando atingir 80% do orçamento
# Comando: /orcamento 3000
# Bot monitora e alerta antes de estourar
```

#### 3. **Exportar dados** 📥
```python
# Gerar CSV/Excel com todas as transações
# Comando: /exportar mes
# Bot envia arquivo prontos para análise em Excel
```

---

### 🎯 MÉDIO PRAZO (3-6 meses)

#### 4. **Categorias customizadas** 🏷️
```python
# Permitir usuário criar suas próprias categorias
# Ex: /categorias add Streaming
# Banco de dados em models/db.py: adicionar tabela CustomCategory
# Bot aprender com padrões do usuário
```

#### 5. **Metas e objetivos** 🎯
```python
# Usuario define: "Quero economizar 500/mês para viagem"
# Bot acompanha progresso
# Envia resumo semanal de quanto falta
```

#### 6. **Integração com múltiplos usuários** 👥
```python
# Forma grupos (casal, família)
# Compartilhar despesas
# Cada um tem saldo individual mas veem total grupal
```

---

### 🎯 LONGO PRAZO (6-12 meses)

#### 7. **IA mais inteligente** 🤖
```python
# Fine-tuning do modelo com histórico do usuário
# Reconhecer padrões: "pizza = lazer, mercado = casa"
# Sugestões automáticas de economia
```

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
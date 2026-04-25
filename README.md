# 🤖 Bot Financeiro Telegram

Bot simples para registrar despesas e receitas pelo Telegram, gerar relatórios e categorizar transações com IA.

---

## Instalação

1. Clone o repositório:
```bash
git clone <seu-repo>
cd bot_financeiro
```
2. Instale as dependências:
```bash
pip install -r requirements.txt
```
3. Crie o arquivo `.env` usando o modelo `.env.example`.

---

## Configuração

No `.env`, preencha as variáveis mínimas:
```env
BOT_TOKEN=seu_token_aqui
DB_URI=postgresql://postgres:senha@localhost:5432/bot_financeiro
ENCRYPTION_KEY=chave_secreta
HF_API_TOKEN=hf_seu_token
DEBUG=False
```

- `BOT_TOKEN`: token do bot Telegram
- `DB_URI`: conexão com PostgreSQL
- `ENCRYPTION_KEY`: chave de criptografia
- `HF_API_TOKEN`: token Hugging Face para categorização com IA

---

## Execução

```bash
python main.py
```

---

## Comandos principais

- `/start` — iniciar o bot
- `/relatorio simples` — resumo do mês atual
- `/relatorio completo` — detalhes com categorias
- `/relatorio semanal` — últimos 7 dias
- `/relatorio mensal` — últimos 30 dias
- `/relatorio mes 1` — relatório de janeiro (1-12)
- `/reset` — limpar transações e saldo
- `/ajustar_saldo 1500` — ajustar saldo atual

---

## Como usar

- Digite valores como `20 pizza` ou `recebi 1000 salario`.
- O bot classifica a transação automaticamente.
- Relatórios mostram receita, despesa e economia.

---

## Observações importantes

- Não suba o arquivo `.env` para o GitHub.
- O diretório `doc_guia/` está configurado como privado e não deve ser enviado ao GitHub.
- Se a IA não responder, o bot usa um fallback por palavra-chave para categorizar.

---

## Tecnologias

- Python 3.10+
- Telegram Bot API
- SQLAlchemy
- PostgreSQL
- Hugging Face Inference API


# Fluxary - Assistente Financeiro

🌎 Idioma: Português | 🇺🇸 [English](README.md)

Este projeto é um bot automatizado em Python com IA pré-treinada para categorizar transações financeiras e fornecer apoio inteligente na gestão de contas. Automatiza tarefas, organiza dados e simplifica a gestão financeira de forma prática e escalável.

---

## Estrutura do Projeto
- `src/` — Código-fonte principal  
- `main.py` — Execução do bot  
- `requirements.txt` — Dependências do projeto  
- `run_bot.bat` — Script de inicialização  
- `README.md` — Documentação do projeto  

---

## Objetivos
- Registrar despesas e receitas de forma prática pelo **Telegram**.  
- Gerar relatórios simples e detalhados (semanais, mensais e por categoria).  
- Utilizar **IA** para categorização automática de transações.  

---

## Demonstração

![Project Demonstration](contacerta.gif)

---

## Tecnologias Utilizadas
- **Python 3.10+**  
- **Telegram Bot API**  
- **SQLAlchemy**  
- **PostgreSQL**  
- **Hugging Face Inference API**  

---

## Diferenciais Técnicos
- Integração direta com o **Telegram** para interação em tempo real.  
- Persistência de dados em banco relacional (**PostgreSQL**) com ORM (**SQLAlchemy**).  
- Uso de **IA** para categorização automática de transações financeiras.  
- Estrutura modular e organizada para fácil manutenção e evolução.  

---

## Como Executar
1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/financial_assistant.git
   ```
2. Crie e ative um ambiente virtual:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1   # no PowerShell
   ```
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente (tokens e credenciais do banco).  
5. Execute o bot:
   ```bash
   python main.py
   ```

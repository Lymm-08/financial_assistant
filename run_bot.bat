@echo off
REM Ativa o ambiente virtual
call .venv\Scripts\activate

REM Executa o bot
python main.py

REM Mantém a janela aberta após execução
pause

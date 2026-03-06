@echo off
cd /d C:\bot_financeiro
call .venv\Scripts\activate.bat
if not exist logs mkdir logs
.venv\Scripts\pythonw.exe main.py >> logs\bot.log 2>&1

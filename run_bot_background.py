#!/usr/bin/env python
# ==========================
# ARQUIVO: run_bot_background.py
# Executa o Bot Financeiro em background (multiplataforma)
# Suporta: Windows, Linux, macOS
# ==========================

import subprocess
import sys
import os
import time
import platform

def run_in_background():
    """Executa o bot em background de forma universal"""
    
    print("=" * 50)
    print("  Bot Financeiro - Inicializando em Background")
    print("=" * 50)
    print()
    
    # Detectar SO
    sistema_operacional = platform.system()
    print(f"🖥️  Sistema: {sistema_operacional}")
    
    # Verificar venv
    venv_path = ".venv"
    python_exe = None
    
    if sistema_operacional == "Windows":
        python_exe = os.path.join(venv_path, "Scripts", "python.exe")
    else:  # Linux, macOS
        python_exe = os.path.join(venv_path, "bin", "python")
    
    if not os.path.exists(python_exe):
        print(f"❌ Ambiente virtual não encontrado em {venv_path}")
        print("📦 Criando ambiente virtual...")
        subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True)
        print("✅ Ambiente virtual criado!")
    
    # Instalar dependências
    print("📦 Verificando dependências...")
    pip_exe = None
    if sistema_operacional == "Windows":
        pip_exe = os.path.join(venv_path, "Scripts", "pip.exe")
    else:
        pip_exe = os.path.join(venv_path, "bin", "pip")
    
    subprocess.run([pip_exe, "install", "-q", "-r", "requirements.txt"], check=True)
    print("✅ Dependências verificadas!")
    
    # Executar bot em background
    print("\n🚀 Iniciando bot em background...")
    
    if sistema_operacional == "Windows":
        # Windows: usar CREATE_NO_WINDOW
        import ctypes
        CREATE_NO_WINDOW = 0x08000000
        process = subprocess.Popen(
            [python_exe, "main.py"],
            creationflags=CREATE_NO_WINDOW,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            cwd=os.getcwd()
        )
    else:
        # Linux/macOS: usar nohup ou subprocess
        with open(os.devnull, 'w') as devnull:
            process = subprocess.Popen(
                [python_exe, "main.py"],
                stdout=devnull,
                stderr=devnull,
                cwd=os.getcwd(),
                start_new_session=True  # Desanexar do terminal
            )
    
    print(f"✅ Bot iniciado em background!")
    print(f"📊 Process ID: {process.pid}")
    print()
    print("💡 PRÓXIMOS PASSOS:")
    print(f"   1. Abra seu Telegram")
    print(f"   2. Procure por seu bot")
    print(f"   3. Envie /start")
    print()
    print("📋 Para verificar se está rodando:")
    
    if sistema_operacional == "Windows":
        print("   • Use Task Manager (Ctrl+Shift+Esc)")
        print("   • Procure por python.exe")
    else:
        print("   • Use: ps aux | grep main.py")
        print("   • Ou: pgrep -f 'main.py'")
    
    print()
    print("⏹️  Para parar o bot:")
    if sistema_operacional == "Windows":
        print("   • Use Task Manager ou: taskkill /IM python.exe")
    else:
        print("   • Use: pkill -f 'main.py'")
        print("   • Ou: kill <PID>")
    
    print()
    print("💾 Acompanhamento:")
    print("   • Logs são salvos no console/terminal")
    print("   • Banco de dados: PostgreSQL integrado")
    print()

if __name__ == '__main__':
    try:
        run_in_background()
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

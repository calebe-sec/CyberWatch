import webbrowser
import logging
import subprocess
import time
import os
import sys
import signal

from colorama import Fore, Style
from pathlib import Path

logger = logging.getLogger(__name__)
SERVER_DIR = Path(__file__).parent.parent /'report' / 'server.py'

sub = None

def open_web():
    
    global sub

    try:

        if not SERVER_DIR.exists():
            print(Fore.RED + "[!] Não tem o server criado")
            logger.warning("[!] Não tem o server criado")
            return
        
        sub = subprocess.Popen(
            [sys.executable, '-m', 'flask', '--app', str(SERVER_DIR), 'run',], 
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)       
        
        
        time.sleep(3)

        if sub.poll() is not None:
            erro = sub.stderr.read().decode(errors="ignore") if sub.stderr else ""
            print(Fore.RED + "[!] O servidor Flask não iniciou")
            logger.error(f"[!] Flask falhou ao iniciar: {erro}")
            return

        return webbrowser.open("http://127.0.0.1:5000")
    
    except Exception as e:
        print(Fore.RED + f"[!] Erro: {e}")
        logger.error(e)

def close_web():

    global sub

    try:
        if os.name == "nt":
            if sub:
                sub.terminate()

        else:
            if sub:
                sub.send_signal(signal.SIGINT)
        sub.wait()
        sub = None

    except Exception as e:
        print(Fore.RED + f"[!] Erro {e}")

def run():

    try:

        print(Style.BRIGHT + Fore.BLUE + "TENTANDO ABRIR O DASHBOARD")
        open_web()

        while True:
            cmd = input(">")

            if not cmd:
                print(Style.BRIGHT + Fore.YELLOW + ("Dashboard rodando"))
                continue

            if cmd.lower() in ["quit", "exit"]:
                print(Style.BRIGHT + "[*] Até logo!")
                break
            
    except (EOFError, KeyboardInterrupt):
        print(Style.BRIGHT + "\n[*] Encerrando...")
    
    except Exception as e:
        print(Fore.RED + f"[!] Erro {e}" )
        logger.warning(f"[!] Erro {e}")
    
    finally:
        close_web()





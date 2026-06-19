import logging
import shlex
import readline
import os

from colorama import Style, Fore, just_fix_windows_console, init
from pathlib import Path

from core.parser import create_parser
from core.banner import get_random_banner
from modules.scanner.port_scanner import scanning, parser_ports
from modules.scanner.dns_target import dns_target
from modules.scanner.ping import ping
from modules.report.report_manager import GerenciadorRelatorio

logger = logging.getLogger(__name__)

(Path(__file__).parent / 'logs').mkdir(exist_ok=True)

logging.basicConfig(
                    format='%(asctime)s %(message)s', 
                    datefmt='%d/%m/%Y %I:%M:%S %p',
                    filename=Path(__file__).parent / 'logs' / 'cyberwatch.log', 
                    encoding='utf-8', 
                    level=logging.DEBUG
                    )

def clean():
    os.system("cls" if os.name == "nt" else "clear")

def init_color():
    if os.name == 'nt':
        just_fix_windows_console()
    else:
        init(autoreset=True)

def display_result(results: list) -> None:
    for result in results:
        status = result.get("status", "unknown").upper()
        port = result.get("port", "?")
        service = result.get("service", "unknown")
        version = result.get("version", "")

        print(f"{Fore.GREEN + Style.BRIGHT + '[' + status}] {port} : {service} : {version}")        
        
        web_info = result.get("web_enum")
        if web_info:
            print(f"  ├─ Title: {web_info.get('title', 'N/A')}")
            print(f"  └─ Content-Type: {web_info.get('content_type', 'N/A')}")

if __name__ == "__main__":
    clean()

    init_color()

    print(get_random_banner())

    parser = create_parser()

    while True:
        try:
            cmd = input("Cyberwatch > ").strip()
        except (EOFError, KeyboardInterrupt):
            print(Style.BRIGHT + "\n[*] Encerrando...")
            break

        if not cmd:
            continue

        if cmd.lower() in ["exit", "quit"]:
            print(Style.BRIGHT + "[*] Até logo!")
            break
    
        try:
            args = parser.parse_args(shlex.split(cmd))

            if not args.command:
                print(f"[!] Nenhum comando fornecido. Use {Style.BRIGHT + 'scan --help'}.")
                continue

            if args.command == "scan":
                target = dns_target(args.target)
                
                if not target:
                    print(Fore.RED + "[!] Alvo Inválido ou não resolvido")
                    continue

                ports = parser_ports(args.ports)

                if not ports:
                    print(Fore.RED + "[!] Intervalo de portas inválido")
                    continue

                try:
                    results = scanning(target, ports, 
                                    args.banner,
                                    args.timeout,
                                    args.threads,
                                    args.web_enum)
                except OSError as e:
                    logger.warning(f"[!] Erro de rede: {e}")
                    print(f"{Fore.RED + '[!] Erro de rede: '}{e}")
                    continue
                
                if args.output:
                    gerenciador = GerenciadorRelatorio(target)
                    gerenciador.salvardados(results)
                    gerenciador.salvarjson(results)
                    
                
                if not results:
                    print(Fore.YELLOW + "[*] Nenhuma porta aberta encontrada")
                else:
                    display_result(results)

            elif args.command == "ping":
                if not args.target:
                    print(f"{Fore.RED + '[!] Alvo inválido, Use:'} {Style.BRIGHT + 'ping <IP>'}")
                    continue
                ping(args.target)
            
            elif args.command == "reports":
                if args.target:
                    gerenciador = GerenciadorRelatorio(args.target)
                    dados = gerenciador.recuperadados()
                    if dados:
                        print(f"\n{Style.BRIGHT + '[*] Último relatório de'} '{args.target}':")
                        
                        print(f"{Style.BRIGHT + 'PORT':<8} {Style.BRIGHT + 'STATUS':<8} {Style.BRIGHT + 'SERVICE':<15} {Style.BRIGHT + 'VERSION'}")
                        
                        print(Style.BRIGHT + "-" * 50)
                        
                        for linha in dados:
                            print(f"{str(linha.get('port','')):<8} "
                                  f"{str(linha.get('status','')):<8} "
                                  f"{str(linha.get('service','')):<15} "
                                  f"{linha.get('version','')}")
                    else:
                        GerenciadorRelatorio.listarRelatorios()


        except SystemExit:
            pass
        except ValueError as e:
            logger.warning(f"[!] valor inválido: {e}")
        except Exception as e:
            logger.warning(f"[!] Erro inesperado: {e}")
import shlex
import readline
import os

from core.parser import create_parser
from core.banner import get_random_banner
from modules.scanner.port_scanner import scanning, parser_ports
from modules.scanner.dns_target import dns_target
from modules.report.report_manager import GerenciadorRelatorio

def clean():
    os.system("cls" if os.name == "nt" else "clear")

def display_result(results: list) -> None:
    for result in results:
        status = result.get("status", "unknown").upper()
        port = result.get("port", "?")
        service = result.get("service", "unknown")
        version = result.get("version", "")

        print(f"[{status}] {port} : {service} : {version}")        
        
        web_info = result.get("web_enum")
        if web_info:
            print(f"  ├─ Title: {web_info.get('title', 'N/A')}")
            print(f"  └─ Content-Type: {web_info.get('content_type', 'N/A')}")

if __name__ == "__main__":
    clean()
    print(get_random_banner())

    parser = create_parser()

    while True:
        try:
            cmd = input("Cyberwatch > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n[*] Encerrando...")
            break

        if not cmd:
            continue

        if cmd.lower() in ["exit", "quit"]:
            print("[*] Até logo!")
            break
    
        try:
            args = parser.parse_args(shlex.split(cmd))

            if not args.command:
                print("[!] Nenhum comando fornecido. Use 'scan --help'.")
                continue

            if args.command == "scan":
                target = dns_target(args.target)
                
                if not target:
                    print("[!] Alvo Inválido ou não resolvido")
                    continue

                ports = parser_ports(args.ports)

                if not ports:
                    print("[!] Intervalo de portas inválido")
                    continue

                try:
                    results = scanning(target, ports, 
                                    args.banner,
                                    args.timeout,
                                    args.threads,
                                    args.web_enum)
                except OSError as e:
                    print(f"[!] Erro de rede: {e}")
                    continue
                
                if args.output:
                    gerenciador = GerenciadorRelatorio(target)
                    gerenciador.salvardados(results)
                    gerenciador.salvarjson(results)
                    
                
                if not results:
                    print("[*] Nenhuma porta aberta encontrada")
                else:
                    display_result(results)
            
            elif args.command == "reports":
                if args.target:
                    gerenciador = GerenciadorRelatorio(args.target)
                    dados = gerenciador.recuperadados()
                    if dados:
                        print(f"\n[*] Último relatório de '{args.target}':")
                        
                        print(f"{'PORT':<8} {'STATUS':<8} {'SERVICE':<15} {'VERSION'}")
                        
                        print("-" * 50)
                        
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
            print(f"[!] valor inválido: {e}")
        except Exception as e:
            print(f"[!] Erro inesperado: {e}")
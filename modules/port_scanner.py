import threading
import socket
from core.parser import create_parser
from modules.banner_grabber import grab_banner
from modules.fingerprint import identify_service

def parser_ports(arguments) -> list[int]:
    ports = []

    itens = arguments.split(",")
    
    for item in itens:
        item = item.strip()

        if "-" in item:
            inicio, fim = item.split("-")
            inicio = int(inicio)
            fim = int(fim)

            for port in range(inicio, fim+1):
                    ports.append(port)
        else:
            ports.append(int(item))

    return ports

def scan(ip: str, port: int, banner_enable=False) -> None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((ip, port))

        if result == 0:

            banner = grab_banner(ip, port)
            service_info = identify_service(banner) or "unknown"

            print(f"[OPEN] port {port} : {service_info}")

            if banner_enable:
                print(banner)
        else:
            print(f"[CLOSE] port {port}")
        
        # print(f"Port {port} -> {result}")
    except Exception as err:
        print(f"[*] ERROR: {err}")

    finally:
        s.close()    

def scanning(ip: str, ports: list[int], banner) -> None:
    threads = []
    
    for port in ports:
        t = threading.Thread(target=scan,
                             args=(ip,port, banner)
                             )
        threads.append(t) 
        t.start()

    for t in threads:
        t.join()



if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()
    port = parser_ports(args.ports)
    scanning(args.target, port)
    

    
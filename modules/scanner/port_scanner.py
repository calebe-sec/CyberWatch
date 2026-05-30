import threading
import socket
from core.parser import create_parser
from modules.scanner.banner_grabber import grab_banner
from modules.scanner.fingerprint import identify_service
from modules.scanner.version_detection import parser_versions

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
        
def scan(ip: str, port: int, banner_enable=False, import_scan=False) -> None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(5)
        result = s.connect_ex((ip, port))

        if result == 0:

            banner = grab_banner(ip, port)
            service_info = identify_service(banner) or "unknown"
            version_service = parser_versions(service_info, banner)

            #print(f"[OPEN] port {port} : {service_info} : {version_service}")

            if banner_enable:
                print(banner)
            
            RESULT = {
                "port"    : port,
                "status"  : "open",
                "service" : service_info,
                "version" : version_service
            }

            return RESULT

            
        #else:
           # print(f"[CLOSE] port {port}")
        
        # print(f"Port {port} -> {result}")
    except Exception as err:
        print(f"[*] ERROR: {err}")

    finally:
        s.close()    


def scanning(ip: str, ports: list[int], banner) -> None:
    threads = []
    results = []

    def worker(ip, port, banner, results):
        result = scan(ip, port, banner)
        if result:
            results.append(result)

    for port in ports:
        t = threading.Thread(target=worker,
                             args=(ip,
                                   port,
                                   banner,
                                   results,
                                   )
                             )
        threads.append(t) 
        t.start()
        
    for t in threads:
        t.join()
    return results



if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()
    port = parser_ports(args.ports)
    scanning(args.target, port)
    

    
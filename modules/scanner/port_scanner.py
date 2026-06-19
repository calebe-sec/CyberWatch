import logging
import socket

from concurrent.futures import ThreadPoolExecutor, as_completed

from core.parser import create_parser
from modules.scanner.banner_grabber import grab_banner
from modules.scanner.fingerprint import identify_service
from modules.scanner.version_detection import parser_versions
from modules.scanner.http_enum import http_enum

logger = logging.getLogger(__name__)

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
        
def scan(ip: str, port: int, banner_enable=False, timeout=5, web_enum=False) -> None:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((ip, port))

        if result == 0:

            banner = grab_banner(ip, port)
            service_info = identify_service(banner) or "unknown"
            version_service = parser_versions(service_info, banner)

            #print(f"[OPEN] port {port} : {service_info} : {version_service}")

            if banner_enable:
                print(banner)

            if web_enum and service_info in ["http", "https"]:
                web_info = http_enum(banner)
            else:
                web_info = None
            
            RESULT = {
                "port"    : port,
                "status"  : "open",
                "service" : service_info,
                "version" : version_service,
                "web_enum": web_info
            }
            

            return RESULT

            
        #else:
           # print(f"[CLOSE] port {port}")
        
        # print(f"Port {port} -> {result}")
    except Exception as err:
        logger.warning(f"[*] ERROR: {err}")

    finally:
        s.close()    


def scanning(ip: str, ports: list[int], banner, timeout=5,threads=100, web_enum=False) -> None:
    results = []
    
    with ThreadPoolExecutor(max_workers=threads) as pool:

        futures = [pool.submit(
            scan,
            ip,
            port,
            banner,
            timeout,
            web_enum
        )
        for port in ports ]

        for future in as_completed(futures):
            result = future.result()

            if result:
                results.append(result)

    results.sort(key=lambda x: x["port"])
    return results

if __name__ == '__main__':

    parser = create_parser()
    args = parser.parse_args()
    port = parser_ports(args.ports)
    scanning(args.target, port)
    

    
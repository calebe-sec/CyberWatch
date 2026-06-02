from core.parser import create_parser
from core.banner import banner
from modules.scanner.port_scanner import scanning, parser_ports
from modules.scanner.export_scan import export_json
from modules.scanner.dns_target import dns_target

if __name__ == "__main__":
    banner()

    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "scan":
        target = dns_target(args.target)
        
        if not target:
            print("[!] Invalid target")
            exit(1)

        ports = parser_ports(args.ports)

        results = scanning(target, ports, 
                           args.banner,
                           args.timeout)
        
        if args.output:
            export_json(args.output, results)
        for result in results:
            print(
    f"[{result['status'].upper()}] "
    f"{result['port']} : "
    f"{result['service']} : "
    f"{result['version']}"
)
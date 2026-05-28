from core.parser import create_parser
from core.banner import banner
from modules.scanner.port_scanner import scanning, parser_ports
from modules.scanner.export_scan import export_json

if __name__ == "__main__":
    banner()

    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "scan":
        ports = parser_ports(args.ports)
        results = scanning(args.target,ports, args.banner)
        if args.output:
            export_json(args.output, results)
        for result in results:
            print(
    f"[{result['status'].upper()}] "
    f"{result['port']} : "
    f"{result['service']} : "
    f"{result['version']}"
)
from core.parser import create_parser
from core.banner import banner
from modules.scanner.port_scanner import scanning, parser_ports


if __name__ == "__main__":
    banner()

    parser = create_parser()
    args = parser.parse_args()
    
    if args.command == "scan":
        ports = parser_ports(args.ports)
        scanning(args.target,ports, args.banner)
    
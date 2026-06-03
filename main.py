import shlex
import readline

from core.parser import create_parser
from core.banner import get_random_banner
from modules.scanner.port_scanner import scanning, parser_ports
from modules.scanner.export_scan import export_json
from modules.scanner.dns_target import dns_target

if __name__ == "__main__":
    print(get_random_banner())

    parser = create_parser()

    while True:
        cmd = input("Cyberwatch > ")

        if cmd.lower() in ["exit", "quit"]:
            break
    
        try:
            args = parser.parse_args(shlex.split(cmd))

            if args.command == "scan":
                target = dns_target(args.target)
                
                if not target:
                    print("[!] Invalid target")
                    exit(1)

                ports = parser_ports(args.ports)

                results = scanning(target, ports, 
                                args.banner,
                                args.timeout,
                                args.web_enum)
                
                if args.output:
                    export_json(args.output, results)
                for result in results:
                    print(
                        f"[{result['status'].upper()}] "
                        f"{result['port']} : "
                        f"{result['service']} : "
                        f"{result['version']}"
                    )

                    web_info = result.get("web_enum")

                    if web_info:
                        print(f"  ├─ Title: {web_info['title']}")
                        print(f"  └─ Content-Type: {web_info['content_Type']}")

        except SystemExit:
            pass
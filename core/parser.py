#!/usr/bin/env python3
import argparse

def create_parser():
    parser = argparse.ArgumentParser(                  #type: ignore
        prog='CyberWatch', 
        description='Ferramenta para monitorar e enumerar alvos'
    )

    subparsers = parser.add_subparsers(
        dest="command"
    )

    # Scan
    scan_parser = subparsers.add_parser(
        "scan",
        help="port scanner"
    )

    scan_parser.add_argument(
        "-t",
        "--target",
        help="Alvo: IP ou hostname (ex: 192.168.1.1 ou example.com)",
        required=True
    )

    scan_parser.add_argument(
        "-p",
        "--ports",
        help="Portas a varrer. Ex: '80', '1-1000', '22,80,443' (padrão: 1-1000)",
        default="1-1000"
    )

    scan_parser.add_argument(
        "--timeout",
        type= int,
        default= 5,
        help="Timeout por porta em segundos (padrão: 5)"
    )

    
    
    scan_parser.add_argument(
        "--output",
        help="os arquivos vão para a pasta reports, em json e CSV",
        action="store_true"
    )

    scan_parser.add_argument(
        "-b",
        "--banner",
        help="Ativa banner grabbing nas portas abertas",
        action="store_true"
    )

    scan_parser.add_argument(
        "--threads",
        type=int,
        default=100,
        help="Número de threads paralelas (padrão: 100)"
    )

    scan_parser.add_argument(
        "--web-enum",
        action="store_true",
        help="Enumera serviços HTTP/HTTPS (título, content-type)",
    )

    '''

    scan_parser.add_argument(
        "--open-only",
        action="store_true",
        help="Exibe apenas portas abertas"
    )

    scan_parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="enable banner grabbing"
    )
    
    scan_parser.add_argument(
        "-s",
        "--save",
        help="save log, mark the path with --output"
    )

    scan_parser.add_argument(
        "-f",
        "--fast",
        help="fast scan",
        action="store_true"
    )
    
    scan_parser.add_argument(
        "-fl",
        "--full",
        action="store_true",
        help="scan all 65535 ports"
    )

    scan_parser.add_argument(
        "-nd",
        "--no-dns",
        action="store_true",
        help="no dns scan"
    )

    
    '''
    #ping
    ping_parser = subparsers.add_parser("ping",
                                        help="faz um ping SCAN")
    
    ping_parser.add_argument(
        "target",
        help="faz o ping pelo host que selecionar"
    )
    
    #reports
    reports_parser = subparsers.add_parser("reports",
                                           help="Gerencia Relatórios de scans anteriores")

    reports_parser.add_argument(
        "-t",
        "--target",
        help="filtra pelo alvo (IP ou hostname) para exibir o último relatório",
        default=None
    )


    #dashboard
    dashboard_parser = subparsers.add_parser("dashboard",
                                             help="envia para o site")
    


    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    print(args)
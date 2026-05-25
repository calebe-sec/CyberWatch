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
        help="Target/IP",
        required=True
    )

    scan_parser.add_argument(
        "-p",
        "--ports",
        help="Ports",
        default="1-1000"
    )

    scan_parser.add_argument(
        "--timeout",
        type= int,
        default= 5,
        help="timeout"
    )

    scan_parser.add_argument(
        "--threads",
        type=int,
        default=1,
        help="number of threads"
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
        "--output",
        help="put your path to save"
    )

    scan_parser.add_argument(
        "-f",
        "--fast",
        help="fast scan",
        action="store_true"
    )

    scan_parser.add_argument(
        "-b",
        "--banner",
        help="banner grabbing",
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

    scan_parser.add_argument(
        "--open-only",
        action="store_true",
        help="only open port"
    )

    return parser


if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    print(args)
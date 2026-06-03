'''
def banner():
    print("""

      ██████╗██╗   ██╗██████╗ ███████╗██████╗ 
     ██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗
     ██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝
     ██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗
     ╚██████╗   ██║   ██████╔╝███████╗██║  ██║
      ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝

    [ CyberWatch - Scan, Monitoring and Enumeration ]
           [ Author: ANOSH | Version: 1.0 ]
               [-h or --help for help]

""")
'''

from pathlib import Path
import random


def get_random_banner():
    banner_dir = Path("/home/catombo/estudos/CyberWatch/asset/banners")

    banners = list(banner_dir.glob("*.txt"))

    if not banners:
        return "[!] No banners found."

    chosen = random.choice(banners)

    return chosen.read_text(encoding="utf-8")

if __name__ == "__main__":
    print(get_random_banner())
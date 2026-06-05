from pathlib import Path
import random


def get_random_banner():
    banner_dir = Path(__file__).parent.parent / "asset" / "banners"

    if not banner_dir.exists():
        return "[CyberWatch] scan, Monitoring and Enumeration\n"

    banners = list(banner_dir.glob("*.txt"))

    if not banners:
        return "[!] Nenhum banner encontrado."

    chosen = random.choice(banners)

    try:
        return chosen.read_text(encoding="utf-8")
    except OSError:
        return "[!] Erro ao ler arquivo de banner."
    
if __name__ == "__main__":
    print(get_random_banner())
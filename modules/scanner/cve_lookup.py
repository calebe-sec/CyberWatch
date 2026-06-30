import urllib.request
import urllib.error
import urllib.parse
import logging
import json

from colorama import Style, Fore

logger = logging.getLogger(__name__)

URL_ = "https://services.nvd.nist.gov/rest/json/cves/2.0" 
MAX_RESULTS = 5
REQUEST_TIMEOUT = 10

def _clean_version(version: str) -> str:
    return version.replace("_", " ").replace("/", " ")

def _extract_metrics(metrics: dict) -> tuple:
    
    for key in ("cvssMetricV31", "cvssMetricV30", "cvssMetricV2"):
        lista = metrics.get(key)

        if lista:
            data = lista[0].get("cvssData", {})
            score = data.get("baseScore", "N/A")
            severity = data.get("baseSeverity", "N/A")

            return score, severity
    
    return "N/A", "N/A"

def _color_score(score) -> str:
    try:
        value = float(score)
    except (ValueError, TypeError):
        return Fore.WHITE
    
    if value >= 9.0:
        return Fore.RED + Style.BRIGHT
    elif value >= 7.0:
        return Fore.RED
    elif value >= 4.0:
        return Fore.YELLOW
    
    return Fore.WHITE

def cve_search(service: str, version: str) -> list:

    if not version or version.lower() == "unknown":
        logger.debug("[cve_lookup] unknown version, search ignored")
        return []
    
    query = f"{service} {_clean_version(version)}"

    params = urllib.parse.urlencode({
                                    "keywordSearch" : query,
                                    "resultsPerPage" : MAX_RESULTS,
    })

    url = f"{URL_}?{params}"

    req = urllib.request.Request(url, headers={"User-Agent": "CyberWatch/1.0"})

    try:

        logger.debug(f"[cve_lookup] find...: {url}")

        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as res:
            data = json.loads(res.read())

        total = data.get("totalResults", 0)
        logger.debug(f"[cve_lookup] {total} results find to '{query}'")

        vulnerabilities = data.get("vulnerabilities", [])

        cves = []

        for item in vulnerabilities:
            cve = item.get("cve", {})
            cve_id = cve.get("id", "N/A")
            descriptions = cve.get("descriptions", [])
            description = next(
                (d["value"] for d in descriptions if d.get("lang") == "en"),
                descriptions[0]["value"] if descriptions else "N/A"
            )

        score, serverity = _extract_metrics(cve.get("metrics", {}))

        cves.append({
            "id"           : cve_id,
            "description"  : description,
            "score"        : score,
            "severity"     : serverity,
        })

        return cves
    
    except urllib.error.HTTPError as e:
        logger.warning(f"[cve_lookup] HTTP {e.code} to consult NVD: {e.reason}")
        return []
 
    except urllib.error.URLError as e:
        logger.warning(f"[cve_lookup] Network error: {e.reason}")
        return []
 
    except Exception as e:
        logger.warning(f"[cve_lookup] Unexpected error: {type(e).__name__} {e}")
        return []
    

def display_cves(cves: list) -> None:

    if not cves:
        return
 
    for cve in cves:
        cor   = _color_score(cve["score"])
        score = cve["score"]
        sev   = cve["severity"]
        cid   = cve["id"]
        desc  = cve["description"]
 
       
        desc_curta = desc[:120] + "..." if len(desc) > 120 else desc
 
        print(
            f"  {Fore.WHITE}├─ {cor}{cid}"
            f"  [{score} / {sev}]{Style.RESET_ALL}"
        )
        print(f"  {Fore.WHITE}│  {Fore.WHITE + Style.BRIGHT}{desc_curta}{Style.RESET_ALL}")


if __name__ == "__main__":
 
    import colorama
    colorama.init(autoreset=True)
 
    tests = [
        ("ssh",  "OpenSSH_9.3"),
        ("http", "nginx/1.18.0"),
        ("ftp",  "vsFTPd"),
        ("ssh",  "unknown"),     
    ]
 
    for service, version in tests:
        print(f"\n{Style.BRIGHT}{'─'*55}")
        print(f"  Buscando CVEs → service={service!r}  version={version!r}")
        print(f"{'─'*55}{Style.RESET_ALL}")
 
        resultados = cve_search(service, version)
 
        if not resultados:
            print(f"  {Fore.WHITE + Style.DIM}Nenhum CVE encontrado.{Style.RESET_ALL}")
        else:
            print(f"  {Fore.GREEN}{len(resultados)} CVE(s) encontrado(s):{Style.RESET_ALL}")
            display_cves(resultados)
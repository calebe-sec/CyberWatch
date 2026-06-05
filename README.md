# CyberWatch

> Network scanning and service enumeration tool written in Python.

CyberWatch is an interactive CLI tool for TCP port scanning, service fingerprinting, banner grabbing, HTTP enumeration, and DNS resolution. Built as a hands-on learning project in offensive security fundamentals.

---

## Features

- **TCP Port Scanner** — scan single ports, ranges (`1-1000`), or comma-separated lists (`22,80,443`)
- **Service Fingerprinting** — identifies SSH, HTTP, HTTPS, FTP, SMTP, and Telnet from banner responses
- **Version Detection** — parses specific version strings (e.g. `OpenSSH_9.3`, `Apache/2.4.7`)
- **Banner Grabbing** — raw banner capture with `--banner`
- **HTTP/HTTPS Enumeration** — extracts page title and `Content-Type` with `--web-enum`
- **DNS Resolution** — accepts hostnames or IPs as targets
- **Threaded Scanning** — configurable thread pool via `--threads` (default: 100)
- **JSON Export** — save results to a file with `--output`
- **Interactive Shell** — persistent session with history support

---

## Project Structure

```
CyberWatch/
├── main.py
├── core/
│   ├── banner.py          # ASCII banner display
│   └── parser.py          # CLI argument parser
└── modules/scanner/
    ├── port_scanner.py    # Core scanner with ThreadPoolExecutor
    ├── banner_grabber.py  # Protocol-specific banner grabbing
    ├── fingerprint.py     # Service identification from banner
    ├── version_detection.py  # Version string parsing per service
    ├── http_enum.py       # HTTP title and content-type extraction
    ├── dns_target.py      # DNS resolution / IP validation
    └── export_scan.py     # JSON report export
```

---

## Requirements

- Python 3.10+
- No external dependencies — uses only the Python standard library

---

## Installation

```bash
git clone https://github.com/calebe-sec/CyberWatch.git
cd CyberWatch
python main.py
```

---

## Usage

Start the interactive shell:

```
$ python main.py
CyberWatch > 
```

### Basic Scan

```
CyberWatch > scan -t scanme.nmap.org -p 22,80,443
[OPEN] 22 : ssh : OpenSSH_8.9p1
[OPEN] 80 : http : apache/2.4.7 (ubuntu)
[OPEN] 443 : https : apache/2.4.7 (ubuntu)
```

### Port Range

```
CyberWatch > scan -t 192.168.1.1 -p 1-1000
```

### Banner Grabbing

```
CyberWatch > scan -t scanme.nmap.org -p 22 --banner
```

### HTTP Enumeration

```
CyberWatch > scan -t scanme.nmap.org -p 80 --web-enum
[OPEN] 80 : http : apache/2.4.7 (ubuntu)
  ├─ Title: Go ahead and ScanMe!
  └─ Content-Type: text/html
```

### Custom Timeout and Threads

```
CyberWatch > scan -t 10.0.0.1 -p 1-65535 --timeout 3 --threads 200
```

### Export Results to JSON

```
CyberWatch > scan -t scanme.nmap.org -p 1-1000 --output results.json
[*] Resultados exportados para: results.json
```

---

## Supported Services

| Service | Detection Method         |
|---------|--------------------------|
| SSH     | OpenSSH version string   |
| HTTP    | Server header            |
| HTTPS   | Server header (SSL)      |
| FTP     | vsFTPd, ProFTPD, FileZilla, etc. |
| SMTP    | Postfix, Sendmail, Exchange, etc. |
| Telnet  | OS/device fingerprint    |

---

## Options Reference

```
scan -t TARGET [options]

  -t, --target     Target IP or hostname (required)
  -p, --ports      Ports to scan. Ex: 80, 1-1000, 22,80,443 (default: 1-1000)
  --timeout        Timeout per port in seconds (default: 5)
  --threads        Number of parallel threads (default: 100)
  --banner         Enable raw banner grabbing
  --web-enum       Enumerate HTTP/HTTPS services (title, content-type)
  --open-only      Show open ports only
  --output FILE    Export results to JSON file
```

---

## Roadmap

- [x] TCP Port Scanner
- [x] Banner Grabbing
- [x] DNS Resolution
- [x] Service Fingerprinting
- [x] Version Detection
- [x] HTTP/HTTPS Enumeration
- [x] Interactive Shell
- [x] Configurable Thread Pool
- [x] JSON Export
- [ ] Host Discovery (ping sweep)
- [ ] Subdomain Enumeration
- [ ] UDP Scan
- [ ] OS Detection
- [ ] CVE Lookup Integration

---

## Disclaimer

This tool is intended for **educational purposes and authorized security assessments only**.  
Always obtain explicit permission before scanning systems you do not own.

---

## Author

**Calebe Araújo (Anosh)** — Cybersecurity Student  
[GitHub](https://github.com/calebe-sec) · [TryHackMe](https://tryhackme.com/p/Anosh)
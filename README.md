# CyberWatch

CyberWatch is a network scanning and service enumeration tool written in Python. It provides TCP port scanning, banner grabbing, service fingerprinting, version detection, HTTP enumeration, DNS resolution, and JSON report export.

---

## Features

* TCP Port Scanner
* Banner Grabbing
* Service Fingerprinting
* SSH Version Detection
* HTTP/HTTPS Server Detection
* FTP Version Detection
* SMTP Detection
* Telnet Detection
* HTTP Enumeration

  * Page Title Extraction
  * Content-Type Detection
* DNS Resolution
* JSON Export
* Configurable Timeout
* Interactive Shell Interface

---

## Project Structure

```text
CyberWatch/
│
├── asset/
│   └── banners/
│
├── config/
├── dashboard/
├── database/
├── logs/
├── reports/
├── tests/
├── utils/
│
├── core/
│   ├── banner.py
│   └── parser.py
│
├── modules/
│   └── scanner/
│       ├── banner_grabber.py
│       ├── dns_target.py
│       ├── export_scan.py
│       ├── fingerprint.py
│       ├── http_enum.py
│       ├── port_scanner.py
│       └── version_detection.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/calebe-sec/CyberWatch.git
cd CyberWatch
```

Verify Python installation:

```bash
python3 --version
```

Currently, CyberWatch uses only Python standard libraries and does not require external dependencies.

---

## Usage

Start the interactive shell:

```bash
python3 main.py
```

Example:

```text
CyberWatch >
```

---

### Basic Scan

```text
CyberWatch > scan -t scanme.nmap.org -p 22,80,443
```

---

### Banner Grabbing

```text
CyberWatch > scan -t scanme.nmap.org -p 80 --banner
```

---

### HTTP Enumeration

```text
CyberWatch > scan -t scanme.nmap.org -p 80 --web-enum
```

Example output:

```text
[OPEN] 80 : http : apache/2.4.7 (ubuntu)
  ├─ Title: Go ahead and ScanMe!
  └─ Content-Type: text/html
```

---

### Custom Timeout

```text
CyberWatch > scan -t scanme.nmap.org -p 1-1000 --timeout 10
```

---

### Export Results

```text
CyberWatch > scan -t scanme.nmap.org -p 1-1000 --output results.json
```

---

## Supported Service Detection

CyberWatch currently identifies:

| Service | Detection                |
| ------- | ------------------------ |
| HTTP    | Server Header            |
| HTTPS   | Server Header            |
| SSH     | OpenSSH Version          |
| FTP     | Common FTP Servers       |
| SMTP    | Common SMTP Servers      |
| Telnet  | Common Telnet Signatures |

---

## Example Output

```text
[OPEN] 22 : ssh : OpenSSH_8.9p1
[OPEN] 80 : http : apache/2.4.7 (ubuntu)
  ├─ Title: Go ahead and ScanMe!
  └─ Content-Type: text/html
```

---

## Roadmap

* [x] Port Scanner
* [x] Banner Grabbing
* [x] DNS Resolution
* [x] Service Fingerprinting
* [x] Version Detection
* [x] HTTP Enumeration
* [x] Interactive Shell
* [x] Configurable Thread Pool
* [ ] UDP Scanner
* [ ] Host Discovery
* [ ] Subdomain Enumeration
* [ ] Report Dashboard
* [ ] OS Detection

---

## Author

Calebe Araujo

Cybersecurity Student & Python Developer

---

## Disclaimer

This tool is intended for educational purposes and authorized security assessments only.

Always obtain permission before scanning systems you do not own.

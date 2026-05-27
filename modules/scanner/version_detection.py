def parser_ssh_versions(banner):
    openssh_versions = [
    "1.2.2p1", "2.5.1p1", "2.9.9", "3.0", "3.4", "3.5", "3.6", "3.6.1",
    "3.7", "3.7.1", "3.8", "3.9", "4.0", "4.1", "4.2", "4.3", "4.4",
    "4.5", "4.6", "4.7", "4.8", "4.9", "5.0", "5.1", "5.2", "5.3",
    "5.4", "5.5", "5.6", "5.7", "5.8", "5.9", "6.0", "6.1", "6.2",
    "6.3", "6.4", "6.5", "6.6", "6.7", "6.8", "6.9", "7.0", "7.1",
    "7.2", "7.3", "7.4", "7.5", "7.6", "7.7", "7.8", "7.9", "8.0",
    "8.1", "8.2", "8.3", "8.3p1", "8.4", "8.4p1", "8.5", "8.6", "8.7",
    "8.8", "8.8p1", "8.9", "9.0", "9.1", "9.2", "9.3", "9.4", "9.5",
    "9.6", "9.7", "9.7p1", "9.8", "9.9", "10.0", "10.2", "10.3", "10.3p1"
]   
    try:
        low_banner = banner.lower()

        for i in openssh_versions:
            find = low_banner.find(f"openssh_{i}")
            if find != -1:
                msg = f"OpenSSH_{i}"
                return msg
            
        
        return "unknown"
        
    except Exception as err:
        print(err)

def parser_http_versions(banner):

    try:
        low_banner = banner.lower()

        for line in low_banner.splitlines():
            if "server:" in line:
                linha = line.split(":", 1)
                msg = linha[1].strip()
                return msg
            
        return "unknown"
    
    except Exception as err:
        print(err)

def parser_telnet_versions(banner):

    TELNET_SIGNATURES = {
    "busybox": "BusyBox",
    "ubuntu": "Ubuntu",
    "debian": "Debian",
    "fedora": "Fedora",
    "centos": "CentOS",
    "mikrotik": "MikroTik",
    "cisco": "Cisco",
    "routeros": "RouterOS",
    "windows": "Windows",
    "linux": "Linux",
    "raspbian": "Raspbian",
    "freebsd": "FreeBSD",
    "openbsd": "OpenBSD",
    "netbsd": "NetBSD",
    "synology": "Synology",
    "qnap": "QNAP",
    "hikvision": "Hikvision",
    "dahua": "Dahua",
    "tp-link": "TP-Link",
    "zte": "ZTE",
    "huawei": "Huawei",
}

    try:
        low_banner = banner.lower()
        
        for assignature, version in TELNET_SIGNATURES.items():
            if assignature in low_banner:
                return version
            
        return "unknown"
    except Exception as err:
        print(err)


def parser_smtp_versions(banner):

    SMTP_SIGNATURES = {
    "postfix": "Postfix",
    "exim": "Exim",
    "sendmail": "Sendmail",
    "qmail": "Qmail",
    "microsoft esmtp": "Microsoft Exchange",
    "exchange": "Microsoft Exchange",
    "courier": "Courier",
    "opensmtpd": "OpenSMTPD",
    "haraka": "Haraka",
    "zimbra": "Zimbra",
}
        
    try:
        low_banner = banner.lower()

        for assignature, software in SMTP_SIGNATURES.items():
            if assignature in low_banner:
                return software
        return "unknown"
    
    except Exception as err:
        print(err)


def parser_ftp_versions(banner):
    FTP_SIGNATURES = {
    "vsftpd": "vsFTPd",
    "proftpd": "ProFTPD",
    "filezilla": "FileZilla",
    "pure-ftpd": "Pure-FTPd",
    "wu-ftpd": "WU-FTPD",
    "serv-u": "Serv-U",
    "gene6": "Gene6 FTP",
    "glftpd": "GLFTPd",
    "microsoft ftp": "Microsoft FTP",
    "iis": "Microsoft IIS FTP",
}
    
    try:
        low_banner = banner.lower()

        for assignature, version in FTP_SIGNATURES.items():
            if assignature in low_banner:
                return version
            
        return "unknown"
    except Exception as err:
        print(err)


PARSERS = {
    "ssh"    :  parser_ssh_versions,
    "https"  :  parser_http_versions,
    "http"   :  parser_http_versions,
    "telnet" :  parser_telnet_versions,
    "smtp"   :  parser_smtp_versions,
    "ftp"    :  parser_ftp_versions,
}

def parser_versions(fingerprint, banner):
        
        handler = PARSERS.get(fingerprint)
        if handler:
            return handler(banner)
        return "unknown"
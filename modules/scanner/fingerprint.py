services = {
    "openssh" : "ssh",
    "apache"  : "http",
    "nginx"   : "http",
    "http/"   : "http",
    "vsftpd"  : "ftp",
    "telnet"  : "telnet",
    "smtp"    : "smtp",
    "ssl"     : "https",
    "tsl"     : "https",

}
def identify_service(banner):

    if not banner:
        return 'unknown'
    
    s_banner = banner.lower()
    for assignature, service in services.items():
        if assignature in s_banner:
            return f"{service}"
        
    return "unknown"
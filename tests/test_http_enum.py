from modules.scanner.http_enum import http_enum
from modules.scanner.banner_grabber import grab_banner_http, grab_banner_https

def http_ok():
    banner_http = grab_banner_http('1.1.1.1', 80)
    resultado = http_enum(banner_http)
    assert resultado is True

def hhtps_ok():
    banner_https = grab_banner_https('1.1.1.1', 445)
    resultado = http_enum(banner_https)
    assert resultado is True
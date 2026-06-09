from modules.scanner.fingerprint import identify_service
from modules.scanner.version_detection import parser_versions

def test_identifica_ssh():
    banner = "SSH-2.0-OpenSSH_9.3"
    assert identify_service(banner) == "ssh"

def test_identifica_http():
    banner = "HTTP/1.1 200 OK\r\nServer: Apache/2.4.7 (Ubuntu)\r\n"
    assert identify_service(banner) == "http"

def test_identifica_ftp():
    banner = "220 (vsFTPd 3.0.3)"
    assert identify_service(banner) == "ftp"

def test_servico_desconhecido():
    banner = "alguma coisa que nao reconheco"
    assert identify_service(banner) == 'unknown'

def test_versao_ssh():
    banner = "SSH-2.0-OpenSSH_9.3"
    assert parser_versions("ssh", banner) == "OpenSSH_9.3"

def test_versao_http():
    banner = "HTTP/1.1 200 OK\r\nServer: nginx/1.18.0\r\n"
    assert parser_versions("http", banner) == "nginx/1.18.0"
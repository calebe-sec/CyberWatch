from modules.scanner.dns_target import dns_target

def teste_ip_valido_retorna_ele_mesmo():
    resultado = dns_target("127.0.0.1")
    assert resultado == "127.0.0.1"

def teste_host_invalido_retorna_none():
    resultado = dns_target("host.que.nao.existe.gtz")
    assert resultado is None
from modules.scanner.port_scanner import parser_ports

def teste_de_uma_porta():
    resultado = parser_ports("80")
    assert resultado == [80]

def teste_lista_de_portas():
    resultado = parser_ports("22,80,443")
    assert resultado == [22,80,443]

def teste_range_de_portas():
    resultado = parser_ports("1-5")
    assert resultado == [1,2,3,4,5]

def teste_range_e_lista_combinada():
    resultado = parser_ports("22,80-82")
    assert resultado == [22,80,81,82]

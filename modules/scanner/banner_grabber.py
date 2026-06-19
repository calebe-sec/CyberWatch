import logging
import socket
import ssl

from pathlib import Path

logger = logging.getLogger(__name__)

def connect_sock(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(5)

    s.connect((ip, port))
    return s

def receive_response(sock) -> str:
    r = sock.recv(4096)

    decod = r.decode(errors="ignore")
    return decod
    

def grab_banner_http(ip: str, port: int):

    sock = None
            
    try:
        sock = connect_sock(ip, port)

        if not sock:
            logger.warning("[!] Não foi possivel fazer a conexão") 

        request =(
            "GET / HTTP/1.1\r\n"
            f"Host: {ip}\r\n"
            "Connection: close\r\n\r\n"
        )
        sock.send(request.encode())

        return receive_response(sock)

    except Exception as err:
            logger.warning(err)

    finally:
        if sock:
            sock.close()

def grab_banner_https(ip:str, port: int):  

    sock = None
    ssl_socket = None         
    
    try: 
        sock = connect_sock(ip, port)
        
        if not sock:
            logger.warning("[!] Não foi possivel fazer a conexão") 

        ssl_socket = ssl.create_default_context().wrap_socket(sock, server_hostname=ip)

        if not ssl_socket:
            logger.warning("[!] conexão SSL não foi completada")

        ssl_socket.send(b"GET / HTTP/1.1\r\n")
        response = ssl_socket.recv(4096)

        decod = response.decode(errors="ignore")

        return decod

    except Exception as err:
            logger.warning(err)

    finally:
        if ssl_socket:
            ssl_socket.close()
        elif sock:
            sock.close()

"""
                ainda tenho que estudar sobre isso aqui, 
                biblioteca SSL,
                TLS handshake
                Certificados
                wrapping sockets
                já que o https é mais complicado
""" 

def grab_banner_ssh(ip: str, port: int):

    sock = None

    try:
        sock = connect_sock(ip, port)

        if not sock:
            logger.warning("[!] Não foi possivel fazer a conexão") 

        return receive_response(sock)

    except Exception as err:
        logger.warning(err)

    finally:
        if sock:
            sock.close()

def grab_banner_ftp(ip: str, port: int):   

    sock = None

    try:
        sock = connect_sock(ip, port)
        
        if not sock:
            logger.warning("[!] Não foi possivel fazer a conexão") 

        return receive_response(sock)
    
    except Exception as err:
        logger.warning(err)
    
    finally:
        if sock:
            sock.close()

def grab_banner_telnet(ip: str, port: int):

    sock = None

    try:
        sock = connect_sock(ip, port)

        if not sock:
            logger.warning("[!] Não foi possivel fazer a conexão") 

        sock.send(b"whoami\r\n")
        return receive_response(sock)
    
    except Exception as err:
        logger.warning(err)

    finally:
        if sock:
            sock.close()

def grab_banner_smtp(ip: str, port: int):

    sock = None

    try:
        sock = connect_sock(ip, port)

        if not sock:
            logger.warning("[!] Não foi possivel fazer a conexão") 

        return receive_response(sock)

    except Exception as e:
        logger.warning(e)
    
    finally:
        if sock:
            sock.close()

SERVICES = {

    21: grab_banner_ftp,

    22: grab_banner_ssh,

    23: grab_banner_telnet,

    25: grab_banner_smtp,

    80: grab_banner_http,

    443: grab_banner_https,


}

def grab_banner(ip: str, port: int) -> str:
    
    try:  
        handler = SERVICES.get(port)

        if handler:
            return handler(ip, port)

        else:
            logger.warning(f"[!] No handler for port {port}")
    except Exception as e:
         logger.warning(e)

if __name__ == '__main__':
    
    ports = [21, 22, 80, 443]

    grab_banner("127.0.0.1", ports)
import socket
import ssl
import threading
from core.parser import create_parser


def connect_sock(ip, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.settimeout(5)

    s.connect((ip, port))
    return s

def receive_response(sock):    
    r = sock.recv(4096)

    decod = r.decode(errors="ignore")
    print(f"SERVICE: {decod}")
    

def grab_banner_http(ip: str, port: int):
            
    try:
        sock = connect_sock(ip, port)   

        request =(
            "GET / HTTP/1.1\r\n"
            f"Host: {ip}\r\n"
            "Connection: close\r\n\r\n"
        )
        sock.send(request.encode())

        receive_response(sock)

    except Exception as err:
            print(err)

    finally:
        sock.close()

def grab_banner_https(ip:str, port: int):           
    
    try: 
        sock = connect_sock(ip, port)

        ssl_socket = ssl.wrap_socket(sock)

        ssl_socket.send(b"GET / HTTP/1.1\r\n")
        response = ssl_socket.recv(4096)

        decod = response.decode(errors="ignore")

        print(f"SERVICE: {decod}")

    except Exception as err:
            print(err)

    finally:
            ssl_socket.close()
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

    try:
        sock = connect_sock(ip, port)

        receive_response(sock)

    except Exception as err:
        print(err)

    finally:
        sock.close()

def grab_banner_ftp(ip: str, port: int):        
    try:
        sock = connect_sock(ip, port)

        receive_response(sock)
    
    except Exception as err:
        print(err)
    
    finally:
        sock.close()

def grab_banner_telnet(ip: str, port: int):
    try:
        sock = connect_sock(ip, port)

        sock.send(b"whoami\r\n")
        receive_response(sock)
    
    except Exception as err:
        print(err)

    finally:
        sock.close()

def grab_banner_smtp(ip: str, port: int):
    try:
        sock = connect_sock(ip, port)

        receive_response(sock)

    except Exception as e:
        print(e)
    
    finally:
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
            handler(ip, port)

        else:
            print(f"[!] No handler for port {port}")
    except Exception as e:
         print(e)

if __name__ == '__main__':
    
    ports = [21, 22, 80, 443]

    grab_banner("127.0.0.1", ports)
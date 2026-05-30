import socket
import ipaddress

def dns_target(target):
    try:
         ipaddress.ip_address(target)
         return target
    
    except ValueError: 
        try:
            return socket.gethostbyname(target)
        
        except socket.gaierror:
            return None
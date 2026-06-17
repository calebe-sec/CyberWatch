import socket
from subprocess import Popen, DEVNULL
import os
import re

def _is_valid_ip(ip):
    pattern = r"^\d{1,3}(\.\d{1,3}){3}$"
    return bool(re.match(pattern, ip))

def verify_network(IPs, start=1, final=254, show_actives=True):
    if not _is_valid_ip(IPs) or start < 1 or final < 2 or final > 254 or not isinstance(show_actives, bool):
        print("Todos os parâmetros devem ser informados de forma correta")
        return False
    
    process = {}
    base_ip = ".".join(IPs.split(".")[:3])

    for host in range(start, final + 1):
        ip = f"{base_ip}.{host}"
        if os.name == "nt":
            proc = Popen(['ping', '-n', '1', '-w', '5', ip], stdout=DEVNULL)
        else:
            proc = Popen(['ping', '-c', '1', '-W', '1', ip], stdout=DEVNULL)
        process[ip] = proc

    return __verify(process, show_actives)

def verify_host(hosts, show_actives=True):
    if not isinstance(hosts, (list, tuple)) or len(hosts) == 0:
        print('Todos os parâmetros devem ser informados de forma correta')
        return False

    process = {}
    for host in hosts:
        try:
            ip = socket.gethostbyname(host)
            if os.name == "nt":
                proc = Popen(['ping', '-n', '1', '-w', '5', ip], stdout=DEVNULL)
            else:
                proc = Popen(['ping', '-c', '1', '-W', '1', ip], stdout=DEVNULL)
            process[ip] = proc
        except Exception as e:
            print(f"Erro ao resolver o ip do host '{host}' : {e}")

    return __verify(process, show_actives)

def __verify(processes, show_actives=True):
    if not isinstance(processes, dict):
        print("Parâmetros inválidos")
        return False

    while processes:
        for ip, proc in list(processes.items()):
            if proc.poll() is not None:
                if proc.returncode == 0:
                    print(f"{ip} -> ativo")
                #elif show_actives:
                #    print(f"{ip} -> sem resposta")
                del processes[ip]

    return True

def ping(target):
    if target.endswith(".0") or "/" in target:
        clean_target = target.split("/")[0]
        if not verify_network(target, 1, 254, True):
            print(f'falha ao verificar a rede {target}/24')
    else:    
        if not verify_host([target], True):  
            print('Falha ao verificar os hosts')

if __name__ == "__main__":
    target = "192.168.18.0"
    ping(target)
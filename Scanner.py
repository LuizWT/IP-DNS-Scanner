from requests import get
import socket
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import asyncio
import ssl
import re

# Tabela de cores ANSI (mantida igual)
COLORS = {
    'Mblack': '\033[1;30m',   # Preto
    'Ired': '\033[1;31m',     # Vermelho
    'Dgreen': '\033[1;32m',   # Verde
    'Nyellow': '\033[1;33m',  # Amarelo
    'Iblue': '\033[1;34m',    # Azul
    'Gpurple': '\033[1;35m',  # Roxo
    'Hcyan': '\033[1;36m',    # Ciano
    'Twhite': '\033[1;37m',   # Branco
    'VRCRM': '\033[0;0m',     # Remover
    'INVTR': '\033[7m'        # Inverter cor
}

logging.basicConfig(filename='port_scan.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

SERVICES = {
    21: {"name": "FTP", "trigger": b"220", "request": None},
    22: {"name": "SSH", "trigger": b"SSH", "request": None},
    25: {"name": "SMTP", "trigger": b"220", "request": None},
    80: {"name": "HTTP", "trigger": b"HTTP", "request": b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n'},
    443: {"name": "HTTPS", "trigger": None, "request": None, "ssl": True},
    8080: {"name": "HTTP", "trigger": b"HTTP", "request": b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n'},
    110: {"name": "POP3", "trigger": b"+OK", "request": None},
    143: {"name": "IMAP", "trigger": b"OK", "request": None},
    3306: {"name": "MySQL", "trigger": b"MySQL", "request": None},
    3389: {"name": "RDP", "trigger": b"RDP", "request": None},
    #TODO Adicionar mais serviços futuramente
}

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def validate_target(target):
    try:
        socket.inet_aton(target)
        return True
    except socket.error:
        try:
            socket.gethostbyname(target)
            return True
        except socket.error:
            return False

async def check_service(alvo, port):
    service_info = SERVICES.get(port)
    if not service_info:
        return None

    ssl_context = None
    if service_info.get("ssl", False):
        ssl_context = ssl.create_default_context()
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(alvo, port, ssl=ssl_context),
            timeout=4.0  # Timeout maior para SSL
        )

        # Se for SSL e não houver trigger, retorna o nome do serviço
        if service_info.get("ssl", False) and service_info["trigger"] is None:
            return service_info["name"]

        # Lógica para serviços com requisição/trigger
        if service_info["request"]:
            writer.write(service_info["request"])
            await writer.drain()

        response = await asyncio.wait_for(reader.read(1024), timeout=3.0)
        if service_info["trigger"] and service_info["trigger"] in response:
            return service_info["name"]

        return None

    except (ssl.SSLError, asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return None
    finally:
        if 'writer' in locals():
            writer.close()
            await writer.wait_closed()

async def scan_port(alvo, port, pbar, semaphore, lock):
    async with semaphore:
        try:
            service = await check_service(alvo, port)
            if service:
                async with lock:  # Bloqueia a saída para evitar sobreposição
                    msg = (f'{COLORS["Nyellow"]}Port {port}  '
                           f'{COLORS["Dgreen"]}...Open '
                           f'{COLORS["Iblue"]}- {service}'
                           f'{COLORS["VRCRM"]}')  # Reset final obrigatório
                    pbar.write(msg)
                    logging.info(f'Porta {port} aberta - {service}')
        except Exception as e:
            logging.error(f'Erro na porta {port}: {str(e)}')
        finally:
            pbar.update(1)

async def scan_ports(alvo):
    print(f'\n{COLORS["Nyellow"]}Scan iniciando... Por favor espere')
    print(f'{COLORS["Ired"]}Ctrl+C para interromper o programa{COLORS["VRCRM"]}\n')

    semaphore = asyncio.Semaphore(1000)
    lock = asyncio.Lock()  # Lock para controle de saída
    
    with tqdm(total=65535, desc=f'{COLORS["Dgreen"]}Scanning ports{COLORS["VRCRM"]}',
             ncols=70, bar_format="{l_bar}%s{bar}%s| {n_fmt}/{total_fmt}" % (COLORS["Iblue"], COLORS["VRCRM"]),
             position=0, leave=True) as pbar:
        
        tasks = []
        for port in range(1, 65536):
            tasks.append(
                asyncio.create_task(
                    scan_port(alvo, port, pbar, semaphore, lock)
                )
            )
        
        await asyncio.gather(*tasks)
    
    print(f'\n{COLORS["Nyellow"]}Scan concluído!{COLORS["VRCRM"]}')

def validar_dominio(dominio):
    regex = re.compile(
        r'^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?\.)+(?:[A-Za-z]{2,6}|[A-Za-z0-9-]{2,})$'
    )
    return re.match(regex, dominio)

def resolver_dns(dominio):
    try:
        return socket.gethostbyname(dominio)
    except socket.gaierror:
        return None
    
async def dns_resolver():
    clear()
    print(f"""\033[1;37m
   ___  _  ______                   
  / _ \/ |/ / __/                   
 / // /    /\ \                     
/____/_/|_/___/                     
     ___              __            
    / _ \___ ______  / /  _____ ____
   / , _/ -_|_-< _ \/ / |/ / -_) __/
  /_/|_|\__/___|___/_/|___/\__/_/   
                                   """)
    print('{:^50}'.format(f'{COLORS["Twhite"]}\n━━━━━━━━━━┫ @LuizWT'.center(50)))
    
    while True:
        alvo = input(f'\n{COLORS["Dgreen"]}Digite o Domínio para DNS (ex: example.com):{COLORS["VRCRM"]} ').strip()

        if not alvo or not validar_dominio(alvo):
            print(f'{COLORS["Ired"]}!!! {COLORS["Nyellow"]}Domínio Inválido {COLORS["Ired"]}!!!')
            continue

        break

    try:
        host = socket.gethostname()
        intern = socket.gethostbyname(host)
        extern = get('https://api.ipify.org').text

        print(f'\n{COLORS["Nyellow"]}Host: {COLORS["Dgreen"]}{host}')
        print(f'{COLORS["Nyellow"]}IP Interno: {COLORS["Dgreen"]}{intern}')
        print(f'{COLORS["Nyellow"]}IP Externo: {COLORS["Dgreen"]}{extern}')

        # Resolver IP do domínio (caso tenha múltiplos IPs)
        target_ips = socket.gethostbyname_ex(alvo)[2]  # Isso retorna uma lista de IPs
        
        if target_ips:
            print(f'{COLORS["Nyellow"]}IPs do Alvo: ')
            for ip in target_ips:
                print(f'{COLORS["Dgreen"]}{ip}')
        else:
            print(f'{COLORS["Ired"]}Erro: Não foi possível resolver o DNS para {alvo}.')

    except socket.gaierror:
        print(f'{COLORS["Ired"]}Erro: Não foi possível resolver o domínio {alvo}.')
    except Exception as e:
        print(f'{COLORS["Ired"]}Erro inesperado: {str(e)}')

def main():
    clear()
    while True:
        print(f'{COLORS["Ired"]}┏━━━━━━━━━━━━━━━━━━━━━━┓\n'
              f'┃ {COLORS["Nyellow"]}[{COLORS["Iblue"]} SCANNER 2.0 {COLORS["Nyellow"]}]{COLORS["Ired"]} ┃\n'
              f'┃                      ┃\n'                     
              f'┣┫{COLORS["Nyellow"]}[01]{COLORS["Dgreen"]} Port Scanner{COLORS["Ired"]}    ┃\n'
              f'┃                      ┃\n'                    
              f'┣┫{COLORS["Nyellow"]}[02]{COLORS["Dgreen"]} DNS Resolver{COLORS["Ired"]}    ┃\n'
              f'┗━━━━━━━━━━━━━━━━━━━━━━┛\n'
              f'{COLORS["Twhite"]}\n━━━━━━━━━━┫ @LuizWT')

        opc = str(input(f'\nDigite a opção que deseja:{COLORS["VRCRM"]} ')).strip().lower()

        if opc in ['1', '01', 'port scanner']:
            clear()
            print("""\033[1;37m
   ___           __                
  / _ \___  ____/ /_               
 / ___/ _ \/ __/ __/               
/_/   \___/_/  \__/                
     ____                          
    / __/______ ____  ___  ___ ____
   _\ \/ __/ _ `/ _ \/ _ \/ -_) __/
  /___/\__/\_,_/_//_/_//_/\__/_/   
                                   """)
            print(f'{COLORS["Twhite"]}\n━━━━━━━━━━┫ @LuizWT'.center(50))
            
            while True:
                alvo = input(f'\n{COLORS["Dgreen"]}Digite o IP/Domínio:{COLORS["VRCRM"]} ').strip()
                if validate_target(alvo):
                    break
                print(f'{COLORS["Ired"]}!!! {COLORS["Nyellow"]}IP/Domínio Inválido {COLORS["Ired"]}!!!')

            asyncio.run(scan_ports(alvo))
            break

        elif opc in ['2', '02', 'dns resolver']:
            asyncio.run(dns_resolver())
            break

        else:
            print(f'{COLORS["Ired"]}!!! {COLORS["Nyellow"]}Opção Inválida {COLORS["Ired"]}!!!')
            clear()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{COLORS['Ired']}Programa interrompido pelo usuário!")
        exit()
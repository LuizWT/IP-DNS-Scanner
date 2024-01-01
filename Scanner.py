from requests import get
import socket
import os
import logging

#Tabela de cores ANSI
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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def check_services(alvo, port):
    service = None
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((alvo, port))
            
            if port == 21:
                response = s.recv(1024)
                if b'220' in response:
                    service = "FTP"
            
            elif port == 25:
                response = s.recv(1024)
                if b'220' in response:
                    service = "SMTP"
            
            elif port == 22:
                response = s.recv(1024)
                if b'SSH' in response:
                    service = "SSH"
            
            if port == 80 or 8080:
                s.sendall(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
                response = s.recv(1024)
                if b'HTTP' in response:
                    service = "HTTP"
            
            elif port == 110:
                response = s.recv(1024)
                if b'+OK' in response:
                    service = "POP3"

            elif port == 135:
                response = s.recv(1024)
                if b'DCE/RPC' in response:
                    service = "DCE/RPC (Microsoft EndPoint Mapper)"

            elif port == 137:
                response = s.recv(1024)
                if b'NetBIOS' in response:
                    service = "NetBIOS Name Service"

            elif port == 138:
                response = s.recv(1024)
                if b'NetBIOS' in response:
                    service = "NetBIOS Datagram Service"

            elif port == 139:
                response = s.recv(1024)
                if b'NetBIOS' in response:
                    service = "NetBIOS Session Service"

            elif port == 140:
                response = s.recv(1024)
                if b'EMFIS Data Service' in response:
                    service = "EMFIS Data Service"

            elif port == 143:
                response = s.recv(1024)
                if b'Internet Message Access Protocol (IMAP)' in response:
                    service = "IMAP"

            elif port == 144:
                response = s.recv(1024)
                if b'News' in response:
                    service = "Usenet News"

            elif port == 389:
                response = s.recv(1024)
                if b'LDAP' in response:
                    service = "LDAP (Lightweight Directory Access Protocol)"

            elif port == 443:
                s.sendall(b'GET / HTTP/1.1\r\nHost: example.com\r\n\r\n')
                response = s.recv(1024)
                if b'HTTP' in response:
                    service = "HTTPS"

            elif port == 445:
                response = s.recv(1024)
                if b'SMB' in response:
                    service = "SMB (Server Message Block)"

            elif port == 1158:
                response = s.recv(1024)
                if b'Oracle' in response:
                    service = "Oracle ORB Listener"

            elif port == 1433:
                response = s.recv(1024)
                if b'Microsoft SQL Server' in response:
                    service = "Microsoft SQL Server"

            elif port == 1433:
                response = s.recv(1024)
                if b'Microsoft SQL Server' in response:
                    service = "Microsoft SQL Server"

            elif port == 1521:
                response = s.recv(1024)
                if b'Oracle' in response:
                    service = "Oracle Database"

            elif port == 3306:
                response = s.recv(1024)
                if b'MySQL' in response:
                    service = "MySQL"
            
            elif port == 3389:
                response = s.recv(1024)
                if b'Remote Desktop Protocol (RDP)' in response:
                    service = "Remote Desktop Protocol (RDP)"

            elif port == 5432:
                response = s.recv(1024)
                if b'PostgreSQL' in response:
                    service = "PostgreSQL"
                
            elif port == 5900:
                response = s.recv(1024)
                if b'VNC (Virtual Network Computing)' in response:
                    service = "VNC (Virtual Network Computing)"
                
            elif port == 6667:
                response = s.recv(1024)
                if b'IRC (Internet Relay Chat)' in response:
                    service = "IRC (Internet Relay Chat)"

            elif port == 8888:
                response = s.recv(1024)
                if b'HTTP' in response:
                    service = "HTTP Alternate (often used for web caching)"

            elif port == 9000:
                response = s.recv(1024)
                if b'Cobalt Strike' in response:
                    service = "CSlistener (commonly associated with Cobalt Strike)"

                #adicionar mais portas aqui em breve
            else:
                service = 'Desconhecido'
    except socket.error as e:
        logging.error(f'Erro ao conectar a porta {port}: {e}')
    return service


def scan_ports(alvo):
    print(f'\n{COLORS["Nyellow"]}Scan iniciando... Por favor espere')
    print(f'{COLORS["Ired"]}Ctrl+C para interromper o programa\n')
    for port in range(65535):
        client = socket.socket()
        client.settimeout(0.05)
        if client.connect_ex((alvo, port)) == 0:
            logging.info(f'Porta {port} aberta')
            service = check_services(alvo, port)
            if service:
                logging.info(f'Servico na porta {port}: {service}')
            print(f'{COLORS["Nyellow"]}Port {port}  {COLORS["Dgreen"]}...Open')
        client.close()


def main():
    clear()
    while True:
        print(f'{COLORS["Ired"]}┏━━━━━━━━━━━━━━━━━━━━━━┓\n'
                              f'┃ {COLORS["Nyellow"]}[{COLORS["Iblue"]} PORT SCANNER 2.0 {COLORS["Nyellow"]}]{COLORS["Ired"]} ┃\n'
                              f'┃                      ┃\n'                     
                              f'┣┫{COLORS["Nyellow"]}[01]{COLORS["Dgreen"]} Port Scanner{COLORS["Ired"]}    ┃\n'
                              f'┃                      ┃\n'                    
                              f'┣┫{COLORS["Nyellow"]}[02]{COLORS["Dgreen"]} DNS Resolver{COLORS["Ired"]}    ┃\n'
                              f'┗━━━━━━━━━━━━━━━━━━━━━━┛\n'
                              f'{COLORS["Twhite"]}━━━━━━━━━━┫ @LuizWT on Discord')


        opc = str(input(f'Digite a opção que deseja:{COLORS["VRCRM"]} ')).strip()

        if opc in ['1', '01', 'Port Scanner']:
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
            print(f'{COLORS["Twhite"]}━━━━━━━━━━┫ @LuizWT on Discord'.center(50))
            while True:
                alvo = input(f'\n{COLORS["Dgreen"]}Digite o IP/Domínio:{COLORS["VRCRM"]} ').strip()
                if len(alvo) > 13 or len(alvo) < 10:
                    print(f'{COLORS["Ired"]}!!! {COLORS["Nyellow"]}IP Inválido {COLORS["Ired"]}!!!')
                else:
                    break
            scan_ports(alvo)
        elif opc in ['2', '02', 'DNS Resolver']:
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
            print('{:^50}'.format(f'{COLORS["Twhite"]}━━━━━━━━━━┫ @LuizWT on Discord'.center(50)))
            while True:
                alvo = input(f'\n{COLORS["Dgreen"]}Digite o Domínio para DNS (http[s]):{COLORS["VRCRM"]} ').strip()
                if 'http' not in alvo:
                    print(f'{COLORS["Ired"]}!!! {COLORS["Nyellow"]}Domínio Inválido {COLORS["Ired"]}!!!')
                else:
                    break

            host = socket.gethostname()
            intern = socket.gethostbyname(host)
            extern = get('https://api.ipify.org').text

            print(f'\n{COLORS["Nyellow"]}Host: {COLORS["Dgreen"]}{host}')
            print(f'{COLORS["Nyellow"]}IP Interno: {COLORS["Dgreen"]}{intern}')
            print(f'{COLORS["Nyellow"]}IP Externo: {COLORS["Dgreen"]}{extern}')

            restart = input(f'\n{COLORS["Twhite"]}Deseja realizar outra consulta S/N?{COLORS["VRCRM"]} ').strip().upper()[0]
            clear()

            if opc not in ['1', '01', 'Port Scanner', '2', '02', 'DNS Resolver']:
                print(f'{COLORS["Ired"]}!!! {COLORS["Nyellow"]}Opção Inválida {COLORS["Ired"]}!!!')
                clear()

if __name__ == "__main__":
    main()

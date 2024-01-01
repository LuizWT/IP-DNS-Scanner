from requests import get
import socket
import os

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

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def scan_ports(alvo):
    print(f'\n{COLORS["Nyellow"]}Scan iniciando... Por favor espere')
    print(f'{COLORS["Ired"]}Ctrl+C para interromper o programa\n')
    for port in range(65535):
        client = socket.socket()
        client.settimeout(0.05)
        if client.connect_ex((alvo, port)) == 0:
            print(f'{COLORS["Nyellow"]}Port {port}  {COLORS["Dgreen"]}...Open')

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

# Scanner de IP e DNS

## Descrição

O **Scanner de IP e DNS** é uma ferramenta simples, mas poderosa, que permite realizar duas funções principais:

1. **Verificação de Portas**:  
   Verifica se as portas de um endereço IP estão abertas ou fechadas. Envia solicitações para portas específicas e aguarda as respostas para determinar o estado da porta.

2. **Verificação de DNS**:  
   Obtém o endereço IP correspondente a um nome de domínio, usando a API pública do [ipify](https://api.ipify.org/) para realizar a consulta.

**Funcionalidades**:
- Verificação de portas.
- Resolução de DNS utilizando uma API confiável.
- Simplicidade de uso com uma interface clara.

<hr>

## Instalação

Clone o repositório para o seu diretório local:

```bash
git clone https://github.com/LuizWT/IP-DNS-Scanner.git ~/Scanner
```

Entre no projeto e instale as dependências:

```bash
cd ~/Scanner && pip3 install -r requirements.txt
```

Inicie a ferramenta:

```bash
python3 Scanner.py
```

## Saída

  Após a varredura ser finalizada, o output ficará salvo em `Scanner/port_scan.log`

<hr>

## Apoio ao Projeto

Se você quiser contribuir com o projeto, sinta-se à vontade para abrir Issues ou fazer Pull Requests no repositório oficial do projeto.
  
Quer apoiar ainda mais? Faça uma doação e ajude a manter este projeto vivo!

**BTC Wallet**:  
`bc1qfy534ujs9yekwthe063fck0zf7hel7paem6sxl`
  
<hr>

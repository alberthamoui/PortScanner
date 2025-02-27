import socket     # para conexões de rede.
import ipaddress  # para validar endereços IP.
import threading  # para acelerar o escaneamento
import argparse   # para processar argumentos de linha de comando


PORTS = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP"
}


listaPorts = []
def scanPort(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # cria o socket TCP
        sock.settimeout(5) # tempo max de espera
        result = sock.connect_ex((ip, port)) # tenta conectar na porta
        if result == 0:
            try:
                service = socket.getservbyport(port) # pega o nome do serviço
            except:
                if port in PORTS:
                    service = PORTS[port]
                else:
                    service = "Desconhecido"
            print(f"\nPorta {port} aberta ({service})")
            listaPorts.append({port: service})
        elif result in [111, 10061]: # pega linux e windows
            print(f"\nPorta {port} fechada")
            pass
        elif result in [110, 13, 10060, 10013]: # pega linux e windows
            print(f"\nPorta {port} filtrada")
            pass
        else:
            print(f"\nOUTROS: {result}")
        
        
        sock.close() # fecha pra liberar recursos
    except Exception as e:
        print(f"Erro ao escanear {ip}:{port} -> {e}")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def scanHost(host, start_port, end_port):
    print(f"\nEscaneando host {host} nas portas {start_port}-{end_port}...\n")
    threads = []
    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scanPort, args=(host, port)) 
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("\nPortas abertas:")
    for port_info in listaPorts:
        for port, service in port_info.items():
            print(f"Porta {port}: {service}")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def main():
    parser = argparse.ArgumentParser(description="Port Scanner em Python")
    parser.add_argument("-t", action="store_true", help="Escaneamento TCP")  # TCP
    parser.add_argument("target", help="IP ou hostname a ser escaneado")  # IP como argumento posicional
    parser.add_argument("ports", help="Intervalo de portas (ex: 20-100)")  # Intervalo de portas como argumento posicional

    args = parser.parse_args()

    # Verifica TCP
    if not args.t:
        print("Erro: Defina '-t' ou '-u' para escanear portas TCP ou UDP.")
        return

    # Valida IP/Hostname
    try:
        ip = ipaddress.ip_address(args.target)  # IP
    except ValueError:
        try:
            ip = socket.gethostbyname(args.target)  # Hostname
        except socket.gaierror:
            print("Erro: Host inválido.")
            return

    # Validação portas
    try:
        start_port, end_port = map(int, args.ports.split("-"))
        if start_port < 1 or end_port > 65535 or start_port > end_port:
            raise ValueError
    except ValueError:
        print("Erro: Intervalo de portas inválido. Use algo como 20-100.")
        return

    # Inicia o escaneamento
    scanHost(str(ip), start_port, end_port)





if __name__ == "__main__":
    main()

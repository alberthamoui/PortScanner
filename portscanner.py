import socket     # para conexões de rede.
import ipaddress  # para validar endereços IP e redes.
import threading  # para acelerar o escaneamento
from tabulate import tabulate  # para exibir resultados organizados


# Serviços conhecidos
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

lock = threading.Lock()


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def scanPort(ip, port, open_ports, lock):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        result = sock.connect_ex((ip, port))
        
        if result == 0:
            try:
                service = socket.getservbyport(port)
            except:
                service = PORTS.get(port, "Desconhecido")
            print(f"\n[ABERTA] Porta {port} ({service})")
            with lock:
                open_ports.append((port, service))
        else:
            if result in [socket.errno.EACCES, socket.errno.ECONNREFUSED]:
                print(f"\n[FECHADA] Porta {port}")
            elif result in [socket.errno.ETIMEDOUT, socket.errno.ENETUNREACH, socket.errno.EHOSTUNREACH]:
                print(f"\n[FILTRADA] Porta {port}")
            else:
                print(f"\n[ERRO] Porta {port} -> Código de erro: {result}")
        sock.close()
    except socket.timeout:
        print(f"\n[FILTRADA] Porta {port} -> Tempo limite excedido")
    except socket.error as e:
        print(f"\n[ERRO] Porta {port} -> {e}")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def scanHost(host, start_port, end_port):
    print(f"\n Escaneando host {host} nas portas {start_port}-{end_port}...\n")
    
    open_ports = []  
    lock = threading.Lock()
    threads = []

    for port in range(start_port, end_port + 1):
        t = threading.Thread(target=scanPort, args=(host, port, open_ports, lock))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print("-=" * 30)
    print("\n Portas abertas:")
    table = [[port, service] for port, service in open_ports]
    print(tabulate(table, headers=["Porta", "Serviço"], tablefmt="grid"))


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def scanRede(rede, start_port, end_port):
    try:
        net = ipaddress.ip_network(rede, strict=False)  
        listaIP = [str(ip) for ip in net.hosts()]  
        print(f"\n Escaneando rede {rede} ({len(listaIP)} hosts)...\n")
        for ip in listaIP:
            scanHost(ip, start_port, end_port)
    except ValueError:
        print("\n ERRO: Rede inválida. Certifique-se de usar um formato correto (ex: 192.168.1.0/24).")
        return

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def pegaPort():
    while True:
        try:
            ports = input("\n Digite o intervalo de portas para escanear (ex: 20-100): ").strip()
            start_port, end_port = map(int, ports.split("-"))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError
            return start_port, end_port
        except ValueError:
            print(" Erro: Intervalo de portas inválido. Use um formato como '20-100' (valores entre 1 e 65535).")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

def main():
    print(" PortScanner ")
    while True:
        print("\n--------------------------------")
        print("1. Escanear um único host")
        print("2. Escanear uma rede inteira")
        print("3. Sair")
        print("--------------------------------")
        opcao = input("\nEscolha uma opção (1, 2 ou 3): ").strip()
        if opcao == "1":
            # Escaneamento de host único
            target = input("\n Digite o IP ou hostname do alvo (192.168.1.1/google.com): ").strip()
            try:
                ip = socket.gethostbyname(target)
            except socket.gaierror:
                print("\n ERRO: Host inválido. Tente novamente.")
                continue
            start_port, end_port = pegaPort()
            scanHost(ip, start_port, end_port)

        elif opcao == "2":
            rede = input("\n Digite a rede no formato CIDR (ex: 192.168.1.0/24): ").strip()
            try:
                ipaddress.ip_network(rede, strict=False)  # Valida a rede
            except ValueError:
                print("\n ERRO: Formato de rede inválido.")
                continue
            start_port, end_port = pegaPort()
            scanRede(rede, start_port, end_port)
        elif opcao == "3":
            print("\n Adeus!")
            break
        else:
            print("\n Opção inválida. Escolha entre 1, 2 ou 3.")

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

if __name__ == "__main__":
    main()

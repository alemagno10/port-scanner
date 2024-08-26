import socket
import threading

# Dicionário de portas conhecidas (Well-Known Ports) e seus serviços associados
well_known_ports = {
    20: "FTP (File Transfer Protocol)",
    21: "FTP (File Transfer Protocol)",
    22: "SSH (Secure Shell)",
    23: "Telnet",
    25: "SMTP (Simple Mail Transfer Protocol)",
    53: "DNS (Domain Name System)",
    80: "HTTP (Hypertext Transfer Protocol)",
    110: "POP3 (Post Office Protocol)",
    143: "IMAP (Internet Message Access Protocol)",
    443: "HTTPS (HTTP Secure)",
    445: "Microsoft-DS (Windows File Sharing)",
    3306: "MySQL",
    3389: "RDP (Remote Desktop Protocol)",
    5432: "PostgreSQL",
    5900: "VNC (Virtual Network Computing)",
    8080: "HTTP (Alternative Port)"
}

# Lista para armazenar as portas abertas
abertas = []
# Lock para evitar conflitos na lista compartilhada entre threads
abertas_lock = threading.Lock()

# Função que escaneia uma porta específica
def scan_port(ip, porta):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(1)
    conexao = sock.connect_ex((ip, porta))
    servico = well_known_ports.get(porta, "Desconhecido")
    if conexao == 0:
        with abertas_lock:
            abertas.append(porta)
        print(f"Porta {porta}: aberta - {servico}")
    else:
        print(f"Porta {porta}: falhou")
    sock.close()

# Função principal de escaneamento de portas
def scanner_de_portas(host, porta_inicial, porta_final):
    ip = socket.gethostbyname(host)

    # Criar uma thread para cada porta dentro do intervalo especificado
    threads = []
    for porta in range(porta_inicial, porta_final + 1):
        t = threading.Thread(target=scan_port, args=(ip, porta))
        threads.append(t)
        t.start()

    # Esperar todas as threads terminarem
    for t in threads:
        t.join()

    print("\nPortas abertas: ", abertas)

# Entrada do usuário
ip = input("Digite um IP ou hostname: ")
print("Em seguida, digite o intervalo de portas para observar: ")
porta_inicial = int(input("Porta inicial: "))
porta_final = int(input("Porta final: "))
print("\n")
scanner_de_portas(ip, porta_inicial, porta_final)

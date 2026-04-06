import socket
import time

HOST = 'localhost'
PORTA = 5000


tamanhos_kb = [1, 10, 20, 30, 40, 50, 60]
NUM_PACOTES = 1000

print(f"{'Tamanho (KB)':<15} | {'Tempo (s)':<15} | {'Taxa (Mbps)':<15}")
print("-" * 50)

for tamanho in tamanhos_kb:
    bytes_payload = b'x' * (tamanho * 1024)
    
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((HOST, PORTA))
    
    inicio = time.time()
    
    for _ in range(NUM_PACOTES):
        cliente.sendall(bytes_payload)
    
    cliente.close()
    
    fim = time.time()
    tempo_total = fim - inicio
    
    total_megabits = (tamanho * 1024 * NUM_PACOTES * 8) / 1_000_000
    
    taxa_mbps = total_megabits / tempo_total if tempo_total > 0 else 0
    
    print(f"{tamanho:<15} | {tempo_total:<15.4f} | {taxa_mbps:.2f}")
    
    time.sleep(0.5)

print("-" * 50)
print("Teste TCP finalizado. Copie esses dados para a sua tabela!")
import socket
import time

HOST = 'localhost'
PORTA = 5001

tamanhos_kb = [1, 10, 20, 30, 40, 50, 60]
NUM_PACOTES = 1000 

print(f"{'Tam (KB)':<10} | {'Tempo (s)':<10} | {'Taxa (Mbps)':<12} | {'Perda (%)':<10} | {'Fora Ordem'}")
print("-" * 65)

for tamanho in tamanhos_kb:
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    cliente.settimeout(2.0) 
    
    inicio = time.time()
    
    for i in range(NUM_PACOTES):
        seq_str = str(i).ljust(10).encode('utf-8')
        tamanho_bytes = tamanho * 1024
        
        payload = seq_str + b'x' * (tamanho_bytes - 10)
        
        cliente.sendto(payload, (HOST, PORTA))
        
        time.sleep(0.0001) 
        
    cliente.sendto(b'FIM', (HOST, PORTA))
    
    try:
        resposta, _ = cliente.recvfrom(1024)
        fim = time.time()
        tempo_total = fim - inicio
        
        dados_ack = resposta.decode('utf-8').split(',')
        recebidos = int(dados_ack[1])
        fora_ordem = int(dados_ack[2])
        
        perda_percentual = ((NUM_PACOTES - recebidos) / NUM_PACOTES) * 100
        
        total_megabits = (tamanho * 1024 * NUM_PACOTES * 8) / 1_000_000
        taxa_mbps = total_megabits / tempo_total if tempo_total > 0 else 0
        
        print(f"{tamanho:<10} | {tempo_total:<10.4f} | {taxa_mbps:<12.2f} | {perda_percentual:<10.1f} | {fora_ordem}")
        
    except socket.timeout:
        print(f"{tamanho:<10} | Ocorreu falha massiva. O pacote 'FIM' ou o 'ACK' se perdeu na rede.")
        
    cliente.close()
    time.sleep(0.5)

print("-" * 65)
print("Teste UDP finalizado. Copie esses dados para a sua tabela!")
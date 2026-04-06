import socket

HOST = 'localhost'
PORTA = 5001

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((HOST, PORTA))

print("Servidor UDP de Teste rodando na porta 5001...")
print("Aguardando o tiroteio de pacotes...")

pacotes_recebidos = 0
pacotes_fora_de_ordem = 0
ultimo_seq_recebido = -1

while True:
    try:
        dados, endereco = servidor.recvfrom(65536) 
        
        if dados.startswith(b'FIM'):
            resposta_ack = f"ACK,{pacotes_recebidos},{pacotes_fora_de_ordem}"
            servidor.sendto(resposta_ack.encode('utf-8'), endereco)
            
            pacotes_recebidos = 0
            pacotes_fora_de_ordem = 0
            ultimo_seq_recebido = -1
            continue
            
        seq_str = dados[:10].decode('utf-8').strip()
        seq = int(seq_str)
        
        pacotes_recebidos += 1
        
        if seq <= ultimo_seq_recebido:
            pacotes_fora_de_ordem += 1
        else:
            ultimo_seq_recebido = seq
            
    except Exception as e:
        pass 
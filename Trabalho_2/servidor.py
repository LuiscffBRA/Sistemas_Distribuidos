import socket
import threading
import time

HOST = 'localhost'
PORTA = 5555

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORTA))
servidor.listen(2)

print("Servidor TCP rodando! Esperando 2 jogadores...")

estado = {
    'p1_y': 250, 'p2_y': 250,
    'bola_x': 400, 'bola_y': 300,
    'vel_x': 5, 'vel_y': 5,
    'pts1': 0, 'pts2': 0
}

conexoes = []

def processar_fisica():
    global estado
    while True:
        time.sleep(0.016) # Aproximadamente 60 frames por segundo
        
        # Só move a bola se tiver 2 jogadores conectados
        if len(conexoes) == 2:
            estado['bola_x'] += estado['vel_x']
            estado['bola_y'] += estado['vel_y']

            # Colisão Teto e Chão
            if estado['bola_y'] <= 0 or estado['bola_y'] >= 585:
                estado['vel_y'] *= -1

            if estado['bola_x'] <= 65 and estado['p1_y'] < estado['bola_y'] < estado['p1_y'] + 100:
                estado['vel_x'] *= -1
                estado['bola_x'] = 66

            if estado['bola_x'] >= 720 and estado['p2_y'] < estado['bola_y'] < estado['p2_y'] + 100:
                estado['vel_x'] *= -1
                estado['bola_x'] = 719

            if estado['bola_x'] < 0:
                estado['pts2'] += 1
                resetar_bola()
            elif estado['bola_x'] > 800:
                estado['pts1'] += 1
                resetar_bola()

def resetar_bola():
    estado['bola_x'] = 400
    estado['bola_y'] = 300
    estado['vel_x'] *= -1

def lidar_com_cliente(conn, jogador_id):
    conn.send(str.encode(str(jogador_id)))
    
    while True:
        try:
            dados = conn.recv(1024).decode('utf-8')
            if not dados: break
            
            if jogador_id == 1:
                estado['p1_y'] = int(dados)
            else:
                estado['p2_y'] = int(dados)

            pacote = f"{estado['p1_y']},{estado['p2_y']},{estado['bola_x']},{estado['bola_y']},{estado['pts1']},{estado['pts2']}"
            conn.send(str.encode(pacote))
        except:
            break
            
    print(f"Jogador {jogador_id} desconectou.")
    conn.close()

threading.Thread(target=processar_fisica, daemon=True).start()

jogador_atual = 1
while True:
    conn, ender = servidor.accept()
    print(f"Jogador {jogador_atual} conectou!")
    conexoes.append(conn)
    threading.Thread(target=lidar_com_cliente, args=(conn, jogador_atual), daemon=True).start()
    jogador_atual += 1
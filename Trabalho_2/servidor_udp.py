import socket
import threading
import time
import random

HOST = 'localhost'
PORTA = 5556

servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
servidor.bind((HOST, PORTA))

print("Servidor UDP rodando! Arremessando pacotes...")

estado = {
    'p1_y': 250, 'p2_y': 250,
    'bola_x': 400, 'bola_y': 300,
    'vel_x': 5, 'vel_y': 5,
    'pts1': 0, 'pts2': 0
}

jogadores = {} # Guarda o endereço (IP, Porta) dos 2 jogadores

def processar_fisica():
    global estado
    while True:
        time.sleep(0.016)
        
        if len(jogadores) == 2:
            estado['bola_x'] += estado['vel_x']
            estado['bola_y'] += estado['vel_y']

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

            # Envia o estado do jogo para os dois jogadores
            pacote = f"{estado['p1_y']},{estado['p2_y']},{estado['bola_x']},{estado['bola_y']},{estado['pts1']},{estado['pts2']},{estado['vel_x']},{estado['vel_y']}"
            
            for ender in jogadores.values():
                # SIMULADOR DE PERDA DE PACOTE (Joga 20% fora pra testar a extrapolação)
                if random.random() > 0.20: 
                    servidor.sendto(str.encode(pacote), ender)
                    
def resetar_bola():
    estado['bola_x'] = 400
    estado['bola_y'] = 300
    estado['vel_x'] *= -1

threading.Thread(target=processar_fisica, daemon=True).start()

while True:
    try:
        dados, endereco = servidor.recvfrom(1024)
        msg = dados.decode('utf-8')
        
        if msg == "CONECTAR" and len(jogadores) < 2:
            id_novo = len(jogadores) + 1
            jogadores[id_novo] = endereco
            print(f"Jogador {id_novo} entrou! {endereco}")
            servidor.sendto(str.encode(str(id_novo)), endereco)
        
        elif endereco in jogadores.values():
            for j_id, j_end in jogadores.items():
                if j_end == endereco:
                    if j_id == 1:
                        estado['p1_y'] = int(msg)
                    else:
                        estado['p2_y'] = int(msg)
    except:
        pass
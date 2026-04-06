import pygame
import sys
import socket

HOST = 'localhost'
PORTA = 5556
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

cliente.settimeout(0.5) 
cliente.sendto(b"CONECTAR", (HOST, PORTA))

try:
    dados, _ = cliente.recvfrom(1024)
    meu_id = int(dados.decode('utf-8'))
    print(f"Conectado via UDP! Eu sou o Jogador {meu_id}")
except socket.timeout:
    print("O Servidor UDP não respondeu. Rodou o servidor_udp.py?")
    sys.exit()
 
# Se o pacote UDP não chegar rápido, o código não trava e vai pra extrapolação
cliente.settimeout(0.005)

pygame.init()
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption(f"Ping Pong - Jogador {meu_id} (UDP c/ EXTRAPOLAÇÃO)")
fonte = pygame.font.Font(None, 74)
fonte_aviso = pygame.font.Font(None, 24)

minha_raquete_y = 250
# O pacote agora tem 8 coisas: [p1_y, p2_y, bola_x, bola_y, pts1, pts2, vel_x, vel_y]
estado = [250, 250, 400, 300, 0, 0, 0, 0] 
relogio = pygame.time.Clock()
rodando = True

while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_UP]: minha_raquete_y -= 5
    if teclas[pygame.K_DOWN]: minha_raquete_y += 5

    if minha_raquete_y < 0: minha_raquete_y = 0
    if minha_raquete_y > 500: minha_raquete_y = 500

    cliente.sendto(str.encode(str(minha_raquete_y)), (HOST, PORTA))

    pacote_recebido = False
    
    try:
        resposta, _ = cliente.recvfrom(1024)
        estado = [int(x) for x in resposta.decode('utf-8').split(',')]
        pacote_recebido = True
    except socket.timeout:
        # O pacote se perdeu na rede. Usaremos a extrapolação para supor a posição
        pass

    if not pacote_recebido:
        estado[2] += estado[6] # bola_x = bola_x + vel_x
        estado[3] += estado[7] # bola_y = bola_y + vel_y
        
        # Simula colisão básica para a bola extrapolada não vazar da tela
        if estado[3] <= 0 or estado[3] >= 585:
            estado[7] *= -1 # Inverte a velocidade Y

    tela.fill((0, 0, 0))
    pygame.draw.line(tela, (255,255,255), (400, 0), (400, 600), 2)
    
    texto_pts1 = fonte.render(str(estado[4]), True, (255,255,255))
    texto_pts2 = fonte.render(str(estado[5]), True, (255,255,255))
    tela.blit(texto_pts1, (250, 20))
    tela.blit(texto_pts2, (510, 20))

    pygame.draw.rect(tela, (255,255,255), (50, estado[0], 15, 100))
    pygame.draw.rect(tela, (255,255,255), (735, estado[1], 15, 100))
    pygame.draw.ellipse(tela, (255,255,255), (estado[2], estado[3], 15, 15))

    if not pacote_recebido:
        aviso = fonte_aviso.render("Pacote Perdido! EXTRAPOLANDO...", True, (255, 0, 0))
        tela.blit(aviso, (10, 10))

    pygame.display.flip()
    relogio.tick(60)

cliente.close()
pygame.quit()
sys.exit()
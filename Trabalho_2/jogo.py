import pygame
import sys
import socket

HOST = 'localhost'
PORTA = 5555
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    cliente.connect((HOST, PORTA))
    meu_id = int(cliente.recv(1024).decode('utf-8'))
    print(f"Conectado! Eu sou o Jogador {meu_id}")
except:
    print("Erro ao conectar. Cadê o servidor?")
    sys.exit()

pygame.init()
tela = pygame.display.set_mode((800, 600))
pygame.display.set_caption(f"Ping Pong - Jogador {meu_id} (TCP)")
fonte = pygame.font.Font(None, 74)

minha_raquete_y = 250
# Array que guarda o pacote do servidor: [p1_y, p2_y, bola_x, bola_y, pts1, pts2]
estado = [250, 250, 400, 300, 0, 0] 

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

    try:
        cliente.send(str.encode(str(minha_raquete_y)))
        resposta = cliente.recv(1024).decode('utf-8')
        estado = [int(x) for x in resposta.split(',')]
    except:
        print("Conexão caiu!")
        break

    tela.fill((0, 0, 0))
    
    pygame.draw.line(tela, (255,255,255), (400, 0), (400, 600), 2)
    
    texto_pts1 = fonte.render(str(estado[4]), True, (255,255,255))
    texto_pts2 = fonte.render(str(estado[5]), True, (255,255,255))
    tela.blit(texto_pts1, (250, 20))
    tela.blit(texto_pts2, (510, 20))

    pygame.draw.rect(tela, (255,255,255), (50, estado[0], 15, 100))
    pygame.draw.rect(tela, (255,255,255), (735, estado[1], 15, 100))
    pygame.draw.ellipse(tela, (255,255,255), (estado[2], estado[3], 15, 15))

    pygame.display.flip()
    relogio.tick(60)

cliente.close()
pygame.quit()
sys.exit()
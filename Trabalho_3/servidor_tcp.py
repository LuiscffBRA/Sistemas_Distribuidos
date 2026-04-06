import socket

HOST = 'localhost'
PORTA = 5000

servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
servidor.bind((HOST, PORTA))
servidor.listen(1)

print("Servidor TCP de Teste rodando na porta 5000...")
print("Aguardando o envio massivo de pacotes do cliente...")

while True:
    conexao, endereco = servidor.accept()
    
    try:
        while True:
            dados = conexao.recv(65536) 
            if not dados:
                break
    except:
        pass
    finally:
        conexao.close()
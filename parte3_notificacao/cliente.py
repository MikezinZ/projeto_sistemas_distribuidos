import socket

arquivo_imagem = "imagens_entrada/detetive_pikachu.png"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    try:
        s.connect(('127.0.0.1', 8080))
        print("Conectado ao Servidor. Enviando pedido....")

        s.sendall(arquivo_imagem.encode('utf-8'))

        resposta = s.recv(1024)
        print(f"Resposta do servidor: {resposta.decode('utf-8')}")

    except ConnectionRefusedError:
        print("Erro: Não foi possível conectar ao servidor.")

print("\nPedido enviado! Fique atento ao terminal do 'Serviço de notificação'!")

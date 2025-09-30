import threading
import socket

contador_de_conexoes = 0
contador_de_conexoes_priv = threading.Lock()

def gestao_cliente(conexao, endereco_cliente):
  
    global contador_de_conexoes

    with contador_de_conexoes_priv:
        contador_de_conexoes += 1
        contador_atual = contador_de_conexoes

    print(f"Nova conexão: {endereco_cliente} se conectou8.\nTotal de conexões: {contador_atual}")

    try:
        while True:
            data = conexao.recv(1024)
            if not data:
                break # sem recebimento de dados, o cliente se desconecta

            mensagem = data.decode('utf-8')
            print(f"Mensagem de {endereco_cliente}: {mensagem}")

            res = f"Hello, Client!! Conexões ativas: {contador_atual}"
            conexao.sendall(res.encode('utf-8'))

    finally:
        with contador_de_conexoes_priv:
             contador_de_conexoes -= 1
        print(f"Conexão Fechada: {endereco_cliente}.\ntotal de conexões: {contador_atual}")
        conexao.close()


# ----- Configuração Servidor -----

HOST = '127.0.0.1' #localhost
PORT = 8080 # Porta server

socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_servidor.bind((HOST, PORT))
socket_servidor.listen()

print(f"Servidor escutando em {HOST}:{PORT}")

while True:
    conexao, endereco_cliente = socket_servidor.accept()

    cliente_thread = threading.Thread(target=gestao_cliente, args=(conexao, endereco_cliente))
    cliente_thread.start()

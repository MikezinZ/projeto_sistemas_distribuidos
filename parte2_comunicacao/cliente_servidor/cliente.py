import socket

HOST = "127.0.0.1"
PORT = 8080


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente_socket:
    cliente_socket.connect((HOST, PORT))

    msg_enviar = "Hello, Server!"
    cliente_socket.sendall(msg_enviar.encode('utf-8'))


    data = cliente_socket.recv(1024)

    print(f"Resposta do servidor: {data.decode('utf-8')}")


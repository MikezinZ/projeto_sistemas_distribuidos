import threading
import socket
from PIL import Image, ImageFilter
import xmlrpc.client
import pika
import queue
import time

cliente_rpc = xmlrpc.client.ServerProxy('http://127.0.0.1:9000')

try:
    connection_pika = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel_pika = connection_pika.channel()
    channel_pika.queue_declare(queue="fila_de_status", durable=True)
except pika.exceptions.AMQConnectionError:
    print('Erro: Servidor de Pedidos não conseguiu conectar ao rabbitMQ.')
    connection_pika = None

tarefa_queue = queue.Queue()


def processador_de_imagens():
   try:
       connection_pika = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
       channel_pika = connection_pika.channel()
       channel_pika.queue_declare(queue='fila_de_status', durable=True)
   except pika.exceptions.AMQConnectionError:
        print("[Error]: Não foi possível conectar ao RabbitMQ.")
        return
   
   print("[SERVIDOR]: Server pronto e conectado ao RabbitMQ.")

   while True:
       id_cliente, caminho_imagem = tarefa_queue.get()
       print(f"[SERVIDOR]: Iniciando processamento para {id_cliente} - {caminho_imagem}")

       try:
           channel_pika.basic_publish(
               exchange='',
               routing_key='fila_de_status',
               body=f"Pedido de '{id_cliente}' está sendo processado. Outros {tarefa_queue.qsize()} na frente.",
               properties=pika.BasicProperties(delivery_mode=2)
           )
       except Exception as e:
           print(f"[ERRO]: Falha ao republicar na fila: {e}")
           continue
       
       time.sleep(5)

       try:
           with Image.open(caminho_imagem) as img:
               img_filtrada = img.filter(ImageFilter.CONTOUR)
               novo_caminho = f"{caminho_imagem.split('.')[0]}_filtrado.png"

               img_filtrada.save(novo_caminho)


               cliente_rpc.notificar_conclusao(id_cliente, novo_caminho)

       except Exception as e:
           print(f"Erro ao processar a imagem: {e}")

           tarefa_queue.task_done()

def fila_conexao_cliente(conexao, endere_cliente):
    try:
        data = conexao.recv(1024)
        if data:
            caminho_imagem = data.decode('utf-8')
            id_cliente = f"{endere_cliente[0]}:{endere_cliente[1]}"

            tarefa_queue.put((id_cliente, caminho_imagem))
            print(f"Novo pedido recebido de {id_cliente} para a imagem {caminho_imagem}")
            conexao.sendall(b"Pedido recebido e colocado na fila!")
    finally:
        conexao.close()

    
if __name__ == '__main__':
    thread_de_trabalho = threading.Thread(target=processador_de_imagens, daemon=True)
    thread_de_trabalho.start()

    socket_servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_servidor.bind(('127.0.0.1', 8080))
    socket_servidor.listen()

    print(f"Servidor escutando em {'127.0.0.1'}:{8080}")

    while True:
        conexao, endereco_cliente = socket_servidor.accept()

        cliente_thread = threading.Thread(target=fila_conexao_cliente, args=(conexao, endereco_cliente))
        cliente_thread.start()


        


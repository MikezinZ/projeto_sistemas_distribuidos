from xmlrpc.server import SimpleXMLRPCServer
import pika
import threading

def notificar_conclusao(id_cliente, nome_arquivo):
    """
    Função que é chamada pelo servidor 
    """
    print(f"[RPC]: Pedido do cliente '{id_cliente}' está pronto! Imagem: {nome_arquivo}")
    return True

def iniciar_servidor_rpc():
    server = SimpleXMLRPCServer(('127.0.0.1', 9000), allow_none= True)
    print(f"O servidor RPC está escutando na porta 9000.")
    server.serve_forever()

def callback_fila(ch, metodo, propriedades, body):
    print(f"Painel de senha: {body.decode()}")
    ch.basic_ack(delivery_tag=metodo.delivery_tag)

def iniciar_consumidor_fila():
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='fila_de_status', durable=True)
        channel.basic_consume(queue='fila_de_status', on_message_callback=callback_fila)

        print("Consumidor da fila (painel de senhas) esperando por mensagens...")
        channel.start_consuming()
    except pika.exceptions.AMQPConnectionError:
        print("Erro: Não foi possível conectar ao rabbitMQ. Verifique se o container está rodando...") 

if __name__ == "__main__":
    rpc_thread = threading.Thread(target=iniciar_servidor_rpc)
    fila_thread = threading.Thread(target=iniciar_consumidor_fila)

    rpc_thread.start()
    fila_thread.start()

    rpc_thread.join()
    fila_thread.join()

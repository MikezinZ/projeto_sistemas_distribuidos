# peer.py

import socket
import threading
import sys

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Lista para manter as conexões ativas com outros peers
        self.peers = []
        # Trava para garantir que a lista de peers seja acessada de forma segura por múltiplas threads
        self.lock = threading.Lock()

    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Peer escutando em {self.host}:{self.port}")

        while True:
            # Aceita uma nova conexão
            conn, addr = self.socket.accept()
            print(f"Nova conexão recebida de {addr}")
            
            # Adiciona a nova conexão à lista de peers
            self.add_peer(conn)
            
            # Inicia uma nova thread para gerenciar a comunicação com este novo peer
            thread = threading.Thread(target=self.handle_peer, args=(conn, addr))
            thread.start()

    def handle_peer(self, conn, addr):
        # Envia uma mensagem de boas-vindas ao peer que se conectou
        try:
            conn.sendall(f"Hello from node: {self.port}!".encode('utf-8'))
        except socket.error:
            print(f" Erro ao enviar mensagem pra {addr}. A conexão fechou")
            self.remove_peer(conn)
            return

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break  # Conexão fechada pelo outro lado
                
                mensagem_recebida = data.decode('utf-8')
                print(f"\n[Mensagem de {addr}]: {mensagem_recebida}\n> ", end="")

            except socket.error:
                break # Erro na conexão

        print(f"Conexão com {addr} foi fechada.")
        self.remove_peer(conn)
        conn.close()

    def connect_to_peer(self, peer_host, peer_port):
        try:
            # Cria um novo socket para atuar como cliente
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, int(peer_port)))
            
            # Adiciona o peer à lista de conexões
            self.add_peer(peer_socket)
            print(f" * Conectado a {peer_host}:{peer_port}")

            # A primeira mensagem recebida será a de boas-vindas
            initial_msg = peer_socket.recv(1024).decode('utf-8')
            print(f"\n[Resposta do Nó]: {initial_msg}\n> ", end="")

            # Inicia uma thread para gerenciar esta nova conexão
            thread = threading.Thread(target=self.handle_peer, args=(peer_socket, (peer_host, peer_port)))
            thread.start()
            return True

        except socket.error as e:
            print(f"Falha ao conectar com {peer_host}:{peer_port}. Erro: {e}")
            return False

    def send_to_peers(self, message):
        # Prepara a mensagem com o identificador deste nó
        full_message = f"Node {self.port}: {message}"

        with self.lock:
            # Cria uma cópia da lista para iterar, caso a original seja modificada
            for peer_conn in list(self.peers):
                try:
                    peer_conn.sendall(full_message.encode('utf-8'))
                except socket.error:
                    # Se não conseguir enviar, remove o peer da lista
                    print(f"[!] Não foi possível enviar mensagem para um peer. Removendo...")
                    self.remove_peer(peer_conn, lock_needed=False) # O lock já foi adquirido

    def add_peer(self, peer_conn):
        """Adiciona um peer à lista de conexões de forma segura."""
        with self.lock:
            if peer_conn not in self.peers:
                self.peers.append(peer_conn)
                print(f"[*] Peers ativos: {len(self.peers)}")

    def remove_peer(self, peer_conn, lock_needed=True):
        """Remove um peer da lista de conexões de forma segura."""
        if lock_needed:
            self.lock.acquire()
        
        if peer_conn in self.peers:
            self.peers.remove(peer_conn)
            print(f"[*] Peers ativos: {len(self.peers)}")
        
        if lock_needed:
            self.lock.release()

    def start(self):
        """Inicia o peer: a thread do servidor e o loop de entrada do usuário."""
        # Inicia a thread do servidor para aceitar conexões em segundo plano
        server_thread = threading.Thread(target=self.start_server)
        server_thread.daemon = True # Permite que o programa feche mesmo se a thread estiver rodando
        server_thread.start()

        print("Bem-vindo ao chat do zap! Digite 'connect <host> <port>' para se conectar a outro contato.")
        
        # Loop principal para entrada do usuário
        while True:
            try:
                user_input = input("> ")
                if user_input.startswith("connect "):
                    parts = user_input.split()
                    if len(parts) == 3:
                        self.connect_to_peer(parts[1], parts[2])
                    else:
                        print("[!] Uso: connect <host> <port>")
                elif user_input: # Se não for vazio
                    self.send_to_peers(user_input)
            except KeyboardInterrupt:
                print("\n[*] Saindo...")
                break
        
        self.socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python peer.py <porta>")
        sys.exit(1)

    port = int(sys.argv[1])
    host = '127.0.0.1' # localhost

    peer_node = Peer(host, port)
    peer_node.start()
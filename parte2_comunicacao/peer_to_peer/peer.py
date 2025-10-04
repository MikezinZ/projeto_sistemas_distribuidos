import socket
import threading
import sys

class Peer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peers = []
        self.lock = threading.Lock()

    def start_server(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        print(f"Peer escutando em {self.host}:{self.port}")

        while True:
            conn, addr = self.socket.accept()
            print(f"Nova conexão recebida de {addr}")
            self.add_peer(conn)
            
            thread = threading.Thread(target=self.handle_peer, args=(conn, addr))
            thread.start()

    def handle_peer(self, conn, addr):
        try:
            conn.sendall(f"Oi! Do nó: {self.port}!".encode('utf-8'))
        except socket.error:
            print(f" Erro ao enviar mensagem pra {addr}. A conexão fechou")
            self.remove_peer(conn)
            return

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break 
                
                mensagem_recebida = data.decode('utf-8')
                print(f"\n[Mensagem de {addr}]: {mensagem_recebida}\n> ", end="")

            except socket.error:
                break 

        print(f"Conexão com {addr} foi desligada.")
        self.remove_peer(conn)
        conn.close()

    def connect_to_peer(self, peer_host, peer_port):
        try:
            peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            peer_socket.connect((peer_host, int(peer_port)))
            
            self.add_peer(peer_socket)
            print(f"Conectado a {peer_host}:{peer_port}")

            initial_msg = peer_socket.recv(1024).decode('utf-8')
            print(f"\nResposta do Nó: {initial_msg}\n> ", end="")

            thread = threading.Thread(target=self.handle_peer, args=(peer_socket, (peer_host, peer_port)))
            thread.start()
            return True

        except socket.error as e:
            print(f"Falha ao conectar com {peer_host}:{peer_port}. Erro: {e}")
            return False

    def send_to_peers(self, message):
        full_message = f"Node {self.port}: {message}"

        with self.lock:
            for peer_conn in list(self.peers):
                try:
                    peer_conn.sendall(full_message.encode('utf-8'))
                except socket.error:
                    print(f"[!] Não foi possível enviar mensagem para um peer. Removendo...")
                    self.remove_peer(peer_conn, lock_needed=False) # O lock já foi adquirido

    def add_peer(self, peer_conn):
    
        with self.lock:
            if peer_conn not in self.peers:
                self.peers.append(peer_conn)
                print(f"Peers ativos: {len(self.peers)}")

    def remove_peer(self, peer_conn, lock_needed=True):
        if lock_needed:
            self.lock.acquire()
        
        if peer_conn in self.peers:
            self.peers.remove(peer_conn)
            print(f"Peers ativos: {len(self.peers)}")
        
        if lock_needed:
            self.lock.release()

    def start(self):
        """Inicia o peer: a thread do servidor e o loop de entrada do usuário."""   
        server_thread = threading.Thread(target=self.start_server)
        server_thread.daemon = True 
        server_thread.start()

        print("Bem-vindo ao chat do zap! Digite 'connect <host> <port>' para se conectar a outro contato.")
        
       
        while True:
            try:
                user_input = input("> ")
                if user_input.startswith("connect "):
                    parts = user_input.split()
                    if len(parts) == 3:
                        self.connect_to_peer(parts[1], parts[2])
                    else:
                        print("[!] Uso: connect <host> <port>")
                elif user_input: 
                    self.send_to_peers(user_input)
            except KeyboardInterrupt:
                print("\nSaindo...")
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
from utils.network.game_socket import ServerSocket

class Server:

    def __init__(self):
        # socket setup
        self.sock = ServerSocket()

        self.sock.bind_to_address('localhost', 9999)
        self.sock.set_socket_recv_buffer_size(1024)

        self.sock.on_new_client = self.on_new_client
        self.sock.on_client_leave = self.on_client_leave

        # game setup
        self.players = {}
        self.entities = {}
    
    def on_new_client(self, client_addr):
        print(f"a new client has joined with the address of {client_addr}")

    def on_client_leave(self, client_addr):
        print(f"a client with the address of {client_addr} has left")
    
    def main_loop(self):
        while True:
            data = self.sock.recv_packet_from()

            if data:
                packet, addr = data

                #print(f"got {packet} from {addr}")

            self.sock.send_packet_to_all_clients('data')

s = Server()
s.main_loop()

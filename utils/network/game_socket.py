import socket
import pickle
from select import select
from typing import Any
import time

from utils.network.packets import PingPacket
from utils.time.repeater import Repeater

_client_ping_rate = 1

class ClientConnectionState:

    def __init__(self):
        self.last_ping = time.time()

class GameSocket:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setblocking(False)

        self.recv_buf_size = 1024
    
    def set_socket_recv_buffer_size(self, size: int):
        self.recv_buf_size = size
    
    def recv_packet_from(self):
        ready_to_read, _, _ = select(
                    [self.sock],
                    [],
                    [],
                    0.0)
        if ready_to_read:
            data, addr = self.sock.recvfrom(self.buf_size)
            packet = pickle.loads(data)
            return (packet, addr)
    
    def recv_packet(self):
        ready_to_read, _, _ = select(
                    [self.sock],
                    [],
                    [],
                    0.0)
        if ready_to_read:
            data = self.sock.recv(self.buf_size)
            packet = pickle.loads(data)
            return packet

    def send_packet_to(self, packet, addr):
        self.sock.sendto(pickle.dumps(packet), addr)

class ServerSocket(GameSocket):

    def __init__(self):
        super().__init__()

        self.clients: dict[Any, ClientConnectionState] = {}

        self.on_new_client = None
        self.on_client_leave = None

        self.max_skiped_client_pings = 5

    def bind_to_address(self, address: str, port: int):
        self.sock.bind((address, port))

    def check_for_disconected_clients(self):
        removed_clients = []

        for client_addr, connection_state in self.clients.items():
            time_since_last_ping = time.time() - connection_state.last_ping

            if time_since_last_ping >= _client_ping_rate * self.max_skiped_client_pings:
                removed_clients.append(client_addr)

        for client_addr in removed_clients:
            del self.clients[client_addr]
            self.on_client_leave(client_addr)

    def recv_packet_from(self):
        ready_to_read, _, _ = select(
                    [self.sock],
                    [],
                    [],
                    0.0)
        if not ready_to_read:
            return
        
        data, addr = self.sock.recvfrom(self.recv_buf_size)
        packet = pickle.loads(data)

        if addr not in self.clients:
            self.clients[addr] = ClientConnectionState()

            if self.on_new_client:
                self.on_new_client(addr)
        
        if type(packet) == PingPacket:
            self.clients[addr].last_ping = time.time()
            return

        return (packet, addr)

    # NOTE: this function needs to be callen repeatetly in the server's event loop of the game
    def send_packet_to_all_clients(self, packet):
        self.check_for_disconected_clients()
        for client in self.clients:
            self.send_packet_to(packet, client)

class ClientSocket(GameSocket):
    
    def __init__(self):
        super().__init__()
        self.server_addr = None

        self.ping_packet = PingPacket()

        self.ping_repeater = Repeater()
        self.ping_repeater.set_repeat_interval_in_seconds(_client_ping_rate)
        self.ping_repeater.set_task(self.__ping_server)
    
    def connect_to_server(self, server_address: str, server_port: int):
        self.server_addr = (server_address, server_port)
    
    def __ping_server(self):
        self.send_packet(self.ping_packet)
    
    def ping_server(self):
        self.ping_repeater.non_blocking_repeat()

    def send_packet(self, packet):
        self.send_packet_to(packet, self.server_addr)

    def recv_packet(self):
        ready_to_read, _, _ = select(
                    [self.sock],
                    [],
                    [],
                    0.0)
        if not ready_to_read:
            return
        
        data = self.sock.recv(self.recv_buf_size)
        packet = pickle.loads(data)

        if type(packet) == PingPacket:
            self.send_packet(self.ping_packet)
            return

        return packet


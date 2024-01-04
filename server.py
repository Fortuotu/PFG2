import pygame

from utils.network.game_socket import ServerSocket
from utils.network.entity import *
from utils.network.packets import *
import prefabs

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

        self.entity_updates = EntitiesUpdatePacket([])

        self.clock = pygame.time.Clock()
        self.server_tick_rate = 30
    
    def on_new_client(self, client_addr):
        print(f"a new client has joined with the address of {client_addr}")

        self.players[client_addr] = create_server_entity('player')
        self.entities[self.players[client_addr].id] = self.players[client_addr]

    def on_client_leave(self, client_addr):
        print(f"a client with the address of {client_addr} has left")

        del self.entities[self.players[client_addr].id]
        del self.players[client_addr]
    
    def update_entities(self):
        self.entity_updates.entity_packets.clear()

        for entity_id, entity in self.entities.items():
            entity.update()
            
            self.entity_updates.entity_packets.append(
                EntityUpdatePacket(
                    entity.type,
                    entity_id,
                    entity.compile_network_attrs()))

    def handle_packet(self, packet, addr):
        packet_type = type(packet)
        player = self.players[addr]

        if packet_type == KeyInputPacket:
            player.handle_key_input(packet.key, packet.key_down, packet.key_up)

    def main_loop(self):
        while True:
            data = self.sock.recv_packet_from()

            if data:
                packet, addr = data
                self.handle_packet(packet, addr)

            self.update_entities()

            self.sock.send_packet_to_all_clients(self.entity_updates)
            self.clock.tick(self.server_tick_rate)

s = Server()
s.main_loop()

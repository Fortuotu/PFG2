import pygame

from utils.network.game_socket import ServerSocket
from utils.network.entity import *
from utils.network.packets import *
import prefabs

class ServerGlobalState:
    
    def __init__(self, socket):
        self.sock = socket

class Server:

    def __init__(self):
        # socket setup
        self.sock = ServerSocket()

        self.sock.bind_to_address('192.168.1.39', 9999)
        self.sock.set_socket_recv_buffer_size(1024)

        self.sock.on_new_client = self.on_new_client
        self.sock.on_client_leave = self.on_client_leave

        # game setup
        self.players = {}
        self.entities = entity_manager.get_all_entities()

        self.clock = pygame.time.Clock()
        self.server_tick_rate = 30

        self.global_state = ServerGlobalState(self.sock)

        set_entity_global_vars(self.global_state)
    
    def on_new_client(self, client_addr):
        print(f"a new client has joined with the address of {client_addr}")

        self.players[client_addr] = entity_manager.create_server_entity('player')

        
        #self.entities[self.players[client_addr].id] = self.players[client_addr]

    def on_client_leave(self, client_addr):
        print(f"a client with the address of {client_addr} has left")

        self.sock.queue_packet(RemoveEntityPacket('player', self.players[client_addr].id))

        del self.entities[self.players[client_addr].id]
        del self.players[client_addr]
    
    def update_entities(self):
        for _, entity in self.entities.items():
            entity.update()
    
    def send_entity_updates(self):
        for entity_id, entity in self.entities.items():
            self.sock.queue_packet(
                    EntityUpdatePacket(
                        entity.type,
                        entity_id,
                        entity.compile_network_attrs()))

    def handle_packet(self, packet, addr):
        packet_type = type(packet)
        player = self.players[addr]

        if packet_type == KeyInputPacket:
            player.handle_key_input(packet.key, packet.key_down, packet.key_up)
        elif packet_type == ShootBulletPacket:
            player.shoot_bullet(packet.mouse_pos)

    def main_loop(self):
        while True:
            data = self.sock.recv_packet_from()

            if data:
                packet, addr = data
                self.handle_packet(packet, addr)

            entity_manager.update_entities()
            entity_manager.flush_removed_entities()
            self.send_entity_updates()
            self.sock.send_queued_packets()
            self.sock.check_for_disconected_clients()

            self.clock.tick(self.server_tick_rate)

s = Server()
s.main_loop()

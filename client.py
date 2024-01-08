import pygame, sys

from utils.network.game_socket import ClientSocket
from utils.network.entity import *
from utils.network.packets import *

from utils.video import Background

import prefabs

class Game:
    
    def __init__(self):
        self.sock = ClientSocket()
        self.sock.set_socket_recv_buffer_size(1024)

        self.screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 60

        self.entities = {}

        #self.background = Background()

    def handle_packet(self, packet):
        packet_type = type(packet)

        if packet_type == EntityUpdatePacket:
            # add entity if doesn't exist on client side
            if packet.entity_id not in self.entities:
                self.entities[packet.entity_id] = create_client_entity(
                    packet.entity_type,
                    packet.entity_id,
                    packet.entity_attrs)
                
            # update client-side entity
            else:
                self.entities[packet.entity_id].set_attrs(packet.entity_attrs)

    def run(self):
        self.sock.connect_to_server('localhost', 9999)
        self.sock.send_packet('CONNECT')
        
        while self.running:
            while True:
                packet = self.sock.recv_packet()
                if packet:
                    self.handle_packet(packet)
                else:
                    break

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                    self.sock.send_packet(
                        KeyInputPacket(event.key,
                                       event.type == pygame.KEYDOWN,
                                       event.type == pygame.KEYUP))
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.sock.send_packet(
                        ShootBulletPacket(pygame.Vector2(pygame.mouse.get_pos())))
                elif event.type == pygame.VIDEORESIZE:
                    pass
            
            #self.background.update(self.screen)

            for _, entity in self.entities.items():
                entity.update(self.screen)

            pygame.display.update()
            self.clock.tick(self.fps)
            self.screen.fill((255, 255, 240))

            self.sock.ping_server()
        pygame.quit()
        sys.exit()

Game().run()

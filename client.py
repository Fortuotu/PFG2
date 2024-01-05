import pygame, sys

from utils.network.game_socket import ClientSocket
from utils.network.entity import *
from utils.network.packets import *
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

        self.background = pygame.image.load('assets/background.png').convert_alpha()
        self.background = pygame.transform.scale(self.background, (128 * 8, 128 * 8))
        self.background.set_alpha(255 * 0.1)

        self.background_rect = self.background.get_rect()
        self.background_rect.center = (0, 0)

        self.x, self.y = self.background_rect.topleft

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
            
            self.screen.blit(self.background, self.background_rect)

            self.x += 0.2
            self.y += 0.2

            self.background_rect.topleft = (self.x, self.y)

            if self.background_rect.x >= 0:
                self.background_rect.center = (0, 0)
                self.x, self.y = self.background_rect.topleft

            for _, entity in self.entities.items():
                entity.update(self.screen)

            pygame.display.update()
            self.clock.tick(self.fps)
            self.screen.fill((255, 255, 255))

            self.sock.ping_server()
        pygame.quit()
        sys.exit()

Game().run()

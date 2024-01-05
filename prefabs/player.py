import pygame

from utils.network.entity import *
from utils.network.entity import EntityNetworkAttrs

class ServerPlayer(ServerEntity):

    def __init__(self):
        super().__init__()
        self.type = 'player'

        self.pos = [0, 0]
        self.rect = pygame.Rect(0, 0, 50, 50)

        self.velocity = pygame.Vector2(0, 0)
        self.normalized_vel = self.velocity

        self.speed = 5

    def compile_network_attrs(self):
        self.rect.topleft = self.pos
        self.network_attrs.rect = self.rect
        return self.network_attrs

    def handle_key_input(self, key: int, key_down: bool, key_up: bool):
        if key_down:
            if key == pygame.K_w:
                self.velocity.y += -1
            if key == pygame.K_s:
                self.velocity.y += 1
            if key == pygame.K_a:
                self.velocity.x += -1
            if key == pygame.K_d:
                self.velocity.x += 1
            
            if key == pygame.K_e:
                create_server_entity('wall', self.rect.topleft)

        elif key_up:
            if key == pygame.K_w:
                self.velocity.y += 1
            if key == pygame.K_s:
                self.velocity.y += -1
            if key == pygame.K_a:
                self.velocity.x += 1
            if key == pygame.K_d:
                self.velocity.x += -1
        
        if self.velocity == [0, 0]:
            self.normalized_vel = self.velocity
            return
        
        self.normalized_vel = self.velocity.normalize()

    def update(self):
        self.pos[0] += self.normalized_vel.x * self.speed
        self.pos[1] += self.normalized_vel.y * self.speed

class ClientPlayer(ClientEntity):

    def __init__(self, attrs: EntityNetworkAttrs) -> None:
        super().__init__(attrs)
        self.type = 'player'
        self.img = pygame.image.load('assets/red-player.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (15 * 4, 15 * 4))
    
    def update(self, screen: pygame.Surface):
        screen.blit(self.img, self.attrs.rect)

        #pygame.draw.rect(screen, (255, 0, 0), self.attrs.rect)

add_entity_type('player', (ServerPlayer, ClientPlayer))

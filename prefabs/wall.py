import pygame

from utils.network.entity import *

wall_size = (15 * 4, 15 * 4)

class ServerWall(ServerEntity):

    def __init__(self, pos):
        super().__init__()
        self.type = 'wall'
        self.rect = pygame.Rect(pos[0], pos[1], wall_size[0], wall_size[1])

    def compile_network_attrs(self):
        self.network_attrs.rect = self.rect
        return self.network_attrs

    def update(self):
        pass

class ClientWall(ClientEntity):

    def __init__(self, attrs: EntityNetworkAttrs):
        super().__init__(attrs)
        self.type = 'wall'
        self.img = pygame.image.load('assets/wall.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, wall_size).convert_alpha()

    def update(self, screen: pygame.Surface):
        screen.blit(self.img, self.attrs.rect)

add_entity_type('wall', (ServerWall, ClientWall))

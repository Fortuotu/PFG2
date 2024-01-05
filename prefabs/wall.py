import pygame

from utils.network.entity import *

class ServerWall(ServerEntity):

    def __init__(self, pos):
        super().__init__()
        self.type = 'wall'

        self.rect = pygame.Rect(pos[0], pos[1], 50, 50)
    
    def compile_network_attrs(self):
        self.network_attrs.rect = self.rect
        return self.network_attrs

    def update(self):
        pass

class ClientWall(ClientEntity):

    def __init__(self, attrs: EntityNetworkAttrs):
        super().__init__(attrs)
        self.type = 'wall'

    def update(self, screen: pygame.Surface):
        pygame.draw.rect(screen, (150, 150, 150), self.attrs.rect)

add_entity_type('wall', (ServerWall, ClientWall))

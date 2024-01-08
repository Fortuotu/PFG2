import math

from pygame import Surface
from utils.network.entity import *
from utils.network.entity import EntityNetworkAttrs

class ServerBullet(ServerEntity):

    def __init__(self, start_pos: pygame.Vector2, mouse_pos: pygame.Vector2):
        super().__init__()
        self.type = 'bullet'

        self.pos = pygame.Vector2(start_pos)
        self.rect = pygame.Rect(0, 0, 3 * 4, 3 * 4)
        self.rect.center = self.pos
        self.distance = math.sqrt((abs(start_pos.x - mouse_pos.x) ** 2) + (abs(start_pos.y - mouse_pos.y) ** 2))
        self.direction = pygame.Vector2((mouse_pos.x - start_pos.x) / self.distance, (mouse_pos.y - start_pos.y) / self.distance)
        self.speed = 5

    def compile_network_attrs(self):
        self.network_attrs.rect = self.rect
        return self.network_attrs

    def update(self):
        self.pos += self.direction * self.speed
        self.rect.center = self.pos

class ClientBullet(ClientEntity):

    def __init__(self, attrs: EntityNetworkAttrs) -> None:
        super().__init__(attrs)
        self.type = 'bullet'
        self.img = pygame.image.load('assets/bullet.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, (3 * 4, 3 * 4))

    def update(self, screen: Surface):
        screen.blit(self.img, self.attrs.rect)

add_entity_type('bullet', (ServerBullet, ClientBullet))

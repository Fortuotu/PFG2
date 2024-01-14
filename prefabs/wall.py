import pygame
from utils.network.packets import *

from utils.network.entity import *

wall_size = (15 * 4, 15 * 4)

class ServerWall(ServerEntity):

    def __init__(self, pos):
        super().__init__()
        self.type = 'wall'
        self.rect = pygame.Rect(pos[0], pos[1], wall_size[0], wall_size[1])
        self.damage_state = 0

        self.bullets: dict = entity_manager.get_entities_by_type('bullet')

    def compile_network_attrs(self):
        self.network_attrs.rect = self.rect
        self.network_attrs.damage_state = self.damage_state
        return self.network_attrs

    def check_collsion_with_bullets(self):
        for bullet_id, bullet in self.bullets.items():
            if self.rect.colliderect(bullet.rect):
                self.global_vars.sock.queue_packet(
                    RemoveEntityPacket('bullet', bullet_id))
                entity_manager.add_entity_to_removed_entities(bullet_id)

    def update(self):
        self.check_collsion_with_bullets()

class ClientWall(ClientEntity):

    def __init__(self, attrs: EntityNetworkAttrs):
        super().__init__(attrs)
        self.type = 'wall'
        self.img = pygame.image.load('assets/wall.png').convert_alpha()
        self.img = pygame.transform.scale(self.img, wall_size).convert_alpha()

    def update(self, screen: pygame.Surface):
        screen.blit(self.img, self.attrs.rect)

entity_manager.add_entity_type('wall', (ServerWall, ClientWall))

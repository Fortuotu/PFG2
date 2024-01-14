import pygame
import random
from utils.network.entity import *
from utils.network.entity import EntityNetworkAttrs

from prefabs.wall import wall_size

class ServerPlayer(ServerEntity):

    def __init__(self):
        super().__init__()
        self.type = 'player'

        self.pos = pygame.Vector2(0, 0)
        self.rect = pygame.Rect(0, 0, 15 * 4, 15 * 4)

        self.last_key = pygame.K_w
        self.color = random.choice(('red', 'blue', 'green'))
        self.velocity = pygame.Vector2(0, 0)
        self.normalized_vel = self.velocity

        self.speed = 5

        self.walls = entity_manager.get_entities_by_type('wall')

    def compile_network_attrs(self):
        self.network_attrs.pos = self.pos
        self.network_attrs.rect = self.rect
        self.network_attrs.color = self.color
        return self.network_attrs

    def shoot_bullet(self, mouse_pos: pygame.Vector2):
        entity_manager.create_server_entity('bullet', pygame.Vector2(self.rect.center), mouse_pos)

    def check_collsion(self):
        self.pos.x += self.normalized_vel.x * self.speed
        self.rect.topleft = self.pos

        for wall_id, wall in self.walls.items():
            if self.rect.colliderect(wall.rect):
                if self.velocity.x == 1:
                    self.pos.x = wall.rect.left - self.rect.w
                elif self.velocity.x == -1:
                    self.pos.x = wall.rect.right
                
                self.rect.topleft = self.pos

        self.pos.y += self.normalized_vel.y * self.speed
        self.rect.topleft = self.pos

        for wall_id, wall in self.walls.items():
            if self.rect.colliderect(wall):
                if self.velocity.y == 1:
                    self.pos.y = wall.rect.top - self.rect.h
                elif self.velocity.y == -1:
                    self.pos.y = wall.rect.bottom
                
                self.rect.topleft = self.pos
        
        self.rect.topleft = self.pos

    def create_wall(self):
        if self.last_key == pygame.K_w:
            creation_pos = (self.rect.x, self.rect.y + wall_size[1])
        elif self.last_key == pygame.K_s:
            creation_pos = (self.rect.x, self.rect.y - wall_size[1])
        elif self.last_key == pygame.K_d:
            creation_pos = (self.rect.x - wall_size[0], self.rect.y)
        elif self.last_key == pygame.K_a:
            creation_pos = (self.rect.x + wall_size[0], self.rect.y)
        
        wall_rect = pygame.Rect(creation_pos[0], creation_pos[1], wall_size[0], wall_size[1])

        for wall_id, wall in self.walls.items():
            if wall.rect.colliderect(wall_rect):
                return

        entity_manager.create_server_entity('wall', creation_pos)

    def handle_key_input(self, key: int, key_down: bool, key_up: bool):
        if key_down:
            if key == pygame.K_e:
                self.create_wall()
                return

            if key == pygame.K_w:
                self.velocity.y += -1
            if key == pygame.K_s:
                self.velocity.y += 1
            if key == pygame.K_a:
                self.velocity.x += -1
            if key == pygame.K_d:
                self.velocity.x += 1
            self.last_key = key
        
        if key_up:
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
        self.check_collsion()

class ClientPlayer(ClientEntity):

    def __init__(self, attrs: EntityNetworkAttrs) -> None:
        super().__init__(attrs)
        self.type = 'player'
        self.color = f'assets/{self.attrs.color}-player.png'
        self.img = pygame.image.load(self.color).convert_alpha()
        self.img = pygame.transform.scale(self.img, (attrs.rect.w, attrs.rect.h))
    
    def update(self, screen: pygame.Surface):
        screen.blit(self.img, self.attrs.pos)

        #pygame.draw.rect(screen, (255, 0, 0), (self.attrs.pos[0], self.attrs.pos[1], 15 * 4, 15 * 4))

entity_manager.add_entity_type('player', (ServerPlayer, ClientPlayer))

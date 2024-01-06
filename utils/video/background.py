import pygame

class Background:

    def __init__(self):
        self.orig_img = pygame.image.load('assets/background.png').convert_alpha()

        self.screen_w = 500
        self.screen_h = 500

        self.main_img = pygame.transform.scale(self.orig_img, (self.screen_w * 2, self.screen_h * 2))
        self.main_img.set_alpha(255 * 0.1)

        self.rect = self.main_img.get_rect()
        self.rect.center = (0, 0)

        self.move_speed = 2

        self.dx, self.dy = 1, 1
        self.x, self.y = self.rect.topleft

    def rescale(self, screen_w: int, screen_h: int):
        self.dx = screen_w / self.screen_w
        self.dy = screen_h / self.screen_h

        self.main_img = self.main_img = pygame.transform.scale(self.orig_img, (screen_w * 2, screen_h * 2))
        self.main_img.set_alpha(255 * 0.1)

    def update(self, screen: pygame.Surface):
        screen.blit(self.main_img, self.rect)

        self.x += self.dx * self.move_speed
        self.y += self.dy * self.move_speed

        if self.x >= 0:
            self.rect.center = (0, 0)
            self.x, self.y = self.rect.topleft
            return

        self.rect.topleft = (self.x, self.y)
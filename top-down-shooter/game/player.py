import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.radius = 15
        self.ammo = 30
        self.reload_timer = 0
        self.shoot_delay = 0
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]: self.y -= self.speed
        if keys[pygame.K_s]: self.y += self.speed
        if keys[pygame.K_a]: self.x -= self.speed
        if keys[pygame.K_d]: self.x += self.speed

        # Boundaries
        self.x = max(self.radius, min(800 - self.radius, self.x))
        self.y = max(self.radius, min(600 - self.radius, self.y))
        self.rect.center = (self.x, self.y)

        if self.shoot_delay > 0:
            self.shoot_delay -= 1

        if self.reload_timer > 0:
            self.reload_timer -= 1
        elif self.ammo == 0:
            self.reload_timer = 60
            self.ammo = 30

    def can_shoot(self):
        return self.ammo > 0 and self.shoot_delay == 0

    def shoot(self, target_pos):
        self.ammo -= 1
        self.shoot_delay = 10
        from bullet import Bullet
        return Bullet(self.x, self.y, target_pos[0], target_pos[1])

    def draw(self, screen):
        pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), self.radius)
        # Draw aiming line
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (mouse_x, mouse_y), 2)
import pygame
import random
import math

class Enemy:
    def __init__(self, width, height):
        # Spawn at screen edges
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.x = random.randint(0, width)
            self.y = -20
        elif side == 'bottom':
            self.x = random.randint(0, width)
            self.y = height + 20
        elif side == 'left':
            self.x = -20
            self.y = random.randint(0, height)
        else:
            self.x = width + 20
            self.y = random.randint(0, height)

        self.speed = 2
        self.radius = 12
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def update(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0), (int(self.x), int(self.y)), self.radius)
import pygame
import random
import math

class Enemy:
    def __init__(self, width, height, player_speed_bonus=0):
        # Spawn at screen edges
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            self.x = random.randint(0, width)
            self.y = -30
        elif side == 'bottom':
            self.x = random.randint(0, width)
            self.y = height + 30
        elif side == 'left':
            self.x = -30
            self.y = random.randint(0, height)
        else:
            self.x = width + 30
            self.y = random.randint(0, height)
        
        # Enemy type variations
        self.type = random.choice(['normal', 'fast', 'tank'])
        if self.type == 'fast':
            self.speed = 3.5 + player_speed_bonus * 0.5
            self.radius = 10
            self.health = 1
            self.color = (255, 200, 0)
        elif self.type == 'tank':
            self.speed = 1.2 + player_speed_bonus * 0.2
            self.radius = 20
            self.health = 3
            self.color = (100, 100, 200)
        else:  # normal
            self.speed = 2 + player_speed_bonus * 0.3
            self.radius = 14
            self.health = 1
            self.color = (255, 0, 0)
        
        self.max_health = self.health
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

    def take_damage(self, damage=1):
        self.health -= damage
        return self.health <= 0

    def update(self, player_x, player_y):
        dx = player_x - self.x
        dy = player_y - self.y
        dist = math.hypot(dx, dy)
        if dist != 0:
            self.x += dx / dist * self.speed
            self.y += dy / dist * self.speed
        self.rect.center = (self.x, self.y)

    def draw(self, screen):
        # Draw health bar for tanks
        if self.type == 'tank' and self.health < self.max_health:
            bar_width = self.radius * 2
            bar_height = 4
            health_percent = self.health / self.max_health
            pygame.draw.rect(screen, (255, 0, 0), (self.x - bar_width//2, self.y - self.radius - 5, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x - bar_width//2, self.y - self.radius - 5, bar_width * health_percent, bar_height))
        
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Eyes for personality
        eye_size = self.radius // 3
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x - self.radius//2), int(self.y - self.radius//2)), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x + self.radius//2), int(self.y - self.radius//2)), eye_size)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x - self.radius//2), int(self.y - self.radius//2)), eye_size//2)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + self.radius//2), int(self.y - self.radius//2)), eye_size//2)
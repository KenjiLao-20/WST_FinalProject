import pygame
import math

class Bullet:
    def __init__(self, x, y, target_x, target_y, angle_offset=0, pierce=0, damage_bonus=0):
        self.x = x
        self.y = y
        self.speed = 14
        # Damage calculation: 1 base damage + bonus (0.5 = +50% = 1.5 damage rounded up to 2)
        self.damage = max(1, int(1 + damage_bonus))
        self.pierce_left = pierce
        
        # Calculate direction with optional spread
        dx = target_x - x
        dy = target_y - y
        base_angle = math.atan2(dy, dx)
        final_angle = base_angle + angle_offset
        
        self.vx = math.cos(final_angle) * self.speed
        self.vy = math.sin(final_angle) * self.speed
        
        self.radius = 5
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.rect.center = (self.x, self.y)

    def off_screen(self, width, height):
        return self.x < -50 or self.x > width + 50 or self.y < -50 or self.y > height + 50

    def draw(self, screen):
        # Glow effect based on damage
        if self.damage > 2:
            pygame.draw.circle(screen, (255, 100, 100), (int(self.x), int(self.y)), self.radius + 2)
        pygame.draw.circle(screen, (255, 255, 100), (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, (255, 200, 0), (int(self.x), int(self.y)), self.radius - 2)
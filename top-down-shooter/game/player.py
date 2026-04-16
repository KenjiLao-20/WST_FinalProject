import pygame
import math
import random

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.base_speed = 5
        self.speed_bonus = 0
        self.speed = self.base_speed
        self.radius = 15
        
        # Health system
        self.max_health = 100
        self.health = 100
        self.invincible_frames = 0
        
        # Shooting stats
        self.ammo = 30
        self.max_ammo = 30
        self.fire_delay = 10
        self.fire_timer = 0
        self.bullet_count = 1
        self.pierce = 0
        self.damage_bonus = 0
        
        # Special abilities
        self.exploding_kills = False
        self.damage_reduction = 0
        self.lifesteal = 0
        self.invincible_on_hit = False
        self.score_multiplier = 1.0
        
        self.active_powerups = []
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

        # Timers
        if self.fire_timer > 0:
            self.fire_timer -= 1
        
        if self.invincible_frames > 0:
            self.invincible_frames -= 1

    def take_damage(self):
        if self.invincible_frames > 0:
            return False
        
        damage = 20 * (1 - self.damage_reduction)
        self.health -= damage
        
        if self.invincible_on_hit:
            self.invincible_frames = 30
        
        return self.health <= 0

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def can_shoot(self):
        return self.ammo > 0 and self.fire_timer == 0

    def shoot(self, target_pos):
        self.ammo -= 1
        self.fire_timer = self.fire_delay
        
        from bullet import Bullet
        bullets = []
        
        # Multi-shot spread
        angles = [-0.2, 0, 0.2] if self.bullet_count >= 3 else [-0.1, 0.1] if self.bullet_count == 2 else [0]
        
        for i in range(self.bullet_count):
            angle_offset = angles[i % len(angles)] if len(angles) > 1 else 0
            bullets.append(Bullet(self.x, self.y, target_pos[0], target_pos[1], 
                                  angle_offset, self.pierce, self.damage_bonus))
        
        return bullets

    def draw(self, screen):
        # Flash when invincible
        if self.invincible_frames > 0 and (pygame.time.get_ticks() % 100) < 50:
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.radius)
        else:
            pygame.draw.circle(screen, (0, 255, 0), (int(self.x), int(self.y)), self.radius)
        
        # Health bar
        bar_width = 40
        bar_height = 6
        health_percent = self.health / self.max_health
        pygame.draw.rect(screen, (255, 0, 0), (self.x - bar_width//2, self.y - self.radius - 10, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (self.x - bar_width//2, self.y - self.radius - 10, bar_width * health_percent, bar_height))
        
        # Draw aiming line
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), (self.x, self.y), (mouse_x, mouse_y), 2)
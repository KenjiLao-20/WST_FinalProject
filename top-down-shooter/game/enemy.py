import pygame
import random
import math

class Enemy:
    # Class variables for global difficulty scaling
    global_difficulty_minute = 0
    global_hp_multiplier = 1.0
    global_speed_multiplier = 1.0
    
    @classmethod
    def update_difficulty(cls, minutes_passed):
        """Update global difficulty based on minutes elapsed"""
        cls.global_difficulty_minute = minutes_passed
        # HP increases by 50% per minute (capped at +250%)
        cls.global_hp_multiplier = 1 + (minutes_passed * 0.5)
        # Speed increases by 15% per minute (capped at +75%)
        cls.global_speed_multiplier = 1 + (minutes_passed * 0.15)
    
    def __init__(self, width, height, player_speed_bonus=0, difficulty_minute=0):
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
        enemy_roll = random.random()
        
        # Base stats (before difficulty scaling)
        if enemy_roll < 0.3:  # 30% chance for fast (yellow)
            self.type = 'fast'
            self.base_speed = 3.5
            self.base_health = 1
            self.radius = 10
            self.color = (255, 200, 0)
            self.score_value = 15
        elif enemy_roll < 0.6:  # 30% chance for tank (blue)
            self.type = 'tank'
            self.base_speed = 1.2
            self.base_health = 3
            self.radius = 20
            self.color = (0, 100, 255)
            self.score_value = 25
        else:  # 40% chance for normal (red)
            self.type = 'normal'
            self.base_speed = 2.0
            self.base_health = 2
            self.radius = 14
            self.color = (255, 0, 0)
            self.score_value = 10
        
        # Apply difficulty scaling
        self.speed = self.base_speed + (self.base_speed * Enemy.global_speed_multiplier * 0.3)
        self.speed += player_speed_bonus * 0.3
        
        # Scale health based on difficulty
        scaled_health = int(self.base_health * Enemy.global_hp_multiplier)
        self.max_health = max(self.base_health, min(scaled_health, self.base_health * 3))  # Cap at 3x base
        self.health = self.max_health
        
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
        # Draw health bar
        if self.health < self.max_health:
            bar_width = self.radius * 2
            bar_height = 4
            health_percent = self.health / self.max_health
            pygame.draw.rect(screen, (255, 0, 0), (self.x - bar_width//2, self.y - self.radius - 5, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x - bar_width//2, self.y - self.radius - 5, bar_width * health_percent, bar_height))
        
        # Draw enemy with pulsing effect if high health
        if self.max_health > self.base_health * 2:
            # Pulsing effect for buffed enemies
            pulse = (pygame.time.get_ticks() % 500) / 500
            color_variant = tuple(min(255, int(c * (0.8 + pulse * 0.4))) for c in self.color)
            pygame.draw.circle(screen, color_variant, (int(self.x), int(self.y)), self.radius)
        else:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Eyes
        eye_size = max(2, self.radius // 4)
        eye_offset = self.radius // 3
        
        # White of eyes
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x - eye_offset), int(self.y - eye_offset)), eye_size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x + eye_offset), int(self.y - eye_offset)), eye_size)
        
        # Pupils (follow player direction - simplified)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x - eye_offset + 2), int(self.y - eye_offset + 1)), eye_size//2)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + eye_offset + 2), int(self.y - eye_offset + 1)), eye_size//2)
        
        # Angry eyebrows for tank
        if self.type == 'tank':
            pygame.draw.line(screen, (0, 0, 0), (self.x - eye_offset - 3, self.y - eye_offset - 2), 
                           (self.x - eye_offset + 3, self.y - eye_offset + 1), 2)
            pygame.draw.line(screen, (0, 0, 0), (self.x + eye_offset + 3, self.y - eye_offset - 2), 
                           (self.x + eye_offset - 3, self.y - eye_offset + 1), 2)
        
        # Show health number on tank enemies
        if self.type == 'tank' and self.max_health > 3:
            font = pygame.font.Font(None, 12)
            health_text = font.render(str(self.health), True, (255, 255, 255))
            screen.blit(health_text, (self.x - 5, self.y - self.radius - 10))
import pygame
import random
import math

class Enemy:
    # Class variables for global difficulty scaling
    global_difficulty_minute = 0
    global_hp_multiplier = 1.0
    global_speed_multiplier = 1.0
    
    # Class variables for images
    red_image = None
    yellow_image = None
    blue_image = None
    
    @classmethod
    def load_images(cls):
        """Load enemy images once at game start"""
        try:
            cls.red_image = pygame.image.load("assets/red.png").convert_alpha()
            cls.red_image = pygame.transform.scale(cls.red_image, (32, 32))
        except:
            print("Warning: Could not load assets/red.png")
            cls.red_image = None
            
        try:
            cls.yellow_image = pygame.image.load("assets/yellow.png").convert_alpha()
            cls.yellow_image = pygame.transform.scale(cls.yellow_image, (24, 24))
        except:
            print("Warning: Could not load assets/yellow.png")
            cls.yellow_image = None
            
        try:
            cls.blue_image = pygame.image.load("assets/blue.png").convert_alpha()
            cls.blue_image = pygame.transform.scale(cls.blue_image, (40, 40))
        except:
            print("Warning: Could not load assets/blue.png")
            cls.blue_image = None
    
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
            self.radius = 12  # Half of 24
            self.color = (255, 200, 0)
            self.score_value = 15
            self.image = Enemy.yellow_image
        elif enemy_roll < 0.6:  # 30% chance for tank (blue)
            self.type = 'tank'
            self.base_speed = 1.2
            self.base_health = 3
            self.radius = 20  # Half of 40
            self.color = (0, 100, 255)
            self.score_value = 25
            self.image = Enemy.blue_image
        else:  # 40% chance for normal (red)
            self.type = 'normal'
            self.base_speed = 2.0
            self.base_health = 2
            self.radius = 16  # Half of 32
            self.color = (255, 0, 0)
            self.score_value = 10
            self.image = Enemy.red_image
        
        # Apply difficulty scaling
        self.speed = self.base_speed + (self.base_speed * Enemy.global_speed_multiplier * 0.3)
        self.speed += player_speed_bonus * 0.3
        
        # Scale health based on difficulty
        scaled_health = int(self.base_health * Enemy.global_hp_multiplier)
        self.max_health = max(self.base_health, min(scaled_health, self.base_health * 3))
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
        # Draw health bar if damaged
        if self.health < self.max_health:
            bar_width = self.radius * 2
            bar_height = 4
            health_percent = self.health / self.max_health
            pygame.draw.rect(screen, (255, 0, 0), (self.x - bar_width//2, self.y - self.radius - 5, bar_width, bar_height))
            pygame.draw.rect(screen, (0, 255, 0), (self.x - bar_width//2, self.y - self.radius - 5, bar_width * health_percent, bar_height))
        
        # Draw enemy image or fallback circle
        if self.image:
            screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        else:
            # Fallback to colored circle if image not found
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        
        # Show health number on tank enemies
        if self.type == 'tank' and self.max_health > 3:
            font = pygame.font.Font(None, 12)
            health_text = font.render(str(int(self.health)), True, (255, 255, 255))
            screen.blit(health_text, (self.x - 5, self.y - self.radius - 12))
import pygame

class Boss:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 80
        self.health = 20
        self.speed_x = 2
        self.rect = pygame.Rect(x, y, self.width, self.height)

    def update(self):
        self.x += self.speed_x
        if self.x <= 0 or self.x >= 720:
            self.speed_x *= -1
        self.rect.topleft = (self.x, self.y)

    def take_damage(self):
        self.health -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, (150, 0, 150), self.rect)
        font = pygame.font.Font(None, 24)
        health_text = font.render(f"BOSS HP: {self.health}", True, (255, 255, 255))
        screen.blit(health_text, (self.x, self.y - 20))
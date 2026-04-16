import pygame
import sys
from player import Player
from enemy import Enemy
from bullet import Bullet
from boss import Boss

# Initialize
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Top-Down Shooter")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

def draw_text(text, font, color, x, y):
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def menu():
    while True:
        screen.fill(BLACK)
        draw_text("TOP-DOWN SHOOTER", big_font, WHITE, SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 - 100)
        draw_text("Press SPACE to Start", font, GREEN, SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2)
        draw_text("WASD to Move | Mouse to Aim & Shoot", font, WHITE, SCREEN_WIDTH//2 - 200, SCREEN_HEIGHT//2 + 50)
        draw_text("Kill 15 enemies → Boss appears | Defeat Boss to Win", font, WHITE, SCREEN_WIDTH//2 - 250, SCREEN_HEIGHT//2 + 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def game_loop():
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    enemies = []
    bullets = []
    boss = None
    score = 0
    kills = 0
    running = True
    boss_defeated = False
    boss_spawned = False

    while running:
        screen.fill(BLACK)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and player.can_shoot():
                    bullets.append(player.shoot(pygame.mouse.get_pos()))

        # Update
        player.update()
        for bullet in bullets[:]:
            bullet.update()
            if bullet.off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                bullets.remove(bullet)

        for enemy in enemies[:]:
            enemy.update(player.x, player.y)
            if enemy.rect.colliderect(player.rect):
                running = False  # Game over
            for bullet in bullets[:]:
                if bullet.rect.colliderect(enemy.rect):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10
                    kills += 1
                    break

        # Boss logic
        if not boss_spawned and kills >= 15:
            boss = Boss(SCREEN_WIDTH//2 - 50, 50)
            boss_spawned = True

        if boss and not boss_defeated:
            boss.update()
            if boss.rect.colliderect(player.rect):
                running = False
            for bullet in bullets[:]:
                if bullet.rect.colliderect(boss.rect):
                    bullets.remove(bullet)
                    boss.take_damage()
                    score += 20
                    if boss.health <= 0:
                        boss_defeated = True
                        boss = None
                        score += 500
                    break

        # Spawn enemies
        if not boss_spawned and len(enemies) < 8 and pygame.time.get_ticks() % 30 == 0:
            enemies.append(Enemy(SCREEN_WIDTH, SCREEN_HEIGHT))

        # Draw
        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        if boss and not boss_defeated:
            boss.draw(screen)

        # UI
        draw_text(f"Score: {score}", font, WHITE, 10, 10)
        draw_text(f"Kills: {kills}/15", font, WHITE, 10, 50)
        draw_text(f"Ammo: {player.ammo}", font, WHITE, 10, 90)

        if boss_defeated:
            draw_text("VICTORY!", big_font, GREEN, SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2)
            draw_text("Click to continue", font, WHITE, SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 60)
            pygame.display.flip()
            pygame.time.wait(500)
            return score

        pygame.display.flip()
        clock.tick(60)

    return score  # Game over

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", big_font, RED, SCREEN_WIDTH//2 - 120, SCREEN_HEIGHT//2 - 100)
        draw_text(f"Final Score: {score}", font, WHITE, SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2)
        draw_text("Press R to Restart or Q to Quit", font, WHITE, SCREEN_WIDTH//2 - 180, SCREEN_HEIGHT//2 + 60)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

def main():
    while True:
        menu()
        score = game_loop()
        if not game_over_screen(score):
            break

if __name__ == "__main__":
    main()
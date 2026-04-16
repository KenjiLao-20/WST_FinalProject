import pygame
import sys
import random
import math
from player import Player
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp, PowerUpChoice

# Initialize
pygame.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("5 Minutes Till Dawn - Top Down Shooter")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 24)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)

def draw_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    if center:
        x = x - surface.get_width() // 2
    screen.blit(surface, (x, y))

def menu():
    while True:
        screen.fill(BLACK)
        
        draw_text("5 MINUTES TILL DAWN", big_font, YELLOW, SCREEN_WIDTH//2, 150, center=True)
        draw_text("Survive 5 Minutes Against Endless Hordes", font, WHITE, SCREEN_WIDTH//2, 250, center=True)
        draw_text("Every 15 kills = Level Up! Choose a Power-Up", small_font, YELLOW, SCREEN_WIDTH//2, 300, center=True)
        draw_text("Press SPACE to Start", font, GREEN, SCREEN_WIDTH//2, 400, center=True)
        draw_text("WASD to Move | Mouse to Aim & Shoot", font, WHITE, SCREEN_WIDTH//2, 450, center=True)
        draw_text("Unlimited Ammo!", small_font, BLUE, SCREEN_WIDTH//2, 500, center=True)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def show_level_up_screen(choices):
    """Display power-up selection screen"""
    selected = 0
    waiting = True
    
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(choices)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(choices)
                elif event.key == pygame.K_SPACE:
                    return selected
        
        # Draw the screen
        screen.fill(BLACK)
        
        # Title
        draw_text("LEVEL UP!", big_font, YELLOW, SCREEN_WIDTH//2, 100, center=True)
        draw_text("Choose your power-up:", font, WHITE, SCREEN_WIDTH//2, 180, center=True)
        
        # Display choices
        for i, choice in enumerate(choices):
            y_pos = 280 + i * 100
            color = GREEN if selected == i else WHITE
            box_rect = pygame.Rect(150, y_pos - 30, 500, 70)
            pygame.draw.rect(screen, (50, 50, 80), box_rect, border_radius=10)
            pygame.draw.rect(screen, color, box_rect, 2, border_radius=10)
            
            draw_text(choice.name, font, color, SCREEN_WIDTH//2, y_pos, center=True)
            draw_text(choice.description, small_font, YELLOW, SCREEN_WIDTH//2, y_pos + 30, center=True)
        
        draw_text("↑ ↓ to select | SPACE to confirm", small_font, WHITE, SCREEN_WIDTH//2, 550, center=True)
        
        pygame.display.flip()
        clock.tick(30)  # Limit FPS while in menu

def game_loop():
    # Game variables
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    enemies = []
    bullets = []
    particles = []
    
    # Survival timers
    start_time = pygame.time.get_ticks()
    survival_duration = 5 * 60 * 1000  # 5 minutes in milliseconds
    
    # Level system
    kills = 0
    exp_needed = 15
    level = 1
    
    running = True
    paused_for_level_up = False
    
    # Score
    score = 0
    
    # Spawn timer
    spawn_counter = 0
    
    while running:
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - start_time
        time_left = max(0, survival_duration - time_elapsed)
        minutes_left = time_left // 60000
        seconds_left = (time_left % 60000) // 1000
        
        # Check win condition
        if time_left <= 0:
            return "win", score, kills, level
        
        # Level up check (only if not already paused)
        if kills >= exp_needed and not paused_for_level_up:
            paused_for_level_up = True
            level += 1
            exp_needed += 15
            
            # Generate power-up choices
            choices = PowerUpChoice.get_random_choices(3)
            selected = show_level_up_screen(choices)
            choices[selected].apply(player)
            paused_for_level_up = False  # Resume game after selection
        
        # Handle events (only if not paused)
        if not paused_for_level_up:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click - unlimited ammo
                        bullets.extend(player.shoot(pygame.mouse.get_pos()))
        
        if not paused_for_level_up:
            # Update player
            player.update()
            
            # Spawn enemies (increases with time and level)
            spawn_counter += 1
            spawn_delay = max(15, 45 - (time_elapsed // 2000) - (level * 2))
            if spawn_counter >= spawn_delay and len(enemies) < 30:
                spawn_counter = 0
                enemies.append(Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, player.speed_bonus))
            
            # Update bullets
            for bullet in bullets[:]:
                bullet.update()
                if bullet.off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    bullets.remove(bullet)
            
            # Update enemies and check collisions
            for enemy in enemies[:]:
                enemy.update(player.x, player.y)
                
                # Enemy-player collision
                if enemy.rect.colliderect(player.rect):
                    if player.take_damage():
                        return "gameover", score, kills, level
                    enemies.remove(enemy)
                    continue
                
                # Bullet collisions
                for bullet in bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        # Apply damage
                        if enemy.take_damage(bullet.damage):
                            # Enemy dies
                            enemies.remove(enemy)
                            kills += 1
                            score += int(10 * player.score_multiplier)
                            
                            # Life steal
                            if player.lifesteal > 0:
                                player.heal(player.lifesteal)
                            
                            # Death particle
                            particles.append({
                                'x': enemy.x, 'y': enemy.y,
                                'life': 10, 'color': enemy.color
                            })
                            
                            # Reduce pierce
                            bullet.pierce_left -= 1
                            if bullet.pierce_left < 0:
                                bullets.remove(bullet)
                        else:
                            # Enemy took damage but didn't die
                            bullet.pierce_left -= 1
                            if bullet.pierce_left < 0:
                                bullets.remove(bullet)
                        break  # Bullet hit, stop checking this enemy
        
        # Draw everything
        screen.fill(BLACK)
        
        # Draw particles
        for p in particles[:]:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), 3)
            p['life'] -= 1
            if p['life'] <= 0:
                particles.remove(p)
        
        # Game objects
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)
        
        # UI
        draw_text(f"TIME: {minutes_left}:{seconds_left:02d}", font, WHITE, 10, 10)
        draw_text(f"KILLS: {kills}/{exp_needed}", font, WHITE, 10, 50)
        draw_text(f"LEVEL: {level}", font, WHITE, 10, 90)
        draw_text(f"HEALTH: {player.health}", font, RED if player.health < 30 else GREEN, 10, 130)
        draw_text(f"SCORE: {score}", font, YELLOW, 10, 170)
        draw_text(f"AMMO: UNLIMITED", font, BLUE, 10, 210)
        
        # Show power-ups
        y_offset = 250
        for powerup in player.active_powerups[-5:]:  # Show last 5
            draw_text(f"✨ {powerup}", small_font, BLUE, 10, y_offset)
            y_offset += 20
        
        # Danger timer visual
        if time_left < 30000:  # Last 30 seconds
            if (pygame.time.get_ticks() % 500) < 250:
                draw_text("FINAL STAND!", big_font, RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, center=True)
        
        pygame.display.flip()
        clock.tick(60)
    
    return "gameover", score, kills, level

def game_over_screen(result, score, kills, level):
    while True:
        screen.fill(BLACK)
        
        if result == "win":
            draw_text("VICTORY!", big_font, GREEN, SCREEN_WIDTH//2, 150, center=True)
            draw_text("You survived 5 minutes!", font, WHITE, SCREEN_WIDTH//2, 250, center=True)
        else:
            draw_text("GAME OVER", big_font, RED, SCREEN_WIDTH//2, 150, center=True)
            draw_text("The darkness consumed you...", font, WHITE, SCREEN_WIDTH//2, 250, center=True)
        
        draw_text(f"Final Score: {score}", font, YELLOW, SCREEN_WIDTH//2, 320, center=True)
        draw_text(f"Total Kills: {kills}", font, WHITE, SCREEN_WIDTH//2, 360, center=True)
        draw_text(f"Level Reached: {level}", font, WHITE, SCREEN_WIDTH//2, 400, center=True)
        draw_text("Press R to Restart | Q to Quit", font, WHITE, SCREEN_WIDTH//2, 500, center=True)
        
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
        result, score, kills, level = game_loop()
        if not game_over_screen(result, score, kills, level):
            break

if __name__ == "__main__":
    main()
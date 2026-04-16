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
font = pygame.font.Font(None, 28)
big_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 20)

# Load enemy images
Enemy.load_images()

# Load background images
title_background = None
game_background = None

try:
    title_background = pygame.image.load("assets/title.png").convert_alpha()
    title_background = pygame.transform.scale(title_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("✓ title.png loaded successfully!")
except:
    print("✗ Could not load assets/title.png - using black background instead")

try:
    game_background = pygame.image.load("assets/background.png").convert_alpha()
    game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("✓ background.png loaded successfully!")
except:
    print("✗ Could not load assets/background.png - using black background instead")

# Colors (for fallback text)
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
        # Draw background
        if title_background:
            screen.blit(title_background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Draw semi-transparent overlay for better text readability
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Title text with glow effect
        draw_text("5 MINUTES TILL DAWN", big_font, YELLOW, SCREEN_WIDTH//2, 150, center=True)
        draw_text("Survive 5 Minutes Against Endless Hordes", font, WHITE, SCREEN_WIDTH//2, 250, center=True)
        draw_text("Level 1: 15 kills | Level 2: 25 kills | Level 3: 35 kills | etc", small_font, YELLOW, SCREEN_WIDTH//2, 300, center=True)
        draw_text("(Kills needed per level, not total)", small_font, WHITE, SCREEN_WIDTH//2, 330, center=True)
        draw_text("Every level up = Choose a Power-Up!", small_font, GREEN, SCREEN_WIDTH//2, 360, center=True)
        draw_text("Press SPACE to Start", font, GREEN, SCREEN_WIDTH//2, 450, center=True)
        draw_text("WASD to Move | Mouse to Aim & Shoot", font, WHITE, SCREEN_WIDTH//2, 500, center=True)
        draw_text("Unlimited Ammo!", small_font, BLUE, SCREEN_WIDTH//2, 540, center=True)
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def show_level_up_screen(choices, current_level, kills_needed_for_next):
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
        if game_background:
            screen.blit(game_background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Semi-transparent overlay for level up screen
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Title
        draw_text(f"LEVEL {current_level} COMPLETE!", big_font, YELLOW, SCREEN_WIDTH//2, 80, center=True)
        draw_text(f"Reached Level {current_level + 1}!", font, GREEN, SCREEN_WIDTH//2, 150, center=True)
        draw_text(f"Next level needs {kills_needed_for_next} kills", small_font, WHITE, SCREEN_WIDTH//2, 190, center=True)
        draw_text("Choose your power-up:", font, WHITE, SCREEN_WIDTH//2, 240, center=True)
        
        # Display choices
        for i, choice in enumerate(choices):
            y_pos = 300 + i * 90
            color = GREEN if selected == i else WHITE
            box_rect = pygame.Rect(150, y_pos - 25, 500, 60)
            pygame.draw.rect(screen, (50, 50, 80), box_rect, border_radius=10)
            pygame.draw.rect(screen, color, box_rect, 2, border_radius=10)
            
            draw_text(choice.name, font, color, SCREEN_WIDTH//2, y_pos, center=True)
            draw_text(choice.description, small_font, YELLOW, SCREEN_WIDTH//2, y_pos + 28, center=True)
        
        draw_text("↑ ↓ to select | SPACE to confirm", small_font, WHITE, SCREEN_WIDTH//2, 550, center=True)
        
        pygame.display.flip()
        clock.tick(30)

def game_loop():
    # Game variables
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    enemies = []
    bullets = []
    particles = []
    
    # Survival timers
    start_time = pygame.time.get_ticks()
    survival_duration = 5 * 60 * 1000  # 5 minutes in milliseconds
    
    # Level system - PER LEVEL kills needed (not cumulative)
    total_kills = 0
    kills_this_level = 0  # Kills since last level up
    level = 1
    
    # Kills needed for CURRENT level to advance
    kills_needed_for_current_level = 15 + (level - 1) * 10
    
    # Difficulty scaling based on time
    last_minute_check = 0
    current_difficulty_minute = 0
    
    running = True
    paused_for_level_up = False
    level_up_selection_active = False
    
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
        minutes_passed = (survival_duration - time_left) // 60000
        
        # Check if a new minute has passed for difficulty increase
        if minutes_passed > last_minute_check:
            last_minute_check = minutes_passed
            current_difficulty_minute = minutes_passed
            Enemy.update_difficulty(current_difficulty_minute)
        
        # Check win condition
        if time_left <= 0:
            return "win", score, total_kills, level
        
        # Level up check - using kills THIS LEVEL only
        if kills_this_level >= kills_needed_for_current_level and not paused_for_level_up and not level_up_selection_active:
            paused_for_level_up = True
            level_up_selection_active = True
            
            next_level_kills_needed = 15 + (level) * 10
            choices = PowerUpChoice.get_random_choices(3)
            selected = show_level_up_screen(choices, level, next_level_kills_needed)
            
            # Apply the selected power-up
            try:
                choices[selected].apply(player)
            except Exception as e:
                print(f"Error applying power-up: {e}")
                player.health = min(player.max_health, player.health + 20)
            
            # Increase level
            level += 1
            
            # Reset kills_this_level (overflow carries over)
            overflow_kills = kills_this_level - kills_needed_for_current_level
            kills_this_level = overflow_kills if overflow_kills > 0 else 0
            
            # Update kills needed for NEW level
            kills_needed_for_current_level = 15 + (level - 1) * 10
            
            paused_for_level_up = False
            level_up_selection_active = False
            continue
        
        # Handle events
        if not paused_for_level_up:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        bullets.extend(player.shoot(pygame.mouse.get_pos()))
        
        if not paused_for_level_up:
            player.update()
            
            # Dynamic spawn delay
            base_spawn_delay = max(8, 45 - (minutes_passed * 3) - (level // 2))
            spawn_counter += 1
            
            max_enemies = min(50, 20 + minutes_passed * 3 + level)
            
            if spawn_counter >= base_spawn_delay and len(enemies) < max_enemies:
                spawn_counter = 0
                enemies_to_spawn = 1
                if minutes_passed >= 3:
                    enemies_to_spawn = random.randint(1, 2)
                if minutes_passed >= 4:
                    enemies_to_spawn = random.randint(1, 3)
                
                for _ in range(enemies_to_spawn):
                    enemies.append(Enemy(SCREEN_WIDTH, SCREEN_HEIGHT, player.speed_bonus, current_difficulty_minute))
            
            # Update bullets
            for bullet in bullets[:]:
                bullet.update()
                if bullet.off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    bullets.remove(bullet)
            
            # Update enemies and check collisions
            for enemy in enemies[:]:
                enemy.update(player.x, player.y)
                
                if enemy.rect.colliderect(player.rect):
                    if player.take_damage():
                        return "gameover", score, total_kills, level
                    enemies.remove(enemy)
                    continue
                
                for bullet in bullets[:]:
                    if bullet.rect.colliderect(enemy.rect):
                        if enemy.take_damage(bullet.damage):
                            enemies.remove(enemy)
                            total_kills += 1
                            kills_this_level += 1
                            
                            base_score = 10
                            if enemy.type == 'tank':
                                base_score = 25
                            elif enemy.type == 'fast':
                                base_score = 15
                            score += int(base_score * player.score_multiplier)
                            
                            # Life steal heal
                            if player.lifesteal > 0:
                                player.heal(player.lifesteal)
                            
                            particles.append({
                                'x': enemy.x, 'y': enemy.y,
                                'life': 10, 'color': enemy.color
                            })
                            
                            bullet.pierce_left -= 1
                            if bullet.pierce_left < 0:
                                bullets.remove(bullet)
                        else:
                            bullet.pierce_left -= 1
                            if bullet.pierce_left < 0:
                                bullets.remove(bullet)
                        break
        
        # Draw everything - with game background
        if game_background:
            screen.blit(game_background, (0, 0))
        else:
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
        
        # Semi-transparent UI background for better text visibility
        ui_panel = pygame.Surface((250, 130))
        ui_panel.set_alpha(180)
        ui_panel.fill(BLACK)
        screen.blit(ui_panel, (0, 0))
        
        # CLEAN UI - Top left corner, compact
        kills_left = kills_needed_for_current_level - kills_this_level
        if kills_left < 0:
            kills_left = 0
            
        # Line 1: Time and Kills to level up
        draw_text(f"TIME: {minutes_left}:{seconds_left:02d}  |  {kills_left} kills to level up", font, WHITE, 10, 10)
        
        # Line 2: Total kills and Score
        draw_text(f"TOTAL KILLS: {total_kills}  |  SCORE: {score}", font, WHITE, 10, 40)
        
        # Line 3: Health bar (visual only)
        health_percent = player.health / player.max_health
        bar_width = 150
        bar_height = 12
        pygame.draw.rect(screen, (100, 0, 0), (10, 65, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (10, 65, bar_width * health_percent, bar_height))
        draw_text(f"HEALTH: {int(player.health)}/{int(player.max_health)}", small_font, WHITE, 10, 80)
        
        # Show active power-ups (compact row at bottom of screen)
        if player.active_powerups:
            powerup_text = " | ".join(player.active_powerups[-3:])
            # Add semi-transparent background for power-up text
            power_bg = pygame.Surface((300, 25))
            power_bg.set_alpha(180)
            power_bg.fill(BLACK)
            screen.blit(power_bg, (5, SCREEN_HEIGHT - 30))
            draw_text(f"POWER-UPS: {powerup_text}", small_font, BLUE, 10, SCREEN_HEIGHT - 25)
        
        # Difficulty indicator (top right)
        difficulty_color = GREEN
        if minutes_passed >= 3:
            difficulty_color = YELLOW
        if minutes_passed >= 4:
            difficulty_color = ORANGE
        if minutes_passed >= 4.5:
            difficulty_color = RED
        draw_text(f"DIFFICULTY: {current_difficulty_minute}/5", small_font, difficulty_color, SCREEN_WIDTH - 100, 10)
        
        # Danger timer visual
        if time_left < 30000:
            if (pygame.time.get_ticks() % 500) < 250:
                draw_text("FINAL STAND!", big_font, RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, center=True)
        
        # Difficulty warning
        if minutes_passed >= 4:
            if (pygame.time.get_ticks() % 1000) < 500:
                draw_text("⚠️ MAXIMUM DIFFICULTY ⚠️", small_font, RED, SCREEN_WIDTH//2, SCREEN_HEIGHT - 50, center=True)
        
        pygame.display.flip()
        clock.tick(60)
    
    return "gameover", score, total_kills, level

def game_over_screen(result, score, kills, level):
    while True:
        # Draw background
        if game_background:
            screen.blit(game_background, (0, 0))
        else:
            screen.fill(BLACK)
        
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
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
import pygame
import sys
import random
import math
import os
from player import Player
from enemy import Enemy
from bullet import Bullet
from powerup import PowerUp, PowerUpChoice

# Initialize
pygame.init()
pygame.mixer.init()
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("5 Minutes Till Dawn - Top Down Shooter")
clock = pygame.time.Clock()

# Get the correct path to assets folder
def get_asset_path(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    asset_path = os.path.join(script_dir, "assets", filename)
    return asset_path

# 8-bit style fonts - Try multiple popular pixel fonts
pixel_font = None
pixel_font_big = None
pixel_font_small = None

# List of possible 8-bit font files to try (in order of preference)
font_options = [
    "Ithaca.ttf",
]

font_loaded = False
for font_name in font_options:
    try:
        font_path = get_asset_path(font_name)
        if os.path.exists(font_path):
            pixel_font = pygame.font.Font(font_path, 24)
            pixel_font_big = pygame.font.Font(font_path, 48)
            pixel_font_small = pygame.font.Font(font_path, 16)
            print(f"✓ Loaded 8-bit font: {font_name}")
            font_loaded = True
            break
    except:
        continue

# Fallback to system fonts if no custom font found
if not font_loaded:
    print("No custom font found, using system pixel-style fonts")
    try:
        pixel_font = pygame.font.SysFont("couriernew", 24, bold=True)
        pixel_font_big = pygame.font.SysFont("couriernew", 48, bold=True)
        pixel_font_small = pygame.font.SysFont("couriernew", 16, bold=True)
    except:
        pixel_font = pygame.font.Font(None, 24)
        pixel_font_big = pygame.font.Font(None, 48)
        pixel_font_small = pygame.font.Font(None, 16)

# Load sounds
shoot_sound = None
powerup_sound = None
gameover_sound = None
soundtrack = None
soundtrack2 = None

try:
    shoot_sound = pygame.mixer.Sound(get_asset_path("shoot.mp3"))
    shoot_sound.set_volume(0.5)
    print("✓ shoot.mp3 loaded")
except:
    print("✗ Could not load shoot.mp3")

try:
    powerup_sound = pygame.mixer.Sound(get_asset_path("powerup.mp3"))
    powerup_sound.set_volume(0.6)
    print("✓ powerup.mp3 loaded")
except:
    print("✗ Could not load powerup.mp3")

try:
    gameover_sound = pygame.mixer.Sound(get_asset_path("gameover.mp3"))
    gameover_sound.set_volume(0.7)
    print("✓ gameover.mp3 loaded")
except:
    print("✗ Could not load gameover.mp3")

try:
    soundtrack = pygame.mixer.Sound(get_asset_path("soundtrack.mp3"))
    soundtrack.set_volume(0.4)
    print("✓ soundtrack.mp3 loaded")
except:
    print("✗ Could not load soundtrack.mp3")

try:
    soundtrack2 = pygame.mixer.Sound(get_asset_path("soundtrack2.mp3"))
    soundtrack2.set_volume(0.4)
    print("✓ soundtrack2.mp3 loaded")
except:
    print("✗ Could not load soundtrack2.mp3")

# Load enemy images
Enemy.load_images()

# Load background images
title_background = None
game_background = None

try:
    title_background = pygame.image.load(get_asset_path("title.png")).convert_alpha()
    title_background = pygame.transform.scale(title_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("✓ title.png loaded!")
except:
    print("title.png not found")

try:
    game_background = pygame.image.load(get_asset_path("background.png")).convert_alpha()
    game_background = pygame.transform.scale(game_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    print("✓ background.png loaded!")
except:
    print("background.png not found")

# Colors - 8-bit retro palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 100, 255)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (200, 200, 200)

def draw_text_8bit(text, font, color, x, y, center=False, shadow=True):
    """Draw text with 8-bit style (with shadow option)"""
    if shadow:
        shadow_surface = font.render(text, True, BLACK)
        if center:
            screen.blit(shadow_surface, (x - shadow_surface.get_width() // 2 + 2, y + 2))
        else:
            screen.blit(shadow_surface, (x + 2, y + 2))
    
    surface = font.render(text, True, color)
    if center:
        x = x - surface.get_width() // 2
    screen.blit(surface, (x, y))

def draw_pixel_button(x, y, width, height, text, is_selected=False):
    """Draw an 8-bit style button"""
    color = YELLOW if is_selected else (80, 80, 100)
    pygame.draw.rect(screen, color, (x, y, width, height))
    pygame.draw.rect(screen, WHITE, (x, y, width, height), 2)
    pygame.draw.rect(screen, DARK_GRAY, (x + 2, y + 2, width - 4, height - 4), 1)
    
    text_surface = pixel_font.render(text, True, BLACK if is_selected else WHITE)
    text_x = x + (width - text_surface.get_width()) // 2
    text_y = y + (height - text_surface.get_height()) // 2
    screen.blit(text_surface, (text_x, text_y))

def show_how_to_play_popup():
    """Display a popup window with game instructions"""
    popup_width = 520
    popup_height = 420
    popup_x = SCREEN_WIDTH//2 - popup_width//2
    popup_y = SCREEN_HEIGHT//2 - popup_height//2
    
    waiting = True
    
    while waiting:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        pygame.draw.rect(screen, (20, 20, 40), (popup_x, popup_y, popup_width, popup_height))
        for i in range(3):
            pygame.draw.rect(screen, YELLOW, (popup_x - i, popup_y - i, popup_width + i*2, popup_height + i*2), 1)
        
        draw_text_8bit("HOW TO PLAY", pixel_font_big, YELLOW, SCREEN_WIDTH//2, popup_y + 35, center=True, shadow=True)
        pygame.draw.line(screen, YELLOW, (popup_x + 20, popup_y + 70), (popup_x + popup_width - 20, popup_y + 70), 2)
        
        draw_text_8bit("> CONTROLS <", pixel_font, CYAN, popup_x + 20, popup_y + 90, center=False, shadow=True)
        draw_text_8bit("W / A / S / D", pixel_font_small, WHITE, popup_x + 35, popup_y + 120, center=False, shadow=True)
        draw_text_8bit("- Move character", pixel_font_small, LIGHT_GRAY, popup_x + 180, popup_y + 120, center=False, shadow=True)
        draw_text_8bit("MOUSE", pixel_font_small, WHITE, popup_x + 35, popup_y + 145, center=False, shadow=True)
        draw_text_8bit("- Aim", pixel_font_small, LIGHT_GRAY, popup_x + 180, popup_y + 145, center=False, shadow=True)
        draw_text_8bit("LEFT CLICK", pixel_font_small, WHITE, popup_x + 35, popup_y + 170, center=False, shadow=True)
        draw_text_8bit("- Shoot", pixel_font_small, LIGHT_GRAY, popup_x + 180, popup_y + 170, center=False, shadow=True)
        
        draw_text_8bit("> GAME MECHANICS <", pixel_font, CYAN, popup_x + 20, popup_y + 210, center=False, shadow=True)
        mechanics = [
            "Survive for 5 minutes",
            "Kill enemies to gain XP",
            "Every 15/25/35+ kills = Level Up!",
            "Choose a Power-Up each level",
            "Enemies get stronger every minute"
        ]
        for i, mechanic in enumerate(mechanics):
            draw_text_8bit(f"• {mechanic}", pixel_font_small, WHITE, popup_x + 35, popup_y + 240 + i * 25, center=False, shadow=True)
        
        close_x = SCREEN_WIDTH//2 - 60
        close_y = popup_y + popup_height - 50
        close_width = 120
        close_height = 35
        
        mouse_pos = pygame.mouse.get_pos()
        is_hover = (close_x < mouse_pos[0] < close_x + close_width and 
                    close_y < mouse_pos[1] < close_y + close_height)
        
        draw_pixel_button(close_x, close_y, close_width, close_height, "CLOSE", is_hover)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and is_hover:
                    waiting = False

def menu():
    if soundtrack:
        soundtrack.play(loops=-1)
    
    while True:
        if title_background:
            screen.blit(title_background, (0, 0))
        else:
            screen.fill(BLACK)
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Side by side buttons
        button_width = 180
        button_height = 50
        button_spacing = 30
        total_width = (button_width * 2) + button_spacing
        
        start_button_x = SCREEN_WIDTH//2 - total_width//2
        start_button_y = SCREEN_HEIGHT//2 + 50
        
        howto_button_x = start_button_x + button_width + button_spacing
        howto_button_y = start_button_y
        
        mouse_pos = pygame.mouse.get_pos()
        
        start_is_hover = (start_button_x < mouse_pos[0] < start_button_x + button_width and 
                          start_button_y < mouse_pos[1] < start_button_y + button_height)
        
        howto_is_hover = (howto_button_x < mouse_pos[0] < howto_button_x + button_width and 
                          howto_button_y < mouse_pos[1] < howto_button_y + button_height)
        
        draw_pixel_button(start_button_x, start_button_y, button_width, button_height, "START GAME", start_is_hover)
        draw_pixel_button(howto_button_x, howto_button_y, button_width, button_height, "HOW TO PLAY", howto_is_hover)
        
        
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if soundtrack:
                        soundtrack.stop()
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if start_is_hover:
                        if soundtrack:
                            soundtrack.stop()
                        return
                    if howto_is_hover:
                        show_how_to_play_popup()

def show_level_up_screen(choices, current_level, kills_needed_for_next):
    if powerup_sound:
        powerup_sound.play()
    
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
        
        if game_background:
            screen.blit(game_background, (0, 0))
        else:
            screen.fill(BLACK)
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        draw_text_8bit(f"LEVEL {current_level} UP!", pixel_font_big, YELLOW, SCREEN_WIDTH//2, 80, center=True)
        draw_text_8bit("CHOOSE YOUR POWER", pixel_font, CYAN, SCREEN_WIDTH//2, 150, center=True)
        
        for i, choice in enumerate(choices):
            y_pos = 220 + i * 100
            color = GREEN if selected == i else WHITE
            box_rect = pygame.Rect(150, y_pos - 20, 500, 70)
            pygame.draw.rect(screen, (50, 50, 80), box_rect, border_radius=5)
            pygame.draw.rect(screen, color, box_rect, 2, border_radius=5)
            
            draw_text_8bit(choice.name, pixel_font, color, SCREEN_WIDTH//2, y_pos, center=True)
            draw_text_8bit(choice.description, pixel_font_small, YELLOW, SCREEN_WIDTH//2, y_pos + 30, center=True)
        
        draw_text_8bit("UP/DOWN  |  SPACE", pixel_font_small, WHITE, SCREEN_WIDTH//2, 550, center=True)
        
        pygame.display.flip()
        clock.tick(30)

def game_loop():
    if soundtrack2:
        soundtrack2.play(loops=-1)
    
    player = Player(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)
    enemies = []
    bullets = []
    particles = []
    
    start_time = pygame.time.get_ticks()
    survival_duration = 5 * 60 * 1000
    
    total_kills = 0
    kills_this_level = 0
    level = 1
    kills_needed_for_current_level = 15 + (level - 1) * 10
    
    last_minute_check = 0
    current_difficulty_minute = 0
    
    running = True
    paused_for_level_up = False
    level_up_selection_active = False
    
    score = 0
    spawn_counter = 0
    
    while running:
        current_time = pygame.time.get_ticks()
        time_elapsed = current_time - start_time
        time_left = max(0, survival_duration - time_elapsed)
        minutes_left = time_left // 60000
        seconds_left = (time_left % 60000) // 1000
        minutes_passed = (survival_duration - time_left) // 60000
        
        if minutes_passed > last_minute_check:
            last_minute_check = minutes_passed
            current_difficulty_minute = minutes_passed
            Enemy.update_difficulty(current_difficulty_minute)
        
        if time_left <= 0:
            if soundtrack2:
                soundtrack2.stop()
            return "win", score, total_kills, level
        
        if kills_this_level >= kills_needed_for_current_level and not paused_for_level_up and not level_up_selection_active:
            paused_for_level_up = True
            level_up_selection_active = True
            
            next_level_kills_needed = 15 + (level) * 10
            choices = PowerUpChoice.get_random_choices(3)
            selected = show_level_up_screen(choices, level, next_level_kills_needed)
            
            try:
                choices[selected].apply(player)
            except Exception as e:
                print(f"Error applying power-up: {e}")
                player.health = min(player.max_health, player.health + 20)
            
            level += 1
            overflow_kills = kills_this_level - kills_needed_for_current_level
            kills_this_level = overflow_kills if overflow_kills > 0 else 0
            kills_needed_for_current_level = 15 + (level - 1) * 10
            
            paused_for_level_up = False
            level_up_selection_active = False
            continue
        
        if not paused_for_level_up:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if shoot_sound:
                            shoot_sound.play()
                        bullets.extend(player.shoot(pygame.mouse.get_pos()))
        
        if not paused_for_level_up:
            player.update()
            
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
            
            for bullet in bullets[:]:
                bullet.update()
                if bullet.off_screen(SCREEN_WIDTH, SCREEN_HEIGHT):
                    bullets.remove(bullet)
            
            for enemy in enemies[:]:
                enemy.update(player.x, player.y)
                
                if enemy.rect.colliderect(player.rect):
                    if player.take_damage():
                        if soundtrack2:
                            soundtrack2.stop()
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
                            
                            if player.lifesteal > 0:
                                player.heal(player.lifesteal)
                            
                            if player.exploding_kills:
                                for _ in range(20):
                                    particles.append({
                                        'x': enemy.x + random.randint(-25, 25),
                                        'y': enemy.y + random.randint(-25, 25),
                                        'life': 15,
                                        'color': (255, 100, 0)
                                    })
                                for _ in range(15):
                                    particles.append({
                                        'x': enemy.x + random.randint(-20, 20),
                                        'y': enemy.y + random.randint(-20, 20),
                                        'life': 10,
                                        'color': (255, 200, 0)
                                    })
                                for other in enemies[:]:
                                    dist = math.hypot(other.x - enemy.x, other.y - enemy.y)
                                    if dist < 80:
                                        other.take_damage(1)
                                        particles.append({
                                            'x': other.x,
                                            'y': other.y,
                                            'life': 5,
                                            'color': (255, 255, 255)
                                        })
                            else:
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
        
        if game_background:
            screen.blit(game_background, (0, 0))
        else:
            screen.fill(BLACK)
        
        for p in particles[:]:
            pygame.draw.circle(screen, p['color'], (int(p['x']), int(p['y'])), 3)
            p['life'] -= 1
            if p['life'] <= 0:
                particles.remove(p)
        
        for bullet in bullets:
            bullet.draw(screen)
        for enemy in enemies:
            enemy.draw(screen)
        player.draw(screen)
        
        kills_left = kills_needed_for_current_level - kills_this_level
        if kills_left < 0:
            kills_left = 0
        
        time_text = f"{minutes_left:02d}:{seconds_left:02d}"
        draw_text_8bit(time_text, pixel_font_big, YELLOW, 15, 10, shadow=True)
        draw_text_8bit(f"KILLS: {kills_left}", pixel_font, CYAN, 15, 60, shadow=True)
        draw_text_8bit(f"SCORE: {score}", pixel_font, WHITE, 15, 90, shadow=True)
        
        health_percent = player.health / player.max_health
        bar_width = 150
        bar_height = 12
        pygame.draw.rect(screen, (100, 0, 0), (15, 120, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (15, 120, bar_width * health_percent, bar_height))
        pygame.draw.rect(screen, WHITE, (15, 120, bar_width, bar_height), 1)
        draw_text_8bit(f"HP: {int(player.health)}/{int(player.max_health)}", pixel_font_small, WHITE, 15, 137, shadow=True)
        
        if player.active_powerups:
            power_text = " > ".join(player.active_powerups[-3:])
            draw_text_8bit(power_text, pixel_font_small, BLUE, SCREEN_WIDTH//2, SCREEN_HEIGHT - 30, center=True, shadow=True)
        
        difficulty_color = [GREEN, YELLOW, ORANGE, RED][min(current_difficulty_minute, 3)]
        draw_text_8bit(f"DIFFICULTY {current_difficulty_minute}/5", pixel_font_small, difficulty_color, SCREEN_WIDTH - 80, 15, shadow=True)
        
        if time_left < 30000:
            if (pygame.time.get_ticks() % 500) < 250:
                draw_text_8bit("!!! FINAL STAND !!!", pixel_font, RED, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, center=True, shadow=True)
        
        pygame.display.flip()
        clock.tick(60)
    
    return "gameover", score, total_kills, level

def game_over_screen(result, score, kills, level):
    if gameover_sound:
        gameover_sound.play()
    
    while True:
        if game_background:
            screen.blit(game_background, (0, 0))
        else:
            screen.fill(BLACK)
        
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        if result == "win":
            draw_text_8bit("VICTORY!", pixel_font_big, GREEN, SCREEN_WIDTH//2, 150, center=True)
            draw_text_8bit("YOU SURVIVED!", pixel_font, CYAN, SCREEN_WIDTH//2, 220, center=True)
        else:
            draw_text_8bit("GAME OVER", pixel_font_big, RED, SCREEN_WIDTH//2, 150, center=True)
            draw_text_8bit("THE DARKNESS WON", pixel_font, YELLOW, SCREEN_WIDTH//2, 220, center=True)
        
        draw_text_8bit(f"SCORE: {score}", pixel_font, WHITE, SCREEN_WIDTH//2, 320, center=True)
        draw_text_8bit(f"KILLS: {kills}", pixel_font, WHITE, SCREEN_WIDTH//2, 360, center=True)
        draw_text_8bit(f"LEVEL: {level}", pixel_font, WHITE, SCREEN_WIDTH//2, 400, center=True)
        
        button_x = SCREEN_WIDTH//2 - 100
        button_y = SCREEN_HEIGHT//2 + 100
        button_width = 200
        button_height = 50
        
        mouse_pos = pygame.mouse.get_pos()
        is_hover = (button_x < mouse_pos[0] < button_x + button_width and 
                    button_y < mouse_pos[1] < button_y + button_height)
        
        draw_pixel_button(button_x, button_y, button_width, button_height, "RESTART", is_hover)
        draw_text_8bit("OR PRESS 'R' KEY", pixel_font_small, WHITE, SCREEN_WIDTH//2, button_y + 70, center=True)
        
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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and is_hover:
                    return True

def main():
    while True:
        menu()
        result, score, kills, level = game_loop()
        if not game_over_screen(result, score, kills, level):
            break

if __name__ == "__main__":
    main()
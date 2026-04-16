import random

class PowerUp:
    def __init__(self, name, description, effect_func):
        self.name = name
        self.description = description
        self.effect_func = effect_func
    
    def apply(self, player):
        self.effect_func(player)
        if self.name not in player.active_powerups:
            player.active_powerups.append(self.name)

class PowerUpChoice:
    @staticmethod
    def get_random_choices(count=3):
        all_powerups = [
            PowerUp("HEALTH BOOST", "+20 Max Health & Full Heal", 
                   lambda p: (setattr(p, 'max_health', p.max_health + 20), 
                             setattr(p, 'health', p.max_health))),
            
            PowerUp("SPEED DEMON", "+30% Movement Speed", 
                   lambda p: (setattr(p, 'speed_bonus', p.speed_bonus + 0.3), 
                             setattr(p, 'speed', p.base_speed + p.speed_bonus))),
            
            PowerUp("DOUBLE SHOT", "Shoot 2 bullets at once", 
                   lambda p: setattr(p, 'bullet_count', min(p.bullet_count + 1, 5))),
            
            PowerUp("FAST HANDS", "+50% Fire Rate", 
                   lambda p: setattr(p, 'fire_delay', max(3, p.fire_delay - 3))),
            
            PowerUp("REAPER", "Enemies explode on death, damaging nearby enemies", 
                   lambda p: setattr(p, 'exploding_kills', True)),
            
            PowerUp("PIERCING SHOTS", "Bullets pierce 2 enemies", 
                   lambda p: setattr(p, 'pierce', p.pierce + 2)),
            
            PowerUp("IRON SKIN", "Take 30% less damage", 
                   lambda p: setattr(p, 'damage_reduction', min(0.7, p.damage_reduction + 0.3))),
            
            PowerUp("LIFE STEAL", "Kills heal 5 HP", 
                   lambda p: setattr(p, 'lifesteal', p.lifesteal + 5)),
            
            PowerUp("GHOST", "Become invincible for 1 second after taking damage", 
                   lambda p: setattr(p, 'invincible_on_hit', True)),
            
            PowerUp("SCORCHER", "+50% Score from kills", 
                   lambda p: setattr(p, 'score_multiplier', p.score_multiplier + 0.5)),
            
            PowerUp("TRIPLE SHOT", "Shoot 3 bullets in a spread", 
                   lambda p: setattr(p, 'bullet_count', min(p.bullet_count + 2, 5))),
            
            PowerUp("NIMBLE", "+20% Speed & Longer invincibility", 
                   lambda p: (setattr(p, 'speed_bonus', p.speed_bonus + 0.2),
                             setattr(p, 'speed', p.base_speed + p.speed_bonus),
                             setattr(p, 'invincible_duration', p.invincible_duration + 15))),
            
            PowerUp("WAVE SHOT", "Shots spread wider (5 bullets)", 
                   lambda p: setattr(p, 'bullet_count', 5)),
            
            PowerUp("MIGHT", "+100% Damage (Double Damage)", 
                   lambda p: setattr(p, 'damage_bonus', p.damage_bonus + 1.0)),
            
            PowerUp("BLOODLUST", "Kills heal 10 HP", 
                   lambda p: setattr(p, 'lifesteal', p.lifesteal + 10)),
            
            PowerUp("RAPID FIRE", "Shoot twice as fast", 
                   lambda p: setattr(p, 'fire_delay', max(2, p.fire_delay - 4))),
        ]
        
        return random.sample(all_powerups, min(count, len(all_powerups)))
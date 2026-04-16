import random

class PowerUp:
    def __init__(self, name, description, effect_func):
        self.name = name
        self.description = description
        self.effect_func = effect_func
    
    def apply(self, player):
        self.effect_func(player)
        player.active_powerups.append(self.name)

class PowerUpChoice:
    @staticmethod
    def get_random_choices(count=3):
        all_powerups = [
            PowerUp("❤️ HEALTH BOOST", "+20 Max Health & Full Heal", 
                   lambda p: setattr(p, 'max_health', p.max_health + 20) or setattr(p, 'health', min(p.health + 20, p.max_health + 20))),
            
            PowerUp("💨 SPEED DEMON", "+30% Movement Speed", 
                   lambda p: setattr(p, 'speed_bonus', p.speed_bonus + 0.3) or setattr(p, 'speed', p.base_speed + p.speed_bonus)),
            
            PowerUp("🔫 DOUBLE SHOT", "Shoot 2 bullets at once", 
                   lambda p: setattr(p, 'bullet_count', min(p.bullet_count + 1, 5))),
            
            PowerUp("⚡ FAST HANDS", "+50% Fire Rate", 
                   lambda p: setattr(p, 'fire_delay', max(3, p.fire_delay - 2))),
            
            PowerUp("📦 BIG MAGAZINE", "+20 Ammo Capacity", 
                   lambda p: setattr(p, 'max_ammo', p.max_ammo + 20) or setattr(p, 'ammo', p.ammo + 20)),
            
            PowerUp("💀 REAPER", "Enemies explode on death", 
                   lambda p: setattr(p, 'exploding_kills', True)),
            
            PowerUp("🔮 PIERCING SHOTS", "Bullets pierce 1 enemy", 
                   lambda p: setattr(p, 'pierce', p.pierce + 1)),
            
            PowerUp("🛡️ IRON SKIN", "Take 50% less damage", 
                   lambda p: setattr(p, 'damage_reduction', p.damage_reduction + 0.5)),
            
            PowerUp("💉 LIFE STEAL", "Kills heal 5 HP", 
                   lambda p: setattr(p, 'lifesteal', p.lifesteal + 5)),
            
            PowerUp("🎯 FOCUS FIRE", "+25% Damage", 
                   lambda p: setattr(p, 'damage_bonus', p.damage_bonus + 0.25)),
            
            PowerUp("🌀 GHOST", "Brief invincibility after hit", 
                   lambda p: setattr(p, 'invincible_on_hit', True)),
            
            PowerUp("💰 SCORCHER", "+50% Score from kills", 
                   lambda p: setattr(p, 'score_multiplier', p.score_multiplier + 0.5)),
        ]
        
        return random.sample(all_powerups, min(count, len(all_powerups)))
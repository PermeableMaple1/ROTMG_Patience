import pygame

class Player(pygame.sprite.Sprite):
    
    def __init__(self, scale, FPS, spd, health, defence):
        super().__init__()
        self.scale = scale
        self.FPS = FPS
        self.player_sprite = pygame.image.load('data\images\Player_Images\Player.png').convert_alpha()
        self.player_sprite = pygame.transform.scale_by(self.player_sprite, self.scale)
        self.animation_count = 0
        self.last_direction = 0
        self.hp = health
        self.maxhp = health
        self.defence = defence
        
        self.bleed_time = 0
        self.curse_time = 0
        self.damage_factor = 1
        self.in_void = False
        
        self.spd = spd
        self.player_spd = self.spd
        
        
        self.walk_left = [pygame.image.load('data\images\Player_Images\walk_left1.png'),
                          pygame.image.load('data\images\Player_Images\walk_left2.png'),
                          pygame.image.load('data\images\Player_Images\walk_left3.png')]
        self.walk_right = [pygame.image.load('data\images\Player_Images\walk_right1.png'),
                          pygame.image.load('data\images\Player_Images\walk_right2.png'),
                          pygame.image.load('data\images\Player_Images\walk_right3.png')]
        self.walk_up = [pygame.image.load('data\images\Player_Images\walk_up1.png'),
                          pygame.image.load('data\images\Player_Images\walk_up2.png'),
                          pygame.image.load('data\images\Player_Images\walk_up3.png')]
        self.walk_down = [pygame.image.load('data\images\Player_Images\walk_down1.png'),
                          pygame.image.load('data\images\Player_Images\walk_down2.png'),
                          pygame.image.load('data\images\Player_Images\walk_down3.png')]
        
        self.lowhp_blink = 0
        self.a = 1
        
        self.bleed_effect = pygame.image.load(r'data\images\Status_Effects\bleeding.png').convert_alpha()
        self.bleed_effect = pygame.transform.scale_by(self.bleed_effect, 1)
        self.bleed_effect_rect = self.bleed_effect.get_rect()
        self.curse_effect = pygame.image.load('data\images\Status_Effects\curse.png').convert_alpha()
        self.curse_effect = pygame.transform.scale_by(self.curse_effect, 1)
        self.curse_effect_rect = self.curse_effect.get_rect()
        
    def main(self, display, sprite):
        screen_center = display.get_rect().center
        self.rect = sprite.get_rect()
        self.rect.center = screen_center
        
        ratio = self.hp/self.maxhp
        self.healthbar(display, ratio)
        
        if ratio <= 0.2:
            self.lowhp_blink += 15*self.a
            if self.lowhp_blink//200 != 0:
                self.a *= -1
                self.lowhp_blink += 15*self.a
            sprite.fill((self.lowhp_blink,0,0,0), None, pygame.BLEND_RGBA_ADD)
            
        self.apply_effects(display)
        
        if self.in_void is True:
           crop = pygame.Rect(0,0,self.rect.width,self.rect.height/2)
           crop.height += 3*self.scale
           display.blit(sprite, (self.rect.left,self.rect.top + self.scale), crop)
        else:  
            pygame.Surface.blit(display, sprite, self.rect)
          
    def movement(self, keys, tiles, hitbox, scroll):
        
        if keys[pygame.K_a] and scroll[0] > -8*17*self.scale:
            scroll[0] -= 8 * self.scale * (4 + 5.6 * (self.player_spd / 75)) / self.FPS            
        if keys[pygame.K_d]  and scroll[0] < 8*17*self.scale:
            scroll[0] += 8 * self.scale * (4 + 5.6 * (self.player_spd / 75)) / self.FPS
        if keys[pygame.K_s] and scroll[1] < 8*9.75*self.scale:
            scroll[1] += 8 * self.scale * (4 + 5.6 * (self.player_spd / 75)) / self.FPS
        if keys[pygame.K_w] and scroll[1] > -8*24.5*self.scale:
            scroll[1] -= 8 * self.scale * (4 + 5.6 * (self.player_spd / 75)) / self.FPS
        return scroll
    
    def get_tile_collisions(self, hitbox, tiles):
        hits = []
        
        for tile in tiles:
            if hitbox.colliderect(tile.rect):
                hits.append(tile)
        
        return hits
    

    
    def animation(self, keys):
        if keys[pygame.K_a]:
            if self.animation_count + 1 >= 36:
                self.animation_count = 0
            self.animation_count += 1
            sprite = self.walk_left[self.animation_count//12]
            sprite = pygame.transform.scale_by(sprite, self.scale)
            self.last_direction = 0
        elif keys[pygame.K_d]:
            if self.animation_count + 1 >= 36:
                self.animation_count = 0
            self.animation_count += 1
            sprite = self.walk_right[self.animation_count//12]
            sprite = pygame.transform.scale_by(sprite, self.scale)
            self.last_direction = 1
        elif keys[pygame.K_s]:
            if self.animation_count + 1 >= 36:
                self.animation_count = 0
            self.animation_count += 1
            sprite = self.walk_down[self.animation_count//12]
            sprite = pygame.transform.scale_by(sprite, self.scale)
            self.last_direction = 2
        elif keys[pygame.K_w]:
            if self.animation_count + 1 >= 36:
                self.animation_count = 0
            self.animation_count += 1
            sprite = self.walk_up[self.animation_count//12]
            sprite = pygame.transform.scale_by(sprite, self.scale)
            self.last_direction = 3
        else:
            if self.last_direction == 0:
                sprite = pygame.transform.flip(self.player_sprite, True, False).copy()
            elif self.last_direction == 1:
                sprite = self.player_sprite.copy()
            elif self.last_direction == 2:
                sprite = self.walk_down[1].copy()
                sprite = pygame.transform.scale_by(sprite, self.scale)
            elif self.last_direction == 3:
                sprite = self.walk_up[0].copy()
                sprite = pygame.transform.scale_by(sprite, self.scale)
            self.animation_count = 0
        return sprite
    
    def healthbar(self, display, ratio):
        screen_center = display.get_rect().center
        outline = pygame.Rect(screen_center[0] - 4.5*self.scale, screen_center[1] + 4.5*self.scale, 9*self.scale, 1.5*self.scale)
        
        healthbar = pygame.Rect(screen_center[0] - 4.5*self.scale, screen_center[1] + 4.5*self.scale, 9*self.scale*ratio, 1.5*self.scale)
        if ratio <= 0.2:
            color = [200,0,0]
        elif ratio < 0.5:
            color = [255,150,0]
        else:
            color = [50,200,0]
        
        pygame.draw.rect(display, color, healthbar)
        pygame.draw.rect(display, [0,0,0], outline, round(self.scale//3))
        
    def status_effect(self, effect, effect_time):
        
        if effect == 'Bleeding':
            self.bleed_time = effect_time
                
        elif effect == 'Curse':
            self.curse_time = effect_time
    
    def apply_effects(self, display):
        screen_center = display.get_rect().center
        
        if self.bleed_time > 0 and (self.hp - 20/self.FPS) > 0:
            self.bleeding = True
            self.bleed_time -= 1/self.FPS
            self.hp -= 20/self.FPS
            
            
            if self.cursed is False:
                self.bleed_effect_rect.centerx = screen_center[0]
            else:
                self.bleed_effect_rect.centerx = screen_center[0] + self.bleed_effect_rect.width/2
            self.bleed_effect_rect.centery = screen_center[1] - 6*self.scale
            pygame.Surface.blit(display, self.bleed_effect, self.bleed_effect_rect)
            
        else:
            self.bleeding = False
            
        if self.curse_time > 0:
            self.cursed = True
            self.damage_factor = 1.25
            self.curse_time -= 1/self.FPS
            
            if self.bleeding is False:
                self.curse_effect_rect.centerx = screen_center[0]
            else:
                self.curse_effect_rect.centerx = screen_center[0] - self.curse_effect_rect.width/2
            self.curse_effect_rect.centery = screen_center[1] - 6*self.scale
            pygame.Surface.blit(display, self.curse_effect, self.curse_effect_rect)
            
        else:
            self.damage_factor = 1
            self.cursed = False
            
        if self.in_void is True:
            self.hp -= 150/self.FPS
            self.player_spd *= 1/3
        else:
            self.player_spd = self.spd
        
            
        
        
        
            
 

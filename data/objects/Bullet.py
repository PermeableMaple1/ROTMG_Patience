import pygame
import random
import math
import numpy as np

class Bullet(pygame.sprite.Sprite):
    
    def __init__(self, x0, y0, angle, scale, FPS, type_):
        super().__init__()
        self.x0 = x0
        self.y0 = y0
        self.x = x0
        self.y = y0
        self.angle = angle
        self.scale = scale
        self.FPS = FPS
        self.hit = False
        
        if type_ == 1:
            self.image = pygame.image.load('data\images\Bullet_Images\BlueBullet1.png').convert_alpha()
            self.image = pygame.transform.scale_by(self.image, self.scale*0.75)
            self.image = pygame.transform.rotate(self.image, -45)
            self.damage = 70
            self.truedmg = 0
            self.status_effect = None
            self.effect_time = 0
            self.speed = 4*8*self.scale / self.FPS
            self.range = 16
            
        elif type_ == 2:
            self.image = pygame.image.load('data\images\Bullet_Images\RedBullet1.png').convert_alpha()
            self.image = pygame.transform.scale_by(self.image, self.scale*0.75)
            self.image = pygame.transform.rotate(self.image, -45)
            self.damage = 100
            self.truedmg = 1
            self.status_effect = 'Curse'
            self.effect_time = 3
            self.speed = 4*8*self.scale / self.FPS
            self.range = 16
            
        elif type_ == 3:
            self.image = pygame.image.load('data\images\Bullet_Images\BlueBullet2.png').convert_alpha()
            self.image = pygame.transform.scale_by(self.image, self.scale)
            self.damage = 45
            self.truedmg = 0
            self.status_effect = None
            self.effect_time = 0
            self.speed = random.choice([2,3,5])*8*self.scale / self.FPS
            self.range = 32
            
        elif type_ == 4:
            self.image = pygame.image.load('data\images\Bullet_Images\RedBullet2.png').convert_alpha()
            self.image = pygame.transform.scale_by(self.image, self.scale)
            self.damage = 20
            self.truedmg = 0
            self.status_effect = 'Bleeding'
            self.effect_time = 3
            self.speed = random.choice([2,3,5])*8*self.scale / self.FPS
            self.range = 32
        
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect(center = (x0,y0))
        self.hitbox = pygame.Rect(0, 0, 2*self.scale, 2*self.scale)
        
    def update(self, scroll):
        self.x += self.speed*math.cos(self.angle*np.pi/180)
        self.y -= self.speed*math.sin(self.angle*np.pi/180)
        
        distance_x = self.x - self.x0
        distance_y = self.y - self.y0
        distance = math.sqrt(distance_x**2 + distance_y**2)
        if distance >= self.range*8*self.scale:
            self.kill()
        self.rect.center = (self.x - scroll[0], self.y - scroll[1])
        self.hitbox.center = self.rect.center
        
        
    

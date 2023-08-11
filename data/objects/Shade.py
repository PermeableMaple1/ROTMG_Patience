import pygame
import math

class Shade(pygame.sprite.Sprite):
    
    def __init__(self, scale, FPS, x0, y0):
        super().__init__()
        self.scale = scale
        self.FPS = FPS
        self.x0 = x0
        self.y0 = y0
        self.x = x0
        self.y = y0
        self.animation_count = 0
        self.tiles_per_s = 2
        self.attack_loop_time = 0
        self.total_time = 0
        
        self.shade_sprites = [pygame.image.load('data\images\Shade_Images\shade1.png'),
                              pygame.image.load('data\images\Shade_Images\shade2.png'),
                              pygame.image.load('data\images\Shade_Images\shade3.png'),
                              pygame.image.load('data\images\Shade_Images\shade4.png')]
        
        # self.bullet_group = pygame.sprite.Group()
        # self.bullet_type = cycle([1, 2])
    
    def update(self, display, scroll, clock):
        self.screen_center = display.get_rect().center
        self.total_time += clock.get_time() / 1000
        
        if self.animation_count + 1 >= 36:
            self.animation_count = 0
        self.animation_count += 1
        self.image = self.shade_sprites[self.animation_count//12]
        self.image = pygame.transform.scale_by(self.image, 1.5*self.scale)
        self.rect = self.image.get_rect()
        
        
        self.distance_from_player_x = self.screen_center[0] - self.x + scroll[0]
        self.distance_from_player_y = self.screen_center[1] - self.y + scroll[1]
        self.distance_from_player = math.sqrt(self.distance_from_player_x**2 + self.distance_from_player_y**2)
        self.player_angle = math.atan2(self.distance_from_player_y, self.distance_from_player_x)

        self.distance_from_spawn_x = self.x0 - self.x
        self.distance_from_spawn_y = self.y0 - self.y
        self.distance_from_spawn = math.sqrt(self.distance_from_spawn_x**2 + self.distance_from_spawn_y**2)
        self.spawn_angle = math.atan2(self.distance_from_spawn_y, self.distance_from_spawn_x)

        if self.total_time > 6:
            if self.attack_loop_time < 5:
                if self.distance_from_player <= 13*8*self.scale and self.distance_from_player > self.scale:
                        self.x += (8*self.scale*self.tiles_per_s / self.FPS) * math.cos(self.player_angle)
                        self.y += (8*self.scale*self.tiles_per_s / self.FPS) * math.sin(self.player_angle)
                self.attack_loop_time += clock.get_time() / 1000
            elif self.attack_loop_time < 10:
                if self.distance_from_spawn > self.scale:
                        self.x += (1.5*8*self.scale*self.tiles_per_s / self.FPS) * math.cos(self.spawn_angle)
                        self.y += (1.5*8*self.scale*self.tiles_per_s / self.FPS) * math.sin(self.spawn_angle)
                self.attack_loop_time += clock.get_time() / 1000
            else:
                self.attack_loop_time = 0
        
        self.rect.center = (self.x - scroll[0], self.y - scroll[1])
        
            
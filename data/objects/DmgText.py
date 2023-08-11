import pygame

class DmgText(pygame.sprite.Sprite):
    
    def __init__(self, text, truedmg, scale, FPS, display, istext=False):
        super().__init__()
        
        pygame.font.init()
        self.scale = scale
        self.FPS = FPS
        font = pygame.font.Font('data\images\Pixeloid.ttf', round(4*self.scale))
        
        if istext is False:
            dmgtext = '-'+str(round(text))
        else:
            dmgtext = str(text)
        
        if truedmg:
            color = (248, 0 , 22)
        else:
            color = (121, 14, 232)
            
        self.textimg = font.render(dmgtext, True, color)
        self.outline = font.render(dmgtext, True, (0,0,0))
        
        self.image = pygame.Surface((self.textimg.get_width()+2,self.textimg.get_height()+2),pygame.SRCALPHA)
        
        x = self.image.get_rect().centerx
        y = self.image.get_rect().centery
        self.textimg_rect = self.textimg.get_rect(center=(x,y))
        
        self.outline_rect = self.outline.get_rect(center=(x+2,y))
        self.image.blit(self.outline, self.outline_rect)
        self.outline_rect = self.outline.get_rect(center=(x-2,y))
        self.image.blit(self.outline, self.outline_rect)
        self.outline_rect = self.outline.get_rect(center=(x,y+2))
        self.image.blit(self.outline, self.outline_rect)
        self.outline_rect = self.outline.get_rect(center=(x,y-2))
        self.image.blit(self.outline, self.outline_rect)
        
        self.image.blit(self.textimg, self.textimg_rect)
        
        self.rect = self.image.get_rect(center=display.get_rect().center)
        self.rect.centery -= 4*self.scale
        self.y0 = self.rect.centery
        
        self.lifetime = 0
        
    def update(self):
        a = self.y0 - self.rect.centery
        l = 1.5*8*self.scale
        if a < l:
            self.rect.centery -= 2*8*self.scale/self.FPS
        if self.lifetime >= self.FPS:
            self.kill()
        self.lifetime += 1
        
        
        
    
        
        
        
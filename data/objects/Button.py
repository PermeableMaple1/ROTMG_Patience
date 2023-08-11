import pygame
import itertools

class Button(pygame.sprite.Sprite):
    
    def __init__(self, w, l, x, y, points, stats, stat, direction):
        super().__init__()
        
        self.w = w
        self.l = l
        self.x = x
        self.y = y
        
        self.points = points
        
        self.cursor = False
        self.held_down = False
        self.timer = 0
        self.stats = stats
        self.stat = stat
        self.direction = direction
        self.difficulties = itertools.cycle(['Easy', 'Normal', 'Hard'])
        
    def update(self):
            
        self.image = pygame.Surface((self.w,self.l), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(self.x,self.y))
        
        if self.cursor is True:
            pygame.draw.polygon(self.image, (30,200,30), self.points)
            pygame.draw.polygon(self.image, (0,0,0), self.points, 2)
            self.image = pygame.transform.scale(self.image,(self.w+5,self.l+5))
            self.rect = self.image.get_rect(center=(self.x,self.y))
        else:
            
            pygame.draw.polygon(self.image, (255,255,255), self.points)
            pygame.draw.polygon(self.image, (0,0,0), self.points, 2)
            
    def update_stats(self):
        
        if self.stat == 4:
            if self.direction == 1:
                self.stats[4] = next(self.difficulties)
                return self.stats
            else:
                next(self.difficulties)
                self.stats[4] = next(self.difficulties)
                return self.stats           
        else:
            if self.stat == 3:
                if   3 > (self.stats[self.stat] + self.direction) or (self.stats[self.stat] + self.direction) > 10:
                    return self.stat
                else:
                    self.stats[self.stat] += self.direction
            else:
                self.stats[self.stat] += self.direction
            return self.stats
            
        
        
        

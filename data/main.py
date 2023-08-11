import pygame, sys, random, itertools
from .map.spritesheet import Spritesheet
from .map import tiles
from .objects.Player import Player
from .objects.Shade import Shade
from .objects.Bullet import Bullet
from .objects.DmgText import DmgText
from .objects.Button import Button

class Patience:
    
    Window_width=1200
    Window_height=700
    Window_size = (Window_width, Window_height)

    def __init__(self, spd, health, defence, zoom, FPS, difficulty):
        
        pygame.init()
        self.screen = pygame.display.set_mode(Patience.Window_size)
        self.screen_center = self.screen.get_rect().center
        pygame.display.set_caption("You test the patience of a GOD!")
        self.clock = pygame.time.Clock()
        
        self.stats = [spd, health, defence, zoom, difficulty]
        self.FPS = FPS

        self.pygame_icon = pygame.image.load('data\images\king.png')
        pygame.display.set_icon(self.pygame_icon)
        
        self.tilesheet = Spritesheet('data\images\output_tileset.png')
        
        self.in_menu = True
        self.menu()
        
    def run(self):
        
        while True:
            self.clock.tick(self.FPS)
            self.screen.fill((0,0,0))
            self.total_time += self.clock.get_time() / 1000
            
                    
            keys = pygame.key.get_pressed()
            self.display_scroll = self.player.movement(keys, self.map.tiles, self.player_hitbox, self.display_scroll)
            
            self.screen.blit(self.canvas, (self.bg_offset_x-self.display_scroll[0],self.bg_offset_y-self.display_scroll[1]))
            
            self.player_animation = self.player.animation(keys)
            
            
            if self.bullet_loop_time < 0.25:
                self.bullet_loop_time += self.clock.get_time() / 1000
            else:
                self.bullets()
                self.bullet_loop_time = 0
               
            if self.shade_bullet_loop_time < 3:
                self.shade_bullet_loop_time += self.clock.get_time() / 1000
            else:
                type_ = next(self.shade_bullet_type)
                for shade in self.shade_group:
                    self.shade_bullets(shade.rect.center[0]+self.display_scroll[0], shade.rect.center[1]+self.display_scroll[1], type_)
                self.shade_bullet_loop_time = 0

            self.bullet_group.update(self.display_scroll)
            self.bullet_group.draw(self.screen)
            
            self.player.main(self.screen,self.player_animation)
            
            self.shade_group.update(self.screen, self.display_scroll, self.clock)
            self.shade_group.draw(self.screen)
            
            self.bullet_damage()
            
            self.dmgtext_group.update()
            self.dmgtext_group.draw(self.screen)
            
            self.void_damage()
            
            self.post_time(self.total_time)
            
            for event in pygame.event.get():
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = True
                        self.pause()
                    elif event.key == pygame.K_r:
                        self.load_map()
                    elif event.key == pygame.K_m:
                        self.in_menu = True
                        self.bullet_group.empty()
                        self.player.kill()
                        self.shade_group.empty()
                        self.menu()
            
            if self.player.hp < 0:
                self.dead = True
                self.gameover()
            
                        
            pygame.display.flip()
            
    def load_map(self):
        self.total_time = 0
        self.dead = False
        self.scale = self.stats[3]
        self.difficulty = self.stats[4]
        
        self.map = tiles.TileMap('data\map\The_Shatters.csv', self.tilesheet, self.scale)
        self.canvas = pygame.Surface((280 * self.scale,280 * self.scale))
        self.map.draw_map(self.canvas)
        self.canvas_rect = self.canvas.get_rect()
        self.canvas_rect.centerx = self.screen_center[0]
        self.canvas_rect.centery = self.screen_center[1] - 7*8*self.scale
        self.bg_offset_x = self.canvas_rect[0]
        self.bg_offset_y = self.canvas_rect[1]
        
        self.player = Player(self.scale,self.FPS, self.stats[0], self.stats[1], self.stats[2])
        self.display_scroll = [0,0]
            
        self.shade_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.dmgtext_group = pygame.sprite.Group()
        
        self.bullet_loop_time = 0
        self.shade_bullet_loop_time = 0
        self.shade_bullet_type = itertools.islice(itertools.cycle([1,2]),random.choice([1,2]),None)
        self.void_dmg_loop_time = 0

        self.screen.blit(self.canvas, (self.bg_offset_x,self.bg_offset_y))
        self.player.main(self.screen, self.player.player_sprite)
        
        self.shade1 = Shade(self.scale, self.FPS,
                            self.screen_center[0] - 8.5*8*self.scale, self.screen_center[1])
        self.shade2 = Shade(self.scale, self.FPS,
                            self.screen_center[0] + 8.5*8*self.scale, self.screen_center[1])
        self.shade3 = Shade(self.scale, self.FPS,
                            self.screen_center[0] - 8.5*8*self.scale, self.screen_center[1] - 16.5*8*self.scale)
        self.shade4 = Shade(self.scale, self.FPS,
                            self.screen_center[0] + 8.5*8*self.scale, self.screen_center[1] - 16.5*8*self.scale)
        
        self.shade_group.add(self.shade1,self.shade2,self.shade3,self.shade4)
        
        self.player_hitbox = pygame.Rect((self.screen_center[0]-3*self.scale, self.screen_center[1]-3*self.scale),
                                         (6*self.scale,7*self.scale))
        
        self.void_tiles = []
        self.poop = 0
        for tile in self.map.tiles:
            if tile.type == '1':
                void_water = tile.rect.copy()
                void_water.centerx += self.bg_offset_x
                void_water.centery += self.bg_offset_y
                self.void_tiles.append(void_water)
        
        pygame.display.flip()
        
        self.run()
        
    def bullets(self):
        left = self.screen_center[0] - 8*15*self.scale
        right = self.screen_center[0] + 8*15*self.scale
        top = self.screen_center[1] - 8*22*self.scale
        bottom = self.screen_center[1] + 8*8*self.scale
        sides = [left, right, top, bottom]
        
        if self.difficulty == 'Hard':
            spawns_per_instance = 5
        elif self.difficulty == 'Normal':
            spawns_per_instance = 4
        elif self.difficulty == 'Easy':
            spawns_per_instance = 3
        
        for i in range(spawns_per_instance):
            side = random.choice(range(4))
            if side == 0:
                x = sides[side]
                y = random.randrange(self.screen_center[1]-8*17*self.scale, self.screen_center[1]+8*self.scale, 8*self.scale)
                a = 0
            elif side == 1:
                x = sides[side]
                y = random.randrange(self.screen_center[1]-8*17*self.scale, self.screen_center[1]+8*self.scale, 8*self.scale)
                a = 180
            elif side == 2:
                x = random.randrange(self.screen_center[0]-8*8*self.scale, self.screen_center[0]+8*8*self.scale, 8*self.scale)
                y = sides[side]
                a = 270
            elif side == 3:
                x = random.randrange(self.screen_center[0]-8*8*self.scale, self.screen_center[0]+8*8*self.scale, 8*self.scale)
                y = sides[side]
                a = 90
                
            bullet = Bullet(x, y, a, self.scale, self.FPS, random.choice([3,4]))
            self.bullet_group.add(bullet)
            
    def shade_bullets(self, x, y, type_):
        
        for i in range(16):
            bullet = Bullet(x, y, 22.5*i, self.scale, self.FPS, type_)
            self.bullet_group.add(bullet)
   
    def bullet_damage(self):
    
        for bullet in self.bullet_group:
            if self.player_hitbox.colliderect(bullet.hitbox) and bullet.hit == False:
                self.player.status_effect(bullet.status_effect, bullet.effect_time)
                damage = (bullet.damage - bullet.truedmg*self.player.defence) * self.player.damage_factor
                self.player.hp -= damage
                bullet.hit = True
                dmgtext = DmgText(damage, bullet.truedmg, self.scale, self.FPS, self.screen)
                self.dmgtext_group.add(dmgtext)
                
                # if bullet.status_effect:
                #     effecttxt = DmgText(bullet.status_effect, 1, self.scale, self.FPS, self.screen, True)
                #     self.dmgtext_group.add(effecttxt)
    
    def void_damage(self):
        in_void = []
        for tile in self.void_tiles:
            void_water = pygame.Rect(tile.left-self.display_scroll[0], tile.top-self.display_scroll[1], tile.width, tile.height)
            in_void.append(void_water.collidepoint(self.screen_center[0], self.player_hitbox.bottom))
        if any(in_void):   
            self.player.in_void = True
            if self.void_dmg_loop_time == 0 or self.void_dmg_loop_time > 0.5:
                dmgtxt = DmgText(75, 0, self.scale, self.FPS, self.screen)
                self.dmgtext_group.add(dmgtxt)
                self.void_dmg_loop_time = 0
            self.void_dmg_loop_time += self.clock.get_time() / 1000
        else:
            self.player.in_void = False
            self.void_dmg_loop_time = 0
    
    def pause(self):
        pygame.font.init()
        
        largetext = pygame.font.Font('data\images\Pixeloid.ttf', round(10*self.scale))
        img = largetext.render('Paused', True, (255,255,255))
        img_rect = img.get_rect()
        img_rect.center = self.screen_center
        bg = pygame.Surface(self.screen.get_rect()[2:4])
        bg.set_alpha(128)
        bg.fill((25,25,25))
        self.screen.blit(bg, (0,0))
        self.screen.blit(img, img_rect)
        pygame.display.flip()
        
        while self.paused:
            
            for event in pygame.event.get():  
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_p:
                        self.paused = False
                        
    def gameover(self):
        
        pygame.font.init()
        
        largetext = pygame.font.Font('data\images\Pixeloid.ttf', round(10*self.scale))
        smalltext = pygame.font.Font('data\images\Pixeloid.ttf', round(5*self.scale))
        
        img = largetext.render('You died!', True, (248,0,22))
        img_rect = img.get_rect()
        img_rect.center = self.screen_center
        
        img2 = smalltext.render('Press \"r\" to try again.', True, (255,255,255))
        img2_rect = img.get_rect()
        img2_rect.centerx = self.screen_center[0] - 7*self.scale
        img2_rect.centery = self.screen_center[1] + 25*self.scale
        
        bg = pygame.Surface(self.screen.get_rect()[2:4])
        bg.set_alpha(128)
        bg.fill((25,25,25))
        self.screen.blit(bg, (0,0))
        self.screen.blit(img, img_rect)
        self.screen.blit(img2, img2_rect)
        pygame.display.flip()
        
        while self.dead:
            
            for event in pygame.event.get():  
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.load_map()
                    elif event.key == pygame.K_m:
                        self.in_menu = True
                        self.bullet_group.empty()
                        self.player.kill()
                        self.shade_group.empty()
                        self.menu()
                    
    def menu(self):
        def create_text(text, border, size, color):
            pygame.font.init()
            font = pygame.font.Font('data\images\Pixeloid.ttf', size)
            text_img = font.render(text, True, color).convert_alpha()
            outline = font.render(text, True, (0,0,0)).convert_alpha()

            img = pygame.Surface((text_img.get_width()+border,text_img.get_height()+border),pygame.SRCALPHA)
            x = img.get_rect().centerx
            y = img.get_rect().centery
            text_rect = text_img.get_rect(center=(x,y))
            
            outline_rect = outline.get_rect(center=(x+border,y))
            img.blit(outline, outline_rect)
            outline_rect = outline.get_rect(center=(x-border,y))
            img.blit(outline, outline_rect)
            outline_rect = outline.get_rect(center=(x,y+border))
            img.blit(outline, outline_rect)
            outline_rect = outline.get_rect(center=(x,y-border))
            img.blit(outline, outline_rect)
            img.blit(text_img, text_rect)
            return img
        
        title_img = create_text('You Test the Patience of a GOD!',3, 50, (255,255,255))
        subtitle = create_text('Press Space to Begin', 2, 25, (255,255,255))
        hp_stat = create_text(str(self.stats[1])+' HP', 2, 25, (50,206,212))
        def_stat = create_text(str(self.stats[2])+' DEF', 2, 25, (85,85,85))
        spd_stat = create_text(str(self.stats[0])+' SPD', 2, 25, (43,207,106))
        zoom_stat = create_text('Zoom: '+str(self.stats[3]), 2, 25, (255,255,255))
        diff_stat = create_text('Difficulty: '+self.stats[4], 2, 25, (255,255,255))
        button_group = pygame.sprite.Group()
        tri1 = ((0,12.5),(25,0),(25,25))
        tri2 = ((0,0),(0,25),(25,12.5))
        
        hp_stat_rect = hp_stat.get_rect(center = (self.screen_center[0]-200,self.screen_center[1]+100))
        hp_button1 = Button(25,25, hp_stat_rect.centerx - 100, hp_stat_rect.centery, tri1, self.stats, 1, -1)
        hp_button2 = Button(25,25, hp_stat_rect.centerx + 100, hp_stat_rect.centery, tri2, self.stats, 1, 1)
        button_group.add(hp_button1,hp_button2)
        
        def_stat_rect = def_stat.get_rect(center = (self.screen_center[0]-200,self.screen_center[1]+200))
        def_button1 = Button(25,25, def_stat_rect.centerx - 100, def_stat_rect.centery, tri1, self.stats, 2, -1)
        def_button2 = Button(25,25, def_stat_rect.centerx + 100, def_stat_rect.centery, tri2, self.stats, 2, 1)
        button_group.add(def_button1,def_button2)
  
        spd_stat_rect = spd_stat.get_rect(center = (self.screen_center[0]+200,self.screen_center[1]+100))
        spd_button1 = Button(25,25, spd_stat_rect.centerx - 100, spd_stat_rect.centery, tri1, self.stats, 0, -1)
        spd_button2 = Button(25,25, spd_stat_rect.centerx + 100, spd_stat_rect.centery, tri2, self.stats, 0, 1)
        button_group.add(spd_button1,spd_button2)
  
        zoom_stat_rect = zoom_stat.get_rect(center = (self.screen_center[0]+200,self.screen_center[1]+200))
        zoom_button1 = Button(25,25, zoom_stat_rect.centerx - 100, zoom_stat_rect.centery, tri1, self.stats, 3, -1)
        zoom_button2 = Button(25,25, zoom_stat_rect.centerx + 100, zoom_stat_rect.centery, tri2, self.stats, 3, 1)
        button_group.add(zoom_button1,zoom_button2)
        
        diff_stat_rect = diff_stat.get_rect(center = (self.screen_center[0],self.screen_center[1]+150))
        diff_button1 = Button(25,25, diff_stat_rect.left - 60, diff_stat_rect.centery, tri1, self.stats, 4, -1)
        diff_button2 = Button(25,25, diff_stat_rect.right + 60, diff_stat_rect.centery, tri2, self.stats, 4, 1)
        button_group.add(diff_button1,diff_button2)
        
        king_animation = pygame.image.load('data\images\menu_animation.png').convert_alpha()
        animation_count = 0
        frame_width = 222
        frame_height = frame_width
        
        self.map = tiles.TileMap('data\map\The_Shatters.csv', self.tilesheet, 5)
        menu_bg = pygame.Surface((280 * 5,280 * 5))
        self.map.draw_map(menu_bg)
        menu_bg_rect = menu_bg.get_rect()
        menu_bg_rect.centerx = self.screen_center[0]
        menu_bg_rect.centery = self.screen_center[1]
        
        while self.in_menu:
            self.clock.tick(self.FPS)
            
            self.screen.fill((0,0,0))     
            self.screen.blit(menu_bg, menu_bg_rect)
            
            if animation_count + 1 > 65*8:
                animation_count = 57*8
            frame_no = animation_count//8
            frame = pygame.Rect(frame_width*(frame_no%5), frame_height*(frame_no//5), frame_width,frame_height)

            img = pygame.Surface((frame_width,frame_height), pygame.SRCALPHA)
            img.blit(king_animation, (0,0), frame)
            
            img_rect = img.get_rect(center=self.screen_center)
            img_rect.centery -= 200
                
            self.screen.blit(img, img_rect)
            self.screen.blit(title_img, title_img.get_rect(center=self.screen_center))
            self.screen.blit(subtitle, subtitle.get_rect(center = (self.screen_center[0],self.screen_center[1]+300)))
            
            hp_stat = create_text(str(self.stats[1])+' HP', 2, 25, (50,206,212))
            def_stat = create_text(str(self.stats[2])+' DEF', 2, 25, (85,85,85))
            spd_stat = create_text(str(self.stats[0])+' SPD', 2, 25, (43,207,106))
            zoom_stat = create_text('Zoom: '+str(self.stats[3]), 2, 25, (255,255,255))
            diff_stat = create_text('Difficulty: '+self.stats[4], 2, 25, (255,255,255))
            self.screen.blit(hp_stat, hp_stat_rect)
            self.screen.blit(def_stat, def_stat_rect)            
            self.screen.blit(spd_stat, spd_stat_rect)
            self.screen.blit(zoom_stat, zoom_stat_rect)
            self.screen.blit(diff_stat, diff_stat_rect)
             
            animation_count += 1
            
            mouse = pygame.mouse.get_pos()
            
            button_group.update()
            button_group.draw(self.screen)
            
            
            for event in pygame.event.get():  
                
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        button_group.empty()
                        self.load_map()
                
                for button in button_group:
                    if button.rect.collidepoint(mouse):
                        button.cursor = True
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            button.update_stats()
                            button.held_down = True
                        elif event.type == pygame.MOUSEBUTTONUP:
                            button.held_down = False
                            button.timer = 0
                    else:
                        button.cursor = False
            for button in button_group:
                if button.held_down:
                    button.timer += 1/self.FPS
                    if button.timer > 1:
                        button.update_stats()
                    
            pygame.display.flip()
            
    
    def post_time(self, total_time):
        pygame.font.init()
        total_time = round(total_time,2)
        
        text = pygame.font.Font('data\images\Pixeloid.ttf', round(3*self.scale))
        
        img = text.render(str(total_time)+'s', True, (255,255,255))
        img_rect = img.get_rect()
        img_rect.top =  self.scale
        img_rect.left =  self.scale
        
        self.screen.blit(img, img_rect)
            
        
        

            

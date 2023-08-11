import pygame, csv, os

tileset = {'1':'A2.png','2':'A3.png','3':'A4.png','4':'A5.png',
           '5':'A6.png','6':'B1.png','7':'B2.png','8':'B3.png',
           '9':'B4.png','10':'B5.png','11':'B6.png','12':'C1.png',
           '13':'C2.png','14':'C3.png','15':'C4.png','16':'C5.png',
           '17':'C6.png','18':'D1.png','19':'D2.png','20':'D3.png',
           '21':'D4.png','22':'D5.png','23':'D6.png','24':'E1.png',
           '25':'E2.png','26':'E3.png','27':'E4.png','28':'E5.png',
           '29':'E6.png','30':'F1.png'}

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet, scale, _type):
        pygame.sprite.Sprite.__init__(self)
        self.type = _type
        self.image = spritesheet.parse_sprite(image)
        self.image = pygame.transform.scale_by(self.image, scale)
        # Manual load in: self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet, scale):
        self.scale = scale
        self.tile_size = 8 * self.scale
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    def read_csv(self, filename):
        map = []
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        return map

    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        for row in map:
            x = 0
            for tile in row:
                tiles.append(Tile(tileset[tile], x * self.tile_size, y * self.tile_size, self.spritesheet, self.scale, tile))
                    # Move to next tile in current row
                x += 1
            # Move to next row
            y += 1
            # Store the size of the tile map
        self.map_w, self.map_h = self.scale * x * self.tile_size, self.scale * y * self.tile_size
        return tiles











import pygame 

class World():
    # def __init__(self, data, tile_size):
    def __init__(self, screen_configs):
        
        self.screen_configs = screen_configs
        self.tile_list = []

        #load images 
        dirt_img = pygame.image.load(self.screen_configs.get("images").get("dirt")) 
        grass_img = pygame.image.load(self.screen_configs.get("images").get("grass")) 
        
        row_count = 0
        for row in self.screen_configs.get("world_data"): 
            col_count = 0
            for tile in row: 
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (self.screen_configs.get("tile_size"), self.screen_configs.get("tile_size")))
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * self.screen_configs.get("tile_size")
                    img_rect.y = row_count * self.screen_configs.get("tile_size")
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (self.screen_configs.get("tile_size"), self.screen_configs.get("tile_size")))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * self.screen_configs.get("tile_size")
                    img_rect.y = row_count * self.screen_configs.get("tile_size")
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)
                     
                col_count += 1
            row_count += 1

    def draw_backgroung(self, screen):
        screen.blit(pygame.image.load(self.screen_configs.get("images").get("sky")) , (0,0))
        screen.blit(pygame.image.load(self.screen_configs.get("images").get("sun")) , (100,100))
        
    def draw_grid(self, screen):
        for line in range(0, int(self.screen_configs.get("screen_width")/self.screen_configs.get("tile_size"))):
            pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(0, line * self.screen_configs.get("tile_size")), end_pos=(self.screen_configs.get("screen_width"), line * self.screen_configs.get("tile_size")), width=1)
            pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(line * self.screen_configs.get("tile_size"), 0), end_pos=(line * self.screen_configs.get("tile_size"), self.screen_configs.get("screen_height")), width=1)
          
    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])
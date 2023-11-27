import pygame 
from modules.enemies.blob import Blob
from modules.enemies.lava import Lava
from modules.exit import Exit
from modules.coin import Coin
from modules.font import Font
from modules.platform import Platform

class World():
    def __init__(self, screen_configs, enemy_configs, 
                 enemy_sprite_group, exit_configs, exit_group, 
                 coin_group, platform_group, current_level, coin_path_image):
        
        self.screen_configs = screen_configs
        self.tile_list = []
        
        score_coin = Coin(coin_path_image, 7, 7, 40) # coin para el score arriba a la izquierda
        coin_group.add(score_coin) 
        
        self.tile_size = self.screen_configs.get("tile_size") # lado de las baldozas (son cuadradas)

        row_count = 0
        for row in self.screen_configs.get("levels").get(str(current_level)): 
            col_count = 0
            for tile in row: 

                coord_x = col_count * self.tile_size
                coord_y = row_count * self.tile_size

                if tile == 1: # dirt
                    dirt_img = pygame.image.load(self.screen_configs.get("images").get("dirt")) 
                    img = pygame.transform.scale(dirt_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect() 
                    img_rect.x = col_count * img_rect.width
                    img_rect.y = row_count * img_rect.height
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)

                elif tile == 2: # grass
                    grass_img = pygame.image.load(self.screen_configs.get("images").get("grass")) 
                    img = pygame.transform.scale(grass_img, (self.tile_size, self.tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * img_rect.width
                    img_rect.y = row_count * img_rect.height
                    tile = (img, img_rect) 
                    self.tile_list.append(tile)
                
                elif tile == 3: # blob
                    blob_path_image = enemy_configs.get("blob").get("path_image")
                    enemy = Blob(blob_path_image, coord_x, coord_y, self.tile_size)
                    enemy_sprite_group.add(enemy)

                elif tile == 4: # plataformas con movimiento en eje X 
                    platform_path_image = self.screen_configs.get("images").get("platform") 
                    platform = Platform(platform_path_image, coord_x, coord_y, self.tile_size, 1, 0)
                    platform_group.add(platform)

                elif tile == 5: # plataformas con movimiento en eje Y 
                    platform_path_image = self.screen_configs.get("images").get("platform") 
                    platform = Platform(platform_path_image, coord_x, coord_y, self.tile_size, 0, 1)
                    platform_group.add(platform)

                elif tile == 6: # lava
                    lava_path_image = enemy_configs.get("lava").get("path_image")
                    lava = Lava(lava_path_image, coord_x, coord_y, self.tile_size)
                    enemy_sprite_group.add(lava)
                
                elif tile == 7: # coins
                    coin = Coin(coin_path_image, coord_x, coord_y, self.tile_size)
                    coin_group.add(coin)

                elif tile == 8: # exit door
                    exit_path_image = exit_configs.get("path_image")
                    exit = Exit(exit_path_image, coord_x, coord_y, self.tile_size)
                    exit_group.add(exit)
                    
                col_count += 1
            row_count += 1
        
    def draw_grid(self, screen):
        for line in range(0, int(self.screen_configs.get("screen_width")/self.tile_size)):
            pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(0, line * self.tile_size), end_pos=(self.screen_configs.get("screen_width"), line * self.tile_size), width=1)
            pygame.draw.line(surface=screen, color=(255, 255, 255), start_pos=(line * self.tile_size, 0), end_pos=(line * self.tile_size, self.screen_configs.get("screen_height")), width=1)
          
    def draw(self, screen):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

    def reset_level(self, screen_configs, enemy_configs, enemy_sprite_group, \
                    exit_configs, exit_group, coin_group, platform_group, current_level, coin_path_image):
        # nueva instancia de World con el mapa del nivel que corresponda
        world = World(screen_configs, enemy_configs, enemy_sprite_group, 
                      exit_configs, exit_group, coin_group, platform_group, current_level,
                      coin_path_image) 
        return world
     
    def draw_text(self, screen, text_info: tuple):

        tipo_texto_a_imprimir = text_info[0] # score|game_over|you_win

        informacion_texto = self.screen_configs.get("texts").get(text_info[0])

        if tipo_texto_a_imprimir == "score":
            score = text_info[1] 
            texto_a_imprimir = informacion_texto.get('text').format(str(score))
        else:
            texto_a_imprimir = informacion_texto.get('text')

        tipo_fuente = informacion_texto.get('font')
        tamanio_fuente = informacion_texto.get('size')
        color = eval(informacion_texto.get('color'))
        x = informacion_texto.get('coord_x')
        y = informacion_texto.get('coord_y')

        instancia_Font = Font(tipo_fuente, tamanio_fuente)
        superficie = instancia_Font.surface_text

        img = superficie.render(texto_a_imprimir, True, color) # antialias = True
        
        screen.blit(img, (x,y))

    @staticmethod
    def inicializar_sonidos():
        pygame.mixer.music.load("assets/sounds/music.wav")
        pygame.mixer.music.play(-1, 0.0, 5000) 
        # param == 5000 -> volumen musica de fondo in crescendo durante 5 segs hasta llegar al 100% del volumen seteado
        pygame.mixer.music.set_volume(0.025)
    
        coin_fx = pygame.mixer.Sound("assets/sounds/coin.wav")
        coin_fx.set_volume(0.05)
        jump_fx = pygame.mixer.Sound("assets/sounds/jump.wav")
        jump_fx.set_volume(0.05)
        game_over_fx = pygame.mixer.Sound("assets/sounds/game_over.wav")
        game_over_fx.set_volume(0.05)
        return (coin_fx, jump_fx, game_over_fx)
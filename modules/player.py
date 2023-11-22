import pygame 

class Player():
    
    def __init__(self, player_configs: dict):
        self.reset(player_configs)

    def update(self, screen, screen_height, tile_list: list[tuple], game_over):
        
        dx = 0
        dy = 0

        walk_cooldown = self.player_configs.get("animation").get("walk_cooldown") # 5
        
        if game_over == 0:
            key = pygame.key.get_pressed() # get kypresses

            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = self.player_configs.get("animation").get("vel_y") # -15
                self.jumped = True
            if key[pygame.K_SPACE] == False:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= self.player_configs.get("animation").get("dx") # 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += self.player_configs.get("animation").get("dx") # 5
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1: # player moving to the right
                    self.image = self.images_right[self.index]
                if self.direction == -1: # player moving to the right
                    self.image = self.images_left[self.index]

            # handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right) - 1:
                    self.index = 0
                if self.direction == 1: # player moving to the right
                    self.image = self.images_right[self.index]
                if self.direction == -1: # player moving to the right
                    self.image = self.images_left[self.index]
                # self.image = self.images_right[self.index]
                
            # add gravity 
            self.vel_y += 1 # -14|-13|-12...9|10|10|10
            if self.vel_y > 10:
                self.vel_y = 10

            dy += self.vel_y
            
            # check for collision
            self.in_air = True
            for tile in tile_list: 

                # check for collision in x direction 
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height): # dx = +/-5 or 0
                    dx = 0

                # if tile[1].colliderect(self.rect): 
                # tile == (<Surface(50x50x24 SW)>, <rect(400, 900, 50, 50)>)
                # check for collision in y direction 
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height): 
                    # check if below the ground i.e jumping 
                    # self.vel_y toma valores entre de entr -14 y 1 (durante la curva de un salto), y de entre 0 y 10 con  el player en reposo
                    if self.vel_y < 0: # el player esta durante la curva de un salto, entonces la colision es entre rl bottom del tile y el top del player
                        dy = tile[1].bottom - self.rect.top # 0
                        self.vel_y = 0
                    # check if above the ground i.e falling
                    elif self.vel_y >= 0: # el player esta en reposo, entonces la colision es entre el bottom del player y el top del tile
                        dy = tile[1].top - self.rect.bottom # 0
                        self.vel_y = 0
                        self.in_air = False

            # update rect player coordinates
            self.rect.x += dx # +/-5 or 0
            self.rect.y += dy 

        # el player perdio la vida, animacion del fantasma subiendo
        if game_over == -1:
            self.image = self.dead_image
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect) # draw player onto screen    
        pygame.draw.rect(screen, (255,0,0), self.rect, 2)

        # print(self.vel_y, self.rect.y)
        # self.rect.y when start the game vvv
        # self.vel_y=1 self.rect.y=871
        # self.vel_y=2 self.rect.y=873
        # self.vel_y=3 self.rect.y=876
        # self.vel_y=4 self.rect.y=880
        # self.vel_y=5 self.rect.y=885
        # self.vel_y=6 self.rect.y=891
        # self.vel_y=7 self.rect.y=898
        # self.vel_y=8 self.rect.y=906
        # self.vel_y=9 self.rect.y=915
        # self.vel_y=10 self.rect.y=920...
        
        # self.rect.y when player jump vvv
        # self.vel_y=-14 self.rect.y=906 UP
        # self.vel_y=-13 self.rect.y=893 UP
        # self.vel_y=-12 self.rect.y=881 UP
        # self.vel_y=-11 self.rect.y=870 UP
        # self.vel_y=-10 self.rect.y=860 UP
        # self.vel_y=-9 self.rect.y=851 UP
        # self.vel_y=-8 self.rect.y=843 UP
        # self.vel_y=-7 self.rect.y=836 UP
        # self.vel_y=-6 self.rect.y=830 UP
        # self.vel_y=-5 self.rect.y=825 UP
        # self.vel_y=-4 self.rect.y=821 UP
        # self.vel_y=-3 self.rect.y=818 UP
        # self.vel_y=-2 self.rect.y=816 UP
        # self.vel_y=-1 self.rect.y=815 UP
        # self.vel_y=0 self.rect.y=815 -
        # self.vel_y=1 self.rect.y=816 DOWN
        # self.vel_y=2 self.rect.y=818 DOWN
        # self.vel_y=3 self.rect.y=821 DOWN
        # self.vel_y=4 self.rect.y=825 DOWN
        # self.vel_y=5 self.rect.y=830 DOWN
        # self.vel_y=6 self.rect.y=836 DOWN
        # self.vel_y=7 self.rect.y=843 DOWN
        # self.vel_y=8 self.rect.y=851 DOWN
        # self.vel_y=9 self.rect.y=860 DOWN
        # self.vel_y=10 self.rect.y=870 DOWN
        # self.vel_y=10 self.rect.y=880 DOWN
        # self.vel_y=10 self.rect.y=890 DOWN
        # self.vel_y=10 self.rect.y=900 DOWN
        # self.vel_y=10 self.rect.y=910 DOWN
        # self.vel_y=10 self.rect.y=920...

    def reset(self, player_configs: dict):
        self.player_configs = player_configs
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0 # frames counter
        for num in range(1,5):
            img_right = pygame.image.load(f"img/guy{num}.png")
            img_right = pygame.transform.scale(img_right, (self.player_configs.get("rect_width"), self.player_configs.get("rect_height")))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load(self.player_configs.get("dead_image"))
        self.image = self.images_right[self.index]     
        self.rect = self.image.get_rect()
        self.rect.x = player_configs.get("coord_x") # 100
        self.rect.y = player_configs.get("coord_y") # 870
        self.width = self.rect.width 
        self.height = self.rect.height 
        self.vel_y = 0
        self.jumped = False
        self.direction = 0    
        self.in_air = True   
import pygame 

class Player():
    
    def __init__(self, player_configs: dict):
        self.initialize(player_configs)

    def update(self, screen, tile_list: list[tuple], player_status, jump_fx, platform_group, dead_value, playing_value):
        
        delta_x = 0
        delta_y = 0
        velocity_animation = self.player_configs.get("animation_settings").get("velocity_animation") 
        col_thresh = 20 # useful in collision with platforms in Y
        
        if player_status == playing_value:
            key = pygame.key.get_pressed()

            if key[pygame.K_SPACE] and self.jumped == False and self.in_air == False:
                self.vel_y = self.player_configs.get("animation_settings").get("jumping_capacity")
                self.jumped = True
                jump_fx.play()
            if key[pygame.K_SPACE] == False: 
                self.jumped = False # ready to the next jump
            if key[pygame.K_LEFT]:
                delta_x -= self.player_configs.get("animation_settings").get("velocity_x") 
                self.frames_in_movement_x += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                delta_x += self.player_configs.get("animation_settings").get("velocity_x") 
                self.frames_in_movement_x += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.frames_in_movement_x = 0
                self.index = 0
                if self.direction == 1: # player was moving to the right
                    self.image = self.images_right[self.index]
                if self.direction == -1: # player was moving to the left
                    self.image = self.images_left[self.index]

            # handle velocity of animation
            if self.frames_in_movement_x > velocity_animation: # player is moving
                self.frames_in_movement_x = 0
                self.index += 1
                if self.index >= len(self.images_right) - 1:
                    self.index = 0
                if self.direction == 1: # player is moving to the right
                    self.image = self.images_right[self.index]
                if self.direction == -1: # player is moving to the right
                    self.image = self.images_left[self.index]
                
            # add gravity 
            self.vel_y += 1 # -14|-13|-12...9|10|10|10
            if self.vel_y > 10:
                self.vel_y = 10

            delta_y += self.vel_y
            
            # check for collision with tiles
            self.in_air = True
            for tile in tile_list: # tile == (<Surface(50x50x24 SW)>, <rect(coord_x, coord_y, width, hright)>)

                # check for collision in x direction 
                if tile[1].colliderect(self.rect.x + delta_x, self.rect.y, self.width, self.height): 
                    delta_x = 0

                # check for collision in y direction 
                if tile[1].colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height): 
                    # check if player is below the tile 
                    # self.vel_y toma valores entre de entre -14 y 1 cuando el player esta en el aire (durante un salto)
                    # si la colision se da en ese momento, entonces la colision es entre el bottom del tile y el top del player
                    if self.vel_y < 0: 
                        delta_y = tile[1].bottom - self.rect.top
                        self.vel_y = 0

                    # check if player is above the tile 
                    # self.vel_y toma valores entre entre 0 y 10 con el player en reposo
                    # si la colision se da en ese momento, entonces la colision es entre el bottom del player y el top del tile (player parado)
                    elif self.vel_y >= 0: 
                        delta_y = tile[1].top - self.rect.bottom 
                        self.vel_y = 0
                        self.in_air = False # habilito que el player pueda volver a saltar una vez parado 

            # check for collision with platform
            for platform in platform_group:

                # check for collision in x direction 
                if platform.rect.colliderect(self.rect.x + delta_x, self.rect.y, self.width, self.height):
                    delta_x = 0
                
                # check for collision in y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + delta_y, self.width, self.height):
                    # hubo colision entre el player y alguna de las plataformas por arriba o por abajo

                    # check if player is below platform 
                    if abs((self.rect.top + delta_y) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        delta_y = platform.rect.bottom - self.rect.top

                    # check if player is above platform 
                    elif abs((self.rect.bottom + delta_y) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1 
                        delta_y = 0
                        self.in_air = False # habilito que el player pueda volver a saltar ya que esta parado 

                    # el player parado en una plataforma se mueve en el eje x junto a la plataforma en la que esta parado
                    if platform.move_x: # move_x = 1 indicate an x direction plataform moving 
                        self.rect.x += platform.move_direction 
                        # move_direction = 1 indicate platform moving to right
                        # = -1 platform moving to left

            # update rect player coordinates
            self.rect.x += delta_x 
            self.rect.y += delta_y 

        # el player perdio la vida, animacion del fantasma subiendo
        if player_status == dead_value:
            self.image = self.dead_image
            if self.rect.y > -50:
                self.rect.y -= 5

        screen.blit(self.image, self.rect) # draw player onto screen    
        # pygame.draw.rect(screen, (255,0,0), self.rect, 2)

    def initialize(self, player_configs: dict):

        self.player_configs = player_configs
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.frames_in_movement_x = 0

        first_sprite = self.player_configs.get("animation_settings").get("first_sprite")
        total_sprites = self.player_configs.get("animation_settings").get("total_sprites")

        for num_sprite in range(first_sprite, total_sprites + 1):

            img_right = pygame.image.load(player_configs.get("image_settings").get("path_main_image").format(num_sprite))

            img_right = pygame.transform.scale(img_right, (self.player_configs.get("image_settings").get("width"), self.player_configs.get("image_settings").get("height")))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load(self.player_configs.get("image_settings").get("path_dead_image"))
        self.image = self.images_right[self.index]     
        self.rect = self.image.get_rect()
        self.rect.x = player_configs.get("image_settings").get("initial_coord_x") 
        self.rect.y = player_configs.get("image_settings").get("initial_coord_y") 
        self.width = self.rect.width 
        self.height = self.rect.height 
        self.vel_y = 0
        self.jumped = False
        self.direction = 0    
        self.in_air = True   
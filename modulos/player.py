import pygame 

class Player():
    def __init__(self, player_configs: dict):
        self.player_configs = player_configs
        print()
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1,5):
            img_right = pygame.image.load(f"img/guy{num}.png")
            img_right = pygame.transform.scale(img_right, (self.player_configs.get("rect_width"), self.player_configs.get("rect_height")))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.image = self.images_right[self.index]     
        self.rect = self.image.get_rect()
        self.rect.x = player_configs.get("coord_x")
        self.rect.y = player_configs.get("coord_y")
        self.vel_y = 0
        self.jumped = False
        self.direction = 0

    def update(self, screen, screen_height):
        dx = 0
        dy = 0
        walk_cooldown = self.player_configs.get("animation").get("walk_cooldown")
        
        key = pygame.key.get_pressed() # get kypresses

        if key[pygame.K_SPACE] and self.jumped == False:
            self.vel_y = self.player_configs.get("animation").get("vel_y")
            self.jumped = True
        if key[pygame.K_SPACE] == False:
            self.jumped = False
        if key[pygame.K_LEFT]:
            dx -= self.player_configs.get("animation").get("dx")
            self.counter += 1
            self.direction = -1
        if key[pygame.K_RIGHT]:
            dx += self.player_configs.get("animation").get("dx")
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
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10

        dy += self.vel_y

        # update player coordinates
        self.rect.x += dx 
        self.rect.y += dy 

        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height
            dy = 0

        screen.blit(self.image, self.rect) # draw player onto screen
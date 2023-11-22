import pygame 

class Button():
    def __init__(self, config_button):
        
        print(config_button)
        
        self.image = pygame.image.load(config_button.get("path_image"))
        self.rect = self.image.get_rect()
        self.rect.x = config_button.get("coord_x")
        self.rect.y = config_button.get("coord_y")
        self.clicked = False

    def draw(self, screen):
        """  
        verifica si el usuario hace click sobre el boton restart cuando el player pierde una vida\n
        en base a eso setea en True o False self.clicked
        """
        
        action =  False

        # get mouse position
        pos = pygame.mouse.get_pos()

        # collidepoint() -> metodo de la clase Rect que nos indica si el mouse pasa por encima de un objeto Rect
        # check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            # pygame.mouse.get_pressed() -> (bool, bool, bool) -> tupla que nos indica si alguno de los 3 botones del mouse esta presionado
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                action = True
                self.clicked = True

            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False

        # draw button
        screen.blit(self.image, self.rect)

        return action
import pygame 

class Font():
    def __init__(self, font, size):
        self.surface_text = pygame.font.SysFont(font, size)
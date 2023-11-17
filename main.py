import pygame 
from pygame.locals import * 
from auxiliar import *
from variables import *
from modulos.world import World
from modulos.player import Player

limpiar_consola()

pygame.init()

configs = open_configs()

clock = pygame.time.Clock()

screen_dimentions = (configs.get("screen").get("screen_width"), configs.get("screen").get("screen_height"))
screen = pygame.display.set_mode(screen_dimentions)
pygame.display.set_caption("UTN - Programacion 1 - TP Final")

# load images 
# sun_img = pygame.image.load(configs.get("screen").get("images").get("sky"))
sun_img = pygame.image.load("img/sun.png")
bg_img = pygame.image.load("img/sky.png")

player = Player(configs.get("player1"))
world = World(configs.get("screen"))

run = True
while run:

    clock.tick(configs.get("fps"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))
    # world.draw_backgroung()
    
    world.draw(screen)

    player.update(screen, configs.get("screen").get("screen_height"))

    world.draw_grid(screen)

    pygame.display.update()

pygame.quit()
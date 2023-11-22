import pygame 
from pygame.locals import * 
from auxiliar import *
from variables import *

from modules.player import Player
from modules.world import World
from modules.button import Button


limpiar_consola()

pygame.init()

configs = open_configs()

clock = pygame.time.Clock()

screen_dimentions = (configs.get("screen").get("screen_width"), configs.get("screen").get("screen_height"))
screen = pygame.display.set_mode(screen_dimentions)
pygame.display.set_caption("UTN - PROOGRAMACION I - TP FINAL")

# game variables
game_over = 0
main_menu = True

# load images 
# sun_img = pygame.image.load(configs.get("screen").get("images").get("sky"))
sun_img = pygame.image.load("img/sun.png")
bg_img = pygame.image.load("img/sky.png")

player = Player(configs.get("player1"))

enemies_group = pygame.sprite.Group()

world = World(configs.get("screen"), 
              configs.get("enemies"), 
              enemy_sprite_group=enemies_group)

print(enemies_group)

# create buttons 
restart_button = Button(configs.get("buttons").get("restart"))
start_button = Button(configs.get("buttons").get("start"))
exit_button = Button(configs.get("buttons").get("exit"))

run = True
while run:

    clock.tick(configs.get("fps"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == \
            pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    screen.blit(bg_img, (0,0))
    screen.blit(sun_img, (100,100))
    # world.draw_backgroung(screen)
    
    world.draw(screen)

    if main_menu == True:
        if start_button.draw(screen):
            main_menu = False
        if exit_button.draw(screen):
            run = False
    else:
        

        if game_over == 0:
            enemies_group.update()
            
        # .draw -> metodo de la clase Group para blitear los elementos de un objeto de tipo Group (sprites)
        enemies_group.draw(screen)

        # check for collision with enemies
        if pygame.sprite.spritecollide(player, enemies_group, False):
            game_over = -1
        
        # if player has died
        if game_over == -1:
            if restart_button.draw(screen):
                player.reset(configs.get("player1"))
                game_over = 0

        player.update(screen, configs.get("screen").get("screen_height"), tile_list = world.tile_list, game_over=game_over)


    world.draw_grid(screen)

    pygame.display.update()

pygame.quit()

# cd /Users/User/Desktop/utn/cuatrimestre1/programacion_1/PYGAME_PRACTICAS/4.juego_tipo_mario/video8/video_08_POO
# python main.py
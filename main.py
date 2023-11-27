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

screen_dimentions = (configs.get("screen").get("screen_width"), 
                     configs.get("screen").get("screen_height"))

screen = pygame.display.set_mode(screen_dimentions)
pygame.display.set_caption("UTN - PROOGRAMACION I - TP FINAL")

fps, initial_level, initial_score, max_levels, player_dead, player_win, playing, step_add_level = configs.get("game_variables").values()

# define game variables
main_menu = True
current_level = initial_level
score = initial_score
player_status = playing

background_image_path, background_image_coord_x, background_image_coord_y = configs.get("screen").get("images").get("background_image").values()
background_surface = pygame.image.load(background_image_path)

sun_img_path, sun_img_coord_x, sun_img_coord_y = configs.get("screen").get("images").get("sun").values()
sun_surface = pygame.image.load(sun_img_path)

player = Player(configs.get("player"))

enemies_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()

world = World(configs.get("screen"), configs.get("enemies"), enemy_sprite_group=enemies_group,
              exit_configs=configs.get("exit"), exit_group=exit_group, coin_group=coin_group,
              platform_group=platform_group, current_level=current_level,
              coin_path_image=configs.get("coins").get("path_image"))

# create buttons 
restart_button = Button(configs.get("buttons").get("restart"))
start_button = Button(configs.get("buttons").get("start"))
exit_button = Button(configs.get("buttons").get("exit"))

coin_fx, jump_fx, game_over_fx = World.inicializar_sonidos()

run = True

while run:
    
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == \
            pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            run = False

    screen.blit(background_surface, (background_image_coord_x, background_image_coord_y))
    screen.blit(sun_surface, (sun_img_coord_x, sun_img_coord_y))
    
    if main_menu == True:
        if start_button.draw(screen):
            main_menu = False
        if exit_button.draw(screen):
            run = False
    else:

        world.draw(screen)

        # group.draw() -> metodo de la clase Group para blitear sprites de un grupo instancia de la clase
        platform_group.draw(screen)
        coin_group.draw(screen)
        enemies_group.draw(screen)
        exit_group.draw(screen)

        if player_status == playing:

            platform_group.update()
            enemies_group.update()

            # check for collision between player and enemies (blobs, lava)
            if pygame.sprite.spritecollide(player, enemies_group, False):
                player_status = player_dead
                game_over_fx.play()

            # check if a coin has been collected
            # True elimina de la pantalla el sprite colisionado
            if pygame.sprite.spritecollide(player, coin_group, True): 
                score += configs.get("coins").get("add_score")
                coin_fx.play()

            # check for collision between player and exit
            if pygame.sprite.spritecollide(player, exit_group, False):
                player_status = player_win
        
        # update score
        world.draw_text(screen, ("score", score, coin_group))

        if player_status == player_dead: 

            world.draw_text(screen, ("game_over",))
            
            if restart_button.draw(screen): # restart button is pressed
                
                player.initialize(configs.get("player"))
                player_status = playing
                score = initial_score
                
                enemies_group.empty()
                exit_group.empty()
                platform_group.empty()
                coin_group.empty()

                world = world.reset_level(configs.get("screen"), configs.get("enemies"), 
                                          enemy_sprite_group=enemies_group, exit_configs=configs.get("exit"),
                                          exit_group=exit_group, coin_group=coin_group,
                                          platform_group=platform_group, current_level=current_level,
                                          coin_path_image=configs.get("coins").get("path_image"))

        if player_status == player_win:

            current_level += step_add_level

            if current_level <= max_levels: # go to the next level
                
                enemies_group.empty()
                exit_group.empty()
                platform_group.empty()
                coin_group.empty()

                player.initialize(configs.get("player"))

                world = world.reset_level(configs.get("screen"), configs.get("enemies"), 
                                          enemy_sprite_group=enemies_group, exit_configs=configs.get("exit"),
                                          exit_group=exit_group, coin_group=coin_group,                    
                                          platform_group=platform_group, current_level=current_level,
                                          coin_path_image=configs.get("coins").get("path_image")) 

                player_status = playing # habilito que se siga moviendo el player y los enemigos
            
            else: 

                world.draw_text(screen, ("you_win",))

                if restart_button.draw(screen): # restart game (first level)
                    
                    current_level = initial_level

                    enemies_group.empty()
                    exit_group.empty()
                    platform_group.empty()
                    coin_group.empty()

                    player.initialize(configs.get("player"))

                    world = world.reset_level(configs.get("screen"), configs.get("enemies"), 
                                              enemy_sprite_group=enemies_group, 
                                              exit_configs=configs.get("exit"),
                                              exit_group=exit_group, coin_group=coin_group,
                                              platform_group=platform_group, 
                                              current_level=current_level,
                                              coin_path_image=configs.get("coins").get("path_image"))
                    
                    player_status = playing # habilito que se siga moviendo el player y los enemigos
                    score = initial_score

        player.update(screen, world.tile_list, player_status,
                      jump_fx, platform_group, player_dead, playing)

        # world.draw_grid(screen)

    pygame.display.update()
    
pygame.quit()

# cd /Users/User/Desktop/utn/cuatrimestre1/programacion_1/PYGAME_PRACTICAS/4.juego_tipo_mario/z_POO_version_final
# python main.py
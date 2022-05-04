# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import sprites
from settings import *

###############################################################################
###############################################################################

pygame.init()

screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Final Game")

# sprite groups
all_sprites = pygame.sprite.Group()
layout_group = pygame.sprite.Group()

layout = sprites.Layout(TILE_SIZE)
layout_list = layout.get_layout()
layout_group.add(layout)


playing = True

clock = pygame.time.Clock()

while playing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        if event.type == pygame.KEYDOWN:  # allow for q key to quit the game
            if event.key == pygame.K_q:
                playing = False
    screen.fill(BG)
    # maybe a gradient look as the player moves lower into the level for BG color?
    all_sprites.update()
    layout_group.update()

    pygame.display.flip()

pygame.quit()

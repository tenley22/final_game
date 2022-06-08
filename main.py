# go to terminal (@ bottom of screen) and write "pip install pygame" after PS C: line
import pygame
import sprites
from settings import *

###############################################################################
###############################################################################

pygame.init()
player_group = pygame.sprite.Group()
layout_group = pygame.sprite.Group()
layout = sprites.Layout(TILE_SIZE)
layout_list = layout.get_layout()
layout_group.add(layout)


def start_screen():
    # beginning screen
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Start Screen")
    clock = pygame.time.Clock()

    # press space to move on to level 1
    start_text1 = 'press space key to begin'
    start_text2 = 'or Q to quit'
    directions = 'avoid the green algae and reach the exit to win'
    font_1 = pygame.font.SysFont('Arial', 30, True, False)
    font = pygame.font.SysFont('Arial', 15, True, False)
    text1 = font_1.render(start_text1, True, LIME)
    text2 = font_1.render(start_text2, True, LIME)
    direct = font.render(directions, True, RED)

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = False
                elif event.key == pygame.K_q:
                    quit()
        screen.fill(BG)

        screen.blit(text1, [80, 200])
        screen.blit(text2, [150, 300])
        screen.blit(direct, [100, 600])

        pygame.display.flip()
        clock.tick(FPS)


def game():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Final Game")

    # sprite groups
    all_sprites = pygame.sprite.Group()

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


def game_over():
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    text1 = 'press space to play again'
    text2 = 'or press Q to quit'
    font_1 = pygame.font.SysFont('Arial', 30, True, False)
    text1 = font_1.render(text1, True, LIME)
    text2 = font_1.render(text2, True, RED)

    playing = True
    while playing:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = False
                elif event.key == pygame.K_q:
                    quit()
        screen.fill(BG)

        screen.blit(text1, [80, 200])
        screen.blit(text2, [80, 400])

        pygame.display.flip()

        clock.tick(FPS)


start_screen()
while True:
    game()
    game_over()

pygame.quit()






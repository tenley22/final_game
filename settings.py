import pygame

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (214, 146, 0)
GREEN = (60, 92, 0)
RED = (166, 0, 0)
PURPLE = (215, 135, 255)
BG = (0, 65, 150)

FPS = 60

WIN_WIDTH = 500
WIN_HEIGHT = 900
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
TILE_SIZE = 25
# layout = 20x36
LAYOUT = ['43000000000000000012',
          '00000000000000000000',
          '00000000000000000000',
          '0P000000000000000000',
          '42424223000000000000',
          '00000000000000000000',
          '00000000000001234000',
          '00000000000000000000',
          '00001002003004000000',
          '00000000000000000000',
          '00000000000000000000',
          '44000000000000000044',
          '22000000000000000022',
          '42220000000000000242',
          '00000424424000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000040000000000000',
          '00000000000000000000',
          '00000000000000000000',  # last line of the visible screen at start of game
          '00000000000000000000',
          '00000000000000000000',
          '24444444444444444444',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000',
          '00000000000000000000']



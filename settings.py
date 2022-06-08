import pygame

# Constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (214, 146, 0)
GREEN = (60, 92, 0)
PURPLE = (215, 135, 255)
BG = (15, 55, 90)
LIME = (181, 230, 29)
RED = (221, 28, 1)


FPS = 60

WIN_WIDTH = 500
WIN_HEIGHT = 900
SCREEN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
TILE_SIZE = 25
# layout = 20x36
# the column of 1s on the right are now shown in the window, they are just there for collision
LAYOUT = ['430000000000000000121',
          '000000000000000000011',
          '000000000000000000001',
          '0P0000000000000000001',
          '424242230000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '001424244244230000001',
          '000000000000000000001',
          '000000000abdbc00abdb1',
          'dbdbbdc00000000000001',
          '000000000000000000001',
          '000000000000012422421',
          '000000000000000000001',
          '000001244230000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '0000000000000abddbdb1',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          'bddc00000000000000001',
          '000000000000000000001',
          '000000000012422bddb21',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          'e00000000000000000001',
          '000000000000000000001',
          '000000400000000000001',
          '000000000000000000001',  # last line of the visible screen at start of game
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '000000000000000000001',
          '0000000000000000000D1',
          '242244424224424242424']


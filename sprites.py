import pygame
from settings import *


class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)
        # try/accept stops program from crashing if there is an error

    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        """rectangle is a tuple with (x, y, x+offset, y+offset)"""
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,50))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
            y_margin=0, y_padding=0, width = None, height = None, colorkey = None):
        """Load a grid of images.
        x_margin is the space between the top of the sheet and top of the first
        row. x_padding is space between rows. Assumes symmetrical padding on
        left and right.  Same reasoning for y. Calls self.images_at() to get a
        list of images.
        """

        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.
        if width and height:
            x_sprite_size = width
            y_sprite_size = height
        else:
            x_sprite_size = (sheet_width - 2 * x_margin
                              - (num_cols - 1) * x_padding) / num_cols
            y_sprite_size = (sheet_height - 2 * y_margin
                              - (num_rows - 1) * y_padding) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        return self.images_at(sprite_rects, colorkey)


class Layout(pygame.sprite.Sprite):
    # creates layout of the game using sprite sheets
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.tile_sheet = SpriteSheet('assets/bg_image.png')
        self.left_end_rock = self.tile_sheet.image_at((0, 0, 64, 64))
        self.left_rock = self.tile_sheet.image_at((65, 0, 64, 64))
        self.right_rock = self.tile_sheet.image_at((65, 64, 64, 64))
        self.right_end_rock = self.tile_sheet.image_at((0, 64, 64, 64))
        self.left_end_rock = pygame.transform.scale(self.left_end_rock, (size, size))
        self.left_rock = pygame.transform.scale(self.left_rock, (size, size))
        self.right_rock = pygame.transform.scale(self.right_rock, (size, size))
        self.right_end_rock = pygame.transform.scale(self.right_end_rock, (size, size))
        self.blocks_group = pygame.sprite.Group()
        self.tile_list = []

        for i, row in enumerate(LAYOUT):
            for j, col in enumerate(row):
                x_val = j * self.size
                y_val = i * self.size

                if col == "1":
                    image_rect = self.left_end_rock.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.left_end_rock, image_rect)
                    self.tile_list.append(tile)

                if col == "2":
                    image_rect = self.left_rock.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.left_rock, image_rect)
                    self.tile_list.append(tile)

                if col == "3":
                    image_rect = self.right_rock.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.right_rock, image_rect)
                    self.tile_list.append(tile)

                if col == "4":
                    image_rect = self.right_end_rock.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.right_end_rock, image_rect)
                    self.tile_list.append(tile)

    def update(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])

    def get_layout(self):
        return self.tile_list

    def get_groups(self):
        return self.blocks_group


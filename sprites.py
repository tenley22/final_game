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
                colorkey = image.get_at((0, 0))
            if colorkey is -2:
                colorkey = image.get_at((2, 63))
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


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, tile_set, enemy_tile_set, display):
        pygame.sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.tile_set = tile_set
        self.enemy_tile_set = enemy_tile_set
        self.display = display
        self.run_right_list = []
        self.run_left_list = []
        self.stand_left = None
        self.load_images()
        self.image = self.run_right_list[1]
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.last = pygame.time.get_ticks()
        self.delay = 100
        self.current_frame = 0
        self.right = True
        self.left = False

        self.velocity_y = 0
        self.jumping = False
        self.falling = False
        self.tile_velocity = 0

    def update(self):
        # create deltas
        dx = 0
        dy = 0

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.right = True
            self.left = False
            dx = 5
            now = pygame.time.get_ticks()
            if now - self.last >= self.delay:
                self.last = now
                if self.current_frame >= len(self.run_right_list):
                    self.current_frame = 0
                    self.current_frame = (self.current_frame + 1)
                self.image = self.run_right_list[self.current_frame]
                self.current_frame += 1
        elif keys[pygame.K_LEFT]:
            self.right = False
            self.left = True
            dx = -5
            now = pygame.time.get_ticks()
            if now - self.last >= self.delay:
                self.last = now
                if self.current_frame >= len(self.run_left_list):
                    self.current_frame = 0
                    self.current_frame = (self.current_frame + 1)
                self.image = self.run_left_list[self.current_frame]
                self.current_frame += 1
        else:
            dx = 0
            self.current_frame = 0
            if self.right:
                self.image = self.stand_right
            elif self.left:
                self.image = self.stand_left
        if keys[pygame.K_UP] and not self.jumping and not self.falling:
            self.jumping = True
            dy = -15
        if not keys[pygame.K_UP]:
            self.jumping = False

        self.velocity_y += 1
        if self.velocity_y < 0:
            self.jumping = True
            self.falling = False
        else:
            self.jumping = False
            self.falling = True

        # terminal velocity
        if self.velocity_y >= 3:
            self.velocity_y = 3

        # update delta with velocity
        dy += self.velocity_y

        # CAMERA SCROLL (VERTICAL)
        if self.image_rect.y <= 10 and self.jumping:
            dy = 0
            self.tile_velocity = 3
        elif self.image_rect.y >= WIN_HEIGHT - 60 and self.falling:
            dy = 0
            self.tile_velocity = -3
        else:
            self.tile_velocity = 0
        for tile in self.tile_set:
            tile[1][1] += self.tile_velocity
        for tile in self.enemy_tile_set:
            tile[1][1] += self.tile_velocity
            # tile[1] gets the rectangle with x,y coordinate and [1] gets just the y coordinate to add velocity to

        # keeping player inside of screen horizontally
        if self.image_rect.x <= 0 and self.left and keys[pygame.K_LEFT]:
            dx = 0
        elif self.image_rect.x >= WIN_WIDTH - 1 and self.right and keys[pygame.K_RIGHT]:
            dx = 0

            # tiles in layout list
        for tile in self.tile_set:
            if tile[1].colliderect(self.image_rect.x+dx, self.image_rect.y, self.image_rect.width,
                                   self.image_rect.height):
                dx = 0
            if tile[1].colliderect(self.image_rect.x, self.image_rect.y+dy, self.image_rect.width,
                                   self.image_rect.height):
                # collision bottom of platform and top of player
                if dy < 0:
                    dy = tile[1].bottom - self.image_rect.top
                    self.velocity_y = 0
                    self.jumping = False
                # collision top of platform and bottom of player
                elif self.falling:
                    dy = tile[1].top - self.image_rect.bottom
                    self.velocity_y = 0
                    self.falling = False

        # slow velocity/send backward on green tiles
        for tile in self.enemy_tile_set:
            if tile[1].colliderect(self.image_rect.x+dx, self.image_rect.y, self.image_rect.width,
                                   self.image_rect.height):
                dx = 0
            if tile[1].colliderect(self.image_rect.x, self.image_rect.y+dy, self.image_rect.width,
                                   self.image_rect.height):
                # collision bottom of platform and top of player
                if dy < 0:
                    dy = tile[1].bottom - self.image_rect.top
                    self.velocity_y = 0
                    self.jumping = False
                # collision top of platform and bottom of player
                elif self.falling:
                    dy = tile[1].top - self.image_rect.bottom
                    self.velocity_y = 0
                    self.falling = False
                    if self.right:
                        dx -= 2
                    elif self.left:
                        dx += 2

        self.image_rect.x += dx
        self.image_rect.y += dy

        self.display.blit(self.image, self.image_rect)

    def load_images(self):
        diver = SpriteSheet("assets/diver.png")
        right_run_1 = diver.image_at((41, 99, 14, 27), -1)
        self.run_right_list.append(right_run_1)
        right_run_2 = diver.image_at((22, 131, 14, 27), -1)
        self.run_right_list.append(right_run_2)
        self.stand_right = diver.image_at((41, 3, 14, 27), -1)
        right_run_3 = diver.image_at((41, 131, 14, 27), -1)
        self.run_right_list.append(right_run_3)

        left_run_1 = diver.image_at((60, 99, 14, 27), -1)
        self.run_left_list.append(left_run_1)
        left_run_2 = diver.image_at((3, 131, 14, 27), -1)
        self.run_left_list.append(left_run_2)
        self.stand_left = diver.image_at((60, 3, 14, 27), -1)
        left_run_3 = diver.image_at((60, 131, 14, 27), -1)
        self.run_left_list.append(left_run_3)


class Shark(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, tile_set, display, speed, direct):
        pygame.sprite.Sprite.__init__(self)
        self.tile_size = tile_size
        self.tile_set = tile_set
        self.display = display
        self.speed = speed
        self.direct = direct
        self.right_list = []
        self.left_list = []
        self.stand_left = None
        self.load_images()
        self.image = self.right_list[1]
        self.image_rect = self.image.get_rect()
        self.image_rect.x = x
        self.image_rect.y = y
        self.last = pygame.time.get_ticks()
        self.delay = 100
        self.current_frame = 0
        self.right = True
        self.left = False

    def update(self):
        dx = 0
        dy = 0

        if self. direct == 0:
            self.right = True
            self.left = False
            dx = self.speed
            now = pygame.time.get_ticks()
            time = 0
            if now - self.last >= self.delay:
                self.last = now
                time += 1
                if self.current_frame >= len(self.right_list):
                    self.current_frame = 0
                    self.current_frame = (self.current_frame + 1)
                self.image = self.right_list[self.current_frame]
                self.current_frame += 1
        elif self. direct == 1:
            self.right = False
            self.left = True
            dx = self.speed * -1
            now = pygame.time.get_ticks()
            time = 0
            if now - self.last >= self.delay:
                self.last = now
                time += 1
                if self.current_frame >= len(self.left_list):
                    self.current_frame = 0
                    self.current_frame = (self.current_frame + 1)
                self.image = self.left_list[self.current_frame]
                self.current_frame += 1

        self.image_rect.x += dx

        self.display.blit(self.image, self.image_rect)

    def load_images(self):
        shark = SpriteSheet("assets/shark.png")
        shark_r1 = shark.image_at((155, 28, 104, 34), -1)
        self.right_list.append(shark_r1)
        shark_r2 = shark.image_at((155, 65, 104, 34), -1)
        self.right_list.append(shark_r2)
        shark_r3 = shark.image_at((155, 154, 104, 34), -1)
        self.right_list.append(shark_r3)
        shark_r4 = shark.image_at((155, 195, 104, 34), -1)
        self.right_list.append(shark_r4)

        shark_l1 = shark.image_at((8, 28, 104, 32), -1)
        self.left_list.append(shark_l1)
        shark_l2 = shark.image_at((8, 65, 104, 37), -1)
        self.left_list.append(shark_l2)
        shark_l3 = shark.image_at((8, 154, 104, 37), -1)
        self.left_list.append(shark_l3)
        shark_l4 = shark.image_at((8, 195, 104, 37), -1)
        self.left_list.append(shark_l4)


class Layout(pygame.sprite.Sprite):
    # creates layout of the game using sprite sheets
    def __init__(self, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        # main rocks tiles
        self.tile_sheet = SpriteSheet('assets/tilemap_2.png')
        self.left_end_rock = self.tile_sheet.image_at((0, 0, 64, 64), -2)
        self.left_rock = self.tile_sheet.image_at((65, 0, 64, 64), -2)
        self.right_rock = self.tile_sheet.image_at((65, 64, 64, 64), -2)
        self.right_end_rock = self.tile_sheet.image_at((0, 64, 64, 64), -2)
        self.left_end_rock = pygame.transform.scale(self.left_end_rock, (size, size))
        self.left_rock = pygame.transform.scale(self.left_rock, (size, size))
        self.right_rock = pygame.transform.scale(self.right_rock, (size, size))
        self.right_end_rock = pygame.transform.scale(self.right_end_rock, (size, size))
        # enemy rocks tiles
        self.enemy_tile_sheet = SpriteSheet('assets/enemy_rocks.png')
        self.le_enemy_rock = self.enemy_tile_sheet.image_at((0, 0, 64, 64), -2)
        self.l_enemy_rock = self.enemy_tile_sheet.image_at((65, 0, 64, 64), -2)
        self.r_enemy_rock = self.enemy_tile_sheet.image_at((65, 64, 64, 64), -2)
        self.re_enemy_rock = self.enemy_tile_sheet.image_at((0, 64, 64, 64), -2)
        self.le_enemy_rock = pygame.transform.scale(self.le_enemy_rock, (size, size))
        self.l_enemy_rock = pygame.transform.scale(self.l_enemy_rock, (size, size))
        self.r_enemy_rock = pygame.transform.scale(self.r_enemy_rock, (size, size))
        self.re_enemy_rock = pygame.transform.scale(self.re_enemy_rock, (size, size))

        self.blocks_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle()
        self.enemy_group = pygame.sprite.GroupSingle()
        self.tile_list = []
        self.enemy_tile_list = []

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
                # enemy tiles, adding 1 for different collision
                if col == "a":
                    image_rect = self.le_enemy_rock.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.le_enemy_rock, image_rect)
                    self.enemy_tile_list.append(tile)

                if col == "b":
                    image_rect = self.l_enemy_rock.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.l_enemy_rock, image_rect)
                    self.enemy_tile_list.append(tile)

                if col == "c":
                    image_rect = self.r_enemy_rock.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.r_enemy_rock, image_rect)
                    self.enemy_tile_list.append(tile)

                if col == "d":
                    image_rect = self.re_enemy_rock.get_rect()
                    image_rect.x = x_val
                    image_rect.y = y_val
                    tile = (self.re_enemy_rock, image_rect)
                    self.enemy_tile_list.append(tile)

                if col == "P":
                    player = Player(TILE_SIZE, WIN_HEIGHT - TILE_SIZE, TILE_SIZE, self.tile_list, self.enemy_tile_list,
                                    SCREEN)
                    player.image_rect.x = x_val
                    player.image_rect.y = y_val
                    self.player_group.add(player)

                if col == "e":
                    enemy = Shark(TILE_SIZE, WIN_HEIGHT - TILE_SIZE, TILE_SIZE, self.tile_list, SCREEN, 2, 0)
                    enemy.image_rect.x = x_val
                    enemy.image_rect.y = y_val
                    self.enemy_group.add(enemy)

    def update(self):
        for tile in self.tile_list:
            SCREEN.blit(tile[0], tile[1])
        for tile in self.enemy_tile_list:
            SCREEN.blit(tile[0], tile[1])

        self.player_group.update()
        self.enemy_group.update()

    def get_layout(self):
        return self.tile_list
        return self.enemy_tile_list

    def get_groups(self):
        return self.blocks_group
        return self.enemy_group


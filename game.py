import pygame

from settings import *
from random import choice
from timer import Timer
from sys import exit

class Game:

    def __init__(self, get_next_shape, update_score):
        self.settings = Settings()
        self.surface = pygame.Surface((self.settings.GAME_WIDTH, self.settings.GAME_HEIGHT))
        self.display_surface = pygame.display.get_surface()
        self.rect = self.surface.get_rect(topleft = (self.settings.padding, self.settings.padding))
        self.sprites = pygame.sprite.Group()

        #game connection
        self.get_next_shape = get_next_shape
        self.update_score = update_score

        #lines
        self.line_surface = self.surface.copy()
        self.line_surface.fill((0,255,0))
        self.line_surface.set_colorkey((0,255,0))
        self.line_surface.set_alpha(120)

        self.field_data = [[0 for x in range(self.settings.columns)] for y in range(self.settings.rows)]

        self.tetromino = Tetromino(
            choice(list(self.settings.TETROMINOS.keys())),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)


        #timer
        self.down_speed = self.settings.update_start_speed
        self.down_speed_faster = self.settings.update_start_speed * 0.3
        self.down_pressed = False
        self.timers = {
            'vertical move': Timer(self.settings.update_start_speed, True, self.move_down),
            'horizontal move': Timer(self.settings.move_wait_time),
            'rotate': Timer(self.settings.rotate_wait_time)
        }
        self.timers['vertical move'].activate()

        #score
        self.current_level = 1
        self.current_score = 0
        self.current_lines = 0

    def calculate_score(self, num_lines):
        self.current_lines += num_lines
        self.current_score += self.settings.score_data[num_lines] * self.current_level

        if self.current_lines / 10 > self.current_level:
            self.current_level += 1
            self.down_speed *= 0.75
            self.down_speed_faster = self.down_speed * 0.3
            self.timers['vertical move'].duration = self.down_speed
        self.update_score(self.current_lines, self.current_score, self.current_level)

    def check_game_over(self):
        for block in self.tetromino.blocks:
            if block.pos.y < 0:
                exit()

    def create_new_tetromino(self):
        self.check_game_over()
        self.check_finished_rows()
        self.tetromino = Tetromino(
            self.get_next_shape(),
            self.sprites,
            self.create_new_tetromino,
            self.field_data)

    def timer_update(self):
        for timer in self.timers.values():
            timer.update()

    def move_down(self):
        self.tetromino.move_down()

    def draw_grid(self):
        for i in range(1, self.settings.columns):
            x = i * self.settings.cell_size
            pygame.draw.line(self.line_surface, self.settings.LINE_COLOR, (x, 0), (x, self.surface.get_height()))

        for i in range(1, self.settings.rows):
            y = i * self.settings.cell_size
            pygame.draw.line(self.line_surface, self.settings.LINE_COLOR, (0, y), (self.surface.get_width(), y))

        self.surface.blit(self.line_surface, (0, 0))

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.timers['horizontal move'].active:
            if keys[pygame.K_LEFT]:
                self.tetromino.move_horizontal(-1)
                self.timers['horizontal move'].activate()
            if keys[pygame.K_RIGHT]:
                self.tetromino.move_horizontal(1)
                self.timers['horizontal move'].activate()

        #check for rotation
        if not self.timers['rotate'].active:
            if keys[pygame.K_UP]:
                self.tetromino.rotate()
                self.timers['rotate'].activate()

        #down speedup
        if not self.down_pressed and keys[pygame.K_DOWN]:
            self.down_pressed = True
            self.timers['vertical move'].duration = self.down_speed_faster

        if self.down_pressed and not keys[pygame.K_DOWN]:
            self.down_pressed = False
            self.timers['vertical move'].duration = self.down_speed


    def check_finished_rows(self):
        delete_rows = []
        for i, row in enumerate(self.field_data):
            if all(row):
                delete_rows.append(i)

        if delete_rows:
            for delete_row in delete_rows:
                for block in self.field_data[delete_row]:
                    block.kill()

                for row in self.field_data:
                    for block in row:
                        if block and block.pos.y < delete_row:
                            block.pos.y += 1

            self.field_data = [[0 for x in range(self.settings.columns)] for y in range(self.settings.rows)]
            for block in self.sprites:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block

            #update score
            self.calculate_score(len(delete_rows))

    def run(self):

        #update
        self.timer_update()
        self.input()
        self.sprites.update()

        #draw
        self.surface.fill(self.settings.GRAY)
        self.sprites.draw(self.surface)

        self.draw_grid()
        self.display_surface.blit(self.surface, (self.settings.padding, self.settings.padding))

        pygame.draw.rect(self.display_surface, self.settings.LINE_COLOR, self.rect, 2, 2)

class Tetromino:
    def __init__(self, shape, group, create_new_tetromino, field_data):
        self.settings = Settings()

        self.shape = shape
        self.block_position = self.settings.TETROMINOS[shape]['shape']
        self.color = self.settings.TETROMINOS[shape]['color']
        self.create_new_tetromino = create_new_tetromino
        self.field_data = field_data

        self.blocks = [Block(group, pygame.Vector2(pos), self.color) for pos in self.block_position]


    def next_move_horizontal_collide(self, blocks, direction):
        collision_list = [block.horizontal_collide(int(block.pos.x + direction), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    def next_move_vertical_collide(self, blocks):
        collision_list = [block.vertical_collide(int(block.pos.y + 1), self.field_data) for block in blocks]
        return True if any(collision_list) else False

    def move_horizontal(self, direction):
        if not self.next_move_horizontal_collide(self.blocks, direction):
            for block in self.blocks:
                block.pos.x += direction
    def move_down(self):
        if not self.next_move_vertical_collide(self.blocks):
            for block in self.blocks:
                block.pos.y += 1

        else:
            for block in self.blocks:
                self.field_data[int(block.pos.y)][int(block.pos.x)] = block
            self.create_new_tetromino()

    def rotate(self):
        if self.shape != 'O':
            pivot_pos = self.blocks[0].pos

            new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]

            for pos in new_block_positions:
                if pos.x < 0 or pos.x >= self.settings.columns:
                    return

                if self.field_data[int(pos.y)][int(pos.x)]:
                    return

                if pos.y >= self.settings.rows:
                    return


            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]


class Block(pygame.sprite.Sprite):
    def __init__(self, group, pos, color):
        super().__init__(group)
        self.settings = Settings()
        self.image = pygame.Surface((self.settings.cell_size, self.settings.cell_size))
        self.image.fill(color)

        #position
        self.pos = pygame.Vector2(pos) + self.settings.block_offset
        x = self.pos.x * self.settings.cell_size
        y = self.pos.y * self.settings.cell_size
        self.rect = self.image.get_rect(topleft = (x, y))

    def rotate(self, pivot_pos):
        return pivot_pos + (self.pos -pivot_pos).rotate(90)

    def horizontal_collide(self, x, field_data):
        if not 0 <= x < self.settings.columns:
            return True

        if field_data[int(self.pos.y)][int(x)]:
            return True

    def vertical_collide(self, y, field_data):
        if not y < self.settings.rows:
            return True

        if y >= 0 and field_data[int(y)][int(self.pos.x)]:
            return True

    def update(self):
        self.rect.topleft = self.pos * self.settings.cell_size
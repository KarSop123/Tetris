import pygame
import sys

class Settings:
    def __init__(self):
        self.columns = 10
        self.rows = 20
        self.cell_size = 40
        self.padding = 10
        self.GAME_WIDTH = self.columns * self.cell_size
        self.GAME_HEIGHT = self.rows * self.cell_size

        #side bar
        self.side_bar_width = 200
        self.preview_height_fraction = 0.7
        self.score_height_fraction = 1 - self.preview_height_fraction

        self.WINDOW_WIDTH = self.columns * self.cell_size + self.side_bar_width + self.padding * 3
        self.WINDOW_HEIGHT = self.rows * self.cell_size + self.padding * 2

        self.update_start_speed = 400
        self.move_wait_time = 200
        self.rotate_wait_time = 200
        self.block_offset = pygame.Vector2(self.columns // 2, -1)

        #Colors
        self.YELLOW = '#f1e60d'
        self.RED = '#e51b20'
        self.BLUE = '#204b9b'
        self.GREEN = '#65b32e'
        self.PURPLE = '#7b217f'
        self.CYAN = '#6cc6d9'
        self.ORANGE = '#f07e13'
        self.GRAY = '#1C1C1C'
        self.LINE_COLOR = '#FFFFFF'

        self.TETROMINOS = {
            'T': {'shape': [(0, 0), (-1, 0), (1, 0), (0, -1)], 'color': self.PURPLE},
            'O': {'shape': [(0, 0), (0, -1), (1, 0), (1, -1)], 'color': self.YELLOW},
            'J': {'shape': [(0, 0), (0, -1), (0, 1), (-1, 1)], 'color': self.BLUE},
            'L': {'shape': [(0, 0), (0, -1), (0, 1), (1, 1)], 'color': self.ORANGE},
            'I': {'shape': [(0, 0), (0, -1), (0, -2), (0, 1)], 'color': self.CYAN},
            'S': {'shape': [(0, 0), (-1, 0), (0, -1), (1, -1)], 'color': self.GREEN},
            'Z': {'shape': [(0, 0), (1, 0), (0, -1), (-1, -1)], 'color': self.RED},
            #'R': {'shape': [(0, 0), (-1, 0),(-2,0), (-2,-1), (1, 0),(2,0),(2,1), (0, -1),(0,-2),(1,-2),(0,1),(0,2),(-1,2)], 'color': self.RED}
        }

        self.score_data = {1: 40, 2: 100, 3: 300, 4: 1200}
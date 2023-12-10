from settings import *
from sys import exit
from os.path import join

from game import Game
from score import Score
from preview import Preview

from random import choice



class Tetris:
    def __init__(self):
        pygame.init()
        self.settings = Settings()


        self.WINDOW_WIDTH = self.settings.WINDOW_WIDTH
        self.WINDOW_HEIGHT = self.settings.WINDOW_HEIGHT

        self.display_surface = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption('Tetris')

        #shapes
        self.next_shapes = [choice(list(self.settings.TETROMINOS.keys())) for shape in range(3)]


        self.game = Game(self.get_next_shape, self.update_score)
        self.score = Score()
        self.preview = Preview()

        #time
        self.clock = pygame.time.Clock()
        self.dt = self.clock.tick() / 1000

        #music
        self.music = pygame.mixer.Sound(join('audio', 'amstrong.mp3'))
        self.music.play(loops = -1)
        self.music.set_volume(0.5)

    def update_score(self, lines, score, level):
        self.score.lines = lines
        self.score.score = score
        self.score.level = level

    def get_next_shape(self):
        next_shape = self.next_shapes.pop(0)
        self.next_shapes.append(choice(list(self.settings.TETROMINOS.keys())))
        return next_shape

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()


            # fill background
            self.display_surface.fill((self.settings.GRAY))

            self.game.run()
            self.score.run()
            self.preview.run(self.next_shapes)

            #display update
            pygame.display.update()


if __name__ == '__main__':
    tetris = Tetris()
    tetris.run()

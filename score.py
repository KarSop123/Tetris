from settings import *
from os.path import join


class Score:
    def __init__(self):
        self.settings = Settings()

        self.surface = pygame.Surface((self.settings.side_bar_width, self.settings.GAME_HEIGHT * self.settings.score_height_fraction - self.settings.padding))
        self.rect = self.surface.get_rect(bottomright = (self.settings.WINDOW_WIDTH - self.settings.padding, self.settings.WINDOW_HEIGHT - self.settings.padding))
        self.display_surface = pygame.display.get_surface()

        self.font = pygame.font.Font(join('graphics', 'Russo_One.ttf'), 30)

        self.increment_height = self.surface.get_height() / 3

        #data
        self.score = 0
        self.level = 1
        self.lines = 0

    def display_text(self, pos, text):
        text_surface = self.font.render(f'{text[0]}: {text[1]}', True, 'white')
        text_rect = text_surface.get_rect(center = pos)
        self.surface.blit(text_surface, text_rect)

    def run(self):

        self.surface.fill(self.settings.GRAY)
        for i, text in enumerate([('Scope', self.score), ('Level', self.level), ('Lines', self.lines)]):
            x = self.surface.get_width() / 2
            y = self.increment_height / 2 + i * self.increment_height
            self.display_text((x, y), text)

        self.display_surface.blit(self.surface, self.rect)
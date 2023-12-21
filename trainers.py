import pygame
from abc import ABC, abstractmethod
from states import *
import colors
from drawutils import *
class Trainer(pygame.sprite.Sprite, ABC):
    def __init__(self, x, y, pic, scale, fix=0):
        super().__init__()
        self.x = x
        self.y = y
        self._picture = pygame.image.load(f"static/images/{pic}").convert_alpha()
        self._picture = pygame.transform.scale(self._picture, scale)
        size = self._picture.get_size()
        self.image = pygame.Surface((size[0] + fix, size[1] + 40), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.box = []
        self.wins = 0
        self.state = TrainerStates.IDLE

    def add_pokemon(self, p):
        self.box.append(p)

    @abstractmethod
    def best_team(self, **kwargs):
        pass

    def update(self):
        self.image.fill((255, 255, 255, 0))
        self.rect.center = (self.x, self.y)
        size = self._picture.get_size()
        self.image.blit(self._picture, (0, 0))
        draw_text(
            self.image, colors.WHITE, f"Wins {self.wins} Poks {len(self.box)}", where=(0, size[1] - 3), font_size=18
        )


class DullTrainer(Trainer):
    def __init__(self, x, y):
        super().__init__(x, y, "trainer.png", (180, 200))

    def best_team(self, n):
        return self.box[:n]


class SmartTrainer(Trainer):
    def __init__(self, x, y):
        super().__init__(x, y, "smart_trainer.png", (100, 200), 25)

    def best_team(self, n):
        # TODO
        return self.box[:n]
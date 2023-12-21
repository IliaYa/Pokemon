import pygame
from abc import ABC, abstractmethod
import random
from states import *
import colors
from drawutils import *

class Pokemon(pygame.sprite.Sprite, ABC):
    def __init__(self, name, atk, df, x, y, pic):
        super().__init__()
        self.x = x
        self.y = y
        self.vx = random.randint(1, 5)
        self.vy = random.randint(1, 5)
        self._picture = pygame.image.load(f"static/images/{pic}").convert_alpha()
        self._picture = pygame.transform.scale(self._picture, (150, 150))
        size = self._picture.get_size()
        self.image = pygame.Surface((size[0], size[1] + 40), pygame.SRCALPHA, 32)
        self.rect = self.image.get_rect()
        self.rect.center = (self.x, self.y)
        self.state = PokemonStates.WILD
        self.name = name
        self.hp = 100
        self.atk = atk
        self.df = df

    def update(self):
        if self.state == PokemonStates.WILD:
            self.y += self.vy
            self.x -= self.vx

        elif self.state == PokemonStates.CAUGHT:
            # TODO сидит около тренера
            pass
        self.image.fill((255, 255, 255, 0))
        self.rect.center = (self.x, self.y)
        size = self._picture.get_size()
        self.image.blit(self._picture, (0, 0))
        draw_text(
            self.image, colors.WHITE, f"Atk {self.atk} Df {self.df} HP {self.hp}", where=(0, size[1] - 10), font_size=18
        )

    @abstractmethod
    def attack(self, other, damage=None):
        if other.hp <= 0:
            other.hp = 0
            return
        if self.hp <= 0:
            self._hp = 0
            return
        if damage is None:
            damage = self.atk - other.df
        if damage >= 0:
            other.hp -= damage
        else:
            other.hp -= 1

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        if self._hp <= 0:
            self._hp = 0
        return self._hp

    @property
    def atk(self):
        return self._atk

    @property
    def df(self):
        return self._df

    @name.setter
    def name(self, value):
        self._name = value

    @hp.setter
    def hp(self, value):
        self._hp = value

    @atk.setter
    def atk(self, value):
        self._atk = value

    @df.setter
    def df(self, value):
        self._df = value

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = value

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = value


class WaterPokemon(Pokemon):
    def __init__(self, name, atk, df, x=0, y=0):
        super(WaterPokemon, self).__init__(name, atk, df, x, y, "squirtle.png")

    def attack(self, other, **kwargs):
        if isinstance(other, FirePokemon):
            super().attack(other, self.atk * 3 - other.df)
        else:
            super().attack(other)


class FirePokemon(Pokemon):
    def __init__(self, name, atk, df, x=0, y=0):
        super().__init__(name, atk, df, x, y, "charmander.png")

    def attack(self, other, **kwargs):
        super().attack(other)


class GrassPokemon(Pokemon):
    def __init__(self, name, atk, df, x=0, y=0):
        super().__init__(name, atk, df, x, y, "bulbasaur.png")

    def attack(self, other, **kwargs):
        if isinstance(other, FirePokemon):
            super().attack(other, self.atk - (other.df // 2))
        else:
            super().attack(other)


class ElectricPokemon(Pokemon):
    def __init__(self, name, atk, df, x=0, y=0):
        super().__init__(name, atk, df, x, y, "pikachu.png")

    def attack(self, other, **kwargs):
        if isinstance(other, WaterPokemon):
            super().attack(other, self.atk)
        else:
            super().attack(other)

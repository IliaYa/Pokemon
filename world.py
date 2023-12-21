import pygame
from trainers import *
import random
from pokemons import *
import sys
SIZE = (1200, 1000)


class Border(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2):
        super().__init__()
        if x1 == x2:
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)
        else:
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)
        self.image.fill((255, 255, 0))  


class World:
    MAX_POKEMON_ATK = 5
    MAX_POKEMON_DF = 5

    def __init__(self, n_pok, x1, y1, x2, y2):
        self.n_pok = n_pok
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        self.horBorders = pygame.sprite.Group()
        self.vertBorders = pygame.sprite.Group()
        self.vertBorders.add(Border(x1, y1, x1, y2))
        self.vertBorders.add(Border(x2, y1, x2, y2))
        self.horBorders.add(Border(x1, y1, x2, y1))
        self.horBorders.add(Border(x1, y2, x2, y2))
        self.rect = pygame.Rect(x1, y1, x2 - x1, y2 - y1)
        size = self.rect.size
        self.pokemons = pygame.sprite.Group()
        self.trainers = pygame.sprite.Group()
        self.dull_trainer = DullTrainer(size[0] - 100, size[1] - 100)
        self.smart_trainer = SmartTrainer(100, size[1] - 100)
        self._generate_pokemons()
        self._generate_trainers()

    def _generate_trainers(self):
        self.trainers.add(self.dull_trainer)
        self.trainers.add(self.smart_trainer)

    def _generate_pokemons(self):
        for _ in range(self.n_pok):
            pok_pick = random.randint(1, 4)
            if pok_pick == 1:
                self.pokemons.add(WaterPokemon(
                    "wp", random.randint(1, World.MAX_POKEMON_ATK),
                    random.randint(1, World.MAX_POKEMON_DF),
                    random.randint(100, self.rect.right - 100), random.randint(100, self.rect.bottom - 100))
                )
            elif pok_pick == 2:
                self.pokemons.add(
                    FirePokemon(
                        "fp", random.randint(1, World.MAX_POKEMON_ATK),
                        random.randint(1, World.MAX_POKEMON_DF),
                        random.randint(100, self.rect.right - 100), random.randint(100, self.rect.bottom - 100))
                )
            elif pok_pick == 3:
                self.pokemons.add(GrassPokemon(
                    "gp", random.randint(1, World.MAX_POKEMON_ATK),
                    random.randint(1, World.MAX_POKEMON_DF),
                    random.randint(100, self.rect.right - 100), random.randint(100, self.rect.bottom - 100))
                )
            else:
                self.pokemons.add(ElectricPokemon(
                    "ep", random.randint(1, World.MAX_POKEMON_ATK),
                    random.randint(1, World.MAX_POKEMON_DF),
                    self.rect.center[0], self.rect.center[1])
                )

    def draw(self, surface):
        self.horBorders.draw(surface)
        self.vertBorders.draw(surface)
        surface.set_clip(self.rect)
        self.pokemons.draw(surface)
        self.trainers.draw(surface)
        surface.set_clip(None)

    def update(self):
        hor_collision = pygame.sprite.groupcollide(self.pokemons, self.horBorders, False, False)
        for p in hor_collision:
            p.vy = -p.vy
        vert_collision = pygame.sprite.groupcollide(self.pokemons, self.vertBorders, False, False)
        for p in vert_collision:
            p.vx = -p.vx
        self.pokemons.update()
        self.trainers.update()

    def events_handler(self, surface, battle, world):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                left, mid, right = pygame.mouse.get_pressed(3)
                if mid:
                    continue
                caught_pokemon = self._catch_pokemon(pygame.mouse.get_pos())
                if caught_pokemon is not None:
                    if left:
                        self.smart_trainer.add_pokemon(caught_pokemon)
                    else:
                        self.dull_trainer.add_pokemon(caught_pokemon)

            elif event.type == pygame.KEYDOWN:
                pressed = pygame.key.get_pressed()
                if pressed[pygame.K_b]:
                    if len(self.smart_trainer.box) < 4:
                        draw_text(surface, colors.RED, "Too few poks", where=(30, SIZE[1] - 150), font_size=18)
                    elif len(self.dull_trainer.box) < 4:
                        draw_text(surface, colors.RED, "Too few poks", where=(SIZE[0] - 180, SIZE[1] - 150),
                                  font_size=18)
                    else:
                        battle.start(world)

    def _catch_pokemon(self, pos):
        for pokemon in self.pokemons:
            if pokemon.rect.collidepoint(pos[0], pos[1]):
                self.pokemons.remove(pokemon)
                return pokemon

    @property
    def smart_trainer(self):
        return self._smart_trainer

    @smart_trainer.setter
    def smart_trainer(self, value):
        self._smart_trainer = value
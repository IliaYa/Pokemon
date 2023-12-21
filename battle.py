from states import *
import pygame
HIT_DELAY = 200
class Battle:
    def __init__(self, n, x, y):
        self.n = n
        self.x = x
        self.y = y
        self.turn = 1
        self.state = BattleStates.NOT_STARTED

    def draw(self, surface):
        if self.state == BattleStates.NOT_STARTED:
            return
        self.smart_trainer_g.draw(surface)
        self.dull_trainer_g.draw(surface)
        if len(self.smart_trainer_g.sprites()) > 0 and len(self.dull_trainer_g.sprites()) > 0:
            pygame.draw.line(surface, (255, 0, 0), self.smart_trainer_g.sprites()[0].rect.midright,
                             self.dull_trainer_g.sprites()[0].rect.midleft, 3)

            hit_circle = pygame.Surface(
                (self.smart_trainer_g.sprites()[0].rect.width, self.smart_trainer_g.sprites()[0].rect.height),
                pygame.SRCALPHA)
            pygame.draw.circle(hit_circle, (255, 0, 0, 100), hit_circle.get_rect().center,
                               hit_circle.get_rect().width // 2 - 5, 0)

            if self.turn == 1:
                surface.blit(hit_circle, self.dull_trainer_g.sprites()[0].rect.topleft)
            else:
                surface.blit(hit_circle, self.smart_trainer_g.sprites()[0].rect.topleft)

    def start(self, world):
        if self.state == BattleStates.NOT_STARTED:
            pygame.mixer.music.load("sound/battle.ogg")
            pygame.mixer.music.play(-1)
            pygame.display.set_caption("Pokemons [BATTLE]")
            world.pokemons.empty()
            self.smart_trainer = world.smart_trainer
            self.dull_trainer = world.dull_trainer
            self.smart_trainer_g = pygame.sprite.Group()
            self.smart_trainer_g.add(world.smart_trainer.best_team(self.n))
            self.dull_trainer_g = pygame.sprite.Group()
            self.dull_trainer_g.add(world.dull_trainer.best_team(self.n))
            # if len(self.smart_trainer_g) < self.n or len(self.dull_trainer_g) < self.n:
            #     return

            y = self.y
            for pokemon in self.smart_trainer_g:
                pokemon.state = PokemonStates.CAUGHT
                pokemon.atk = pokemon.atk * 3
                pokemon._picture = pygame.transform.scale(pokemon._picture, (90, 90))
                pokemon.x = self.x + 500
                pokemon.y = y
                pokemon.rect.topleft = (self.x, y)
                y += pokemon.rect.height + 10
                pokemon.vx = pokemon.vy = 0
            y = self.y
            for pokemon in self.dull_trainer_g:
                pokemon.state = PokemonStates.CAUGHT
                pokemon.atk = pokemon.atk * 3
                pokemon._picture = pygame.transform.scale(pokemon._picture, (90, 90))
                pokemon.x = self.x + 780
                pokemon.y = y
                pokemon.rect.topleft = (self.x + 280, y)
                y += pokemon.rect.height + 10
                pokemon.vx = pokemon.vy = 0
            self.state = BattleStates.STARTED
            self.last_update = pygame.time.get_ticks()

    def update(self):
        if self.state == BattleStates.STARTED:
            now_time = pygame.time.get_ticks()
            if now_time - self.last_update > HIT_DELAY:
                self.last_update = now_time
            else:
                return
            if self.turn == 1 and len(self.smart_trainer_g.sprites()) > 0 and len(self.dull_trainer_g.sprites()) > 0:
                self.smart_trainer_g.sprites()[0].attack(self.dull_trainer_g.sprites()[0])
                if self.dull_trainer_g.sprites()[0].hp <= 0:
                    self.dull_trainer_g.remove(self.dull_trainer_g.sprites()[0])
                if len(self.dull_trainer_g.sprites()) == 0:
                    return self.finish(1)
            elif self.turn == 2 and len(self.smart_trainer_g.sprites()) > 0 and len(self.dull_trainer_g.sprites()) > 0:
                self.dull_trainer_g.sprites()[0].attack(self.smart_trainer_g.sprites()[0])
                if self.smart_trainer_g.sprites()[0].hp <= 0:
                    self.smart_trainer_g.remove(self.smart_trainer_g.sprites()[0])
                if len(self.smart_trainer_g.sprites()) == 0:
                    return self.finish(2)
            if self.turn == 1:
                self.turn = 2
            else:
                self.turn = 1
            self.smart_trainer_g.update()
            self.dull_trainer_g.update()

    def finish(self, result):
        self.state = BattleStates.FINISHED
        for p in self.smart_trainer_g:
            self.smart_trainer.add_pokemon(p)
        for p in self.dull_trainer_g:
            self.dull_trainer.add_pokemon(p)
        if result == 1:
            self.smart_trainer.wins += 1
        else:
            self.dull_trainer.wins += 1

    def is_started(self):
        return self.state == BattleStates.STARTED

    def is_finished(self):
        return self.state == BattleStates.FINISHED
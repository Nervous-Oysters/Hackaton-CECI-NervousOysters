import pygame


class Player(pygame.sprite.Sprite):

    def __init__(self, player_characteristics, position, direction):
        super().__init__(self)
        self.name = player_characteristics.get("name")
        self.pv = player_characteristics.get("pv")
        self.stats = player_characteristics.get("stats")

        self.position = position
        self.direction = direction

        self.animations = player_characteristics.get("animations")


    def get_pv(self):
        return self.pv

    def get_stats(self):
        return self.stats

    def get_specific_stat(self, stat_name):
        return self.stats.get(stat_name)

    def get_name(self):
        return self.get_name()

    def get_animations(self):
        return self.animations

    def get_pos(self):
        return self.position
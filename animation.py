import os
import numpy as np
import pygame
from player import Player

class Animation:
    
    def __init__(self, animation_folder:str, player:Player, direction:bool, size=150, speed=10, loop=1):
        self.size = size
        self.player = player
        self.position = player.position
        if not direction:
            self.position = [self.position[0]+20, self.position[1]]
        self.direction = direction
        self.animation_folder = "animations/" + animation_folder # animations/fire-ball_10
        self.sprites_list = os.listdir(self.animation_folder) # animations/fire-ball_10/*
        self.sprites_list.sort()
        print(self.sprites_list)
        self.sprite_index = 0
        self.frame_counter = 0
        self.update_image(self.animation_folder + "/" + self.sprites_list[self.sprite_index])
        self.speed = speed # pixel per frame
        self.loop = loop
        
    def update_image(self, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, np.array((1,1))*self.size)
        if not self.direction:
            self.image = pygame.transform.flip(self.image, True, False)
        
    def next(self):
        self.update_image(self.animation_folder + "/" + self.sprites_list[self.sprite_index])
        self.sprite_index += 1
        if self.sprite_index >= len(self.sprites_list):
            return "end"
        
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.speed:
            if self.next() == "end": 
                self.loop -= 1
                if self.loop <= 0:
                    return "end"
                else:
                    self.sprite_index = 0
            self.frame_counter = 0
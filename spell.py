import os
import numpy as np
import pygame

class Spell():
    
    def __init__(self, animation_folder:str, damage, from_player, to_player, size=10, velocity=1):
        self.size = size
        self.damage = damage
        self.from_player = from_player
        self.to_player = to_player
                
        self.animation_folder = "animations/" + animation_folder # animations/fire-ball_20
        self.sprites_list = os.listdir("animations/"+self.animation_folder) # animations/fire-ball_20/*
        self.update_image()
        self.sprite_index = 0
        self.frame_counter = 0
        self.animation_speed = int(self.animation_folder.split('_')[-1]) # nb of frame before update
        self.velocity = velocity # pixel per frame
        self.position = self.from_player.position
        
    def update(self):
        self.position = (self.position[0]+self.velocity, self.position[1])
        if self.position[0] >= self.to_player: return "shooted"
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites_list)
            self.update_image(self.animation_folder + "/" + self.sprites_list[self.sprite_index])
        
    def update_image(self, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, np.array((1,1))*self.size)
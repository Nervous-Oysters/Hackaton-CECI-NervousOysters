import os
import numpy as np
import pygame
from player import Player

class Animation:
    
    def __init__(self, animation_folder:str, player:Player, size=100, velocity=10):
        self.size = size
        self.player = player
        self.position = player.position
        
        self.animation_folder = "animations/" + animation_folder # animations/fire-ball_10
        self.sprites_list = os.listdir(self.animation_folder) # animations/fire-ball_10/*
        self.sprite_index = 0
        self.frame_counter = 0
        self.update_image(self.animation_folder + "/" + self.sprites_list[self.sprite_index])
        self.animation_speed = int(self.animation_folder.split('_')[-1]) # nb of frame before update
        self.velocity = velocity # pixel per frame
        
    def update_image(self, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, np.array((1,1))*self.size)
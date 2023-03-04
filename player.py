import pygame
import json
import os
import numpy as np


def load_json(filename):
    with open(filename) as file:
        return json.load(file)


class Player():

    def __init__(self, filename, sprites_folder, position, direction, animation="t-pose_60", size=100):
        player_characteristics = load_json(filename)
        self.name = player_characteristics.get("name")
        self.pv = player_characteristics.get("pv")
        self.stats = player_characteristics.get("stats")

        self.size = size
        self.sprites_folder = sprites_folder # example : Hubert
        self.sprites_folder_list = os.listdir(self.sprites_folder) # Hubert/*        
        self.current_animation = self.sprites_folder + animation # example : Hubert/t-pose_60
        self.sprites_list = os.listdir(self.current_animation) # Hubert/t-pose_60/*
        self.sprite_index = 0
        self.update_image(self.current_animation + "/" + self.sprites_list[self.sprite_index])
        self.animation_speed = int(self.current_animation.split('_')[-1]) # nb of frame before update
        self.frame_counter = 0

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
        return self.name

    def get_animations(self):
        return self.animations

    def get_pos(self):
        return self.position

    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            self.frame_counter = 0
            self.sprite_index = (self.sprite_index + 1) % len(self.sprites_list)
            self.update_image(self.current_animation + "/" + self.sprites_list[self.sprite_index])
            
    def change_animation(self, animation:str):
        self.current_animation = self.sprites_folder + animation # example : Hubert/t-pose_60
        self.sprites_list = os.listdir(self.current_animation) # Hubert/t-pose_60/*
        self.sprite_index = 0 
        self.update_image(self.current_animation + "/" + self.sprites_list[self.sprite_index])
        self.animation_speed = int(self.current_animation.split('_')[-1]) # nb of frame before update
        self.frame_counter = 0
    
    def update_image(self, path):
        self.image = pygame.image.load(path)
        self.image = pygame.transform.scale(self.image, np.array((1,1))*self.size)
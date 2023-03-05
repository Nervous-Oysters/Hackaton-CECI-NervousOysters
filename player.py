import pygame
import json
import os
import numpy as np
import Mainpipe

def load_json(filename):
    with open(filename) as file:
        return json.load(file)


class Player():

    def __init__(self, filename, sprites_folder, position, bar_position, direction:bool, pose, size=100, animation="t-pose_60"):
        player_characteristics = load_json(filename)
        self.name = player_characteristics.get("name")
        self.pv = player_characteristics.get("pv")
        self.max_pv = self.pv
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
        self.bar_position = bar_position
        self.health_bar = self.get_health_bar()

        self.pose = pose
        self.choice = ["", 0]

        self.animations = player_characteristics.get("animations")

    def damage(self, amount):
        self.pv -= amount
        return self.is_dead()
        
    def is_dead(self):
        return self.pv <= 0
    
    def get_health_bar(self):
        return pygame.Rect(self.bar_position[0], self.bar_position[1], self.size*(self.pv/self.max_pv), self.size/5)

    def update(self, pose):
        self.pose = pose
        if Mainpipe.defense_move1(self.pose):
            if self.choice[0] =="move1": self.choice[1] += 1
            else: self.choice = ["move1", 1]
        if Mainpipe.defense_move2(self.pose):
            if self.choice[0] =="move2": self.choice[1] += 1
            else: self.choice = ["move2", 1]
        if Mainpipe.defense_move3(self.pose):
            if self.choice[0] =="move3": self.choice[1] += 1
            else: self.choice = ["move3", 1]
            
        self.health_bar = self.get_health_bar()
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
        
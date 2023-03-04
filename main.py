import pygame
import pygame_menu

import voice_recognition
from player import Player
from spell import Spell
import numpy as np
import speech_recognition as sr
import pyaudio
pa = pyaudio.PyAudio()
chosen_device_index = -1
for x in range(0,pa.get_device_count()):
    info = pa.get_device_info_by_index(x)
    print(pa.get_device_info_by_index(x))
    if info["name"] == "pulse":
        chosen_device_index = info["index"]
        print("Chosen index: ", chosen_device_index)


recognizer = sr.Recognizer()
microphone = sr.Microphone(8)

player_list = ["penguin", "bear"]


def get_player_name():
    player_choice = voice_recognition.recognize_speech_from_mic(recognizer, microphone)
    # player_choice_list = player_choice.split(" ")
    for alternative in player_choice["transcription"]["alternative"]:
        current = alternative["transcript"].split(" ")
        for word in current:
            if word.lower() in player_list:
                return word


def set_difficulty(*args, **kwargs):
    pass


class Game:
    def __init__(self, screen, background, player1: Player, player2: Player) -> None:
        self.screen = screen
        self.background = background
        self.clock = pygame.time.Clock()
        self.running = True
        self.player1 = player1
        self.player2 = player2
        self.spells = [] # contains all objects Spell
        
        
    def handling_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.spells.append(Spell("fire-ball_10", 5, self.player1, self.player2, self.player1.size))
                    if event.key == pygame.K_RIGHT:
                        self.spells.append(Spell("fire-ball_10", 5, self.player2, self.player1, self.player1.size))
                    
    def update(self):
        self.player1.update()
        self.player2.update()
        to_remove = []
        for spell in self.spells:
            if spell.update() == "shooted": 
                to_remove.append(spell)
                if spell.apply_damage():
                    # is dead
                    pass
        for remove in to_remove:
            self.spells.remove(remove)
                
    
    def display(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.player1.image, self.player1.position)
        self.screen.blit(self.player2.image, self.player2.position)
        color = (0, 204, 0)
        pygame.draw.rect(screen, color, self.player1.health_bar)
        pygame.draw.rect(screen, color, self.player2.health_bar)
        for spell in self.spells:
            self.screen.blit(spell.image, spell.position)
        pygame.display.flip()
        
    
    
    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)
            

screen_size = (1920, 1080)
            
if __name__ == "__main__":
    players_size = screen_size[0]/10
    p1_pos = (screen_size[0]/10, screen_size[1]*2/3)
    p1_bar_pos = (screen_size[0]/5, screen_size[1]/10)
    print(f"pos 1 : {p1_pos}, bar1 : {p1_bar_pos}")
    p1 = Player("players/example.json", "sprites/", p1_pos, p1_bar_pos, True, players_size)
    p2_pos = (screen_size[0] - p1_pos[0] - players_size, p1_pos[1])
    p2_bar_pos = (screen_size[0] - p1_bar_pos[0] - players_size, p1_bar_pos[1])
    print(f"pos 2 : {p2_pos}, bar2 : {p2_bar_pos}")
    p2 = Player("players/example.json", "sprites/", p2_pos, p2_bar_pos, True, players_size)
    bg = pygame.image.load("background.jpg")
    bg = pygame.transform.scale(bg, screen_size) # transform, doesn't cut    
    
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    game = Game(screen, bg, p1, p2)
    game.run()
    pygame.quit()
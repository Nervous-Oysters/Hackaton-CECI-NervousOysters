import threading

import pygame
import tensorflow as tf
import tensorflow_hub as hub
import cv2
import Mainpipe
from player import Player
from spell import Spell
import numpy as np


class Game:
    def __init__(self, screen, screen_size, background, menu, player1=None, player2=None) -> None:
        self.screen = screen
        self.background = background
        self.menu = menu
        self.clock = pygame.time.Clock()
        self.running = True
        self.player1 = player1
        self.p1_choice = ["", 0]
        self.player2 = player2
        self.p2_choice = ["", 0]
        self.spells = []  # contains all objects Spell
        self.on_menu = True
        self.screen_size = screen_size

        self.model = hub.load('movenet_multipose_lightning_1')
        self.movenet = self.model.signatures['serving_default']
        self.webcam = cv2.VideoCapture(0)
        self.pose = None

        self.turn = False
        self.wand_on = pygame.image.load("images/wand_on.png")
        self.wand_off = pygame.image.load("images/wand_off.png")

        self.intro_time = 180

        self.music_queue_launched = False

    def handling_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                case pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.spells.append(Spell("fire-ball_10", 5, self.player1, self.player2, self.player1.size))
                        self.player1.music_queue.append({"path": "sounds/fire.wav", "loop": 0})
                    if event.key == pygame.K_RIGHT:
                        self.spells.append(Spell("fire-ball_10", 5, self.player2, self.player1, self.player2.size))
                        self.player2.music_queue.append({"path": "sounds/earth.wav", "loop": 0})

    def update(self):
        self.handle_turn()
        cam = self.handle_cam()
        self.player1.update(cam["left"])
        self.player2.update(cam["right"])
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
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.player1.image, self.player1.position)
        self.screen.blit(self.player2.image, self.player2.position)
        color = (0, 204, 0)
        pygame.draw.rect(screen, color, self.player1.health_bar)
        pygame.draw.rect(screen, color, self.player2.health_bar)
        for spell in self.spells:
            self.screen.blit(spell.image, spell.position[1])
        pygame.display.flip()

    def handle_turn(self):
        if self.player1 is None or self.player2 is None:
            return
        if not self.player1.is_my_turn and not self.player2.is_my_turn:
            if not self.turn:
                self.player1.start_turn()
                self.turn = True
            else:
                self.player2.start_turn()
                self.turn = False
        if self.turn:
            self.screen.blit(self.wand_on, (self.player1.bar_position[1], self.player1.bar_position[1] + 32))
            self.screen.blit(self.wand_off, (self.player2.bar_position[0], self.player2.bar_position[0] + 32))
        else:
            self.screen.blit(self.wand_on, (self.player2.bar_position[0] -32 , self.player2.bar_position[0]))
            self.screen.blit(self.wand_off, (self.player1.bar_position[1], self.player1.bar_position[1] + 32))

    def handle_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.on_menu = False
                self.running = False
        cam = self.handle_cam()
        choose1 = 0
        if self.player1 == None:
            choose1 = Mainpipe.choose_player(cam["left"])
            print(choose1)
        else:
            print(f"Player 1 choosed : {self.p1_choice[0]}")
        if choose1:
            if self.p1_choice[0] == choose1:
                self.p1_choice[1] += 1
                if self.p1_choice[1] >= 120:  # 2 secondes
                    self.set_p1(choose1, cam["left"])
            else:
                self.p1_choice = [choose1, 0]

        choose2 = 0
        if self.player2 == None:
            choose2 = Mainpipe.choose_player(cam["right"])
            print(choose2)
        else:
            print(f"Player 2 choosed : {self.p2_choice[0]}")
        if choose2:
            if self.p2_choice[0] == choose2:
                self.p2_choice[1] += 1
                if self.p2_choice[1] >= 120:  # 2 secondes
                    self.set_p2(choose2, cam["right"])
            else:
                self.p2_choice = [choose2, 0]

    def set_player(self, choose, pose, position: str):
        players_size = self.screen_size[0] * 0.20
        if position == "left":
            direction = True
            player_position = (self.screen_size[0] / 10, self.screen_size[1] * 0.5)
            bar_postition = (self.screen_size[0] / 18, self.screen_size[1] / 15)
        elif position == "right":
            direction = False
            player_position = (self.screen_size[0] * 9 / 10 - players_size * 942, self.screen_size[1] * 0.5)
            bar_postition = (self.screen_size[0] * 17 / 18 - players_size * 942, self.screen_size[1] / 15)
        else:
            raise Exception("Error in setting characters")
        match choose:
            case "up":
                return Player("players/daniel.json", "sprites/daniel/", player_position, bar_postition, direction, pose,
                              players_size)
            case "right":
                return Player("players/louise.json", "sprites/louise/", player_position, bar_postition, direction, pose,
                              players_size)
            case "left":
                return Player("players/jacques.json", "sprites/jacques/", player_position, bar_postition, direction,
                              pose, players_size)
            case _:
                raise Exception("Error in choose of characters")

    def set_p1(self, choose, pose):
        self.player1 = self.set_player(choose, pose, "left")

    def set_p2(self, choose, pose):
        self.player2 = self.set_player(choose, pose, "right")

    def handle_cam(self):
        ret, frame = self.webcam.read()
        image = frame.copy()
        image = tf.expand_dims(image, axis=0)
        # Resize and pad the image to keep the aspect ratio and fit the expected size.
        image = tf.cast(tf.image.resize_with_pad(image, 192, 192), dtype=tf.int32)
        results = self.movenet(image)
        keypoints_with_scores = results['output_0'].numpy()[:, :, :51].reshape((6, 17, 3))
        players_pose = {}
        if keypoints_with_scores[0][0][1] < keypoints_with_scores[1][0][1]:
            players_pose["left"] = keypoints_with_scores[0]
            players_pose["right"] = keypoints_with_scores[1]
        else:
            players_pose["left"] = keypoints_with_scores[1]
            players_pose["right"] = keypoints_with_scores[0]
        return players_pose

    def handle_music_intro(self):
        for music in [{"path": "sounds/spawn.wav", "loop": 0}, {"path": "sounds/background_music.wav", "loop": -1}]:
            pygame.mixer.Channel(0).play(pygame.mixer.Sound(music["path"]), loops=music["loop"])
            if music["loop"] != -1:
                while pygame.mixer.get_busy():
                    pass

    def handle_music_p1(self):
        while True:
            if len(self.player1.music_queue) <= 0: continue
            music = self.player1.music_queue.pop(0)
            pygame.mixer.Channel(1).play(pygame.mixer.Sound(music["path"]), loops=music["loop"])
            if music["loop"] != -1:
                while pygame.mixer.get_busy():
                    pass

    def handle_music_p2(self):
        while True:
            if len(self.player2.music_queue) <= 0: continue
            music = self.player2.music_queue.pop(0)
            pygame.mixer.Channel(2).player(pygame.mixer.Sound(music["path"]), loops=music["loop"])
            if music["loop"] != -1:
                while pygame.mixer.get_busy():
                    pass

    def run(self):
        music_thread_intro = threading.Thread(target=self.handle_music_intro)
        try:
            music_thread_intro.start()
        except:
            pass
        while self.running:
            while self.player1 == None or self.player2 == None:
                self.handle_menu()
                self.screen.blit(self.menu, (0, 0))
                pygame.display.flip()
                self.clock.tick(60)
            if not self.music_queue_launched:
                music_thread_p1 = threading.Thread(target=self.handle_music_p1)
                music_thread_p2 = threading.Thread(target=self.handle_music_p2)
                try:
                    music_thread_p1.start()
                    music_thread_p2.start()
                except:
                    pass
                self.music_queue_launched = True
                
            while self.intro_time >= 0:
                self.player1.update(0)
                self.player2.update(0)
                if self.intro_time == 0:
                    self.player1.change_animation("fighting_40")
                    self.player2.change_animation("fighting_40")
                self.intro_time -= 1
                self.display()
                #self.clock.tick(60)
                print(self.intro_time)
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)


screen_size = (1080, 720)

if __name__ == "__main__":
    bg = pygame.image.load("background1.png")
    bg = pygame.transform.scale(bg, screen_size)  # transform, doesn't cut
    menu = pygame.image.load("menu.jpg")
    menu = pygame.transform.scale(menu, screen_size)

    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    # p1 = Player("players/example.json", "sprites/", (100, 500), (0, 0), True, None, 100)
    p2 = Player("players/daniel.json", "sprites/daniel/", (900, 500), (0, 0), False, None, 100)
    game = Game(screen, screen_size, bg, menu, None, p2)
    game.run()
    game.webcam.release()
    pygame.quit()

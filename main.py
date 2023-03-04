import pygame
from player import Player
from spell import Spell
import numpy as np

class Game:
    def __init__(self, screen, background, player1:Player, player2:Player) -> None:
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
    p1 = Player("players/example.json", "sprites/", (100,500), (200, 100), True, screen_size[0]/10)
    p2 = Player("players/example.json", "sprites/", (800,500), (600, 100), True, screen_size[0]/10)
    bg = pygame.image.load("background.jpg")
    bg = pygame.transform.scale(bg, screen_size) # transform, doesn't cut    
    
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    game = Game(screen, bg, p1, p2)
    game.run()
    pygame.quit()
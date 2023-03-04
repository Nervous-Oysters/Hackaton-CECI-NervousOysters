import pygame

class Game:
    def __init__(self, screen) -> None:
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True
        
    def handling_events(self):
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    self.running = False
                    
    def update(self):
        pass
    
    def display(self):
        pass
    
    def run(self):
        while self.running:
            self.handling_events()
            self.update()
            self.display()
            self.clock.tick(60)
            
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((1080, 720))
    game = Game(screen)
    game.run()
    pygame.quit()
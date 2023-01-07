import pygame

import mainmenu
import overworld
import candy
import snake


pygame.init()
screen = pygame.display.set_mode((1280, 720), flags=pygame.SCALED)
pygame.display.set_caption("Overhyped")
ico = pygame.image.load("./resources/graphics/bananas.png")
pygame.display.set_icon(ico)
clock = pygame.time.Clock()
pygame.mixer.init()
theme = pygame.mixer.Sound("./resources/audio/theme.wav")
theme.set_volume(0.75)
theme.play(-1, 0, 1000)

mainmenu.Game(screen, clock).run()
overworld.Game(screen, clock, 0).run()
overworld.Game(screen, clock, 1).run()
candy.Game(screen, clock).run()
overworld.Game(screen, clock, 2).run()
overworld.Game(screen, clock, 3).run()
snake.Game(screen, clock).run()
overworld.Game(screen, clock, 4).run()
overworld.Game(screen, clock, 5).run()

theme.stop()
pygame.quit()

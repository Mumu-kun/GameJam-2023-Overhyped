import pygame

from sys import exit as sys_exit


class Game:
    def __init__(self, screen: pygame.surface.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock
        text_font_tiny = pygame.font.Font("resources/font/FreePixel.ttf", 16)
        text_font_small = pygame.font.Font("resources/font/FreePixel.ttf", 60)
        text_font = pygame.font.Font("resources/font/FreePixel.ttf", 120)

        self.title_surf = text_font.render("Overhyped", False, "white")
        self.title_rect = self.title_surf.get_rect(center=(640, 250))

        self.play_surf = text_font_small.render("Play", False, "white")
        self.play_rect = self.play_surf.get_rect(center=(640, 450))

        self.kg_surf = text_font_tiny.render("KOLAGACH", False, "grey15")
        self.kg_rect = self.kg_surf.get_rect(bottomright=(1278, 718))

    def run(self):
        self.running = True

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys_exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT):
                        pygame.display.toggle_fullscreen()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.play_rect.collidepoint(event.pos):
                        self.running = False

            self.screen.fill("black")
            self.screen.blit(self.title_surf, self.title_rect)
            self.screen.blit(self.play_surf, self.play_rect)
            self.play_rect.inflate_ip(20 * 2, 20)
            pygame.draw.rect(self.screen, "white", self.play_rect, 4, 2)
            self.play_rect.inflate_ip(-20 * 2, -20)
            self.screen.blit(self.kg_surf, self.kg_rect)

            pygame.display.update()
            self.clock.tick(60)

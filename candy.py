import pygame
from random import randint, choice, random as randfloat


class Pig(pygame.sprite.Sprite):
    def __init__(self, pig_frames):
        super().__init__()
        self.frames = pig_frames
        self.frame_ind = 0

        self.candy_image = pygame.image.load(
            f"resources/graphics/candy/candy{randint(1,3)}-p.png"
        ).convert_alpha()
        self.candy_rect = self.candy_image.get_rect()

        self.dir = -1

        self.image: pygame.surface.Surface = pig_frames[0]
        self.rect = self.image.get_rect(bottomleft=(1300, 645))

        self.vx = -randfloat() * 4 - 3

    def physics(self):
        self.rect.x += self.vx

    def animation(self):
        self.frame_ind += 0.2
        if self.frame_ind > len(self.frames):
            self.frame_ind = 0
        self.image = self.frames[int(self.frame_ind)]

    def changeDir(self, dir):
        if dir == self.dir:
            return
        else:
            self.dir = dir
            for i in range(len(self.frames)):
                self.frames[i] = pygame.transform.flip(self.frames[i], True, False)

    def outOfScreen(self):
        if self.rect.right < 350:
            self.kill()

    def roam(self):
        if self.rect.left < 400:
            self.vx = 10
            self.changeDir(1)
        elif self.rect.right > 1200:
            self.vx = -10
            self.changeDir(-1)

    def drawCandy(self, screen):
        self.candy_rect.midbottom = self.rect.midtop
        self.candy_rect.y += 4
        screen.blit(self.candy_image, self.candy_rect)

    def update(self, game_state):
        self.animation()
        self.physics()
        if game_state == 0:
            self.outOfScreen()
        elif game_state == 1:
            self.roam()


class Bird(pygame.sprite.Sprite):
    def __init__(self, spawn_pos, frames, dead_frames, type=0) -> None:
        super().__init__()
        self.type = type
        self.new = True
        self.alive = True

        self.frames = frames
        self.frame_ind = 0
        self.dead_frames = dead_frames

        self.vx = 0
        self.vy = 0
        self.ay = 1

        self.image: pygame.surface.Surface = self.frames[self.frame_ind]
        self.rect = self.image.get_rect(center=spawn_pos)

    def forceToMouse(self):
        self.rect.center = tuple(map(sum, zip(pygame.mouse.get_pos(), (5, -5))))

    def setVelocity(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def physics(self):
        self.rect.x += self.vx

        self.vy += self.ay
        self.rect.y += self.vy

    def animation(self):
        self.frame_ind += 0.2
        if self.frame_ind > len(self.frames):
            if self.alive:
                self.frame_ind = 0
            else:
                self.kill()
                return
        self.image = self.frames[int(self.frame_ind)]

    def outOfScreenCheck(self):
        if not (-self.rect.width < self.rect.left < 1280) or not (
            -self.rect.height < self.rect.top < 630
        ):
            self.death()

    def death(self):
        self.vx = 0
        self.vy = -8
        self.alive = False
        self.frames = self.dead_frames

    def update(self):
        self.animation()
        self.outOfScreenCheck()
        if not self.new:
            self.physics()
        else:
            self.forceToMouse()


class Candy:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.pic = [0] * 3
        self.x = [0] * 3
        self.y = [0] * 3
        self.change_y = [0] * 3
        self.type = 0
        self.poison = 0
        self.image = [
            pygame.image.load("resources/graphics/candy/candy1.png").convert_alpha(),
            pygame.image.load("resources/graphics/candy/candy2.png").convert_alpha(),
            pygame.image.load("resources/graphics/candy/candy3.png").convert_alpha(),
        ]

    def position(self):
        for i in range(3):
            if i == 0:
                self.x[i] = randint(426, 1064)
            else:
                self.x[i] = self.x[i - 1] + 64
            self.y[i] = -70
            self.change_y[i] = (randfloat()) * 2 + 3
            self.pic[i] = self.image[self.type]
        self.poison = choice([0, 1, 1, 1, 1, 2, 2, 2])
        self.pic[self.poison] = pygame.image.load(
            f"resources/graphics/candy/candy{1+self.type}-p.png"
        ).convert_alpha()

    def hit(self, i):
        self.y[i] = -70
        self.change_y[i] = 0

    def move(self):
        for i in range(3):
            self.y[i] += self.change_y[i]
            if self.y[i] >= 600:
                self.change_y[i] = 0

    def draw(self):
        for i in range(3):
            self.parent_screen.blit(self.pic[i], (self.x[i], self.y[i]))


class Game:
    def __init__(self, screen: pygame.surface.Surface, clock: pygame.time.Clock):
        self.screen = screen
        self.clock = clock

        self.text_font_small = pygame.font.Font("resources/font/FreePixel.ttf", 50)
        self.text_font = pygame.font.Font("resources/font/FreePixel.ttf", 200)

        ## Background
        self.background = pygame.image.load(
            "resources/graphics/candy_bg/background.png"
        ).convert()
        self.ground = pygame.image.load(
            "resources/graphics/candy_bg/ground.png"
        ).convert_alpha()
        self.ground_rect = self.ground.get_rect(bottomleft=(0, 720))

        ## Misc
        self.timer = 0
        self.game_state = -1
        self.gravity_bird = 1
        self.spawn_pos = (200, 410)
        self.health = 20
        self.health_real = 20
        self.heal_event_type = pygame.USEREVENT + 10
        self.dmg_event_type = pygame.USEREVENT + 11

        ## Slingshot
        self.slingshot_far = pygame.image.load(
            "resources/graphics/slingshot/slingshot_far-small.png"
        ).convert_alpha()
        self.slingshot_close = pygame.image.load(
            "resources/graphics/slingshot/slingshot_close-small.png"
        ).convert_alpha()
        self.slingshot_rect = self.slingshot_far.get_rect(midbottom=(200, 620))
        self.slingshot_head = pygame.rect.Rect((0, 0), (120, 120))
        self.slingshot_head.topright = self.spawn_pos
        self.slingshot_head.right += 45
        self.slingshot_head.top -= 40

        ## Candy
        self.candy = Candy(self.screen)
        self.candy.position()

        ## Bird
        self.bird_frames_list = []
        for j in range(3):
            bird_frame = []
            for i in range(4):
                bird_frame.append(
                    pygame.transform.rotozoom(
                        pygame.transform.flip(
                            pygame.image.load(
                                f"resources/graphics/birds/bird{j+1}0{i}.png"
                            ).convert_alpha(),
                            True,
                            False,
                        ),
                        0,
                        1.2,
                    )
                )
            self.bird_frames_list.append(bird_frame)

        self.bird_dead_frames_list = []
        for j in range(3):
            bird_dead_frame = []
            for i in range(4):
                bird_dead_frame.append(
                    pygame.transform.rotozoom(
                        pygame.transform.flip(
                            pygame.image.load(
                                f"resources/graphics/birds/birddeath{j+1}0{i}.png"
                            ).convert_alpha(),
                            True,
                            False,
                        ),
                        0,
                        1.2,
                    )
                )
            self.bird_dead_frames_list.append(bird_dead_frame)

        self.birds = pygame.sprite.Group()
        self.new_bird: pygame.sprite.Sprite = None

        self.spawn_flag = False

        ## Pig
        self.pig_frames = []
        for i in range(4):
            self.pig_frames.append(
                pygame.transform.rotozoom(
                    pygame.image.load(
                        f"resources/graphics/pig/pig10{i}.png"
                    ).convert_alpha(),
                    0,
                    1.5,
                )
            )

        self.pigs = pygame.sprite.Group()
        self.pigs.add(Pig(self.pig_frames))

        self.pig_spawn_event = pygame.event.Event(pygame.USEREVENT + 1)
        self.pig_spawn_timer = pygame.time.set_timer(self.pig_spawn_event, 200, 10)

    def drawHealth(self):
        health_rect = pygame.rect.Rect((0, 0), (20, self.health * 5))
        health_rect.bottomright = (1260, 550)

        health_rect_total = pygame.rect.Rect((0, 0), (30, 100 * 5))
        health_rect_total.midbottom = health_rect.midbottom
        health_rect_total.bottom += 5

        if self.health_real < self.health:
            pygame.draw.rect(self.screen, "orangered3", health_rect)
        else:
            pygame.draw.rect(self.screen, "olivedrab4", health_rect)
        pygame.draw.rect(self.screen, "grey20", health_rect_total, 5, 2)

    def update(self):
        if self.game_state == 0:
            self.pigs.update(0)
            collide = pygame.sprite.groupcollide(self.birds, self.pigs, False, False)
            for key in collide:
                key.death()
            if not len(self.pigs.sprites()):
                self.game_state = 1
                self.pigs.add(Pig(self.pig_frames))

        if self.game_state == 1:
            self.pigs.update(1)
            self.candy.move()
            candy_left = 3
            candy_rect_list = []
            for i in range(3):
                candy_surf = self.candy.pic[i]
                candy_rect_list.append(
                    candy_surf.get_rect(topleft=(self.candy.x[i], self.candy.y[i]))
                )
                if self.candy.change_y[i] == 0 and self.candy.y[i] < 0:
                    candy_left -= 1
            if candy_left == 0:
                self.candy.type = randint(0, 2)
                self.candy.position()

            ## Bird Pig Collision
            collide = pygame.sprite.groupcollide(self.birds, self.pigs, False, False)
            for key in collide:
                key.death()

            ## Bird Candy Collision
            for bird in self.birds:
                collide2 = bird.rect.collidelist(candy_rect_list)
                if collide2 != -1:
                    bird.death()
                    self.candy.hit(collide2)

            ## Pig Candy Collision
            collide3 = self.pigs.sprites()[0].rect.collidelist(candy_rect_list)
            if collide3 != -1:
                self.candy.hit(collide3)
                if collide3 == self.candy.poison:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 11))
                else:
                    pygame.event.post(pygame.event.Event(pygame.USEREVENT + 10))

        self.birds.update()

        ## Health
        if self.health_real > self.health:
            self.health += 1
        if self.health_real < self.health:
            self.health -= 1

    def frame(self):
        self.screen.blit(self.background, (0, 0))

        if not self.spawn_flag:
            pygame.draw.line(
                self.screen,
                "red4",
                tuple(map(sum, zip(self.spawn_pos, (-25, 0)))),
                tuple(map(sum, zip(self.spawn_pos, (25, 0)))),
            )

        if self.spawn_flag:
            pygame.draw.line(
                self.screen,
                "red4",
                tuple(map(sum, zip(self.spawn_pos, (25, 0)))),
                pygame.mouse.get_pos(),
            )
        if self.game_state == 1:
            self.candy.draw()
        self.pigs.draw(self.screen)
        self.birds.draw(self.screen)
        if self.game_state == 0:
            for pig in self.pigs.sprites():
                pig.drawCandy(self.screen)

        self.screen.blit(self.slingshot_far, self.slingshot_rect)
        self.screen.blit(self.ground, self.ground_rect)

        if self.spawn_flag:
            pygame.draw.line(
                self.screen,
                "red4",
                tuple(map(sum, zip(self.spawn_pos, (-25, 0)))),
                pygame.mouse.get_pos(),
            )
        self.screen.blit(self.slingshot_close, self.slingshot_rect)

        if self.spawn_flag:
            vx = (self.spawn_pos[0] - pygame.mouse.get_pos()[0]) / 3
            vy = (self.spawn_pos[1] - pygame.mouse.get_pos()[1]) / 3
            x, y = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            for i in range(50):
                pygame.draw.circle(self.screen, "black", (x, y), 3)
                x += vx
                vy += 1
                y += vy
        if self.game_state == 1:
            self.drawHealth()


    def gameStart(self, timer):
        text = "Don't let him get poisoned!"
        text_surf = self.text_font_small.render(text, False, "White")
        if timer <= 135:
            text_surf = self.text_font_small.render(
                text[: int(timer / 5)], False, "White"
            )
        elif 200 <= timer <= 335:
            text_surf = self.text_font_small.render(
                text[: int(27 - (timer - 200) / 5)], False, "White"
            )
        elif timer > 335:
            text_surf = self.text_font_small.render("", False, "White")

        text_rect = text_surf.get_rect(center=(640, 360))

        self.screen.fill("black")
        self.screen.blit(text_surf, text_rect)

    def gameOver(self, w):
        rect = pygame.rect.Rect((0, 0), (1280, 720))

        text_surf = None
        if self.health < 0:
            text_surf = self.text_font.render("You Lose", False, "White")
        else:
            text_surf = self.text_font.render("You Win", False, "White")
        text_rect = text_surf.get_rect(center=(640, 360))

        pygame.draw.rect(self.screen, "black", rect, w)

        pygame.draw.rect(self.screen, "black", text_rect)
        self.screen.blit(text_surf, text_rect)

    def eventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT):
                    pygame.display.toggle_fullscreen()

            if event == self.pig_spawn_event:
                self.pigs.add(Pig(self.pig_frames))
            if event.type == self.heal_event_type:
                self.health_real += 4
            if event.type == self.dmg_event_type:
                self.health_real -= 8

            if event.type == pygame.MOUSEBUTTONDOWN:
                if not self.spawn_flag and self.slingshot_head.collidepoint(event.pos):
                    type = randint(0, 2)
                    self.new_bird = Bird(
                        self.spawn_pos,
                        self.bird_frames_list[type],
                        self.bird_dead_frames_list[type],
                        type,
                    )
                    self.birds.add(self.new_bird)
                    self.spawn_flag = True

            if event.type == pygame.MOUSEBUTTONUP:
                if self.spawn_flag:
                    vx = (self.spawn_pos[0] - event.pos[0]) / 3
                    vy = (self.spawn_pos[1] - event.pos[1]) / 3
                    self.new_bird.setVelocity(vx, vy)
                    self.new_bird.new = False
                    self.new_bird = None
                    self.spawn_flag = False

    def run(self):
        self.running = True
        self.timer = 0
        # Game loop
        while self.running:
            self.eventHandle()
            if self.game_state == -1:
                self.gameStart(self.timer)
                self.timer += 1
                if self.timer >= 380:
                    self.timer = 0
                    self.game_state = 0

            if 0 <= self.game_state < 2:
                self.update()
                self.frame()

            if self.health >= 100 or self.health < 0:
                self.game_state = 2
            if self.game_state == 2:
                self.timer += 5
                self.gameOver(self.timer)
                if self.timer >= 600:
                    if self.health_real < 0:
                        self.__init__(self.screen, self.clock)
                    else:
                        self.running = False
            pygame.display.update()
            self.clock.tick(60)

import pygame
from sys import exit as sys_exit


class Teacher(pygame.sprite.Sprite):
    def __init__(self, id: str, pos) -> None:
        super().__init__()
        self.image = pygame.image.load(
            f"resources/graphics/characters/teacher{id}.png"
        ).convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, walkR: list, dir: str):
        super().__init__()
        self.walkR = walkR
        self.walkL = walkR.copy()
        for i in range(len(self.walkL)):
            self.walkL[i] = pygame.transform.flip(self.walkL[i], True, False)
        self.frame_ind = 0

        self.frames = self.walkR if dir.lower() == "r" else self.walkL
        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=pos)

        self.vel = 5
        self.dir = dir
        self.walking = False

    def right(self):
        if self.dir != "r":
            self.frames = self.walkR
            self.dir = "r"

        if self.rect.left >= 1120 and (self.rect.top >= 280 or self.rect.top <= 220):
            self.rect.left = 1120
        else:
            self.rect.left += self.vel

    def left(self):
        if self.dir != "l":
            self.frames = self.walkL
            self.dir = "l"

        if self.rect.left <= 110:
            self.rect.left = 110
        else:
            self.rect.left -= self.vel

    def up(self):
        if self.rect.top <= 80:
            self.rect.top = 80
        else:
            self.rect.top -= self.vel

    def down(self):
        if self.rect.top >= 450:
            self.rect.top = 450
        else:
            self.rect.top += self.vel

    def animation(self):
        self.frame_ind += 0.2
        if self.frame_ind > len(self.frames):
            self.frame_ind = 0
        self.image = self.frames[int(self.frame_ind)]

    def update(self, *args, **kwargs):
        if self.walking:
            self.animation()

        keys = pygame.key.get_pressed()
        self.walking = False
        if keys[pygame.K_LEFT]:
            self.left()
            self.walking = True
        if keys[pygame.K_RIGHT]:
            self.right()
            self.walking = True
        if keys[pygame.K_UP]:
            self.up()
            self.walking = True
        if keys[pygame.K_DOWN]:
            self.down()
            self.walking = True


class Game:
    def __init__(self, screen, clock, state):
        self.screen = screen
        self.clock = clock

        ## Flags
        self.game_state = state
        self.running = False
        self.moveable = False
        self.dialogueBoxBottom = 870
        self.stage_dialogue = False

        self.bg_base = pygame.image.load(
            f"resources/graphics/overworld/bg{0 if self.game_state == 0 else 1}_base.png"
        ).convert()
        self.bg_top = pygame.image.load(
            f"resources/graphics/overworld/bg{0 if self.game_state == 0 else 1}_top.png"
        ).convert_alpha()

        self.text_font = pygame.font.Font("resources/font/FreePixel.ttf", 48)

        ## Player
        walkR = []
        for i in range(5):
            walkR.append(
                pygame.image.load(
                    f"resources/graphics/player/playerwalkR{i}.png"
                ).convert_alpha(),
            )
        spawn_pos_list = [
            (360, 370),
            (0, 258),
            (1000, 250),
            (0, 258),
            (1000, 250),
            (0, 258),
        ]
        spawn_dir_list = ["l", "r", "r", "r", "r", "r"]
        self.player = pygame.sprite.GroupSingle(
            Player(
                spawn_pos_list[self.game_state], walkR, spawn_dir_list[self.game_state]
            )
        )

        ## Teacher
        spawn_pos_list_teacher = [
            (250, 374),
            (1048, 260),
            (-100, -100),
            (1048, 260),
            (-100, -100),
            (1048, 260),
        ]
        teacher_id_list = [0, 1, 1, 2, 2, 3]
        self.teacher = pygame.sprite.GroupSingle(
            Teacher(
                teacher_id_list[self.game_state],
                spawn_pos_list_teacher[self.game_state],
            )
        )

        if self.game_state > 0:
            self.moveable = True

        if self.game_state == 5:
            self.music = pygame.mixer.Sound("./resources/audio/music.mp3")
            self.music.set_volume(0.75)
            self.music_playing = False

    def dialogueEnter(self):
        box_rect = pygame.rect.Rect((0, 0), (1280, 150))
        box_rect.bottomleft = (0, self.dialogueBoxBottom)
        pygame.draw.rect(self.screen, "black", box_rect, 0, 2)
        pygame.draw.rect(self.screen, "grey25", box_rect, 8, 2)
        pygame.draw.rect(self.screen, "grey95", box_rect, 3, 2)
        if self.dialogueBoxBottom > 720:
            self.dialogueBoxBottom -= 5

    def dialogueEnd(self, text):
        box_rect = pygame.rect.Rect((0, 0), (1280, 150))
        box_rect.bottomleft = (0, self.dialogueBoxBottom)

        text_surf = self.text_font.render(text, False, "white")
        text_rect = text_surf.get_rect()
        text_rect.center = box_rect.center

        pygame.draw.rect(self.screen, "black", box_rect, 0, 2)
        pygame.draw.rect(self.screen, "grey25", box_rect, 8, 2)
        pygame.draw.rect(self.screen, "grey95", box_rect, 3, 2)
        self.screen.blit(text_surf, text_rect)
        if self.dialogueBoxBottom < 870:
            self.dialogueBoxBottom += 10

    def dialogue(self, text: str):

        box_rect = pygame.rect.Rect((0, 0), (1280, 150))
        box_rect.bottomleft = (0, 720)

        text_surf = self.text_font.render(text, False, "white")
        text_rect = text_surf.get_rect()
        text_rect.center = box_rect.center

        pygame.draw.rect(self.screen, "black", box_rect, 0, 2)
        pygame.draw.rect(self.screen, "grey25", box_rect, 8, 2)
        pygame.draw.rect(self.screen, "grey95", box_rect, 3, 2)
        self.screen.blit(text_surf, text_rect)

    def gameOver(self, w):
        rect = pygame.rect.Rect((0, 0), (1280, 720))
        pygame.draw.rect(self.screen, "black", rect, w)

    def update(self):
        if self.moveable:
            self.teacher.update()
            self.player.update()
            if pygame.sprite.groupcollide(self.player, self.teacher, False, False):
                self.stage_dialogue = True
                self.moveable = False
                self.timer = 0

    def eventHandle(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys_exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and (event.mod & pygame.KMOD_ALT):
                    pygame.display.toggle_fullscreen()

    def frame(self):
        self.screen.blit(self.bg_base, (0, 0))
        self.player.draw(self.screen)
        self.teacher.draw(self.screen)
        self.screen.blit(self.bg_top, (0, 0))

        if self.game_state % 2 == 0:
            pygame.draw.rect(
                self.screen, "black", pygame.rect.Rect((-40, 0), (1360, 720)), 40
            )

    def run(self):
        self.running = True

        self.timer = 0
        while self.running:
            self.eventHandle()
            self.update()
            self.frame()
            if self.game_state == 0:
                if 0 < self.timer <= 50:
                    self.dialogueEnter()
                elif 200 > self.timer:
                    self.dialogue("Mr.Bob: I'm very disappointed.")
                elif 300 > self.timer:
                    self.dialogue("Mr.Bob: I didn't expect this from you.")
                elif 400 > self.timer:
                    self.dialogue("Mr.Bob: I'll teach you a lesson.")
                elif 500 > self.timer:
                    self.dialogue("Mr.Bob: How about you go outside.")
                elif 600 > self.timer:
                    self.dialogue("Mr.Bob: You'll see how it feels-")
                elif 700 > self.timer:
                    self.dialogue("-when things don't go as you expect.")
                elif 730 > self.timer:
                    self.dialogueEnd("-when things don't go as you expect.")
                elif 830 > self.timer:
                    self.player.sprite.frames = self.player.sprite.walkR
                    self.player.sprite.rect.x += 10
                    self.player.sprite.animation()
                elif 930 > self.timer:
                    self.gameOver((self.timer - 830) * 6)
                else:
                    self.screen.fill("black")
                    self.running = False
            elif self.game_state == 1 and self.stage_dialogue:
                if 0 < self.timer <= 50:
                    self.dialogueEnter()
                elif 200 > self.timer:
                    self.dialogue("Ms.Alex: Why must birds and pigs be enemies?")
                elif 300 > self.timer:
                    self.dialogue("Ms.Alex: Why can't they just help each other?")
                elif 370 > self.timer:
                    self.dialogueEnd("Ms.Alex: Why can't they just help each other?")
                elif 470 > self.timer:
                    self.gameOver((self.timer - 370) * 6)
                else:
                    self.screen.fill("black")
                    self.running = False
            elif self.game_state == 2 or self.game_state == 4:
                if 0 < self.timer <= 20:
                    pass
                elif 100 > self.timer:
                    self.player.sprite.frames = self.player.sprite.walkR
                    self.player.sprite.rect.x += 5
                    self.player.sprite.animation()
                elif 200 > self.timer:
                    self.gameOver((self.timer - 100) * 6)
                elif self.timer > 200:
                    self.screen.fill("black")
                    self.running = False
            elif self.game_state == 3 and self.stage_dialogue:
                if 0 < self.timer <= 50:
                    self.dialogueEnter()
                elif 200 > self.timer:
                    self.dialogue("Ms.John: Snakes are tough pets to keep.")
                elif 300 > self.timer:
                    self.dialogue("Ms.John: How much should you feed them?")
                elif 320 > self.timer:
                    self.dialogue("Ms.John: Ouroboros!")
                elif 340 > self.timer:
                    self.dialogueEnd("Ms.John: Ouroboros!")
                elif 400 > self.timer:
                    self.gameOver((self.timer - 340) * 6)
                else:
                    self.screen.fill("black")
                    self.running = False
            elif self.game_state == 5 and self.stage_dialogue:
                if 0 < self.timer <= 50:
                    self.dialogueEnter()
                elif 200 > self.timer:
                    self.dialogue("Ms.Bob: Great Job! Here is the lesson-")
                elif 300 > self.timer:
                    self.dialogue("Ms.Bob: -you should always remember.")
                elif 432 > self.timer:
                    if not self.music_playing:
                        self.music.play()
                        self.music_playing = True
                    self.dialogue("Ms.Bob: Never gonna give you up")
                elif 576 > self.timer:
                    self.dialogue("Ms.Bob: Never gonna let you down")
                elif 810 > self.timer:
                    self.dialogue("Ms.Bob: Never gonna run around and desert you")
                elif 954 > self.timer:
                    self.dialogue("Ms.Bob: Never gonna make you cry")
                elif 1080 > self.timer:
                    self.dialogue("Ms.Bob: Never gonna say goodbye")
                elif 1320 > self.timer:
                    self.dialogue("Ms.Bob: Never gonna tell a lie and hurt you")
                elif 1420 > self.timer:
                    self.dialogue("Ms.Bob: Thank you!")
                elif 1450 > self.timer:
                    self.dialogueEnd("Ms.Bob: Thank you!")
                elif 1550 > self.timer:
                    self.gameOver((self.timer - 1450) * 6)
                else:
                    self.screen.fill("black")
                    self.running = False
            self.timer += 1

            pygame.display.update()
            self.clock.tick(60)

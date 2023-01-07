import pygame
from pygame.locals import *
import random
from sys import exit as sys_exit


class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/snake/food.png")
        self.parent_screen = parent_screen
        self.apple_number = 1
        self.x = [80] * self.apple_number
        self.y = [80] * self.apple_number

    def draw(self):
        for i in range(self.apple_number):
            self.parent_screen.blit(self.image, (self.x[i], self.y[i]))

    def move(self):
        if self.apple_number < 30:
            self.apple_number += 3
            for i in range(3):
                self.x.append(random.randint(1, 32) * 40)
                self.y.append((random.randint(1, 18) * 40))

        else:
            for i in range(self.apple_number):
                self.x[i] = random.randint(1, 32) * 40
                self.y[i] = random.randint(1, 18) * 40


class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/snake/body.png")
        self.head = pygame.image.load("resources/snake/Head_right.png")
        self.head_op = pygame.image.load("resources/snake/Head_right_op.png")
        self.x = [1] * length
        self.y = [1] * length
        self.direction = "right"
        self.n = True

    def decrease_length(self):
        self.length -= 1
        self.x.pop(-1)
        self.y.pop(-1)

    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        if self.n:
            self.parent_screen.blit(self.head, (self.x[0], self.y[0]))
            self.n = False
        else:
            self.parent_screen.blit(self.head_op, (self.x[0], self.y[0]))
            self.n = True
        for i in range(1, self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def move_left(self):
        self.direction = "left"
        self.head = pygame.image.load("resources/snake/Head_left.png")
        self.head_op = pygame.image.load("resources/snake/Head_left_op.png")

    def move_right(self):
        self.direction = "right"
        self.head = pygame.image.load("resources/snake/Head_right.png")
        self.head_op = pygame.image.load("resources/snake/Head_right_op.png")

    def move_up(self):
        self.direction = "up"
        self.head = pygame.image.load("resources/snake/Head_up.png")
        self.head_op = pygame.image.load("resources/snake/Head_up_op.png")

    def move_down(self):
        self.direction = "down"
        self.head = pygame.image.load("resources/snake/Head_down.png")
        self.head_op = pygame.image.load("resources/snake/Head_down_op.png")

    def walk(self):

        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == "left":
            self.x[0] -= 40
        if self.direction == "right":
            self.x[0] += 40
        if self.direction == "up":
            self.y[0] -= 40
        if self.direction == "down":
            self.y[0] += 40

        self.draw()


class Special_Food:
    def __init__(self, parent_screen):
        self.pic = pygame.image.load("resources/snake/op_food.png")
        self.x = 120
        self.y = 120
        self.parent_screen = parent_screen

    def draw(self):
        self.parent_screen.blit(self.pic, (self.x, self.y))

    def move(self):
        self.x = random.randint(1, 32) * 40
        self.y = random.randint(1, 18) * 40


class Game:
    def __init__(self, screen, clock):

        self.surface = screen
        self.clock = clock
        self.bg = pygame.image.load("resources/snake/map.png")
        self.snake = Snake(self.surface, 9)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.food = Special_Food(self.surface)
        self.food.draw()
        self.apple.draw()
        self.scr = 2
        self.opposite = False
        self.win = False

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + 40:
            if y1 >= y2 and y1 < y2 + 40:
                return True
        return False

    def bounds(self, x, y):
        if x < 0 or x > 1280 or y < 0 or y > 720:
            return True
        return False

    def play(self):
        self.surface.blit(self.bg, (0, 0))
        self.snake.walk()
        self.apple.draw()
        self.food.draw()
        self.display_score()
        pygame.display.flip()

        if self.bounds(self.snake.x[0], self.snake.y[0]):
            if self.snake.direction == "left":
                self.snake.x[0] = 1280 - 40

            elif self.snake.direction == "right":
                self.snake.x[0] = 0

            elif self.snake.direction == "up":
                self.snake.y[0] = 720 - 40

            elif self.snake.direction == "down":
                self.snake.y[0] = 0

        if self.is_collision(
            self.snake.x[0], self.snake.y[0], self.snake.x[-1], self.snake.y[-1]
        ):
            self.snake.decrease_length()
            self.apple.move()
            self.food.move()
            self.scr += 5
            if self.scr >= 100:
                return 1

        elif self.is_collision(
            self.snake.x[0], self.snake.y[0], self.snake.x[-2], self.snake.y[-2]
        ):

            self.snake.decrease_length()
            self.apple.move()
            self.food.move()
            self.scr += 5
            if self.scr >= 100:
                return 1

        if self.is_collision(
            self.snake.x[0], self.snake.y[0], self.food.x, self.food.y
        ):
            self.scr -= 2
            self.food.move()
            self.opposite = True

        for i in range(self.apple.apple_number):
            if self.is_collision(
                self.snake.x[0], self.snake.y[0], self.apple.x[i], self.apple.y[i]
            ):
                self.scr -= 1
                self.opposite = False
                self.apple.x[i] = random.randint(1, 32) * 40
                self.apple.y[i] = random.randint(1, 18) * 40
                self.snake.increase_length()
                self.apple.move()
                self.food.move()

        if self.snake.length == 3 or self.scr < 0:
            raise "Game over"

    def display_score(self):
        score_rect = pygame.rect.Rect((0, 0), (20, self.scr * 5))
        score_rect.bottomright = (1260, 550)
        score_rect_total = pygame.rect.Rect((0, 0), (30, 100 * 5))
        score_rect_total.midbottom = score_rect.midbottom
        score_rect_total.bottom += 5
        pygame.draw.rect(self.surface, "olivedrab3", score_rect)
        pygame.draw.rect(self.surface, "darkolivegreen", score_rect_total, 5, 2)

    def show_game_over(self):
        self.surface.fill((0, 155, 0))
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render(
            f"Game is over! Your score is {self.scr}", True, (255, 255, 255)
        )
        self.surface.blit(line1, (300, 300))
        line2 = font.render("To play again press Enter.", True, (255, 255, 255))
        self.surface.blit(line2, (300, 350))
        pygame.display.flip()

    def show_win(self):
        self.surface.fill((0, 155, 0))
        font = pygame.font.SysFont("arial", 30)
        line1 = font.render("You scored 100! You win!", True, (255, 255, 255))
        self.surface.blit(line1, (300, 300))
        line2 = font.render(
            "To play again press Enter. To exit press Escape!", True, (255, 255, 255)
        )
        self.surface.blit(line2, (300, 350))
        pygame.display.flip()

    def reset(self):
        self.snake = Snake(self.surface, 10)
        self.apple = Apple(self.surface)
        self.food = Special_Food(self.surface)
        self.scr = 2

    def run(self):
        self.running = True
        self.opposite = False
        pause = False

        while self.running:
            if self.opposite == False:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE and self.win:
                            self.running = False

                        if event.key == K_RETURN:
                            pause = False

                        if not pause:
                            if event.key == K_LEFT:
                                self.snake.move_left()

                            if event.key == K_RIGHT:
                                self.snake.move_right()

                            if event.key == K_UP:
                                self.snake.move_up()

                            if event.key == K_DOWN:
                                self.snake.move_down()
                        if event.key == pygame.K_RETURN and (
                            event.mod & pygame.KMOD_ALT
                        ):
                            pygame.display.toggle_fullscreen()

                    elif event.type == QUIT:
                        sys_exit()
            elif self.opposite == True:
                for event in pygame.event.get():
                    if event.type == KEYDOWN:
                        if event.key == K_ESCAPE and self.win:
                            self.running = False

                        if event.key == K_RETURN:
                            pause = False

                        if not pause:
                            if event.key == K_LEFT:
                                self.snake.move_right()

                            if event.key == K_RIGHT:
                                self.snake.move_left()

                            if event.key == K_UP:
                                self.snake.move_down()

                            if event.key == K_DOWN:
                                self.snake.move_up()
                        if event.key == pygame.K_RETURN and (
                            event.mod & pygame.KMOD_ALT
                        ):
                            pygame.display.toggle_fullscreen()

                    elif event.type == QUIT:
                        sys_exit()

            try:
                if not pause:
                    if self.play():
                        if self.scr >= 100:
                            self.win = True
                        self.show_win()
                        pause = True
                        self.reset()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

            self.clock.tick(5)

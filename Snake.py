import random

import pygame

from pygame.locals import *

import time

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)
STARTING_LENGTH = 1
GAME_SPEED = .3

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load('resources/apple.jpg').convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 25-1) * SIZE
        self.y = random.randint(0, 20-1) * SIZE


class Snake:
    def __init__(self, parent_screen, length):
        self.parent_screen = parent_screen
        self.block = pygame.image.load('resources/block.jpg').convert()
        self.direction = 'right'

        self.length = length
        self.x = [SIZE] * length
        self.y = [SIZE] * length

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

    def increase_length(self):
        self.length+=1
        self.x.append(-1)
        self.y.append(-1)


    def walk(self):

        for i in range(self.length-1, 0, -1):  # length is the number of blocks
            # 0 is the limit. it goes up to, but does not include the item with
            # this index number. By using '0' and because we are going in reverse,
            # we end at 1.
            # The -1 is the step size. by doing -1 we go in reverse
            # that reverses the array in the brackets for self.x and self.y
            #
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]
        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()


class Game:
    def __init__(self):
        pygame.init()
        pygame.init()
        pygame.display.set_caption('Stephen made a python game')

        pygame.mixer.init()
        self.play_background_music()

        self.surface = pygame.display.set_mode((1000, 800))
        self.snake = Snake(self.surface, STARTING_LENGTH
                           )
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()
        self.score = 0
        self.game_speed = GAME_SPEED

    def reset(self):
        self.snake = Snake(self.surface, STARTING_LENGTH)
        self. apple = Apple(self.surface)
        self.score = 0
        self.game_speed = GAME_SPEED

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + SIZE:
            if y1 >= y2 and y1 < y2 + SIZE:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f'resources/{sound}.mp3')
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # snake colliding with apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound('ding')
            self.snake.increase_length()
            self.apple.move()
            self.score += 1
            new_speed = self.game_speed * .9
            self.game_speed = new_speed

        # snake colliding with itself
        for i in range(3,self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound('crash')
                print('Game Over')
                raise "Game Over"

        # snake colliding with the boundaries of the window
        if not (0 <= self.snake.x[0] <= 1000 and 0 <= self.snake.y[0] <= 800):
            self.play_sound('crash')
            raise "Hit the boundary error"

    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f'Score: {self.score}', True, (255, 255, 255))
        self.surface.blit(score, (800, 10))

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f'GAME OVER! Your score is {self.score}', True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render('To play again press Enter. To exit, press escape', True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.mixer.music.pause()
        pygame.display.flip()

    def run(self):
        running = True
        paused = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        paused = False
                        pygame.mixer.music.unpause()
# You can write the functions how they'll look in the rest of
# the code like this, and then write how the functions and
# variables work later on
                    if not paused:
                        if event.key == K_UP:
                            self.snake.move_up()
                        if event.key == K_DOWN:
                            self.snake.move_down()
                        if event.key == K_LEFT:
                            self.snake.move_left()
                        if event.key == K_RIGHT:
                            self.snake.move_right()

                elif event.type == QUIT:
                    running = False

            try:
                if not paused:
                    self.play()

            except Exception as e:
                paused = True
                self.show_game_over()
                self.reset()

            current_speed = self.game_speed
            time.sleep(current_speed)


if __name__ == "__main__":
    game = Game()
    game.run()

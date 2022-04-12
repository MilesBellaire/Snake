import pygame
import os
import time
import random
import math

pygame.font.init()

WIDTH, HEIGHT = 800, 800
BOXES = 400
BOXES_PER_SIDE = int(math.sqrt(BOXES))
BOX_WIDTH = WIDTH / BOXES_PER_SIDE
BOX_HEIGHT = HEIGHT / BOXES_PER_SIDE

green = pygame.image.load(os.path.join("", "green.png"))

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")


class Snake:
    def __init__(self, x, y, body_parts, direction):
        self.direction = direction
        self.body_parts = body_parts

        self.x = []
        self.x = [-50 for i in range(BOXES)]
        self.x[0] = x

        self.y = []
        self.y = [0 for i in range(BOXES)]
        self.y[0] = y

    def move(self):
        for part in range(1, self.body_parts):
            body_part = self.body_parts - part
            self.x[body_part] = self.x[body_part - 1]
            self.y[body_part] = self.y[body_part - 1]
        if self.direction == 'U':
            self.y[0] = self.y[0] - int(BOX_HEIGHT/5)
        if self.direction == 'D':
            self.y[0] = self.y[0] + int(BOX_HEIGHT/5)
        if self.direction == 'L':
            self.x[0] = self.x[0] - int(BOX_WIDTH/5)
        if self.direction == 'R':
            self.x[0] = self.x[0] + int(BOX_WIDTH/5)

    def draw(self, window):
        back_parts = self.body_parts/3
        for parts in range(0, self.body_parts):
            part = self.body_parts - parts
            #pygame.draw.rect(window, (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)), (self.x[part] + 1, self.y[part] + 1, self.x[part] + int(BOX_WIDTH) - 2, self.y[part] + int(BOX_HEIGHT) - 2))
            equation_one = -math.tan((BOX_WIDTH/2)/self.body_parts/3) * back_parts * 10
            if parts / self.body_parts < 1/3:
                window.blit(green, (self.x[part] - math.floor(equation_one) + 1, self.y[part] - math.floor(equation_one) + 1), (part, part, BOX_WIDTH + math.ceil(equation_one*2) - 2, BOX_HEIGHT + math.ceil(equation_one*2) - 2))
                back_parts -= 1
            else:
                window.blit(green,(self.x[part] + 2, self.y[part] + 2),(part, part, BOX_WIDTH - 3, BOX_HEIGHT - 3))


class Apple:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def new_apple(self):
        self.x = random.randrange(0, BOXES_PER_SIDE) * BOX_WIDTH
        self.y = random.randrange(0, BOXES_PER_SIDE) * BOX_HEIGHT

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x + BOX_WIDTH / 2, self.y + BOX_HEIGHT / 2), BOX_WIDTH / 2 - 2)


def background(window):
    pygame.draw.rect(window, (0, 0, 0), (0, 0, WIDTH, HEIGHT))
    for i in range(0, BOXES_PER_SIDE + 1):
        pygame.draw.rect(window, (50, 50, 50), (int(i * BOX_WIDTH), 0, 1, HEIGHT))
        pygame.draw.rect(window, (50, 50, 50), (0, int(i * BOX_HEIGHT), WIDTH, 1))


def update_scores(score):
    scores_write = open("scores.txt", "w")
    scores_read = open("scores.txt", "r")
    prefix = "HighScore: "

    line = scores_read.readline()
    scores_write.write("hello sir ")
    print("line: " + str(scores_read.readline()))
    if line[:10] == prefix:
        highscore = int(line.removeprefix(prefix))
        if highscore < score:
            scores_write.write(prefix + str(score))
    else:
        scores_write.write(prefix + str(score))

    scores_write.close()
    scores_read.close()


def main():
    run = True
    paused = False
    reset = False
    FPS = 60
    apples_eaten = 0
    start_length = 26
    units_per_apple = 5
    high_score = 0
    timer = 0
    queue = []
    direction = 'R'
    main_font = pygame.font.SysFont("comicsans", 50)

    loss_font = pygame.font.SysFont("comicsans", 100)
    loss_label = loss_font.render("Game Over", 1, (255, 255, 255))

    clock = pygame.time.Clock()

    apple = Apple(0, 0, (255, 0, 0))
    apple.new_apple()
    snake = Snake(0, 0, start_length, direction)

    update_scores(apples_eaten)
    #high_score = int(open("scores.txt", "r").readline().removeprefix("HighScore: "))

    def redraw_window(window):
        background(window)
        lives_label = main_font.render(f"Score: {apples_eaten}", 1, (255, 255, 255))
        level_label = main_font.render(f"Highscore: {high_score}", 1, (255, 255, 255))

        apple.draw(WIN)
        snake.draw(WIN)

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - 10 - level_label.get_width(), 10))

        if reset:
            WIN.blit(loss_label, ((WIDTH - loss_label.get_width())/2, HEIGHT/2 - loss_label.get_height()))

        pygame.display.update()

    def check_wall():
        if snake.x[0] < 0:
            snake.x[0] = int(WIDTH - BOX_WIDTH)
        if snake.x[0] >= WIDTH:
            snake.x[0] = 0
        if snake.y[0] < 0:
            snake.y[0] = int(HEIGHT - BOX_HEIGHT)
        if snake.y[0] >= HEIGHT:
            snake.y[0] = 0

    def is_on_grid():
        if snake.x[0] % BOX_WIDTH == 0 and snake.y[0] % BOX_HEIGHT == 0:
            return True
        else:
            return False

    while run:
        keys = pygame.key.get_pressed()
        if not paused:
            if keys[pygame.K_a]:  # left
                queue.append('L')

            elif keys[pygame.K_d]:  # right
                queue.append('R')

            elif keys[pygame.K_w]:  # Up
                queue.append('U')

            elif keys[pygame.K_s]:  # Down
                queue.append('D')

            # Filtering the queue
            if len(queue) > 0:
                turn = queue[0]
                if len(queue) >= 1:
                    for element in queue:
                        if queue.count(element) >= 2:
                            queue.remove(element)
                if (snake.direction == 'L' and turn == 'R') or (snake.direction == 'R' and turn == 'L') or (snake.direction == 'U' and turn == 'D') or (snake.direction == 'D' and turn == 'U'):
                    queue.remove(turn)
                elif (snake.direction == 'L' and turn == 'L') or (snake.direction == 'R' and turn == 'R') or (snake.direction == 'U' and turn == 'U') or (snake.direction == 'D' and turn == 'D'):
                    queue.remove(turn)
                elif is_on_grid():
                    snake.direction = turn
                    queue.remove(turn)

        if keys[pygame.K_SPACE]:
            if timer == 0:
                if paused and reset:
                    # Restarts after loss
                    paused = False
                    reset = False
                    apple = Apple(0, 0, (255, 0, 0))
                    apple.new_apple()
                    snake = Snake(0, 0, start_length, direction)
                    apples_eaten = 0
                    direction = 'R'
                    queue.clear()
                elif paused:
                    paused = False
                else:
                    paused = True
                timer = 20
        if timer != 0:
            timer -= 1

        clock.tick(FPS)

        if apples_eaten > high_score:
            high_score = apples_eaten

        if not paused:
            snake.move()
        redraw_window(WIN)
        check_wall()

        # Checks collisions
        for part in range(1, snake.body_parts):
            if snake.x[0] == snake.x[part]:
                if snake.y[0] == snake.y[part]:
                    if not reset:
                        update_scores(apples_eaten)
                    paused, reset = True, True

        # Checks apples
        if snake.x[0] == apple.x:
            if snake.y[0] == apple.y:
                apples_eaten += 1
                snake.body_parts += units_per_apple
                apple.new_apple()

        # Checks if window is closed
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()

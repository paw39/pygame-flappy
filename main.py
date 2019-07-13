import pygame
import sys
import random

pygame.init()
pygame.time.set_timer(pygame.USEREVENT+1, 2500)

display_height = 504
display_width = 900

black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
green = (0,255,0)
blue = (0,0,255)


flappy_size = 42

score = 0
pipes = []
play = False

myfont = pygame.font.SysFont("monospace", 15)
window = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Flappy')
clock = pygame.time.Clock()
background = pygame.image.load('background.png')


class Bird():
    dead = False

    def __init__(self):
        self.x = 100
        self.y = display_height / 2
        self.flappy = pygame.image.load('flappy.png').convert_alpha()
        self.velocity = 0
        self.gravity = 1.2
        self.lift = -15

    def draw(self):
        window.blit(self.flappy, (self.x, self.y))
        pygame.display.flip()


    def jump(self):
        self.velocity += self.lift

    def update(self):
        self.velocity += self.gravity
        self.y += self.velocity

        if self.y > 558:
            self.y = 558
            self.velocity = 0
            self.dead = True  # jesli spadnie to zakonc gre

        if self.y < 0:
            self.y = 0
            self.velocity = 0


class Pipe():
    global score

    def __init__(self):
        self.top = random.randint(20, (display_height/2) - 20)
        self.bottom = random.randint(20, (display_height/2) - 20)
        self.x = display_width
        self.w = 40
        self.speed = 5

    def show(self):
        pygame.draw.rect(window, green, (self.x, 0, self.w, self.top), 0)
        pygame.draw.rect(window, green, (self.x, display_height - self.bottom, self.w, self.bottom), 0)

    def update(self):
        self.x -= self.speed

    def hits(self, bird):
        if bird.y < self.top or bird.y + flappy_size > display_height - self.bottom:
            if bird.x + 33 > self.x and bird.x < self.x + self.w:
                return True

    def score_add(self, bird):
        if bird.x == self.x + 20:
            return True


def manage_pipes():
    pipes.append(Pipe())
    if len(pipes) > 3:
        pipes.pop(0)


def draw_pipes():
    global score
    for pipe in pipes:
        pipe.show()
        pipe.update()
        if(pipe.hits(bird)):
            print("HIT!")
            game_over()
        if pipe.score_add(bird):
            score += 1


def texts(score):
   font = pygame.font.Font(None, 50)
   score_surf = font.render(str(score), True, (0, 0, 0))
   score_rect = score_surf.get_rect()
   score_rect.midtop = ((display_width/2), (display_height - 550))
   window.blit(score_surf, score_rect)


def game_over():
    global play
    play = False
    myFont = pygame.font.SysFont('monaco', 52)

    GOsurf = myFont.render('Game Over!', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (display_width/2, display_height/2 - 100)
    window.blit(GOsurf, GOrect)
    GOsurf = myFont.render('Tap Space to play again.', True, red)
    GOrect = GOsurf.get_rect()
    GOrect.midtop = (display_width / 2, display_height / 2)
    window.blit(GOsurf, GOrect)
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit(0)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pygame.time.wait(1000)
                setup()


def setup():
    global play, pipes, pipe, score

    pipes = []
    pipe = Pipe()
    bird.y = display_height / 2 - 200
    score = 0
    play = True


def main():

    global score
    while True:
        if play:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bird.jump()
                if event.type == pygame.USEREVENT+1:    # manage pipes
                    manage_pipes()

            window.blit(background,(0,0))
            draw_pipes()
            bird.update()
            bird.draw()
            texts(score)
            pygame.display.update()
            clock.tick(30)
        else:
            game_over()


bird = Bird()

setup()
main()




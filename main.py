import neat
import pygame
import os
import random
pygame.font.init()

WIDTH = 600
HEIGHT = 800
FPS = 30

BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png")))
]
PIP_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))
PIP2_IMG = pygame.transform.flip(PIP_IMG, False, True)
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK= (0, 0, 0)
BLUE = (0,0,255)
FONT = pygame.font.SysFont("comicsans", 50)


class Bird(pygame.sprite.Sprite):
    ANIMATION_TIME = 5
    MAX_ROTATION = 25
    ROT_VEL = 20
    # sprite of thee player
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # self.image = pygame.Surface((50, 50))
        self.image = BIRD_IMGS[0]
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.y_speed = 0
        self.image.set_colorkey(BLACK) # this will eliminate the black bos from the image
        self.tck_cnt = 0
        self.img_cnt = 0
        self.rect.y = 0
        self.height = self.rect.y
        self.tilt = 0

    def jump(self):
        self.y_speed = -10.5
        self.tck_cnt = 0
        self.height = self.rect.y

    def move(self):
        self.tck_cnt +=1
        displacement = self.y_speed*(self.tck_cnt) + 0.5*3*(self.tck_cnt)**2

        if displacement >= 16:
            displacement = 16
            print("D>")

        self.rect.y = self.rect.y + displacement
        if displacement < 0 or self.rect.y < self.height + 50:  # tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:  # tilt down
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def update(self):

        self.img_cnt += 1

        if self.img_cnt < self.ANIMATION_TIME:
            self.img = BIRD_IMGS[0]
        elif self.img_cnt < self.ANIMATION_TIME * 2:
            self.img = BIRD_IMGS[1]
        elif self.img_cnt < self.ANIMATION_TIME * 3:
            self.img = BIRD_IMGS[2]
        elif self.img_cnt < self.ANIMATION_TIME * 4:
            self.img = BIRD_IMGS[1]
        elif self.img_cnt < self.ANIMATION_TIME * 4 + 1:
            self.img = BIRD_IMGS[0]
            self.img_cnt = 0
        '''
        self.rect.x += 5
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT-200:
            self.y_speed = -5
        if self.rect.top < 200:
            self.y_speed = +5
        if self.rect.left > WIDTH:
            self.rect.right = 0
        self.y_speed += self.y_speed
        '''


class PIPE1(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = PIP_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 200, HEIGHT)
        self.passed = False

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.right = WIDTH
            self.rect.y = random.randint(200, 400)

    def collide(self, bird):
        contacted = bird.rect.colliderect(self.rect)
        if contacted:
            return True
        return False


class PIPE2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = PIP2_IMG
        self.rect = self.image.get_rect()
        self.rect.x = 350
        self.rect.y = -300
        self.passed = False

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.right = WIDTH
            self.rect.y = -random.randint(450, 500)

    def collide(self, bird):
        contacted = bird.rect.colliderect(self.rect)
        if contacted:
            return True
        return False

class BG(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = BG_IMG
        self.rect = self.image.get_rect()


class BASE(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = BASE_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH, HEIGHT)
        self.x = 0
        self.speed = 0

    def update(self):
        self.rect.x -= 5

        if self.rect.right < WIDTH - 360:
            self.rect.x = WIDTH


class BASE2(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = BASE_IMG
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 300, HEIGHT)
        self.x = WIDTH
        self.speed = 0

    def update(self):
        self.rect.x -= 5

        if self.rect.right < WIDTH - 300:
            self.rect.x = WIDTH

# initialise
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()


def main(genomes, config):

    all_sprites = pygame.sprite.Group()
    nets =[]
    ge = []
    birds = []  #  Bird(230, 350)
    pipes = []
    for _,g in genomes:    # genome id and genome
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append(Bird(230, 350))
        g.fitness = 0
        ge.append(g)

    bg = BG()
    base = BASE()
    base2 = BASE2()
    pipe1 = PIPE1()
    pipe2 = PIPE2()
    pipes = [pipe1,pipe2]
    all_sprites.add(bg)
    for bird in birds:
        all_sprites.add(bird)
    all_sprites.add(pipe1)
    all_sprites.add(pipe2)
    all_sprites.add(base)
    all_sprites.add(base2)

    # Game loop
    running = True
    score = 0
    add_pipe =False
    rem = []
    while running:
        clock.tick(FPS)
        # process input
        for event in pygame.event.get():
            # check for exit
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                quit()

        # Update
        all_sprites.update()

        for x,bird in enumerate(birds):
            ge[x].fitness+= 0.1
            bird.move()

            output = nets[birds.index(bird)].activate((bird.rect.y,abs(bird.rect.y - pipe1.rect.y), abs(bird.rect.y - pipe2.rect.y)))

            if output[0] > 0.5:
                bird.jump()


        for pipe in pipes:
            for x, bird in enumerate(birds):
                print("S")
                if pipe.collide(bird):
                    ge[x].fitness -= 1
                    birds.pop(x)
                    nets.pop(x)
                    ge.pop(x)

            if not pipe.passed and pipe.rect.x < bird.rect.x:
                    add_pipe = True

        if add_pipe:
            score += 1
            for g in ge:
                g.fitness += 5

        for r in rem:
            pipes.remove(r)

        for x,bird in enumerate(birds):
            if bird.rect.y + bird.image.get_height() > 730 or bird.rect.y <0:
                birds.pop(x)
                nets.pop(x)
                ge.pop(x)



        # Draw
        # bird.blit(bird.image, bird.rect)
        # screen.fill((BLUE))
        all_sprites.draw(screen)
        # Display scores:
        text_font = FONT.render("Score :"+ str(score), True, BLACK)
        text_rect = text_font.get_rect()
        text_rect.midtop = (WIDTH/2, 10)
        screen.blit(text_font,text_rect)

        pygame.display.flip()


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction
                                , neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    population = neat.Population(config)

    # statictic info
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    # run , (fitness function,50 is no of generatio)
    winner = population.run(main,50)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"NEAT_Configuration_File.txt")
    run(config_path)
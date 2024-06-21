import pygame, random, os, neat

# Initialization
pygame.font.init()  
FLOOR = 730
STAT_FONT = pygame.font.Font("assets/font.otf", 50)
DRAW_LINES = False

WIN_WIDTH = 600
WIN_HEIGHT = 800
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

pipe_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets","pipe.png")).convert_alpha())
bg_img = pygame.transform.scale(pygame.image.load(os.path.join("assets","bg.png")).convert_alpha(), (600, 900))
bird_images = [pygame.transform.scale2x(pygame.image.load(os.path.join("assets","bird" + str(x) + ".png"))) for x in range(1,4)]
base_img = pygame.transform.scale2x(pygame.image.load(os.path.join("assets","base.png")).convert_alpha())

gen = 0

class Base:
    # The floor of the screen is defined here
    VEL = 5
    WIDTH = base_img.get_width()
    IMG = base_img

    def __init__(self, y):
        # Initialize the floor object - x and y are the coordinates on screen
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        # Make the floor slide across screen continuously
        self.x1 -= self.VEL
        self.x2 -= self.VEL
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        # Drawing the sliding floor
        ## Two instances of the base image is rendered, and one slides after the other so that the screen always has a floor instance
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

class Pipe():
    # The pipe objects are defined here
    GAP = 200
    VEL = 5

    def __init__(self, x):
        # Initialize the pipe object - x and y are the coordinates on screen
        self.x = x
        self.height = 0

        # Set variables for holding top and bottom of pipe position
        self.top = 0
        self.bottom = 0

        # Flip the pipe image vertically to get the bottom pipe
        self.PIPE_TOP = pygame.transform.flip(pipe_img, False, True)
        self.PIPE_BOTTOM = pipe_img

        self.passed = False
        self.set_height()

    def set_height(self):
        # The height of the top pipe will be set randomly 
        # Bottom pipe height will be calculated according to gap value defined above, and top height
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    def move(self):
        # Move pipe right to left, according to valocity value defined above
        self.x -= self.VEL

    def draw(self, win):
        # draw top
        win.blit(self.PIPE_TOP, (self.x, self.top))
        # draw bottom
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))


    def collide(self, bird, win):
        # Check if bird has collided with pipe. A mask will be used to do so.
        # In pygame, masks enable pixel perfect collision detection. 
        # They can be thought of as an invisible 'wrapper' around the pixel groups of interest
        # In our case, desired pixel groups are those correspondiing to the bird objects and pipe objects

        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)
        top_offset = (self.x - bird.x, self.top - round(bird.y))
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        # A pygame mask uses 1 bit per-pixel to store which parts collide, calculating overlap automatically
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask,top_offset)

        if b_point or t_point:
            return True

        return False



class Bird:
    # The bird objects are defined here
    MAX_ROTATION = 25
    IMGS = bird_images
    ROT_VEL = 20
    ANIMATION_TIME = 5

    def __init__(self, x, y):
        # Initialize the bird objects
        self.x = x
        self.y = y
        self.tilt = 0  # degrees to tilt
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]

    def jump(self):
        # Defining variables related to the bird jump
        # Tick variable will be used to gain control over the rendered framerate, as well as a measure of time
        # Object's height will be set according to the y value calculated below
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        # Mathematically defining the bird movement
        # The bird should be constantly falling down under the force of in-game gravity
        # Only way for the bird to fight this fall is to make constant jumps, while avoiding the pipes!
        self.tick_count += 1

        # Calculating the downwards displacement due to gravity
        # Using the second fundamental equation of motion: s = ut + 0.5 at^2 
        # 's' is distance, 'u' is initial velocity, 't' is time and 'a' is acceleration of a body in projectile motion
        displacement = self.vel*(self.tick_count) + 0.5*(3)*(self.tick_count)**2  

        # Calculate terminal velocity
        # In physics, terminal velocity is defined as the constant speed that a freely falling object eventually reaches when the resistance of the medium through which it is falling prevents further acceleration.
        if displacement >= 16:
            displacement = (displacement/abs(displacement)) * 16

        if displacement < 0:
            displacement -= 2

        self.y = self.y + displacement

        # The bird will tilt up or down depending on whether it is rising or falling down in the screen
        # Tilt up
        if displacement < 0 or self.y < self.height + 50:  
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        # Tilt down
        else:  
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL

    def draw(self, win):
        # Draw the bird object on the screen
        self.img_count += 1

        # The bird's wings will be animated by constantly cycling through the three bird images stored in 'assets' folder
        if self.img_count <= self.ANIMATION_TIME:
            self.img = self.IMGS[0]
        elif self.img_count <= self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count <= self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count <= self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        elif self.img_count == self.ANIMATION_TIME*4 + 1:
            self.img = self.IMGS[0]
            self.img_count = 0

        # The bird will not flap its wings if it is falling downwards
        if self.tilt <= -80:
            self.img = self.IMGS[1]
            self.img_count = self.ANIMATION_TIME*2


        # Apply the angular tilt of the bird
        # Not important for our purposes - just adds to the aesthetics
        blitRotateCenter(win, self.img, (self.x, self.y), self.tilt)

    def get_mask(self):
        # Obtains and returns the mask for the current object
        return pygame.mask.from_surface(self.img)

def blitRotateCenter(surf, image, topleft, angle):
    # Rotating a bird instance according to the definitions above
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

    surf.blit(rotated_image, new_rect.topleft)

def draw_window(win, birds, pipes, base, score, gen, pipe_ind):
    
    # Draw the window for our simualtion
    # List of parameters:
        # win: pygame window surface
        # bird: a Bird object
        # pipes: List of pipes
        # score: score of the game -> integer value
        # gen: current generation
        # pipe_ind: index of closest pipe

    if gen == 0:
        gen = 1
    win.blit(bg_img, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)
    for bird in birds:
        # Draw lines from bird to pipe
        if DRAW_LINES:
            try:
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_TOP.get_width()/2, pipes[pipe_ind].height), 5)
                pygame.draw.line(win, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[pipe_ind].x + pipes[pipe_ind].PIPE_BOTTOM.get_width()/2, pipes[pipe_ind].bottom), 5)
            except:
                pass
        # Draw bird
        bird.draw(win)

    # Draw score on screen
    score_label = STAT_FONT.render("Score: " + str(score),1,(255,255,255))
    win.blit(score_label, (WIN_WIDTH - score_label.get_width() - 15, 10))

    # Draw 'generation number' value on screen
    score_label = STAT_FONT.render("Gens: " + str(gen-1),1,(255,255,255))
    win.blit(score_label, (10, 10))

    # Draw 'number of birds alive' value on screen
    score_label = STAT_FONT.render("Alive: " + str(len(birds)),1,(255,255,255))
    win.blit(score_label, (10, 50))

    pygame.display.update()



def eval_genomes(genomes, config):
    # The simulation will functionally begin from this point
    # A generation of birds will be created and neural networks attached to each bird object
    # Fitness will be calculated based on distance travelled without collision

    global WIN, gen
    win = WIN
    gen += 1

    # Three lists created
        # birds[] holds all the bird objects that are part of a generation
        # ge[] holds all the genomes associated to each birds (genome is a collection of genes)
            ## In NEAT-python, a population of individual genomes is maintained. 
            ## Each genome contains 1) Node genes 2) Connection genes
            ## The purpose is to identify useful genes (specific combinations of nodes and connections) over time
        # nets[] contains all the whole neural networks that each corresponding bird object uses to decide its move

    nets = []
    birds = []
    ge = []

    for genome_id, genome in genomes:
        genome.fitness = 0  # start with fitness level of 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        birds.append(Bird(230,350))
        ge.append(genome)

    base = Base(FLOOR)
    pipes = [Pipe(700)]
    score = 0

    clock = pygame.time.Clock()

    run = True
    while run and len(birds) > 0:
        # Limit framerate to 30/60/120/etc
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break

        # Determine if we'll use the first or second pipe on the screen for neural network input
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width():  
                pipe_ind = 1                                                                 

        # Each bird is given a fitness of 0.1 for each frame it stays alive. We're generating 30/60/etc frames per second, so survival accrues a lot of reward 
        for x, bird in enumerate(birds):  
            ge[x].fitness += 0.1
            bird.move()

            # Neural network reserves a number of inputs, and produces an ouput
                # Inputs: location of bird, location of top pipe, location of bottom pipe
                # Outputs: Depends on activation function defined in config file. Using tanh function will result in a number between -1 and 1

            output = nets[birds.index(bird)].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))

            # Output value > 0.5 will result in a jump command for the bird
            if output[0] > 0.5: 
                bird.jump()

        base.move()

        rem = []
        add_pipe = False
        for pipe in pipes:
            pipe.move()
            # Check for pipe-bird collision, remove colliding (bad) birds from the genome pool
            for bird in birds:
                if pipe.collide(bird, win):
                    ge[birds.index(bird)].fitness -= 1
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

        if add_pipe:
            score += 1
            # Giving more reward for each successful pass through a pipe
            for genome in ge:
                genome.fitness += 0.5
            pipes.append(Pipe(WIN_WIDTH))

        for r in rem:
            pipes.remove(r)

        for bird in birds:
            if bird.y + bird.img.get_height() - 10 >= FLOOR or bird.y < -50:
                nets.pop(birds.index(bird))
                ge.pop(birds.index(bird))
                birds.pop(birds.index(bird))

        draw_window(WIN, birds, pipes, base, score, gen, pipe_ind)

        # Stop simulation if score gets large enough
        if score > 20:       
           break


def run(config_file):
    # Initializes the NEAT algorithm before starting the simulation
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Begin simulation, run for up to 50 generations.
    winner = p.run(eval_genomes, 50)
    stats.save()
    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

# This will be executed only when flappy-bird.py is run individually
# Avoids double execution of simulation when the run() command is called from the main.py file  
if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config-feedforward.txt')
    run(config_path)

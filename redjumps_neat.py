import os
import pygame
import sys 
from pygame.locals import *
import random
import neat


pygame.init()

# Global constants

GRAVITY = 0.6
SCREEN_THRESH = 200
MAX_PLATFORM = 20

SCREEN_WIDTH = 448 # (320 * 1.4)
SCREEN_HEIGHT = 672 # (480 * 1.4)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont("Lucia Sans", 30)


class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.vel_y = 0
        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.direction = 1
        self.flip = False
        self.speed = 4
        self.in_air = True
        image = pygame.image.load('image/player.png')
        self.image = pygame.transform.scale(image, (int(image.get_width()*0.5), int(image.get_height()*0.5)))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
        self.data = []

    def move(self, scroll_bg):
        scroll = 0
        dx = 0
        dy = 0
        if self.moving_right:
            dx = self.speed
            self.flip = True
            self.direction = -1
        if self.moving_left:
            dx = - self.speed
            self.flip = False
            self.direction = 1

        # Jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -12
            self.jump = False
            self.in_air = True
        
        
        # Apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            self.vel_y
        dy += self.vel_y

        # Check collision with the edges
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = self.rect.right - SCREEN_WIDTH
        if self.rect.left + dx < 0:
            dx = self.rect.left     

        # Check collusion with the platform
        # Check only when falling
        if self.vel_y > 0:
            hits = pygame.sprite.spritecollide(self, platform_list, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.rect.bottom < lowest.rect.centery:
                    self.rect.bottom = lowest.rect.top
                    dy = 0 
                    self.vel_y = 0
                    self.in_air = False
                              
        # Check if the player has bounced to the top of the screen
        if self.rect.top <= SCREEN_THRESH:
            # if player is jumping
            if self.vel_y < 0:
                scroll = -dy


        # Update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll + scroll_bg

        return scroll
    
    def update(self):
        for platform in platform_list:
            self.data = [self.rect.left-platform.rect.left, self.rect.right-platform.rect.right]

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('image/platform.png')
        self.image = pygame.transform.scale(image,(int(image.get_width()*0.3*width), int(image.get_height()*0.3)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            for platform in platform_list:
                if platform == self:
                    platform_list.remove(platform)

def remove(index):
    fifty.pop(index)
    ge.pop(index)
    nets.pop(index)

def eval_genomes(genomes, config):
    global score_scroll, platform_list, hit_platform, fifty, ge, nets, points

    clock = pygame.time.Clock()
    score_scroll = 0
    check = 0
    counter = 150

    platform_list = []
    platform2 = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
    platform = Platform(SCREEN_WIDTH//2 + 70, SCREEN_HEIGHT -150, 2)
    platform_list.append(platform)
    platform_list.append(platform2)

    fifty = []
    ge = []
    nets = []

    hit_platform = []


    for genome_id, genome in genomes:
        fifty.append(Player())
        ge.append(genome)
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        hit_platform.append(0)

    def draw_text(text, font, text_col, x, y):
        img = font.render(text, True, text_col)
        screen.blit(img, (x, y))
        
    def score(scroll):
        global score_scroll, points
        score_scroll += scroll
        points = score_scroll//10
        pygame.draw.rect(screen, 'White', (0, 0, SCREEN_WIDTH, 20))
        draw_text("SCORE: " + str(int(points)), font, 'Black', 0, 0)
        return int(points)

    def statistics():
        global fifty, ge
        # Change x and y
        draw_text('Characters Alive:' + str(len(fifty)), font, 'White', 0, 30)
        draw_text('Generation:' + str(pop.generation +1) , font, 'White', SCREEN_WIDTH*2//3, 30)

    
    def top_player():
        global fifty
        players_rect_y = []
        for player in fifty:
            players_rect_y.append(player.rect.y)
        min_y = min(players_rect_y)
        top_player_index = players_rect_y.index(min_y)
        #top_player = fifty[top_player_index]
        return top_player_index

    def platforms_hit_update():
        for i,player in enumerate(fifty):
            for j,plat in enumerate(platform_list):
                hits = pygame.sprite.collide_rect(player, plat)
                if hits:
                    if j > hit_platform[i]:
                        ge[i].fitness += 5
                    if j < hit_platform[i]:
                        ge[i].fitness -= 0.5
                    hit_platform[i] = j

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill('BLUE')

        if len(platform_list) < MAX_PLATFORM:
            p_w = random.randint(1, 2)
            p_x = random.randint(0, SCREEN_WIDTH - platform.rect.width)
            p_y = platform.rect.y - random.randint(80, 100) 
            platform = Platform(p_x, p_y, 2)
            platform_list.append(platform)

        top_player_index = top_player()

        platforms_hit_update()

        for i,player in enumerate(fifty):
            player.draw()
            player.update()
            if i == top_player_index:
                scroll_bg = player.move(0)
            else:
                player.move(scroll_bg)
            
            player.jump = True

            output = nets[i].activate(player.data)
            if output[0] > 0.5:
                player.moving_right = True
                player.moving_left = False
            if output[1] > 0.5:
                player.moving_left = True
                player.moving_right = False
            if output[2] > 0.5:
                player.moving_left = False
                player.moving_right = False
            if player.rect.top > SCREEN_HEIGHT: 
                ge[i].fitness -= 1           
                remove(i)

        if len(fifty) == 0:
            break
        

        for plat in platform_list:
            plat.draw()
            plat.update(scroll_bg)

        statistics()
        player_score = score(scroll_bg)

        # detect if the players are not moving for specific duration of time
        counter -=1
        if counter == 0:
            if check == player_score:
                for i,player in enumerate(fifty):
                    ge[i].fitness -=1
                break
            else:
                for i,player in enumerate(fifty):
                    ge[i].fitness += 5
                check = player_score
                counter = 150 
                
        pygame.display.update()
        clock.tick(60)

# Setup the Neat Neural Network
def run(config_path):
    global pop
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    pop = neat.Population(config)
    pop.run(eval_genomes, 50)

if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, 'config.txt')
    run(config_path)

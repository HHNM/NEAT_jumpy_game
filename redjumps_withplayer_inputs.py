import pygame
import sys 
from pygame.locals import *
import random

pygame.init()

# Global constants
score_scroll = 0

GRAVITY = 0.6
SCREEN_THRESH = 200
MAX_PLATFORM = 20

SCREEN_WIDTH = 448
SCREEN_HEIGHT = 672 
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

font = pygame.font.SysFont("Lucia Sans", 30)

clock = pygame.time.Clock()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def score(scroll):
    global score_scroll
    score_scroll += scroll
    score = score_scroll//10
    pygame.draw.rect(screen, 'White', (0, 0, SCREEN_WIDTH, 20))
    draw_text("SCORE: " + str(int(score)), font, 'Black', 0, 0)

class Player(pygame.sprite.Sprite):

    def __init__(self, speed):
        pygame.sprite.Sprite.__init__(self)
        self.vel_y = 0
        self.moving_left = False
        self.moving_right = False
        self.jump = False
        self.direction = 1
        self.flip = False
        self.speed = speed
        self.in_air = True
        image = pygame.image.load('image/player.png')
        self.image = pygame.transform.scale(image, (int(image.get_width()*0.5), int(image.get_height()*0.5)))
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH//2, SCREEN_HEIGHT-100)
     

    def move(self):
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
        self.rect.y += dy + scroll
        return scroll

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)
    
    def get_input(self):
        key = pygame.key.get_pressed()    
        if key[K_LEFT]:
            self.moving_left = True
            self.moving_right = False
        elif key[K_RIGHT]:
            self.moving_right = True
            self.moving_left = False
        else:
            self.moving_left = False
            self.moving_right = False
        if key[K_UP]:
            self.jump = True
        else:
            self.jump = False



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
        global platform_list
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            for platform in platform_list:
                if platform == self:
                    platform_list.remove(platform)


def main():
    global platform_list

    platform_list = []

    platform = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
    platform_list.append(platform)


    fifty = Player(4)

    while True:

        scroll = fifty.move()

        screen.fill('BLUE')

        if len(platform_list) < MAX_PLATFORM:
            p_w = random.randint(1, 2)
            p_x = random.randint(0, SCREEN_WIDTH - platform.rect.width)
            p_y = platform.rect.y - random.randint(80, 100) 
            platform = Platform(p_x, p_y, p_w)
            platform_list.append(platform)

        if fifty.rect.top > SCREEN_HEIGHT:
            break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        fifty.get_input()

        
        fifty.draw()

        for plat in platform_list:
            plat.draw()
            plat.update(scroll)

        score(scroll)
        pygame.display.update()
        clock.tick(60)

main()
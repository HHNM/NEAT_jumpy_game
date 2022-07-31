import pygame
import sys 
from pygame.locals import *
import random

pygame.init()

score_scroll = 0
# Global constants

GRAVITY = 0.6
SCREEN_THRESH = 200
MAX_PLATFORM = 20

SCREEN_WIDTH = 448 # (320 * 1.4)
SCREEN_HEIGHT = 672 # (480 * 1.4)

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
    return int(score)

def check_score(score):
    global counter




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
        self.data = []
        self.index = 0
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
            hits = pygame.sprite.spritecollide(self, platform_group, False)
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


    def movetoplatform(self):
        if self.in_air:
            for platform in platform_group:
                if self.rect.bottom < platform.rect.top:
                    if self.rect.left < platform.rect.left:
                        self.moving_right = True
                    else:
                        self.moving_right = False
                if self.rect.bottom < platform.rect.top:
                    if self.rect.right > platform.rect.right:
                        self.moving_left = True
                    else:
                        self.moving_left = False

    def inputs(self):
        for platform in platform_group:
            self.data = [self.rect.bottom - platform.rect.top, self.rect.x-platform.rect.x, self.rect.right-platform.rect.right]
            pygame.draw.line(screen, "White", self.rect.center, platform.rect.center, 2)
    
    def update(self):
        if self.rect.bottom < platform_list[self.index].rect.top:
            self.index += 1
        pygame.draw.line(screen, "White", (self.rect.left, self.rect.centery), (platform_list[self.index].rect.left, platform_list[self.index].rect.centery))
        pygame.draw.line(screen, "White", (self.rect.right,self.rect.centery), (platform_list[self.index].rect.right, platform_list[self.index].rect.centery))
        

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width):
        pygame.sprite.Sprite.__init__(self)
        image = pygame.image.load('image/platform.png')
        self.image = pygame.transform.scale(image,(int(image.get_width()*0.3*width), int(image.get_height()*0.3)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
            self.rect.center = (80, 520)
            screen.blit(self.image, self.rect)

    def update(self, scroll):
        self.rect.y += scroll
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()


    #self.data = [self.rect.bottom - platform.rect.top, self.rect.x-platform.rect.x, self.rect.right-platform.rect.right]   

def main():
    global platform_group, platform_list, fifty
    counter = 200
    check = 0
    START_PLATFORMS = [(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2),(SCREEN_WIDTH//2 -90 + 120, SCREEN_HEIGHT -50 -100, 2),(SCREEN_WIDTH//2 -90 - 120, SCREEN_HEIGHT -50 -200, 2),(100, 100, 2),(40, -100, 2),(350, -250, 2),(10, -400, 2),(60, -550, 2)]
    platform_group = pygame.sprite.Group()

    platform = Platform(SCREEN_WIDTH//2 -90, SCREEN_HEIGHT -50, 2)
    platform2 = Platform(SCREEN_WIDTH//2 -90 + 120, SCREEN_HEIGHT -50 -100, 2)
    platform3 = Platform(SCREEN_WIDTH//2 -90 - 120, SCREEN_HEIGHT -50 -200, 2)
    platform_group.add(platform)
    platform_list = [platform]
    fifty = Player(4)

    while True:
        
        scroll = fifty.move()


        if len(platform_group) < MAX_PLATFORM:
            p_w = random.randint(1, 2)
            p_x = random.randint(0, SCREEN_WIDTH - platform.rect.width -60)
            p_y = platform.rect.y - random.randint(80, 100) + 10 
            platform = Platform(p_x, p_y, p_w)
            platform_group.add(platform)
            platform_list.append(platform)

        if fifty.rect.top > SCREEN_HEIGHT:
            break
        fifty.jump = True
        fifty.movetoplatform()
        screen.fill('BLUE')
        fifty.draw()
        fifty.update()

        platform_group.draw(screen)
        platform_group.update(scroll)
        player_score = score(scroll)

        # check if the score is increasing: the ai is moving up
        # if not break the loop
        counter -=1
        if counter == 0:
            if check == player_score:
                break
            else:
                check = player_score
                counter = 200 
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        
        pygame.display.update()
        clock.tick(60)

main()
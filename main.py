import pygame
from PIL import Image
import math
import os


# pillow to crop sprites dynamically omegalul
# x = 0
# value = math.floor(240 / 4) - 12
# val = value
# for i in range(5):
#     img = Image.open('images\TeamGunner_By_SecretHideout_060519\CHARACTER_SPRITES\Green\Gunner_Green_Crouch.png')
#     # img.show()
#     # cropped = img.crop((x, 0, val, 45))
#     cropped = img.crop((x, 0, val, 45))
#     # cropped.show()
#     cropped.save(f'Assets/player/Crouch/{i}.png')
#     x += value
#     val += value


pygame.init()


SCREEN_WIDTH = 800
SCREEN_HEIGHT = int(SCREEN_WIDTH * 0.8)
BG = (144, 201, 120)

# frame rate limit
clock = pygame.time.Clock()
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('2D Shooter')


# player actions

moving_left = False
moving_right = False
crouched = False


def draw_background():
    rect = pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT / 2)
    screen.fill(BG)
    pygame.draw.rect(screen, (137, 207, 240), rect)
    pygame.draw.line(screen, (107, 105, 99), (0, SCREEN_HEIGHT / 2), (SCREEN_WIDTH, SCREEN_HEIGHT / 2))


class Player(pygame.sprite.Sprite):
    def __init__(self, Ctype, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.Ctype = Ctype
        self.direction = 1  # facing right
        self.flip = False
        self.speed = speed
        self.alive = True

        #sprite animations
        self.update_time = pygame.time.get_ticks()
        self.animation_list = []
        self.frame_index = 0
        
        #sprite action [idle, run] etc
        self.action = 0 #initially idle
        animation_types = ['Idle', 'Run', 'Crouch']
        
        for animation in animation_types:
            
            temp_list = []
            
            frame_count = len(os.listdir(f'Assets/{self.Ctype}/{animation}'))
            
            for i in range(frame_count):
                img = pygame.image.load(f'Assets/{self.Ctype}/{animation}/{i}.png')
                img = pygame.transform.scale(
                img, (int(img.get_width() * scale),
                      int(img.get_height() * scale))
                )   
                temp_list.append(img)
            self.animation_list.append(temp_list)
            
        print(self.animation_list)
                


        # render sprites
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, moving_left, moving_right):
        # reset vars
        # delta x & y
        dx = 0
        dy = 0

        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1  # face left
        if moving_right:
            dx = self.speed
            self.flip = False
            self.direction = 1  # face right again

        # update rect pos

        self.rect.x += dx
        self.rect.y += dy


    def update_animation(self):
        ANIMATION_COOLDOWN = 100
        #update based on index
        self.image = self.animation_list[self.action][self.frame_index]
        # print(self.image)
        #check if enough time has passed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            
    def update_action(self, new_action):
        #check if the new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    def draw(self):
        screen.blit(
            pygame.transform.flip(self.image, self.flip, False),
            self.rect
        )


player = Player('player', 200, SCREEN_HEIGHT / 2, 3, 5)
# enemy = Player(player.x + 200, 200, 3)


# main game loop
run = True

while run:
    # fps limit
    clock.tick(FPS)

    # reset background
    draw_background()

    player.update_animation()
    # player.update()
    player.draw()
    
    if player.alive:
        # if player.in_air:
        #     player.update_action(2)#2: jump
        # elif moving_left or moving_right:
        #     player.update_action(1)#1: run
        # else:
        if moving_left or moving_right:
            player.update_action(1)
        elif crouched:
            player.update_action(2)
        else:
            player.update_action(0)#0: idle
        player.move(moving_left, moving_right)
    # enemy.draw()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_ESCAPE:
                run = False
            if event.key == pygame.K_s:
                crouched = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_s:
                crouched = False

    pygame.display.update()


pygame.quit()

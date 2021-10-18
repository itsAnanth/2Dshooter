import pygame
from PIL import Image
import math



# x = 0
# value = math.floor(240 / 4) - 12
# val = value
# for i in range(5):
#     img = Image.open('Assets\images\TeamGunner_By_SecretHideout_060519\CHARACTER_SPRITES\Green\Gunner_Green_Idle.png')
#     # img.show()
#     # cropped = img.crop((x, 0, val, 45))
#     cropped = img.crop((x, 0, val, 45))
#     # cropped.show()
#     cropped.save(f'Assets/player/Idle/{i}.png')
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


def draw_background():
    screen.fill(BG)


class Player(pygame.sprite.Sprite):
    def __init__(self, Ctype, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.Ctype = Ctype
        self.direction = 1  # facing right
        self.flip = False
        self.speed = speed

        #sprite animations
        self.update_time = pygame.time.get_ticks();
        self.animation_list = []
        self.frame_index = 0
        
        #sprite action [idle, run] etc
        self.action = 0 #initially idle
        animation_types = ['Idle']
        
        for i in range(5):
            img = pygame.image.load(f'Assets/{self.Ctype}/Idle/{i}.png')
            img = pygame.transform.scale(
                img, (int(img.get_width() * scale),
                      int(img.get_height() * scale))
            )
            self.animation_list.append(img)

        # render sprites
        self.image = self.animation_list[self.frame_index]
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
        self.image = self.animation_list[self.frame_index]
        #check if enough time has passed
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list):
            self.frame_index = 0
        
    def draw(self):
        screen.blit(
            pygame.transform.flip(self.image, self.flip, False),
            self.rect
        )


player = Player('player', 200, 200, 3, 5)
# enemy = Player(player.x + 200, 200, 3)


# main game loop
run = True

while run:
    # fps limit
    clock.tick(FPS)

    # reset background
    draw_background()

    player.update_animation()
    player.update()
    player.draw()
    # enemy.draw()
    player.move(moving_left, moving_right)

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

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False

    pygame.display.update()


pygame.quit()

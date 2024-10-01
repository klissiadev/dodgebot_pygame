import pygame
from util import blocks as bc

pygame.init()

# Define colors
COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_DARK_GRAY = (50, 50, 50)

# Screen size
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
FPS = 60

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodgebot - PyGame Edition - 2024-09-30")

# Playing field
FIELD_WIDTH = SCREEN_WIDTH - 10
FIELD_HEIGHT = 515
BORDER_THICKNESS = 5

bc.get_size(FIELD_WIDTH, FIELD_HEIGHT, SCREEN_HEIGHT)

# Screws // lives
screw_img = pygame.image.load(".//assets/screw.png")
screw_img = pygame.transform.scale(screw_img,(50,50))

def draw_lives_player_1(width, lives):
    for column in range(lives):
        screw_x = width + column * (60)
        screw_y = 10
        screen.blit(screw_img, (screw_x, screw_y))

BALL_WIDTH = 30
BALL_HEIGHT = 30
BALL_RADIUS = BALL_WIDTH / 2

class Ball:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load('.//assets/ball.png'),(BALL_WIDTH,BALL_HEIGHT))
        self.rect = self.image.get_rect(topleft = (x, y))
        self.x = x
        self.y = y
        self.speed_x = 3
        self.speed_y = 3

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y


    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

'''def check_collision(ball, blocks):
    ball_rect = pygame.Rect()
    for block in blocks:
        if ball_rect.colliderect(block.rect):
            '''

# Game loop
running = True
ball = Ball(475, 320)
blocks = bc.create_blocks()

while running:
    screen.fill(COLOR_BLACK)

    # Game event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw field
    pygame.draw.rect(screen, COLOR_DARK_GRAY, (BORDER_THICKNESS, 80, FIELD_WIDTH, FIELD_HEIGHT))
    pygame.draw.rect(screen,COLOR_WHITE,(BORDER_THICKNESS, 80, FIELD_WIDTH, FIELD_HEIGHT),BORDER_THICKNESS)
    draw_lives_player_1(40,3)
    draw_lives_player_1(SCREEN_WIDTH - 210,3)


    # Draw blocks and ball
    ball.draw(screen)
    for block in blocks:
        block.draw(screen)

    # update screen
    pygame.display.flip()

pygame.quit()
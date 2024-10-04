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
screw_img = pygame.transform.scale(screw_img, (50, 50))


def draw_lives_player_1(width, lives):
    for column in range(lives):
        screw_x = width + column * (60)
        screw_y = 10
        screen.blit(screw_img, (screw_x, screw_y))


BALL_WIDTH = 25
BALL_HEIGHT = 25
BALL_RADIUS = BALL_WIDTH / 2


class Ball:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load('.//assets/ball.png'), (BALL_WIDTH, BALL_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.speed_x = 3
        self.speed_y = 3

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y

        if self.rect.left <= BORDER_THICKNESS or self.rect.right >= FIELD_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 80 or self.rect.bottom >= 80 + FIELD_HEIGHT:
            self.speed_y *= -1

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


'''def check_collision(ball, blocks):
    ball_rect = pygame.Rect()
    for block in blocks:
        if ball_rect.colliderect(block.rect):
            '''


# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, controls, images):
        super().__init__()
        self.images = {
            'normal': pygame.transform.scale(pygame.image.load(images['normal']).convert_alpha(), (60, 60)),
            'normal_right': pygame.transform.scale(pygame.image.load(images['normal_right']).convert_alpha(), (60, 60)),
            'normal_left': pygame.transform.scale(pygame.image.load(images['normal_left']).convert_alpha(), (60, 60)),
            'normal_down': pygame.transform.scale(pygame.image.load(images['normal_down']).convert_alpha(), (60, 60)),
            'throwing': pygame.transform.scale(pygame.image.load(images['throwing']).convert_alpha(), (60, 60)),
            'defense': pygame.transform.scale(pygame.image.load(images['defense']).convert_alpha(), (60, 60))
        }
        self.image = self.images['normal']
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.speed = 0.4
        self.controls = controls  # Set controls
        self.holding_ball = False
        self.defending = False

    def move(self, keys, blocks):
        dx, dy = 0, 0

        if keys[self.controls['left']]:
            dx = -self.speed
        if keys[self.controls['right']]:
            dx = self.speed
        if keys[self.controls['up']]:
            dy = -self.speed
        if keys[self.controls['down']]:
            dy = self.speed

        self.x += dx
        self.y += dy
        self.rect.topleft = (self.x, self.y)

        if self.check_collision(blocks):
            self.x -= dx
            self.y -= dy
            self.rect.topleft = (self.x, self.y)
        self.rect.topleft = (self.x, self.y)

        if self.rect.left < BORDER_THICKNESS:
            self.rect.left = BORDER_THICKNESS + 5
        if self.rect.right > FIELD_WIDTH:
            self.rect.right = FIELD_WIDTH
        if self.rect.top < 80:
            self.rect.top = 80
        if self.rect.bottom > 80 + FIELD_HEIGHT:
            self.rect.bottom = 70 + FIELD_HEIGHT

    def check_collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                return True
        return False

    def update_animation(self):
        if keys[self.controls['defend_or_throw']]:
            self.image = self.images['defense']
        elif self.holding_ball:
            self.image = self.images['throwing']
        else:
            if keys[self.controls['left']]:
                self.image = self.images['normal_left']
            if keys[self.controls['right']]:
                self.image = self.images['normal_right']
            if keys[self.controls['up']]:
                self.image = self.images['normal']
            if keys[self.controls['down']]:
                self.image = self.images['normal_down']

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


# Controls for Player 1 (WASD + E for defense/attack) and player 2 (Arrow keys + Space for defense/attack)
player1_controls = {
    'up': pygame.K_w,
    'down': pygame.K_s,
    'left': pygame.K_a,
    'right': pygame.K_d,
    'defend_or_throw': pygame.K_e
}

player2_controls = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'defend_or_throw': pygame.K_SPACE
}

player1_image = {
    'normal': './assets/players/normal.png',
    'normal_right': './assets/players/normal_right.png',
    'normal_left': './assets/players/normal_left.png',
    'normal_down': './assets/players/normal_down.png',
    'throwing': './assets/players/throwing.png',
    'defense': './assets/players/defense.png'
}

player2_image = {
    'normal': './assets/players/normal2.png',
    'normal_right': './assets/players/normal2_right.png',
    'normal_left': './assets/players/normal2_left.png',
    'normal_down': './assets/players/normal2_down.png',
    'throwing': './assets/players/throwing.png',
    'defense': './assets/players/defense.png'
}

# Create the two players
player1 = Player(60, FIELD_HEIGHT / 2 + 30, player1_controls, player1_image)
player2 = Player(FIELD_WIDTH - 120, FIELD_HEIGHT / 2 + 30, player2_controls, player2_image)

# loop
running = True
ball = Ball(480, 325)
blocks = bc.create_blocks()

while running:
    screen.fill(COLOR_BLACK)

    # Game event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    ball.move()

    keys = pygame.key.get_pressed()

    player1.move(keys, blocks)
    player2.move(keys, blocks)

    player1.update_animation()
    player2.update_animation()

    # Catching the ball when speed equals to zero
    if ball.speed_x == 0 and ball.speed_y == 0:
        if player1.x == ball.rect.left and player1.y == ball.rect.top:
            player1.image = player1.images['throwing']

    # Draw field
    pygame.draw.rect(screen, COLOR_DARK_GRAY, (BORDER_THICKNESS, 80, FIELD_WIDTH, FIELD_HEIGHT))
    pygame.draw.rect(screen, COLOR_WHITE, (BORDER_THICKNESS, 80, FIELD_WIDTH, FIELD_HEIGHT), BORDER_THICKNESS)
    draw_lives_player_1(40, 3)
    draw_lives_player_1(SCREEN_WIDTH - 210, 3)

    # Draw players, blocks, and ball
    player1.draw(screen)
    player2.draw(screen)
    ball.draw(screen)

    for block in blocks:
        block.draw(screen)

    # update screen
    pygame.display.flip()

pygame.quit()

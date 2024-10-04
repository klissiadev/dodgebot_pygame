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
        self.speed_x = 2
        self.speed_y = 2
        self.in_move = False
        self.friction = 0.99

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.topleft = (self.x, self.y)
        if self.rect.left <= BORDER_THICKNESS or self.rect.right >= FIELD_WIDTH:
            self.speed_x *= -1
        if self.rect.top <= 80 or self.rect.bottom >= 80 + FIELD_HEIGHT:
            self.speed_y *= -1

        self.speed_x *= self.friction
        self.speed_y *= self.friction

        # If the speed is low the ball stops
        if abs(self.speed_x) < 0.01 and abs(self.speed_y) < 0.01:
            self.speed_x = 0
            self.speed_y = 0
            self.in_move = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)


    def check_collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                block.apply_effect(self,blocks)


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
        self.orientation = "Left"
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.speed = 0.4
        self.controls = controls  # Set controls
        self.holding_ball = False
        self.defending = False

    def move(self, keys, blocks, ball):
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

        self.check_holdingball(ball)

    def check_collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                return True
        return False

    def check_holdingball(self, ball):
        if self.rect.colliderect(ball.rect) and not ball.in_move:
            ball.rect.topleft = (self.x, self.rect.y)  # Mantém a bola com o jogador
            self.holding_ball = True  # O jogador está segurando a bola

            # Resetar as velocidades da bola para que o jogador possa lançar novamente
            ball.speed_x = 2  # Ou outro valor inicial padrão
            ball.speed_y = 2

    def update_animation(self,keys, ball):
        if keys[self.controls['left']]:
            self.orientation = "Left"
            self.image = self.images['normal_left']
        if keys[self.controls['right']]:
            self.orientation = "Right"
            self.image = self.images['normal_right']
        if keys[self.controls['up']]:
            self.orientation = "Up"
            self.image = self.images['normal']
        if keys[self.controls['down']]:
            self.orientation = "Down"
            self.image = self.images['normal_down']
        if self.holding_ball:
            self.image = self.images['throwing']
            self.flip_image()
        if keys[self.controls['defend_or_throw']]:
            if not ball.in_move and self.holding_ball:
                self.define_ball_position(ball)
                ball.in_move = True
                self.holding_ball = False
            else:
                self.image = self.images['defense']
                self.flip_image()


    def define_ball_position(self, ball):
        if self.orientation == "Left":
            ball.x = self.x - BALL_WIDTH
            ball.y = self.y + 30 - BALL_RADIUS
            ball.speed_x *= -5
            ball.speed_y = 0
        elif self.orientation == "Right":
            ball.x = self.x + 60
            ball.y = self.y + 30 - BALL_RADIUS
            ball.speed_x *= 5
            ball.speed_y = 0
        elif self.orientation == "Up":
            ball.x = self.x + 30 - BALL_RADIUS
            ball.y = self.y - BALL_HEIGHT
            ball.speed_x = 0
            ball.speed_y *= -5
        elif self.orientation == "Down":
            ball.x = self.x + 30 - BALL_RADIUS
            ball.y = self.y + 60
            ball.speed_x = 0
            ball.speed_y *= 5

    def flip_image(self):
        if self.orientation == "Right":
            angle = -90
        elif self.orientation == "Left":
            angle = 90
        elif self.orientation == "Up":
            angle = 0
        elif self.orientation == "Down":
            angle = 180
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect(center= self.image.get_rect(center=self.rect.center).center)

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

    keys = pygame.key.get_pressed()

    player1.move(keys, blocks, ball)
    player2.move(keys, blocks, ball)

    if ball.in_move:
        ball.move()
        ball.check_collision(blocks)

    player1.update_animation(keys,ball)
    player2.update_animation(keys,ball)
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

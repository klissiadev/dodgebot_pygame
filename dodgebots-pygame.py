import pygame
import random
import time
from util import players as pl
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

home_screen = pygame.transform.scale(pygame.image.load("./assets/home.png").convert_alpha(), (750, 460))
start_font = pygame.font.Font('assets/PressStart2P.ttf', 18)
start_text = start_font.render("Press ENTER to start the game", True, COLOR_WHITE)
start_text_rect = start_text.get_rect()
start_text_rect.center = (500, 530)
on_text = 0

# Playing field
FIELD_WIDTH = SCREEN_WIDTH - 10
FIELD_HEIGHT = 515
BORDER_THICKNESS = 5

# Arenas images
factory_stage = pygame.image.load('./assets/arenas/Factory.png').convert()

bc.get_size(FIELD_WIDTH, FIELD_HEIGHT, SCREEN_HEIGHT)

# Screws // lives
screw_img = pygame.image.load(".//assets/screw.png")
screw_img = pygame.transform.scale(screw_img, (50, 50))


def draw_lives_player(width, lives):
    for column in range(lives):
        screw_x = width + column * (60)
        screw_y = 10
        screen.blit(screw_img, (screw_x, screw_y))


def reset_game():
    global player1_hits, player2_hits, player1_hit, player2_hit
    global winner, announcement_played, show_victory_screen, interval
    global ball, blocks

    player1_hits = 0
    player2_hits = 0
    player1_hit = False
    player2_hit = False
    winner = None
    announcement_played = False
    show_victory_screen = False
    interval = False

    # Reset players
    player1.life = 3
    player1.start_position(True)

    player2.life = 3
    player2.start_position(False)

    # Reset ball
    ball = Ball(480, 325)

    # Reset blocks
    blocks = bc.create_blocks()

# ball size
BALL_WIDTH = 25
BALL_HEIGHT = 25
BALL_RADIUS = BALL_WIDTH / 2


class Ball:
    def __init__(self, x, y):
        self.image = pygame.transform.scale(pygame.image.load('.//assets/ball.png'), (BALL_WIDTH, BALL_HEIGHT))
        self.safe_state = pygame.transform.scale(pygame.image.load('.//assets/safe ball.png'), (BALL_WIDTH, BALL_HEIGHT))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.x = x
        self.y = y
        self.speed_x = 2
        self.speed_y = 2
        self.in_move = False
        self.friction = 0.99

    def random_spawn(self, blocks):
        while True:
            self.x = random.randint(SCREEN_WIDTH - FIELD_WIDTH, SCREEN_WIDTH - BALL_WIDTH)
            self.y = random.randint(SCREEN_HEIGHT - FIELD_HEIGHT, SCREEN_HEIGHT - BALL_HEIGHT)
            self.rect.topleft = (self.x, self.y)
            self.speed_x = 0
            self.speed_y = 0
            if not self.check_collision(blocks):
                self.in_move = False
                break

        return True

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.topleft = (self.x, self.y)

        if self.x + BALL_WIDTH < BORDER_THICKNESS or self.x > FIELD_WIDTH or self.y + BALL_HEIGHT < SCREEN_HEIGHT - FIELD_HEIGHT or self.y  > SCREEN_HEIGHT - BORDER_THICKNESS:
            self.x = (FIELD_WIDTH - BALL_WIDTH) // 2
            self.y = 80 + (FIELD_HEIGHT - BALL_HEIGHT) // 2
            self.rect.topleft = (self.x, self.y)
            self.speed_x = 2
            self.speed_y = 2
            self.in_move = False
            return

        if self.rect.left <= BORDER_THICKNESS or self.rect.right >= FIELD_WIDTH:
            self.speed_x *= -1
            block_sound.play()
        if self.rect.top <= 80 or self.rect.bottom >= 80 + FIELD_HEIGHT:
            self.speed_y *= -1
            block_sound.play()

        self.speed_x *= self.friction
        self.speed_y *= self.friction

        # If the speed is low the ball stops
        if abs(self.speed_x) < 0.01 and abs(self.speed_y) < 0.01:
            self.speed_x = 0
            self.speed_y = 0
            self.in_move = False

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        if abs(self.speed_x) <= 0.5 and abs(self.speed_y) <= 0.5:
            surface.blit(self.safe_state, self.rect.topleft)
        else:
            surface.blit(self.image, self.rect.topleft)

    def check_collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                block.apply_effect(self,blocks)
                block_sound.play()
                return True

    def hit_player(self, player):
        if self.speed_x <= 0.5 and self.speed_y <= 0.5:
            return False
        if player.holding_ball:
            return False
        return self.rect.colliderect(player.rect)

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
    'throwing': './assets/players/throwing2.png',
    'defense': './assets/players/defense2.png'
}

credits = [
    "Alexandre Elias \n"
    "Ana Klissia \n",
    "Arthur Marshall \n",
    "João Guilherme"
]

pl.get_global_variables(BORDER_THICKNESS, FIELD_WIDTH, FIELD_HEIGHT, BALL_WIDTH, BALL_HEIGHT, BALL_RADIUS)

# old games font
font_path = './assets/game_font/8-bit-hud.ttf'
font_size = 18
game_font = pygame.font.Font(font_path, font_size)

# Create the two players
player1 = pl.Player(60, FIELD_HEIGHT / 2 + 30, player1_controls, player1_image)
player2 = pl.Player(FIELD_WIDTH - 120, FIELD_HEIGHT / 2 + 30, player2_controls, player2_image)

# Victory sprites
vic1_sprite = './assets/B01.png'
vic2_sprite = './assets/B02.png'

# PLayers hit controller
player1_hit = False
player2_hit = False

# count of player hits
player1_hits = 0
player2_hits = 0


# loop
start = True
winner = None
interval = False
winner_podium = False
running = True
pause_time = 0
is_paused = False
show_victory_screen = False
ball = Ball(480, 325)
blocks = bc.create_blocks()

# tense pause
announce_pause = 6
announce_time = time.time()

# play music
dodging_theme = pygame.mixer.Sound('./assets/DODGING!.mp3')
dodging_theme.play(-1)
block_sound = pygame.mixer.Sound('./assets/block_sound.mp3')
crash_sound = pygame.mixer.Sound('./assets/crash.mp3')
clean_sound = pygame.mixer.Sound('./assets/narrator/clean.mp3')
beauty_sound = pygame.mixer.Sound('./assets/narrator/beautifaul.mp3')
slam_sound = pygame.mixer.Sound('./assets/narrator/slam.mp3')
that_hit_sound = pygame.mixer.Sound('./assets/narrator/thats a hit.mp3')
announcement_sound = pygame.mixer.Sound('./assets/narrator/who_winner.mp3')
p1_wins_sound = pygame.mixer.Sound('./assets/narrator/p1_victory.mp3')
p2_wins_sound = pygame.mixer.Sound('./assets/narrator/p2_victory.mp3')

# Narrator random speechs
reaction = [clean_sound, beauty_sound, slam_sound, that_hit_sound]
announcement_time = 0
announcement_played = False

font = pygame.font.Font(None, 74)


while running:
    screen.fill(COLOR_BLACK)

    # Game event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                start = False
                interval = True
            if (event.key == pygame.K_SPACE or event.key == pygame.K_e) and interval:
                interval = False

    keys = pygame.key.get_pressed()

    if start:
        screen.fill(COLOR_BLACK)
        screen.blit(home_screen, (150, 20))
        # flashing TEXT
        if on_text < 240:
            screen.blit(start_text, start_text_rect)
            on_text += 1
        elif on_text < 400:
            on_text += 1
        else:
            on_text = 0
    else:
        if interval and announcement_played is True:
            message_surface = game_font.render("Ok, that's enough!", True, COLOR_WHITE)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 13))
            screen.blit(message_surface, message_rect)

        if interval and announcement_played is False:
            message_surface = game_font.render("STANDBY!", True, COLOR_WHITE)
            message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 13))
            screen.blit(message_surface, message_rect)
        else:

            if is_paused and announcement_played is False:
                message_surface = game_font.render("It´s a Hit!", True, COLOR_WHITE)
                message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 13))
                screen.blit(message_surface, message_rect)

                if time.time() - pause_time >= 2:
                    is_paused = False
                    react = random.choice(reaction)
                    if player1.life >= 1 or player2.life >= 1:
                        react.play()


            else:
                player1.move(keys, blocks, ball, player2)
                player2.move(keys, blocks, ball, player1)

                if ball.in_move:
                    ball.move()
                    ball.check_collision(blocks)

                player1.update_animation(keys,ball)
                player2.update_animation(keys,ball)

                # Catching the ball when speed equals to zero
                if ball.speed_x <= 0.5 and ball.speed_y <= 0.5:
                    if player1.x == ball.rect.left and player1.y == ball.rect.top:
                        player1.image = player1.images['throwing']

                # checks if player 1 was hit
                if ball.hit_player(player1) is True and not player1.holding_ball and not player1_hit:
                    crash_sound.play()
                    if player1.throw_state is False and not player2.holding_ball:
                        player1_hits += 1
                        player1_hit = True
                        if player1_hits <= 3:
                            player1.life -= 1
                            is_paused = True
                            pause_time = time.time()
                            player1.start_position(True)
                            player2.start_position(False)
                            ball.random_spawn(blocks)

                # checks if player 2 was hit
                if ball.hit_player(player2) is True and not player2.holding_ball and not player2_hit:
                    crash_sound.play()
                    if player2.throw_state is False and not player1.holding_ball:
                        player2_hits += 1
                        player2_hit = True
                        if player2_hits <= 3:
                            player2.life -= 1
                            is_paused = True
                            pause_time = time.time()
                            player1.start_position(True)
                            player2.start_position(False)
                            ball.random_spawn(blocks)

                if not ball.in_move:
                    player1_hit = False
                    player2_hit = False

                for block in blocks:
                    if block.block_type == "vertical-chaotic":
                        block.chaotic_move()

                if player1.life <= 0 or player2.life <= 0:
                    if not announcement_played:
                        if player1.life <= 0:
                            winner = 'player2'
                        if player2.life <= 0:
                            winner = 'player1'
                        announcement_time = time.time()
                        dodging_theme.stop()
                        announcement_sound.play()
                        announcement_played = True
                        show_victory_screen = False
                        interval = True

                if announcement_played:
                    if time.time() - announcement_time >= 6:
                        show_victory_screen = True

                if show_victory_screen and winner:
                    screen.fill(COLOR_BLACK)
                    if winner == 'player1':
                        winner_image = pygame.image.load(vic1_sprite)
                        p1_wins_sound.play()
                        message_surface = game_font.render("Player 1 Wins", True, COLOR_WHITE)
                        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 13))
                        screen.blit(message_surface, message_rect)

                        message_surface = game_font.render("Press 'enter' to restart", True, COLOR_WHITE)
                        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
                        screen.blit(message_surface, message_rect)

                        message_surface = game_font.render("CREDITS", True, COLOR_WHITE)
                        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
                        screen.blit(message_surface, message_rect)

                        for index, nome in enumerate(credits):
                            nome_surface = game_font.render(nome, True, COLOR_WHITE)
                            nome_rect = nome_surface.get_rect(center=(
                            SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5 + index * 30))

                            screen.blit(nome_surface, nome_rect)

                    else:
                        winner_image = pygame.image.load(vic2_sprite)
                        p2_wins_sound.play()
                        message_surface = game_font.render("Player 2 Wins!", True, COLOR_WHITE)
                        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 13))
                        screen.blit(message_surface, message_rect)

                        message_surface = game_font.render("Press 'enter' to restart", True, COLOR_WHITE)
                        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 6))
                        screen.blit(message_surface, message_rect)

                        message_surface = game_font.render("CREDITS", True, COLOR_WHITE)
                        message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3 ))
                        screen.blit(message_surface, message_rect)

                        for index, nome in enumerate(credits):
                            nome_surface = game_font.render(nome, True, COLOR_WHITE)
                            nome_rect = nome_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5 + index * 30))
                            screen.blit(nome_surface, nome_rect)

                    winner_image = pygame.transform.scale(winner_image, (200, 200))
                    winner_rect = winner_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                    screen.blit(winner_image, winner_rect)
                    pygame.display.flip()
                    time.sleep(5)
                    waiting_for_restart = True
                    while waiting_for_restart:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                running = False
                                waiting_for_restart = False
                            if event.type == pygame.KEYDOWN:
                                dodging_theme.play(-1)
                                if event.key == pygame.K_RETURN:
                                    reset_game()
                                    waiting_for_restart = False

        # Draw field
        screen.blit(factory_stage, (BORDER_THICKNESS, 80))
        pygame.draw.rect(screen, COLOR_WHITE, (BORDER_THICKNESS, 80, FIELD_WIDTH, FIELD_HEIGHT), BORDER_THICKNESS)
        draw_lives_player(40, player1.life)
        draw_lives_player(SCREEN_WIDTH - 210, player2.life)

        # Draw players, blocks, and ball
        player1.draw(screen)
        player2.draw(screen)
        ball.draw(screen)

        for block in blocks:
            block.draw(screen)


        # update screen
    pygame.display.flip()

pygame.quit()

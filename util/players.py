import pygame

pygame.init()
pygame.mixer.init()

BORDER_THICKNESS = 0
FIELD_WIDTH = 0
FIELD_HEIGHT = 0
BALL_WIDTH = 0
BALL_HEIGHT = 0
BALL_RADIUS = 0
angle = 0

# players sounds
reflect_sound = pygame.mixer.Sound('./assets/reflect_sound.mp3')
throw_sound = pygame.mixer.Sound('./assets/throw_sound.mp3')

def get_global_variables(border,field_w,field_h, ball_w, ball_y,ball_rad):
    global BORDER_THICKNESS, FIELD_WIDTH, FIELD_HEIGHT, BALL_WIDTH, BALL_HEIGHT, BALL_RADIUS
    BORDER_THICKNESS = border
    FIELD_WIDTH = field_w
    FIELD_HEIGHT = field_h
    BALL_WIDTH = ball_w
    BALL_HEIGHT = ball_y
    BALL_RADIUS = ball_rad

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
        self.DEFENSE_DISTANCE = 50
        self.life = 3
        self.throw_state = False
        self.catch = False

    def move(self, keys, blocks, ball, adversary):
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

        if self.rect.left < BORDER_THICKNESS:
            self.rect.left = BORDER_THICKNESS + 5
        if self.rect.right > FIELD_WIDTH:
            self.rect.right = FIELD_WIDTH
        if self.rect.top < 80:
            self.rect.top = 80
        if self.rect.bottom > 80 + FIELD_HEIGHT:
            self.rect.bottom = 70 + FIELD_HEIGHT

        self.check_holdingball(ball,adversary)

    def start_position(self, state):
        if state is True:
            self.x = 60
            self.y = FIELD_HEIGHT / 2 + 30
            self.rect.topleft = (self.x, self.y)
            self.image = self.images['normal_right']
        if state is False:
            self.x = FIELD_WIDTH - 120
            self.y = FIELD_HEIGHT / 2 + 30
            self.rect.topleft = (self.x, self.y)
            self.image = self.images['normal_left']

    def check_collision(self, blocks):
        for block in blocks:
            if self.rect.colliderect(block.rect):
                return True
        return False

    def check_defense(self, ball):
        defense_buffer = 10
        defense_width = 30
        defense_height = 40

        distance_x = abs(self.rect.centerx - ball.rect.centerx)
        distance_y = abs(self.rect.centery - ball.rect.centery)

        if distance_x > self.DEFENSE_DISTANCE or distance_y > self.DEFENSE_DISTANCE:
            reflect_sound.play()

        self.defense1 = pygame.Rect(
            self.rect.right - defense_buffer, self.rect.centery - defense_height // 2,
            defense_width, defense_height)

        self.defense2 = pygame.Rect(
            self.rect.left + defense_buffer, self.rect.centery - defense_height // 2,
            defense_width, defense_height)

        self.defense_up = pygame.Rect(
            self.rect.centerx - defense_width // 2,
            self.rect.top - defense_height - defense_buffer,
            defense_width,
            defense_height
        )

        self.defense_down = pygame.Rect(
            self.rect.centerx - defense_width // 2,
            self.rect.bottom + defense_buffer,
            defense_width,
            defense_height
        )

        if ball.rect.colliderect(self.defense1):
            ball.speed_x = 5
            return

        if ball.rect.colliderect(self.defense2):
            ball.speed_x = -5
            return

        if ball.rect.colliderect(self.defense_up):
            ball.speed_y = -5
            return

        if ball.rect.colliderect(self.defense_down):
            ball.speed_y = 5
            return

    def check_holdingball(self, ball, adversary):
        if self.rect.colliderect(
                ball.rect) and not ball.in_move and not self.holding_ball and not adversary.holding_ball:
            self.holding_ball = True  # O jogador está segurando a bola
            self.catch = True

            # Resetar as velocidades da bola para que o jogador possa lançar novamente
            throw_sound.play()
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
            ball.rect.topleft = (self.x, self.rect.y)

        if keys[self.controls['defend_or_throw']]:
            if not self.holding_ball:
                if keys[self.controls['defend_or_throw']]:
                    self.image = self.images['defense']
                    self.flip_image()
                    self.check_defense(ball)

        if keys[self.controls['defend_or_throw']]:
            if not ball.in_move and self.holding_ball:
                self.define_ball_position(ball)
                self.catch = True
                ball.in_move = True
                self.holding_ball = False
                self.image = self.images['throwing']
                self.throw_state = True
                throw_sound.play()
        else:
                self.throw_state = False
                self.catch = False
                if self.orientation == "Left":
                    self.image = self.images['normal_left']
                elif self.orientation == "Right":
                    self.image = self.images['normal_right']
                elif self.orientation == "Up":
                    self.image = self.images['normal']
                elif self.orientation == "Down":
                    self.image = self.images['normal_down']


    def define_ball_position(self, ball):
        if self.orientation == "Left":
            ball.x = self.x - BALL_WIDTH
            ball.y = self.y + 30 - BALL_RADIUS
            ball.speed_x *= -5
            ball.speed_y = 1
        elif self.orientation == "Right":
            ball.x = self.x + 60
            ball.y = self.y + 30 - BALL_RADIUS
            ball.speed_x *= 5
            ball.speed_y = 1
        elif self.orientation == "Up":
            ball.x = self.x + 30 - BALL_RADIUS
            ball.y = self.y - BALL_HEIGHT
            ball.speed_x = 1
            ball.speed_y *= -5
        elif self.orientation == "Down":
            ball.x = self.x + 30 - BALL_RADIUS
            ball.y = self.y + 60
            ball.speed_x = 1
            ball.speed_y *= 5

    def flip_image(self):
        global angle
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
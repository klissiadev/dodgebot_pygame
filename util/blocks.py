import random

import pygame

BLOCK_WIDTH = 75
BLOCK_HEIGHT = 30
FIELD_WIDTH = 0
FIELD_HEIGHT = 0
SCREEN_HEIGHT = 0

def get_size(width, height, screen_height):
    global FIELD_WIDTH, FIELD_HEIGHT, SCREEN_HEIGHT
    FIELD_WIDTH = width - 20
    FIELD_HEIGHT = height
    SCREEN_HEIGHT = screen_height

block_images = {
    "horizontal-solid": pygame.transform.scale(pygame.image.load('.//assets/blocks/horizontal-solid.png'),(BLOCK_WIDTH,BLOCK_HEIGHT)),
    "horizontal-breakable": pygame.transform.scale(pygame.image.load('.//assets/blocks/horizontal-breakable.png'),(BLOCK_WIDTH,BLOCK_HEIGHT)),
    "horizontal-translucent": pygame.transform.scale(pygame.image.load('.//assets/blocks/horizontal-translucent.png'),(BLOCK_WIDTH,BLOCK_HEIGHT)),
    "horizontal-chaotic": pygame.transform.scale(pygame.image.load('.//assets/blocks/horizontal-chaotic.png'),(BLOCK_WIDTH,BLOCK_HEIGHT)),
    "vertical-solid": pygame.transform.scale(pygame.image.load('.//assets/blocks/vertical-solid.png'),(BLOCK_HEIGHT,BLOCK_WIDTH)),
    "vertical-breakable": pygame.transform.scale(pygame.image.load('.//assets/blocks/vertical-breakable.png'),(BLOCK_HEIGHT,BLOCK_WIDTH)),
    "vertical-translucent": pygame.transform.scale(pygame.image.load('.//assets/blocks/vertical-translucent.png'),(BLOCK_HEIGHT,BLOCK_WIDTH)),
    "vertical-chaotic": pygame.transform.scale(pygame.image.load('.//assets/blocks/vertical-chaotic.png'),(BLOCK_HEIGHT,BLOCK_WIDTH)),
}

class Block:
    def __init__(self, x, y, block_type):
        self.image = block_images[block_type]
        self.rect = self.image.get_rect(topleft = (x, y))
        self.block_type = block_type
        self.touch_top = True
        self.touch_bottom = False
        self.x = x
        self.y = y

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    def apply_effect(self, ball, blocks):
        if self.block_type in ["horizontal-solid", "vertical-solid"]:
            ball.speed_x = -ball.speed_x * random.uniform(0.8, 1.2)
            ball.speed_y = -ball.speed_y * random.uniform(0.8, 1.2)
        if self.block_type in ["horizontal-breakable", "vertical-breakable"]:
            ball.speed_x = -ball.speed_x * random.uniform(0.8, 1.2)
            ball.speed_y = -ball.speed_y * random.uniform(0.8, 1.2)
            blocks.remove(self)
        if self.block_type in ["horizontal-chaotic", "vertical-chaotic"]:

            random_speed = random.uniform(0.9, 1.06)  # Variação maior para tornar mais caótico
            random_direction_x = random.choice([-1, 1])  # Aleatoriamente inverte o eixo X
            random_direction_y = random.choice([-1, 1])  # Aleatoriamente inverte o eixo Y

            ball.speed_x = ball.speed_x * random_speed * random_direction_x
            ball.speed_y = ball.speed_y * random_speed * random_direction_y

    def chaotic_move(self):
        if self.touch_top:
            self.y += 0.4
            if self.y + 75 > SCREEN_HEIGHT:
                self.touch_bottom = True
                self.touch_top = False
        if self.touch_bottom:
            self.y -= 0.4
            if self.y < SCREEN_HEIGHT - FIELD_HEIGHT:
                self.touch_bottom = False
                self.touch_top = True
        self.rect.topleft = (self.x, self.y)


def blocks_overlap(block1, block2):
    return block1.rect.colliderect(block2.rect)

def create_blocks():
    blocks = []

    x = 80
    y = SCREEN_HEIGHT-FIELD_HEIGHT
    block_type = "vertical-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 110
    y = 125
    block_type = "vertical-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 140
    y = 165
    block_type = "vertical-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 80
    y = SCREEN_HEIGHT - 85
    block_type = "vertical-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 110
    y = SCREEN_HEIGHT - 120
    block_type = "vertical-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)
    x = 110
    y = SCREEN_HEIGHT - 120
    block_type = "vertical-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 140
    y = SCREEN_HEIGHT - 150
    block_type = "vertical-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 220
    y = SCREEN_HEIGHT - 290
    block_type = "vertical-chaotic"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH - 80
    y = SCREEN_HEIGHT - FIELD_HEIGHT
    block_type = "vertical-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH - 110
    y = 125
    block_type = "vertical-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH - 140
    y = 165
    block_type = "vertical-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH - 80
    y = SCREEN_HEIGHT - 85
    block_type = "vertical-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH - 110
    y = SCREEN_HEIGHT - 120
    block_type = "vertical-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH - 140
    y = SCREEN_HEIGHT - 150
    block_type = "vertical-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH - 220
    y = SCREEN_HEIGHT - 290
    block_type = "vertical-chaotic"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    # BLOCKS OF HORIZONTAL WALL

    x = FIELD_WIDTH/2 - 37
    y = 165
    block_type = "horizontal-chaotic"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = x - 75
    y = 165
    block_type = "horizontal-breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = x - 75
    y = 165
    block_type = "horizontal-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH / 2 + 37
    y = 165
    block_type = "horizontal-breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = x + 75
    y = 165
    block_type = "horizontal-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH / 2 - 37
    y = SCREEN_HEIGHT - 120
    block_type = "horizontal-chaotic"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = x - 75
    y = SCREEN_HEIGHT - 120
    block_type = "horizontal-breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = x - 75
    y = SCREEN_HEIGHT - 120
    block_type = "horizontal-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH / 2 + 37
    y = SCREEN_HEIGHT - 120
    block_type = "horizontal-breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = x + 75
    y = SCREEN_HEIGHT - 120
    block_type = "horizontal-translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    # BLOCKS OF HORIZONTAL CENTER
    x = FIELD_WIDTH / 2
    y = 265
    block_type = "horizontal-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH / 2 + 75
    block_type = "vertical-breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH / 2 + 75
    y = y + 73
    block_type = "vertical-breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = FIELD_WIDTH / 2 - 75
    y = SCREEN_HEIGHT - 215
    block_type = "horizontal-solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = x - 30
    y = y - 45
    block_type = "vertical-breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    y = y - 73
    block_type = "vertical-breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    return blocks

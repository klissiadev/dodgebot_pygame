import pygame

BLOCK_WIDTH = 75
BLOCK_HEIGHT = 30
FIELD_WIDTH = 0
FIELD_HEIGHT = 0
SCREEN_HEIGHT = 0

def get_size(width, height, screen_height):
    global FIELD_WIDTH, FIELD_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
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

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

    '''def apply_effect(self, ball):
        if self.block_type == "solid":
            ball.speed_x = -ball.speed_x
            ball.speed_y = -ball.speed_y'''

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

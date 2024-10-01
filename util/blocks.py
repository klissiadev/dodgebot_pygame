import pygame

BLOCK_WIDTH = 60
BLOCK_HEIGHT = 30
WIDTH = 0
HEIGHT = 0

def get_size(width, height):
    global WIDTH, HEIGHT
    WIDTH = width
    HEIGHT = height

block_images = {
    "solid": pygame.transform.scale(pygame.image.load('.//assets/blocks/horizontal-solid.png'),(BLOCK_WIDTH,BLOCK_HEIGHT)),
    "breakable": pygame.transform.scale(pygame.image.load('.//assets/blocks/horizontal-breakable.png'),(BLOCK_WIDTH,BLOCK_HEIGHT)),
    "translucent": pygame.transform.scale(pygame.image.load('.//assets/blocks/horizontal-translucent.png'),(BLOCK_WIDTH,BLOCK_HEIGHT)),
    "caotic": pygame.transform.scale(pygame.image.load('.//assets/blocks/horizontal-caotic.png'),(BLOCK_WIDTH,BLOCK_HEIGHT))
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

    x = 10
    y = 85
    block_type = "solid"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 70
    y = 85
    block_type = "breakable"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 130
    y = 85
    block_type = "translucent"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    x = 190
    y = 85
    block_type = "caotic"
    new_block = Block(x, y, block_type)
    blocks.append(new_block)

    return blocks
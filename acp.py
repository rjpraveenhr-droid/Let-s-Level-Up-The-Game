
import pygame
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 500, 400
MOVEMENT_SPEED = 5
FONT_SIZE = 48
FOOD_COUNT = 5

# Initialize Pygame
pygame.init()

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dog Food Collection Game")

# Load background image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(
    background_image, (SCREEN_WIDTH, SCREEN_HEIGHT)
)

# Load dog image
dog_image = pygame.image.load("dog.jpeg")
dog_image = pygame.transform.scale(dog_image, (60, 60))

# Load font
font = pygame.font.SysFont("Times New Roman", FONT_SIZE)


# Sprite class for food
class Sprite(pygame.sprite.Sprite):

    def __init__(self, color, height, width):
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        self.rect = self.image.get_rect()

    def move(self, x_change, y_change):
        self.rect.x = max(
            min(self.rect.x + x_change,
                SCREEN_WIDTH - self.rect.width), 0
        )

        self.rect.y = max(
            min(self.rect.y + y_change,
                SCREEN_HEIGHT - self.rect.height), 0
        )


# Create sprite groups
all_sprites = pygame.sprite.Group()
food_sprites = pygame.sprite.Group()

# Create dog
dog = pygame.sprite.Sprite()
dog.image = dog_image
dog.rect = dog.image.get_rect()

dog.rect.x = random.randint(
    0, SCREEN_WIDTH - dog.rect.width
)
dog.rect.y = random.randint(
    0, SCREEN_HEIGHT - dog.rect.height
)

all_sprites.add(dog)

# Create food
for i in range(FOOD_COUNT):

    food = Sprite(pygame.Color('brown'), 20, 20)

    food.rect.x = random.randint(
        0, SCREEN_WIDTH - food.rect.width
    )
    food.rect.y = random.randint(
        0, SCREEN_HEIGHT - food.rect.height
    )

    all_sprites.add(food)
    food_sprites.add(food)


# Game loop variables
running = True
won = False

clock = pygame.time.Clock()

# Main game loop
while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            running = False

    if not won:

        # Keyboard controls
        keys = pygame.key.get_pressed()

        x_change = (
            keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]
        ) * MOVEMENT_SPEED

        y_change = (
            keys[pygame.K_DOWN] - keys[pygame.K_UP]
        ) * MOVEMENT_SPEED

        # Move dog
        dog.rect.x = max(
            min(dog.rect.x + x_change,
                SCREEN_WIDTH - dog.rect.width), 0
        )

        dog.rect.y = max(
            min(dog.rect.y + y_change,
                SCREEN_HEIGHT - dog.rect.height), 0
        )

        # Check food collision
        collected_food = pygame.sprite.spritecollide(
            dog, food_sprites, True
        )

        # Remove collected food
        for food in collected_food:
            all_sprites.remove(food)

        # Check if all food is collected
        if len(food_sprites) == 0:
            won = True

    # Draw background
    screen.blit(background_image, (0, 0))

    # Draw sprites
    all_sprites.draw(screen)

    # Display completion message
    if won:

        win_text = font.render(
            "You Win!",
            True,
            pygame.Color('black')
        )

        screen.blit(
            win_text,
            (
                (SCREEN_WIDTH - win_text.get_width()) // 2,
                (SCREEN_HEIGHT - win_text.get_height()) // 2
            )
        )

    pygame.display.flip()
    clock.tick(90)

pygame.quit()

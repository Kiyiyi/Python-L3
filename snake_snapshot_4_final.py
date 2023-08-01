# Import the necessary libraries
import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define some constants
WIDTH, HEIGHT = 600, 600  # The width and height of the game window
BACKGROUND_COLOR = (0, 0, 0)  # The color of the background (black)
SNAKE_COLOR = (0, 255, 0)  # The color of the snake (green)
FOOD_COLOR = (255, 0, 0)  # The color of the food (red)
TEXT_COLOR = (255, 255, 255)  # The color of the text (white)
SNAKE_SIZE = 20  # The size of the snake segments and food items
FPS = 15  # The speed of the game (frames per second)


class Snake:
    def __init__(self):
        # Set initial position and speed
        self.position = [[300, 300], [320, 300], [340, 300]]
        self.speed = [0, 0]

    def move(self):
        tail = self.position[-1]
        self.position = [[self.position[0][0] + self.speed[0],
                          self.position[0][1] + self.speed[1]]] + self.position[:-1]
        return tail

    def eat(self, food_position, tail):
        if self.position[0] == food_position:
            self.position.append(tail)
            return True
        return False

    def draw(self):
        # Draw each segment of the snake
        for position in self.position:
            pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(position[0], position[1], SNAKE_SIZE, SNAKE_SIZE))


# functions
def is_game_over(snake):
    # The game is over if the snake's head is outside the screen or if the snake's head is in its body
    return snake.position[0] in snake.position[1:] or \
           snake.position[0][0] not in range(0, WIDTH, SNAKE_SIZE) or \
           snake.position[0][1] not in range(0, HEIGHT, SNAKE_SIZE)


def get_high_score():
    try:
        with open('highscore.txt', 'r') as f:
            return int(f.read())
    except FileNotFoundError:
        return 0


def save_high_score(highscore):
    with open('highscore.txt', 'w') as f:
        f.write(str(highscore))


# Define a function to display the start screen
def start_screen(snake):
    # Display the text "Press any arrow key to start" at the center of the screen
    high_score = get_high_score()
    font = pygame.font.Font(None, 36)
    text = font.render('Press any arrow key to start', True, TEXT_COLOR)
    text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2))
    score_text = font.render('High Score: ' + str(high_score), True, TEXT_COLOR)
    score_text_rect = score_text.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))

    while True:
        screen.fill(BACKGROUND_COLOR)
        screen.blit(text, text_rect)
        screen.blit(score_text, score_text_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.speed = [0, -SNAKE_SIZE]  # Go up
                    return
                elif event.key == pygame.K_DOWN:
                    snake.speed = [0, SNAKE_SIZE]  # Go down
                    return
                elif event.key == pygame.K_LEFT:
                    snake.speed = [-SNAKE_SIZE, 0]  # Go left
                    return
                elif event.key == pygame.K_RIGHT:
                    snake.position = [[300, 300], [280, 300], [260, 300]]  # Reset the snake's position
                    snake.speed = [SNAKE_SIZE, 0]  # Go right
                    return


# Define a function to handle events
def process_events(snake):
    # Loop through all the events
    for event in pygame.event.get():
        # If the event is QUIT, exit the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # If the event is a key press
        elif event.type == pygame.KEYDOWN:
            # If the key is UP and the snake is not moving down
            if event.key == pygame.K_UP and snake.speed != [0, SNAKE_SIZE]:
                # Set the snake's speed to move up
                snake.speed = [0, -SNAKE_SIZE]
            # If the key is DOWN and the snake is not moving up
            elif event.key == pygame.K_DOWN and snake.speed != [0, -SNAKE_SIZE]:
                # Set the snake's speed to move down
                snake.speed = [0, SNAKE_SIZE]
            # If the key is LEFT and the snake is not moving right
            elif event.key == pygame.K_LEFT and snake.speed != [SNAKE_SIZE, 0]:
                # Set the snake's speed to move left
                snake.speed = [-SNAKE_SIZE, 0]
            # If the key is RIGHT and the snake is not moving left
            elif event.key == pygame.K_RIGHT and snake.speed != [-SNAKE_SIZE, 0]:
                # Set the snake's speed to move right
                snake.speed = [SNAKE_SIZE, 0]


# Define a function to update the game's state
def update_game_state(snake, food_position):
    # Move the snake and get the old tail position
    tail = snake.move()
    # Check if the snake eats the food
    food_eaten = snake.eat(food_position, tail)
    # If the food was eaten, generate a new food position
    if food_eaten:
        food_position = [(random.randrange(0, WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                         (random.randrange(0, HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]
    return food_position, food_eaten

# Function to display the score
def display_score(score):
    font = pygame.font.Font(None, 36)  # Create a font object
    score_text = font.render('Score: ' + str(score), True, TEXT_COLOR)  # Create a text surface
    screen.blit(score_text, (10, 10))  # Draw the text surface onto the screen

# Define a function to draw the game objects
def draw_game_objects(snake, food_position):
    # Clear the screen and draw the snake and the food
    screen.fill(BACKGROUND_COLOR)
    snake.draw()
    pygame.draw.rect(screen, FOOD_COLOR, pygame.Rect(food_position[0], food_position[1], SNAKE_SIZE, SNAKE_SIZE))


# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

snake = Snake()
food_position = [(random.randrange(0, WIDTH // SNAKE_SIZE)) * SNAKE_SIZE,
                 (random.randrange(0, HEIGHT // SNAKE_SIZE)) * SNAKE_SIZE]



# Main game loop
while True:
    # Process events, update the game state, and draw the game objects
    process_events(snake)
    food_position, food_eaten = update_game_state(snake, food_position)
    draw_game_objects(snake, food_position)
    # Draw the score
    score = len(snake.position) - 3  # Calculate the score
    display_score(score)
    # Update the display
    pygame.display.update()
    # Check for game over
    if is_game_over(snake):
        if len(snake.position) - 3 > get_high_score():
            save_high_score(len(snake.position) - 3)
        snake = Snake()
        start_screen(snake)
    pygame.time.Clock().tick(FPS)
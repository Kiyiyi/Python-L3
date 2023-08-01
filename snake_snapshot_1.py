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

	def draw(self):
		# Draw each segment of the snake
		for position in self.position:
			pygame.draw.rect(screen, SNAKE_COLOR, pygame.Rect(position[0], position[1], SNAKE_SIZE, SNAKE_SIZE))


# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))

snake = Snake()

# Main game loop
while True:
	# Fill the background
	screen.fill(BACKGROUND_COLOR)
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
	tail = snake.move()
	snake.draw()
	# Update the display
	pygame.display.update()
	pygame.time.Clock().tick(FPS)
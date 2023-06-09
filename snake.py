import pygame
import random

# Initialize Pygame
pygame.init()

# Define the game window dimensions
window_width = 800
window_height = 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Snake Game")


class Snake:
    def __init__(self):
        # Initialize the snake's position, speed, and size
        self.size = 1
        self.segments = [(window_width // 2, window_height // 2)]
        self.speed = 20

    def move(self, direction):
        # Update the snake's position based on the current direction
        x, y = self.segments[0]
        if direction == "UP":
            y -= self.speed
        elif direction == "DOWN":
            y += self.speed
        elif direction == "LEFT":
            x -= self.speed
        elif direction == "RIGHT":
            x += self.speed
        self.segments.insert(0, (x, y))
        if len(self.segments) >= self.size:
            self.segments.pop()

    def draw(self):
        # Draw the snake on the game window
        for segment in self.segments:
            pygame.draw.rect(window, (0, 255, 0),
                             (segment[0], segment[1], self.speed, self.speed))


class Food:
    def __init__(self):
        # Initialize the food's position
        self.x = random.randint(0, window_width - 20)
        self.y = random.randint(0, window_height - 20)

    def draw(self):
        # Draw the food on the game window
        pygame.draw.rect(window, (255, 0, 0), (self.x, self.y, 20, 20))


def game_loop():
    snake = Snake()
    food = Food()
    direction = "RIGHT"

    clock = pygame.time.Clock()
    game_over = False
    lives = 10  # Maximum number of lives

    font = pygame.font.Font(None, 36)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        snake.move(direction)

        if snake.segments[0] == (food.x, food.y):
            snake.size += 1
            food = Food()

        x, y = snake.segments[0]
        if (x < 0 or x >= window_width or y < 0 or y >= window_height):
            x = (x + window_width) % window_width
            y = (y + window_height) % window_height
            snake.segments[0] = (x, y)
            lives -= 1
            if lives == 0:
                game_over = True

        window.fill((0, 0, 0))  # Clear the window
        snake.draw()
        food.draw()

        # Display remaining lives
        lives_text = font.render("Lives: " + str(lives), True, (255, 255, 255))
        window.blit(lives_text, (10, 10))

        pygame.display.update()
        clock.tick(10)  # Control the game's frame rate

    # Display game over screen
    game_over_text = font.render(
        "Game Over, Please Try Again!", True, (255, 255, 255))
    game_over_rect = game_over_text.get_rect(
        center=(window_width // 2, window_height // 2))
    try_again_button = pygame.Rect(
        (window_width // 2) - 75, (window_height // 2) + 50, 150, 50)
    try_again_text = font.render("Try Again", True, (255, 255, 255))

    while game_over:
        window.fill((0, 0, 0))
        window.blit(game_over_text, game_over_rect)

        pygame.draw.rect(window, (0, 0, 255), try_again_button)
        window.blit(try_again_text, try_again_button.move(25, 10).topleft)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if try_again_button.collidepoint(mouse_pos):
                    game_over = False


# Start the game
game_loop()

# Quit Pygame
pygame.quit()

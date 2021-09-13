import pygame
import random
import time
from typing import List

pygame.init()
DIRECTIONS = {"UP": 1, "DOWN": 2, "LEFT": 3, "RIGHT": 4}
font = pygame.font.Font('arial.ttf', 25)

# rgb colors
WHITE = (255, 255, 255)
RED = (200, 0, 0)
GREEN1 = (0, 128, 0)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)

BLOCK_SIZE = 20
SPEED = 15


class Point:
    """
    Creates a point object to store locations
    """
    x: int
    y: int

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def update(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other) -> bool:
        if type(other) == Point:
            if self.x == other.x and self.y == other.y:
                return True
        return False


class Snake:
    """
    Starts the Snake Game
    Pixels: 25 x 25
    === Attributes ===
    height: height of the display window
    width: width of the display window
    display: pygame's display window
    direction: Current Snake movement direction
    snake: List[] - All of the Snake's body parts
    head: Point()
    """
    height: int
    width: int
    direction: int
    snake: List[Point]
    head: Point
    score: int
    clock: pygame.time.Clock
    food: Point

    def __init__(self, height=500, width=500) -> None:
        self.score = 0
        self.height = height
        self.width = width
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake Game")
        self.direction = DIRECTIONS["RIGHT"]
        self.head = Point(12 * BLOCK_SIZE, 12 * BLOCK_SIZE)
        self.snake = [self.head, Point(self.head.x - BLOCK_SIZE, self.head.y)]
        self.clock = pygame.time.Clock()
        self.food = Point(0, 0)
        self._place_food()

        # Draw the initial state
        self._update_ui()

    def step_game(self):
        """
        Moves the game through one frame
        """
        # 1. Check if player moved
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    self.direction = DIRECTIONS["DOWN"]
                elif event.key == pygame.K_UP:
                    self.direction = DIRECTIONS["UP"]
                elif event.key == pygame.K_LEFT:
                    self.direction = DIRECTIONS["LEFT"]
                elif event.key == pygame.K_RIGHT:
                    self.direction = DIRECTIONS["RIGHT"]
        # 2. Move the snake in the direction the player moved

        if self.direction == 1:
            self.head = Point(self.head.x, self.head.y - BLOCK_SIZE)
        elif self.direction == 2:
            self.head = Point(self.head.x, self.head.y + BLOCK_SIZE)
        elif self.direction == 3:
            self.head = Point(self.head.x - BLOCK_SIZE, self.head.y)
        elif self.direction == 4:
            self.head = Point(self.head.x + BLOCK_SIZE, self.head.y)

        self.snake.insert(0, self.head)

        # 3. Check if the player lost
        game_over = self._check_lose()

        # 4. Check if the player hit the food and add to the snake
        if self.food == self.head:
            self._place_food()
            self.score += 1
        else:
            self.snake.pop()

        # 5. Update the score and the UI accordingly
        self._update_ui()
        self.clock.tick(SPEED)

        return game_over, self.score

    def _check_lose(self) -> bool:
        if 0 <= self.head.x <= 480 and 0 <= self.head.y <= 480:
            if self.head not in self.snake[1:]:
                return True
        return False

    def _update_ui(self) -> None:
        """
        Updates the game screen
        :return:
        """
        # Fills the display black
        self.display.fill(BLACK)

        # Used for testing axis
        # pygame.draw.rect(self.display, GREEN1, pygame.Rect(20, 20, BLOCK_SIZE, BLOCK_SIZE))

        # Draws the snake out
        for point in self.snake:
            pygame.draw.rect(self.display, GREEN1,
                             pygame.Rect(point.x, point.y, BLOCK_SIZE,
                                         BLOCK_SIZE))
            # pygame.draw.rect(self.display, BLUE2,
            #                  pygame.Rect(point.x + 4, point.y + 4, 12, 12))

        # Draws the food out
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        # Draws out the score board
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _place_food(self):
        """
        Places the food randomly on the screen
        :return:
        """
        food = Point(random.randint(0, 24) * BLOCK_SIZE, random.randint(0, 24) * BLOCK_SIZE)
        if food in self.snake:
            self._place_food()
        else:
            self.food = food


if __name__ == "__main__":
    # x = Point(1, 2)
    # y = Point(1, 2)
    # print(x == y)

    game = Snake()
    while True:
        result, score = game.step_game()
        if result is False:
            break
    print("High Score:", score)
    pygame.quit()

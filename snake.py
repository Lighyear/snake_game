import tkinter as tk
import random

# Constants
GAME_WIDTH = 600
GAME_HEIGHT = 400
SQUARE_SIZE = 20
GAME_SPEED = 100
SNAKE_COLOR = "green"
FOOD_COLOR = "red"
BACKGROUND_COLOR = "black"

class SnakeGame:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Snake Game")
        self.canvas = tk.Canvas(self.window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
        self.canvas.pack()

        self.score = 0
        self.game_over = False
        self.is_paused = False

        # Snake initial setup
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.snake_direction = "Right"

        # Food setup
        self.food = [0, 0]
        self.place_food()

        # Bind controls
        self.window.bind("<KeyPress>", self.handle_keypress)

        # Game loop
        self.run_game()
        self.window.mainloop()

    def place_food(self):
        x = random.randint(0, (GAME_WIDTH // SQUARE_SIZE) - 1) * SQUARE_SIZE
        y = random.randint(0, (GAME_HEIGHT // SQUARE_SIZE) - 1) * SQUARE_SIZE
        self.food = [x, y]

    def handle_keypress(self, event):
        if event.keysym == "Left" and self.snake_direction != "Right":
            self.snake_direction = "Left"
        elif event.keysym == "Right" and self.snake_direction != "Left":
            self.snake_direction = "Right"
        elif event.keysym == "Up" and self.snake_direction != "Down":
            self.snake_direction = "Up"
        elif event.keysym == "Down" and self.snake_direction != "Up":
            self.snake_direction = "Down"
        elif event.keysym == "p":  # Pause/Resume
            self.is_paused = not self.is_paused
        elif event.keysym == "r":  # Restart
            self.restart_game()

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.snake_direction == "Right":
            head_x += SQUARE_SIZE
        elif self.snake_direction == "Left":
            head_x -= SQUARE_SIZE
        elif self.snake_direction == "Up":
            head_y -= SQUARE_SIZE
        elif self.snake_direction == "Down":
            head_y += SQUARE_SIZE

        # Add new head
        new_head = [head_x, head_y]
        self.snake.insert(0, new_head)

        # Check collision with food
        if head_x == self.food[0] and head_y == self.food[1]:
            self.score += 1
            self.place_food()
        else:
            # Remove tail
            self.snake.pop()

    def check_collision(self):
        head_x, head_y = self.snake[0]

        # Check wall collision
        if head_x < 0 or head_x >= GAME_WIDTH or head_y < 0 or head_y >= GAME_HEIGHT:
            return True

        # Check self collision
        if [head_x, head_y] in self.snake[1:]:
            return True

        return False

    def draw_elements(self):
        self.canvas.delete("all")

        # Draw snake
        for segment in self.snake:
            self.canvas.create_rectangle(
                segment[0], segment[1],
                segment[0] + SQUARE_SIZE, segment[1] + SQUARE_SIZE,
                fill=SNAKE_COLOR
            )

        # Draw food
        self.canvas.create_oval(
            self.food[0], self.food[1],
            self.food[0] + SQUARE_SIZE, self.food[1] + SQUARE_SIZE,
            fill=FOOD_COLOR
        )

        # Draw score
        self.canvas.create_text(
            50, 10, text=f"Score: {self.score}", fill="white", font=("Arial", 14)
        )

    def run_game(self):
        if not self.game_over:
            if not self.is_paused:
                self.move_snake()
                if self.check_collision():
                    self.game_over = True
                    self.canvas.create_text(
                        GAME_WIDTH // 2, GAME_HEIGHT // 2,
                        text="GAME OVER",
                        fill="white",
                        font=("Arial", 24)
                    )
                else:
                    self.draw_elements()
            self.window.after(GAME_SPEED, self.run_game)

    def restart_game(self):
        # Reset game state
        self.score = 0
        self.game_over = False
        self.is_paused = False
        self.snake = [[100, 100], [80, 100], [60, 100]]
        self.snake_direction = "Right"
        self.place_food()
        self.run_game()

# Run the game
if __name__ == "__main__":
    SnakeGame()
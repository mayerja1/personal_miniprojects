from random import randint


class Game:
    EMPTY = 0
    SNAKE = 1
    FOOD = 2

    LEFT = (0, -1)
    RIGHT = (0, 1)
    UP = (-1, 0)
    DOWN = (1, 0)

    DIRS = (LEFT, RIGHT, UP, DOWN)

    def __init__(self, snake_init_len=1, width=30, height=30):
        self.WIDTH, self.HEIGHT = width, height
        self.board = [self.WIDTH * [0] for _ in range(self.HEIGHT)]
        self.snake = [(self.HEIGHT // 2, self.WIDTH // 2 - snake_init_len // 2 + i) for i in range(snake_init_len)]
        self.direction = self.LEFT
        self.game_over = False
        self.place_snake()
        self.food_coords = -1, -1
        self.new_food()

    def map_on_snakes_positions(self, func):
        for x, y in self.snake:
            self.board[x][y] = func(self.board[x][y])

    def new_food(self):
        found = False
        x, y = -1, -1
        while not found:
            x, y = randint(0, self.WIDTH - 1), randint(0, self.HEIGHT - 1)
            if (x, y) not in self.snake:
                found = True
        self.board[x][y] = self.FOOD
        self.food_coords = (x, y)

    def place_snake(self):
        self.map_on_snakes_positions(lambda _: self.SNAKE)

    def remove_snake(self):
        self.map_on_snakes_positions(lambda _: self.EMPTY)

    def board_at_coords(self, coords):
        x, y = coords
        return self.board[x][y]

    def move_snake(self):
        head_x, head_y = self.snake[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        if new_head in self.snake or not self.validate_coords(new_head):
            self.game_over = True
            print('game over, snake atempted to move to {0}'.format(new_head))
        else:
            self.remove_snake()
            rest = self.snake[:-1]
            if self.board_at_coords(new_head) == self.FOOD:
                rest = self.snake
                self.new_food()
            self.snake = [new_head] + rest
            self.place_snake()

    def change_direction(self, direction):
        d = {self.LEFT: 1, self.RIGHT: -1, self.UP: 2, self.DOWN: -2}
        # if we're not trying to change to the opposite direction
        if d[direction] != -d[self.direction]:
            self.direction = direction

    def validate_coords(self, coords):
        x, y = coords
        return 0 <= x < self.HEIGHT and 0 <= y < self.WIDTH

    @staticmethod
    def valid_moves(snake, width, height):
        snake_x, snake_y = snake[0]
        for dx, dy in Game.DIRS:
            new_x, new_y = snake_x + dx, snake_y + dy
            if 0 <= new_x < height and 0 <= new_y < width and (new_x, new_y) not in snake:
                yield new_x, new_y

    def print_board(self):
        for row in self.board:
            print(row)

from queue import PriorityQueue
from Game import Game
import abc
from random import choice


class Player(abc.ABC):
    @abc.abstractmethod
    def get_next_move(self, game):
        pass

    @staticmethod
    def direction_from_move(pos, snake):
        d = {(0, -1): Game.LEFT, (0, 1): Game.RIGHT, (-1, 0): Game.UP, (1, 0): Game.DOWN}
        x, y = pos
        head_x, head_y = snake[0]
        dx, dy = x - head_x, y - head_y

        assert (dx, dy) in d
        return d[(dx, dy)]


class AIPlayer(Player):
    def get_next_move(self, game):
        closed_set = set()
        q = PriorityQueue()
        came_from = {}
        dists = {}
        q.put((0, tuple(game.snake)))
        dists[tuple(game.snake)] = 0
        food_x, food_y = game.food_coords
        counter = 0
        while not q.empty():
            dist, snake = q.get()
            closed_set.add(snake[0])
            counter += 1
            if snake[0] == (food_x, food_y):
                return AIPlayer.first_move(snake, came_from, game.snake)
            for m in Game.valid_moves(snake, game.WIDTH, game.HEIGHT):
                new_snake = tuple([m] + list(snake)[:-1])
                if new_snake[0] not in closed_set:
                    new_dist = dists[snake] + 1
                    if new_snake not in dists:
                        dists[new_snake] = new_dist
                    elif dists[new_snake] < new_dist:
                        continue
                    came_from[new_snake] = snake
                    dists[new_snake] = new_dist
                    newhead_x, newhead_y = new_snake[0]
                    q.put((new_dist + AIPlayer.get_heuristic(newhead_x, newhead_y, food_x, food_y), tuple(new_snake)))
        # there is no way the snake will be able to get the food
        return RandomPlayer().get_next_move(game)


    @staticmethod
    def get_heuristic(x1, y1, x2, y2):
        return abs(x2 - x1) + abs(y2 - y1)

    @staticmethod
    def first_move(end, came_from, start):
        path = [end]
        while end in came_from:
            path.append(came_from[end])
            end = came_from[end]
        #print(([x[0] for x in path]))
        #print(path[1][0], path[0][0])
        #fixme
        return Player.direction_from_move(path[-2][0], path[-1])


class RandomPlayer(Player):
    def get_next_move(self, game):
        return Player.direction_from_move(choice(list(Game.valid_moves(game.snake, game.WIDTH, game.HEIGHT))), game.snake)

if __name__ == '__main__':
    g = Game(snake_init_len=3, width=30, height=30)
    player = AIPlayer()
    #g.print_board()
    for _ in range(1):
        g.change_direction(player.get_next_move(g))
        print(g.direction)
        g.move_snake()
    print()
    #g.print_board()

import numpy as np
import random
from PIL import Image, ImageDraw
from copy import copy
from collections import deque

# maze parameters
ENTRANCE = (1, 0)
EXIT = (-2, -1)

# constants to distinguish parts of the maze
WALL = 0
FREE = 1
SOLUTION = 2

# constants for maze rendering
BLOCK_SIZE = 10
PADDING = 50

def generate_maze(size):
    DIRS = np.array(((0, 2), (2, 0), (-2, 0), (0, -2)))
    maze = np.ones(size) * WALL

    def create_paths(start):
        stack = [start]
        while stack:
            cur = stack.pop()
            maze[cur] = FREE
            for d in shuffled(DIRS):
                neighbour = cur + d
                wall = cur + d // 2
                t_neighbour = tuple(neighbour)
                if possible_free_coords(size, neighbour) and maze[tuple(neighbour)] != FREE:
                    maze[tuple(wall)] = FREE
                    stack.append(cur)
                    stack.append(t_neighbour)
                    break

    create_paths((1, 1))
    # create entrance and exit
    maze[ENTRANCE] = FREE
    maze[EXIT] = FREE
    return maze

def render_maze(maze):
    pic = Image.new('RGB', tuple(maze.shape * np.array([BLOCK_SIZE]) + 2 * PADDING), color='#FFF')
    draw = ImageDraw.Draw(pic)
    for x, row in enumerate(maze):
        for y, block in enumerate(row):
            color = '#FFF'
            if maze[x, y] == WALL: color = '#000'
            elif maze[x, y] == SOLUTION: color = '#F00'
            draw.rectangle([x * BLOCK_SIZE + PADDING, y * BLOCK_SIZE + PADDING, \
                            (x + 1) * BLOCK_SIZE + PADDING, (y + 1) * BLOCK_SIZE + PADDING], fill=color)
    pic.save('maze.png')

def possible_free_coords(size, coords):
    return ((0, 0) < coords).all() and (coords + 1 < size).all()

def valid_coords(size, coords):
    return ((0, 0) <= coords).all() and (coords < size).all()

def shuffled(arr):
    ret = copy(arr)
    np.random.shuffle(ret)
    return ret

def get_path(maze):
    q = deque([ENTRANCE])
    end = np.array(maze.shape) + EXIT
    visited = set()
    previous = {ENTRANCE: None}
    DIRS = np.array(((0, 1), (1, 0), (-1, 0), (0, -1)))
    while q:
        cur_node = q.popleft()
        visited.add(tuple(cur_node))
        if (cur_node == end).all():
            path = [tuple(end)]
            prev = previous[tuple(end)]
            while prev is not None:
                path.append(prev)
                prev = previous[prev]
            return path[::-1]
        for d in DIRS:
            neighbour = cur_node + d
            t_neighbour = tuple(neighbour)
            if valid_coords(maze.shape, neighbour) and maze[t_neighbour] == 1 and t_neighbour not in visited:
                q.append(neighbour)
                previous[t_neighbour] = tuple(cur_node)

def solve_maze(maze):
    path = get_path(maze)
    if not path:
        raise Exception("Maze doesn't have a solution")
    for n in path:
        maze[n] = SOLUTION


if __name__ == '__main__':
    maze = generate_maze((1001, 1001))
    solve_maze(maze)
    render_maze(maze)

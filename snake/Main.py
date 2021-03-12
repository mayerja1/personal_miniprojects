import pygame as pg
from Game import Game
from Player import RandomPlayer, AIPlayer


class Main:
    # constants
    GAME_W, GAME_H = 10, 10
    WIDTH, HEIGHT = 600, 600
    RECT_SIZE = WIDTH // GAME_W
    FRAMERATE = 5
    PERIOD = 1000 // FRAMERATE

    def __init__(self):
        pg.init()
        self.win = pg.display.set_mode((self.WIDTH, self.HEIGHT))
        pg.display.set_caption("Snake")

    def draw_game(self, board, offset_x=0, offset_y=0):
        colors = pg.color.THECOLORS
        coloring = {Game.SNAKE: colors['green'], Game.EMPTY: colors['black'], Game.FOOD: colors['red']}
        pg.draw.rect(self.win, (50, 50, 50, 50), (0, 0, self.WIDTH, self.HEIGHT))
        for x, row in enumerate(board):
            for y, val in enumerate(row):
                if val != Game.EMPTY:
                    pg.draw.rect(self.win, coloring[val], (y * self.RECT_SIZE + offset_y, x * self.RECT_SIZE + offset_x,
                                                           self.RECT_SIZE, self.RECT_SIZE))
        pg.display.update()

    def play_round(self):
        game = Game(snake_init_len=self.GAME_W // 3, width=self.GAME_W, height=self.GAME_H)
        run = True
        player = AIPlayer()
        while run and not game.game_over:
            pg.time.delay(self.PERIOD)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False
                elif event.type == pg.KEYDOWN:
                    continue
                    dirs = {pg.K_UP: Game.UP, pg.K_DOWN: Game.DOWN, pg.K_RIGHT: Game.RIGHT, pg.K_LEFT: Game.LEFT}
                    if event.key in dirs:
                        game.change_direction(dirs[event.key])
            self.draw_game(game.board)
            game.change_direction(player.get_next_move(game))
            game.move_snake()
        return run

    def main(self):
        while self.play_round():
            pass
        pg.quit()


if __name__ == '__main__':
    Main().main()

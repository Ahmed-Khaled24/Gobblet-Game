import pygame
from pygame.locals import *
from src.backend.game import Game

CIRCLE_ON_BOARD = USEREVENT + 2
BLACK_STACKS = USEREVENT + 3
RED_STACKS = USEREVENT + 4
STACK_DISTANCE = 80
BLACK_STACK_Y = -10
RED_STACK_Y = -11


class Human:
    def __init__(self):
        self.left, self.top = 161, 80
        self._i, self._j = -1, -1
        self.selected = False

    def on_event(self, event, game: Game):

        if event.type == CIRCLE_ON_BOARD:
            if (game.board.grid[event.x][event.y][-1] is not None and
                    game.board.grid[event.x][event.y][-1].color.value == game.turn.value):
                if not self.selected:
                    self._i = event.x
                    self._j = event.y

        if event.type == BLACK_STACKS:  # Black stacks
            if event.player == 'B':
                if not self.selected:
                    self._i = event.x
                    self._j = BLACK_STACK_Y

        if event.type == RED_STACKS:  # Red stacks
            if event.player == 'R':
                if not self.selected:
                    self._i = event.x
                    self._j = RED_STACK_Y

        if event.type == pygame.MOUSEBUTTONUP:
            x = event.pos[0]
            y = event.pos[1]
            for i in range(4):
                for j in range(4):
                    if not self.selected:
                        if game.board.grid[i][j][-1] is not None:
                            if (x - (200 + STACK_DISTANCE * i)) ** 2 + (y - (120 + STACK_DISTANCE * j)) ** 2 <= (
                                    9 * game.board.grid[i][j][-1].size.value) ** 2:
                                if game.turn.value == game.board.grid[i][j][-1].color.value:
                                    self.selected = True
                    else:
                        try:
                            if Rect(self.left + STACK_DISTANCE * i, self.top + STACK_DISTANCE * j, STACK_DISTANCE,
                                    STACK_DISTANCE).collidepoint(x, y):
                                if self._j == BLACK_STACK_Y:
                                    game.addGobblet(i, j, game.player2.pieces[-(self._i + 2)][-1], -(self._i + 2))

                                elif self._j == RED_STACK_Y:
                                    game.addGobblet(i, j, game.player1.pieces[self._i - 4][-1], self._i - 4)

                                else:
                                    game.moveGobblet(self._i, self._j, i, j)
                                self.selected = False
                                game.statusCheck()
                                return True
                        except Exception:
                            pass

            for i in range(3):
                if game.turn.value == 'B':
                    if (x - 100) ** 2 + (y - (280 + (STACK_DISTANCE * i))) ** 2 <= (9 * 4) ** 2:
                        self.selected = True

            for i in range(3):
                if game.turn.value == 'R':
                    if (x - 540) ** 2 + (y - (40 + (STACK_DISTANCE * (2 - i)))) ** 2 <= (9 * 4) ** 2:
                        self.selected = True
        return self.selected

    def on_loop(self, game: Game):
        x, y = pygame.mouse.get_pos()
        for i in range(4):
            for j in range(4):
                if game.board.grid[i][j][-1] is not None:
                    if (x - (200 + STACK_DISTANCE * i)) ** 2 + (y - (120 + STACK_DISTANCE * j)) ** 2 <= (
                            10 * game.board.grid[i][j][-1].size.value) ** 2:
                        hover = CIRCLE_ON_BOARD
                        MouseHoverevent = pygame.event.Event(hover, x=i, y=j, player=game.turn.value)
                        pygame.event.post(MouseHoverevent)
        for i in range(3):
            if (x - 100) ** 2 + (y - (280 + (STACK_DISTANCE * i))) ** 2 <= (9 * 4) ** 2:
                hover = BLACK_STACKS
                MouseHoverevent = pygame.event.Event(hover, x=-2 - i, player=game.turn.value)
                pygame.event.post(MouseHoverevent)
        for i in range(3):
            if (x - 540) ** 2 + (y - (40 + (STACK_DISTANCE * (2 - i)))) ** 2 <= (9 * 4) ** 2:
                hover = RED_STACKS
                MouseHoverevent = pygame.event.Event(hover, x=4 + i, player=game.turn.value)
                pygame.event.post(MouseHoverevent)

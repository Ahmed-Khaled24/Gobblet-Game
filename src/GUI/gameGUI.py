import pygame
from pygame.locals import *
from src.backend.game import Game

COLOURS = {'B': (35, 31, 38), 'R': (69, 0, 1), 'W': (255, 255, 255)}


def cleanup():
    pygame.quit()


class GUI:
    def __init__(self):
        self._running = True
        self.win = None
        self.size = self.weight, self.height = 640, 480
        self.center = self.left, self.top = 162, 80
        self.turn = 'R'
        self._i, self._j = -1, -1
        self.selected = False
        self.myfont = pygame.font.SysFont("monospace", 28)
        self.turns = {'R': (self.myfont.size("Red's turn"),
                            self.myfont.render("Red's turn", True, COLOURS['W'])),
                      'B': (self.myfont.size("Black's turn"),
                            self.myfont.render("Black's turn", True, COLOURS['W'])),
                      'WB': (self.myfont.size("BLACK WON"),
                             self.myfont.render("BLACK WON!!", True, COLOURS['W'])),
                      'WR': (self.myfont.size("RED WON"),
                             self.myfont.render("RED WON!!", True, COLOURS['W']))}

    def nextturn(self):
        if self.turn == 'R':
            self.turn = 'B'
        elif self.turn == 'B':
            self.turn = 'R'

    def on_init(self):
        pygame.init()
        self.win = pygame.display.set_mode(self.size)
        self._running = True

    def on_event(self, event, game: Game):
        if event.type == pygame.QUIT:
            cleanup()
        if event.type == USEREVENT + 2:  # Circle on board
            if game.board.grid[event.x][event.y][-1] is not None and game.board.grid[event.x][event.y][
                -1].color.value == self.turn:
                if not (self.selected):
                    self._i = event.x
                    self._j = event.y

        if event.type == USEREVENT + 3:  # Black stacks
            if event.player == 'B':
                if not (self.selected):
                    self._i = event.x
                    self._j = -10

        if event.type == USEREVENT + 4:  # Red stacks
            if event.player == 'R':
                if not (self.selected):
                    self._i = event.x
                    self._j = -11

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self._running = False
            if event.key == pygame.K_SPACE:
                self._running = False

        if event.type == pygame.MOUSEBUTTONUP:
            x = event.pos[0]
            y = event.pos[1]
            for i in range(4):
                for j in range(4):
                    if not (self.selected):
                        if game.board.grid[i][j][-1] is not None:
                            if (x - (self.left + 80 * i + 40)) ** 2 + (y - (self.top + 80 * j + 40)) ** 2 <= (
                                    10 * game.board.grid[i][j][-1].size.value) ** 2:
                                if self.turn == game.board.grid[i][j][-1].color.value:
                                    self.selected = True
                    else:
                        try:
                            if Rect(self.left + 80 * i, self.top + 80 * j, 80, 80).collidepoint(x, y):
                                if self._j == -10:
                                    game.addGobblet(i, j, game.player2.pieces[-(self._i + 2)][-1])
                                    game.player2.remove_from_external_stack(-(self._i + 2))
                                elif self._j == -11:
                                    game.addGobblet(i, j, game.player1.pieces[self._i - 4][-1])
                                    game.player1.remove_from_external_stack(self._i - 4)
                                else:
                                    game.moveGobblet((self._i, self._j), (i, j))
                                self.selected = False
                                game.statusCheck()
                                self.nextturn()
                        except Exception:
                            pass

            for i in range(3):
                if self.turn == 'B':
                    if (x - (self.left + 80 * -1 - 20 + 40)) ** 2 + (y - (self.top + 80 * 2 + 40 + 80 * i)) ** 2 <= (
                            9 * game.player2.pieces[i][-1].size.value) ** 2:
                        self.selected = True

            for i in range(3):
                if self.turn == 'R':
                    if (x - (self.left + 80 * 4 + 20 + 40)) ** 2 + (y - (self.top + 120 - 80 * i)) ** 2 <= (
                            9 * game.player1.pieces[i][-1].size.value) ** 2:
                        self.selected = True

    def on_loop(self, game: Game):
        x, y = pygame.mouse.get_pos()
        for i in range(4):
            for j in range(4):
                if game.board.grid[i][j][-1] is not None:
                    if (x - (self.left + 80 * i + 40)) ** 2 + (y - (self.top + 80 * j + 40)) ** 2 <= (
                            10 * game.board.grid[i][j][-1].size.value) ** 2:
                        hover = USEREVENT + 2
                        MouseHoverevent = pygame.event.Event(hover, x=i, y=j, player=self.turn)
                        pygame.event.post(MouseHoverevent)

        for i in range(3):
            if (x - (self.left + 80 * -1 - 20 + 40)) ** 2 + (y - (self.top + 80 * 2 + 40 + 80 * i)) ** 2 <= (
                    9 * game.player2.pieces[i][-1].size.value) ** 2:
                hover = USEREVENT + 3
                MouseHoverevent = pygame.event.Event(hover, x=-2 - i, player=self.turn)
                pygame.event.post(MouseHoverevent)

        for i in range(3):
            if (x - (self.left + 80 * 4 + 20 + 40)) ** 2 + (y - (self.top + 120 - 80 * i)) ** 2 <= (
                    9 * game.player1.pieces[i][-1].size.value) ** 2:
                hover = USEREVENT + 4
                MouseHoverevent = pygame.event.Event(hover, x=4 + i, player=self.turn)
                pygame.event.post(MouseHoverevent)

    def render(self, game: Game):
        self.win.fill((0, 0, 0))
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(self.win, (255, 255, 255), (self.left + 80 * i, self.top + 80 * j, 80, 80), 2, 0)
                if game.board.grid[i][j][-1] is not None:
                    pygame.draw.circle(self.win, COLOURS[game.board.grid[i][j][-1].color.value],
                                       (self.left + 80 * i + 40, self.top + 80 * j + 40),
                                       9 * game.board.grid[i][j][-1].size.value)

        for i in range(3):
            pygame.draw.circle(self.win, COLOURS['B'], (self.left - 60, self.top + 200 + 80 * i),
                               9 * game.player2.pieces[i][-1].size.value)

        for i in range(3):
            pygame.draw.circle(self.win, COLOURS['R'], (self.left + 360, self.top + 120 - 80 * i),
                               9 * game.player1.pieces[i][-1].size.value)

        if self.selected:
            pc, pr = pygame.mouse.get_pos()
            pw = 60
            ph = pw
            pr -= ph // 2
            pc -= pw // 2
            pygame.draw.circle(self.win, COLOURS[self.turn], (pc + pw // 2, pr + ph // 2), min(ph, pw) // 2)
        size, text = self.turns[self.turn]
        tw, th = size
        offset = (50 - th)
        self.win.blit(text, (offset + 10, offset))

        pygame.display.flip()

    def on_execute(self, game: Game):
        if not self.on_init():
            self._running = False
        while self._running:
            self.render(game)
            for event in pygame.event.get():
                self.on_event(event, game)
            self.on_loop(game)
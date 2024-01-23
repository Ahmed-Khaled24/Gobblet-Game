from time import sleep
import pygame
from src.GUI.ai_agent import AiAgent

from src.GUI.status_box import GameStatusBox
from src.backend.game import Game, GameModes, GameStatus
from src.GUI.human_agent import Human
from src.utils.move import MoveType

BOARD_SIZE = 4
CIRCLE_RADIUS_FACTOR = 8
COLOURS = {"B": (35, 31, 38), "R": (69, 0, 1), "W": (255, 255, 255)}


class GUI:
    def __init__(self):
        self._running = True
        self.win = None
        self.size = self.weight, self.height = 640, 480
        self.center = self.left, self.top = 161, 80
        self.selected = False
        self.Human = Human()
        self.game = None
        self.Ai = None
        self.myfont = pygame.font.SysFont("monospace", 28)
        self.turns = {
            "R": (
                self.myfont.size("Red's turn"),
                self.myfont.render("Red's turn", True, COLOURS["W"]),
            ),
            "B": (
                self.myfont.size("Black's turn"),
                self.myfont.render("Black's turn", True, COLOURS["W"]),
            ),
        }

    def on_init(self):
        pygame.init()
        self.win = pygame.display.set_mode(self.size)
        self._running = True
        return True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self.cleanup()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self._running = False

    def on_loop(self):
        self.Human.on_loop(self.game)

    def render(self):
        self.win.fill((0, 0, 0))
        for i in range(4):
            for j in range(4):
                pygame.draw.rect(
                    self.win,
                    (255, 255, 255),
                    (self.left + 80 * i, self.top + 80 * j, 80, 80),
                    2,
                    0,
                )
                if self.game.board.grid[i][j][-1] is not None:
                    pygame.draw.circle(
                        self.win,
                        COLOURS[self.game.board.grid[i][j][-1].color.value],
                        (self.left + 80 * i + 40, self.top + 80 * j + 40),
                        9 * self.game.board.grid[i][j][-1].size.value,
                    )

        for i in range(3):
            if len(self.game.player2.pieces[i]) > 0:
                pygame.draw.circle(
                    self.win,
                    COLOURS["B"],
                    (100, (280 + (80 * i))),
                    9 * self.game.player2.pieces[i][-1].size.value,
                )

        for i in range(3):
            if len(self.game.player1.pieces[i]) > 0:
                pygame.draw.circle(
                    self.win,
                    COLOURS["R"],
                    (540, (40 + 80 * (2 - i))),
                    9 * self.game.player1.pieces[i][-1].size.value,
                )

        if self.selected:
            pc, pr = pygame.mouse.get_pos()
            pw = 60
            ph = pw
            pr -= ph // 2
            pc -= pw // 2
            pygame.draw.circle(
                self.win,
                COLOURS[self.game.turn.value],
                (pc + pw // 2, pr + ph // 2),
                min(ph, pw) // 2,
            )
        size, text = self.turns[self.game.turn.value]
        tw, th = size
        offset = 50 - th
        self.win.blit(text, (offset + 10, offset))

        pygame.display.flip()

    def cleanup(self):
        sleep(5)
        pygame.quit()

    def __handle_game_status_check(self, game: Game):
        self.render()
        game.statusCheck()
        if game.game_status == GameStatus.Win:
            try:
                screen = pygame.display.get_surface()
                sleep(5)
                print(f"Winner is: {self.game.winner.color.value}")
                GameStatusBox(screen).draw_winner_box(
                    game.winner.color.value, game.winner.name
                )
            except Exception as e:
                print("Error in WinnerBox")
                print(e)
        elif game.game_status == GameStatus.Draw:
            sleep(5)
            print("Draw")
            try:
                screen = pygame.display.get_surface()
                GameStatusBox(screen).draw_draw_box()
            except Exception as e:
                print("Error in DrawBox")
                print(e)

            # Continue the game

    def on_execute(self, game: Game, mode: GameModes, TYPE):
        global event
        if self.on_init() == False:
            self._running = False
        self.game = game
        self.Ai = AiAgent(game)
        while self._running:
            self.render()
            for event in pygame.event.get():
                self.on_event(event)
            if mode == GameModes.HumanVsHuman:
                self.selected = self.Human.on_event(event, self.game)
                self.on_loop()
            elif mode == GameModes.HumanVsAi:
                if self.game.turn.value == "R":
                    self.selected = self.Human.on_event(event, self.game)
                    self.on_loop()
                elif self.game.turn.value == "B":
                    self.selected = False
                    self.Ai.on_turn(TYPE)

            elif mode == GameModes.AiVsAi:
                self.Ai.on_turn(TYPE)
                
            self.__handle_game_status_check(game)

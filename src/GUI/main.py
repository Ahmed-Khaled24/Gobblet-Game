import sys
import os
from pygame.locals import *

# sys.path.insert(0, os.path.abspath('../.'))
# TODO: remake this if it works for everybody but me
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
print(path)
sys.path.insert(0, path)

import pygame
import pygame_menu
from src.backend.player import Color
from typing import Tuple, Any
from gameGUI import GUI
from src.backend.game import Game, GameModes

pygame.init()
display_width = 680
display_height = 500
difficulty = 25
win = pygame.display.set_mode((display_width, display_height))
clock = pygame.time.Clock()
COLOURS = {'B': (35, 31, 38), 'R': (69, 0, 1), 'W': (255, 255, 255)}
turn = 'R'
center = left, top = 162, 80
_i, _j = -1, -1
running = True
selected = False
myfont = pygame.font.SysFont("monospace", 28)
turns = {'R': (myfont.size("Red's turn"),
               myfont.render("Red's turn", True, COLOURS['W'])),
         'B': (myfont.size("Black's turn"),
               myfont.render("Black's turn", True, COLOURS['W'])),
         'WB': (myfont.size("BLACK WON"),
                myfont.render("BLACK WON!!", True, COLOURS['W'])),
         'WR': (myfont.size("RED WON"),
                myfont.render("RED WON!!", True, COLOURS['W']))}


def aivai_menu():
    start_menu._open(aivai)


def aivh_menu():
    start_menu._open(aivh)


def show_start_screen():
    global start_menu, aivai, aivh
    start_menu = pygame_menu.Menu(width=display_width, height=display_height, title='Welcome to Gobblet Game!',
                                  theme=pygame_menu.themes.THEME_DARK)
    start_menu.add.button("AI Vs AI", aivai_menu)
    start_menu.add.button("AI Vs Human", aivh_menu)
    start_menu.add.button("Human Vs Human", lambda: game_loop(GameModes.HumanVsHuman))

    start_menu.add.button("Quit", pygame_menu.events.EXIT)
    aivai = pygame_menu.Menu(width=display_width, height=display_height, title='AI vs AI',
                             theme=pygame_menu.themes.THEME_DARK)
    aivai.add.selector('Difficulty AI 1:', [('Hard', 1), ('Easy', 2)], onchange=set_game_difficulty)
    aivai.add.selector('Difficulty AI 2:', [('Hard', 1), ('Easy', 2)], onchange=set_game_difficulty)
    aivai.add.button('Play', lambda: game_loop(GameModes.AiVsAi))

    aivh = pygame_menu.Menu(width=display_width, height=display_height, title='AI vs Human',
                            theme=pygame_menu.themes.THEME_DARK)
    aivh.add.selector('Difficulty:', [('Hard', 1), ('Easy', 2)], onchange=set_game_difficulty)
    aivh.add.button('Play', lambda: game_loop(GameModes.HumanVsAi))
    start_menu.mainloop(win)


def set_game_difficulty(selected: Tuple, value: Any):
    if (value == 1):
        difficulty = 25
    elif (value == 2):
        difficulty = 50
    elif (value == 3):
        difficulty = 100
    else:
        difficulty = 25


def game_loop(mode: GameModes):
    game = Game(mode, "Player1", "Player2", Color.WHITE, Color.BLACK)
    gui = GUI()
    gui.on_execute(game, mode)


show_start_screen()

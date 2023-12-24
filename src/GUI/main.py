import sys
import os
sys.path.insert(0, os.path.abspath('../.'))

import pygame
import pygame_menu

from typing import Tuple, Any
from game import game
from src.utils.gameModesEnum import GameModes 

pygame.init()
display_width = 680
display_height = 500
difficulty = 25
win = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()

def aivai_menu():
    start_menu._open(aivai)
    
def aivh_menu():
    start_menu._open(aivh)
    
def show_start_screen():
    global start_menu,aivai,aivh
    start_menu = pygame_menu.Menu(width=display_width, height=display_height, title='Welcome to Gobblet Game!',theme=pygame_menu.themes.THEME_DARK)
    start_menu.add.button("AI Vs AI",aivai_menu)
    start_menu.add.button("AI Vs Human", aivh_menu)
    start_menu.add.button("Human Vs Human", lambda: game_loop(GameModes.HumanVsHuman))
    
    start_menu.add.button("Quit", pygame_menu.events.EXIT)
    aivai = pygame_menu.Menu(width=display_width, height=display_height, title='AI vs AI',theme=pygame_menu.themes.THEME_DARK)
    aivai.add.selector('Difficulty AI 1:', [('Hard', 1), ('Easy', 2)], onchange=set_game_difficulty)
    aivai.add.selector('Difficulty AI 2:', [('Hard', 1), ('Easy', 2)], onchange=set_game_difficulty)
    aivai.add.button('Play', lambda: game_loop(GameModes.AiVsAi))
    
    aivh = pygame_menu.Menu(width=display_width, height=display_height, title='AI vs Human',theme=pygame_menu.themes.THEME_DARK)
    aivh.add.selector('Difficulty:', [('Hard', 1), ('Easy', 2)], onchange=set_game_difficulty)
    aivh.add.button('Play', lambda: game_loop(GameModes.AiVsHuman))
    start_menu.mainloop(win)


def set_game_difficulty(selected: Tuple, value: Any):
    if(value == 1):
        difficulty = 25
    elif(value == 2):
        difficulty = 50
    elif(value == 3):
        difficulty = 100
    else:
        difficulty = 25

def game_loop(mode: GameModes):
    Game = game()
    print(mode)
    Game.on_execute()

show_start_screen()

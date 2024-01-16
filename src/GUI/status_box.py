import pygame
from pygame.locals import *

PLAY_AGAIN_EVENT = USEREVENT + 1


class GameStatusBox:
    ## This class is the box that appears when the game is over and it shows the winner or if it is a draw
    ## It is a modal box that appears on top of the game screen
    ## You first instantiate a new GameStatusBox and then call the draw_winner_box or draw_draw_box methods depending on game State
    def __init__(self, screen):
        ## screen is the pygame screen object that is passed from the main game loop
        self.screen = screen

        self.WIDTH, self.HEIGHT = 300, 200
        self.font = pygame.font.Font(None, 32)

        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)

        self.button_rect = None

        self.running = False

    def display_box(self, color, message):
        button_color = None
        if color == "B":
            color = self.BLACK
            button_color = self.BLACK
        elif color == "R":
            color = self.RED
            button_color = self.RED

        box_width, box_height = self.WIDTH, self.HEIGHT
        screen_width, screen_height = self.screen.get_size()

        box_x = (screen_width - box_width) // 2
        box_y = (screen_height - box_height) // 2

        modal_surface = pygame.Surface((box_width, box_height))
        modal_surface.fill(self.WHITE)

        pygame.draw.rect(
            modal_surface, color, (10, 10, box_width - 20, box_height - 20)
        )

        text_render = self.font.render(message, True, self.WHITE)
        text_rect = text_render.get_rect(center=(box_width // 2, box_height // 2))
        modal_surface.blit(text_render, text_rect.topleft)
        # Create "Play again" button
        self.button_rect = pygame.Rect(100, 150, 100, 50)
        pygame.draw.rect(modal_surface, button_color, self.button_rect)

        # Add text to the button
        button_text = self.font.render("Play again", True, self.WHITE)
        button_text_rect = button_text.get_rect(center=self.button_rect.center)
        modal_surface.blit(button_text, button_text_rect.topleft)

        self.screen.blit(modal_surface, (box_x, box_y))
        pygame.display.flip()

    def _draw_box(self, color, message):
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                    pygame.quit()

                ## Here i check for every mouse click
                elif event.type == pygame.MOUSEBUTTONUP:
                    # if the mouse click is on the close button of the box then i fire the close event

                    # TODO: adjust button rect from modal to screen coordinates dynamically
                    # adjust button rect from modal to screen coordinates
                    adjusted_rect = pygame.Rect(280, 300, 100, 50)

                    if adjusted_rect.collidepoint(event.pos):
                        pygame.event.post(pygame.event.Event(PLAY_AGAIN_EVENT))

                if event.type == PLAY_AGAIN_EVENT:
                    # Start a new game loop and close the current one
                    self.running = False

                    # This is necessary to avoid circular imports
                    from src.GUI.main import show_start_screen

                    # Reset the screen
                    pygame.display.set_mode((680, 500))

                    # Show the start menu again
                    show_start_screen()

            self.display_box(color, message)

    def draw_winner_box(self, color, player_name):
        self._draw_box(color, f"{player_name} wins!")

    def draw_draw_box(self):
        self._draw_box(self.GRAY, "Draw")

    def stop(self):
        self.running = False

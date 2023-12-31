import pygame

class WinnerBox:
    def __init__(self, screen):
        self.screen = screen
        self.WIDTH, self.HEIGHT = 300, 200
        self.font = pygame.font.Font(None, 32)
        self.WHITE = (255, 255, 255)
        self.RED = (255, 0, 0)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.running = False

    def display_box(self, color, message):

        if color == 'B':
            color = self.BLACK
        elif color == 'R':
            color = self.RED


        box_width, box_height = self.WIDTH, self.HEIGHT
        screen_width, screen_height = self.screen.get_size()

        box_x = (screen_width - box_width) // 2
        box_y = (screen_height - box_height) // 2

        modal_surface = pygame.Surface((box_width, box_height))
        modal_surface.fill(self.WHITE)

        pygame.draw.rect(modal_surface, color, (10, 10, box_width - 20, box_height - 20))

        text_render = self.font.render(message, True, self.WHITE)
        text_rect = text_render.get_rect(center=(box_width // 2, box_height // 2))
        modal_surface.blit(text_render, text_rect.topleft)

        self.screen.blit(modal_surface, (box_x, box_y))
        pygame.display.flip()



    def _draw_box(self, color, message):
        box_closed = False
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    box_closed = True
                    from src.GUI.main import show_start_screen
                    show_start_screen()

            self.display_box(color, message)


                

    def draw_winner_box(self, color, player_name):
        self._draw_box(color,  f'{player_name} wins!')
    
    def draw_draw_box(self):
        self._draw_box(self.GRAY, "Draw")

    def stop(self):
        self.running = False


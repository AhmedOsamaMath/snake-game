import pygame
import sys
from game_states import GameState
from settings import Settings
from game_manager import GameManager

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Snake Game")
        
        self.clock = pygame.time.Clock()
        self.game_state = GameState.MAIN_MENU
        self.game_manager = GameManager(self.screen, self.settings)
        
        # Difficulty selection
        self.selected_difficulty = None
        self.difficulty_options = ['easy', 'medium', 'hard']
        self.current_difficulty_index = 1  # Default to medium

    def run(self):
        while True:
            self._handle_events()
            self._update()
            self._render()
            self.clock.tick(self.settings.fps)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._quit_game()
            
            if self.game_state == GameState.MAIN_MENU:
                self._handle_menu_events(event)
            elif self.game_state == GameState.DIFFICULTY_SELECT:
                self._handle_difficulty_select_events(event)
            elif self.game_state == GameState.PLAYING:
                self._handle_game_events(event)
            elif self.game_state == GameState.GAME_OVER:
                self._handle_game_over_events(event)

    def _handle_menu_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                # Move to difficulty selection
                self.game_state = GameState.DIFFICULTY_SELECT
                self.current_difficulty_index = 1  # Reset to medium

    def _handle_difficulty_select_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                # Cycle difficulty up
                self.current_difficulty_index = (self.current_difficulty_index - 1) % len(self.difficulty_options)
            elif event.key == pygame.K_DOWN:
                # Cycle difficulty down
                self.current_difficulty_index = (self.current_difficulty_index + 1) % len(self.difficulty_options)
            elif event.key == pygame.K_RETURN:
                # Select difficulty and start game
                self.selected_difficulty = self.difficulty_options[self.current_difficulty_index]
                self.settings.set_difficulty(self.selected_difficulty)
                self.game_state = GameState.PLAYING
                self.game_manager.start_game()
            elif event.key == pygame.K_ESCAPE:
                # Return to main menu
                self.game_state = GameState.MAIN_MENU

    def _handle_game_events(self, event):
        self.game_manager.handle_events(event)

    def _handle_game_over_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.game_state = GameState.DIFFICULTY_SELECT
            elif event.key == pygame.K_ESCAPE:
                self.game_state = GameState.MAIN_MENU

    def _update(self):
        if self.game_state == GameState.PLAYING:
            game_result = self.game_manager.update()
            if game_result == "game_over":
                self.game_state = GameState.GAME_OVER

    def _render(self):
        self.screen.fill(self.settings.background_color)

        if self.game_state == GameState.MAIN_MENU:
            self._render_main_menu()
        elif self.game_state == GameState.DIFFICULTY_SELECT:
            self._render_difficulty_select()
        elif self.game_state == GameState.PLAYING:
            self.game_manager.render()
        elif self.game_state == GameState.GAME_OVER:
            self._render_game_over()

        pygame.display.flip()

    def _render_main_menu(self):
        font = pygame.font.Font(None, 74)
        title = font.render("SNAKE GAME", True, (255, 255, 255))
        start_text = pygame.font.Font(None, 36).render("Press ENTER to Start", True, (200, 200, 200))
        
        self.screen.blit(title, (self.settings.screen_width//2 - title.get_width()//2, 200))
        self.screen.blit(start_text, (self.settings.screen_width//2 - start_text.get_width()//2, 300))

    def _render_difficulty_select(self):
        font_title = pygame.font.Font(None, 64)
        font_options = pygame.font.Font(None, 48)
        
        # Title
        title = font_title.render("SELECT DIFFICULTY", True, (255, 255, 255))
        self.screen.blit(title, (self.settings.screen_width//2 - title.get_width()//2, 100))

        # Difficulty options
        for i, difficulty in enumerate(self.difficulty_options):
            color = (255, 255, 255) if i == self.current_difficulty_index else (100, 100, 100)
            difficulty_text = font_options.render(difficulty.upper(), True, color)
            
            # Center the text
            text_x = self.settings.screen_width//2 - difficulty_text.get_width()//2
            text_y = 250 + (i * 80)
            
            self.screen.blit(difficulty_text, (text_x, text_y))

        # Instructions
        font_instructions = pygame.font.Font(None, 30)
        up_down = font_instructions.render("Use UP/DOWN to select", True, (200, 200, 200))
        select = font_instructions.render("Press ENTER to start", True, (200, 200, 200))
        back = font_instructions.render("Press ESC to go back", True, (200, 200, 200))
        
        self.screen.blit(up_down, (self.settings.screen_width//2 - up_down.get_width()//2, 500))
        self.screen.blit(select, (self.settings.screen_width//2 - select.get_width()//2, 530))
        self.screen.blit(back, (self.settings.screen_width//2 - back.get_width()//2, 560))

    def _render_game_over(self):
        font = pygame.font.Font(None, 74)
        game_over = font.render("GAME OVER", True, (255, 0, 0))
        restart_text = pygame.font.Font(None, 36).render("Press R to Select Difficulty", True, (200, 200, 200))
        menu_text = pygame.font.Font(None, 36).render("Press ESC for Menu", True, (200, 200, 200))
        
        self.screen.blit(game_over, (self.settings.screen_width//2 - game_over.get_width()//2, 200))
        self.screen.blit(restart_text, (self.settings.screen_width//2 - restart_text.get_width()//2, 300))
        self.screen.blit(menu_text, (self.settings.screen_width//2 - menu_text.get_width()//2, 350))

    def _quit_game(self):
        pygame.quit()
        sys.exit()

def main():
    game = SnakeGame()
    game.run()

if __name__ == "__main__":
    main()
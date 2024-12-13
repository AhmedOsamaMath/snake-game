import pygame
import random
import math

class Snake:
    def __init__(self, settings):
        self.settings = settings
        self.cell_size = settings.get_grid_cell_size()
        self.movement_delay = self._calculate_movement_delay()
        self.last_move_time = 0
        self.reset()

    def _calculate_movement_delay(self):
        # Implement movement delays based on difficulty
        difficulty_delays = {
            'easy': 250,  # 250 milliseconds between moves (slowest)
            'medium': 150,  # 150 milliseconds between moves
            'hard': 100  # 100 milliseconds between moves (fastest)
        }
        return difficulty_delays.get(self.settings.current_difficulty, 150)

    def reset(self):
        grid_center_x = self.settings.screen_width // (2 * self.cell_size)
        grid_center_y = self.settings.screen_height // (2 * self.cell_size)
        
        self.body = [(grid_center_x, grid_center_y)]
        self.direction = (1, 0)  # Start moving right
        self.length = self.settings.current_settings['initial_length']
        self.grow_to = self.length
        
        # Recalculate movement delay in case difficulty changed
        self.movement_delay = self._calculate_movement_delay()
        self.last_move_time = pygame.time.get_ticks()

    def should_move(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time > self.movement_delay:
            self.last_move_time = current_time
            return True
        return False
    
    def move(self):
        if not self.should_move():
            return

        head = self.body[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        
        # Wrap-around or stop based on difficulty setting
        if self.settings.current_settings['wall_collision'] == 'wrap':
            new_head = (
                new_head[0] % (self.settings.screen_width // self.cell_size),
                new_head[1] % (self.settings.screen_height // self.cell_size)
            )
        
        self.body.insert(0, new_head)
        
        # Grow snake if needed
        if len(self.body) > self.grow_to:
            self.body.pop()

    def change_direction(self, new_direction):
        # Prevent 180-degree turns
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

class Food:
    def __init__(self, settings, snake):
        self.settings = settings
        self.snake = snake
        self.cell_size = settings.get_grid_cell_size()
        self.respawn()

    def respawn(self):
        grid_width = self.settings.screen_width // self.cell_size
        grid_height = self.settings.screen_height // self.cell_size
        
        while True:
            x = random.randint(0, grid_width - 1)
            y = random.randint(0, grid_height - 1)
            
            # Ensure food doesn't spawn on snake
            if (x, y) not in self.snake.body:
                self.position = (x, y)
                break

class GameManager:
    def __init__(self, screen, settings):
        self.screen = screen
        self.settings = settings
        self.snake = Snake(settings)
        self.food = Food(settings, self.snake)
        self.score = 0
        self.cell_size = settings.get_grid_cell_size()

    def start_game(self):
        self.snake.reset()
        self.food.respawn()
        self.score = 0

    def restart_game(self):
        self.start_game()

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.snake.change_direction((-1, 0))
            elif event.key == pygame.K_RIGHT:
                self.snake.change_direction((1, 0))
            elif event.key == pygame.K_UP:
                self.snake.change_direction((0, -1))
            elif event.key == pygame.K_DOWN:
                self.snake.change_direction((0, 1))

    def update(self):
        self.snake.move()
        
        # Check food collision
        if self.snake.body[0] == self.food.position:
            self.snake.grow_to += 1
            self.score += 10
            self.food.respawn()
        
        # Check self collision
        if len(set(self.snake.body)) < len(self.snake.body):
            return "game_over"
        
        # Check wall collision for non-wrap modes
        if self.settings.current_settings['wall_collision'] == 'stop':
            grid_width = self.settings.screen_width // self.cell_size
            grid_height = self.settings.screen_height // self.cell_size
            
            head = self.snake.body[0]
            if (head[0] < 0 or head[0] >= grid_width or 
                head[1] < 0 or head[1] >= grid_height):
                return "game_over"
        
        return "continue"

    def render(self):
        # Render Snake
        for segment in self.snake.body:
            pygame.draw.rect(self.screen, 
                             self.settings.snake_color, 
                             (segment[0] * self.cell_size, 
                              segment[1] * self.cell_size, 
                              self.cell_size, 
                              self.cell_size))
        
        # Render Food
        pygame.draw.rect(self.screen, 
                         self.settings.food_color, 
                         (self.food.position[0] * self.cell_size, 
                          self.food.position[1] * self.cell_size, 
                          self.cell_size, 
                          self.cell_size))
        
        # Render Score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
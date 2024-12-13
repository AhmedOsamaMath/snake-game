import pygame

class Settings:
    def __init__(self):
        # Screen Settings
        self.screen_width = 800
        self.screen_height = 600
        self.fps = 60

        # Color Palette
        self.background_color = (20, 20, 40)  # Dark blue-black
        self.snake_color = (0, 255, 0)  # Bright green
        self.food_color = (255, 0, 0)  # Bright red
        self.obstacle_color = (100, 100, 100)  # Gray

        # Difficulty Levels
        self.difficulties = {
            'easy': {
                'speed': 5,
                'grid_size': 40,
                'food_spawn_rate': 0.02,
                'initial_length': 4,
                'wall_collision': 'wrap',
                'obstacles': 0
            },
            'medium': {
                'speed': 10,
                'grid_size': 30,
                'food_spawn_rate': 0.015,
                'initial_length': 3,
                'wall_collision': 'stop',
                'obstacles': 3
            },
            'hard': {
                'speed': 15,
                'grid_size': 20,
                'food_spawn_rate': 0.01,
                'initial_length': 2,
                'wall_collision': 'stop',
                'obstacles': 5
            }
        }

        # Current Game Settings (default to medium)
        self.current_difficulty = 'hard'
        self.current_settings = self.difficulties[self.current_difficulty]

    def set_difficulty(self, difficulty):
        if difficulty in self.difficulties:
            self.current_difficulty = difficulty
            self.current_settings = self.difficulties[difficulty]

    def get_grid_cell_size(self):
        return min(self.screen_width, self.screen_height) // self.current_settings['grid_size']
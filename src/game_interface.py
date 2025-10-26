import pygame
import sys
import time

class RushHourGame:
    """
    Pygame interface to visualize the Rush Hour puzzle solution.
    """
    
    def __init__(self, initial_state, solution_node=None, algorithm_name="", steps=0):
        """
        Initialize the game interface.
        
        Parameters:
        - initial_state: Initial RushHourPuzzle state
        - solution_node: Node containing the solution
        - algorithm_name: Name of algorithm used
        - steps: Number of steps taken by algorithm
        """
        pygame.init()
        
        # Game settings
        self.CELL_SIZE = 80
        self.MARGIN = 10
        self.INFO_HEIGHT = 150
        
        # Calculate window size based on board size
        self.board_width = initial_state.board_width
        self.board_height = initial_state.board_height
        
        self.WINDOW_WIDTH = self.board_width * self.CELL_SIZE + 2 * self.MARGIN
        self.WINDOW_HEIGHT = self.board_height * self.CELL_SIZE + 2 * self.MARGIN + self.INFO_HEIGHT
        
        # Create window
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Rush Hour Puzzle Solution")
        
        # Colors
        self.BACKGROUND = (245, 245, 245)
        self.GRID_COLOR = (200, 200, 200)
        self.RED_CAR = (231, 76, 60)
        self.CAR_COLORS = {
            'X': (231, 76, 60),  # Red
        }
        self.DEFAULT_CAR_COLOR = (52, 152, 219)  # Blue
        self.TRUCK_COLOR = (52, 152, 219)  # BLUE
        self.WALL_COLOR = (50, 50, 50)
        self.TEXT_COLOR = (50, 50, 50)
        self.EXIT_COLOR = (255, 215, 0)  # Gold
        
        # Fonts
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 24)
        
        # Solution data
        self.solution_node = solution_node
        self.algorithm_name = algorithm_name
        self.steps = steps
        
        # Animation
        self.current_state_index = 0
        self.path = []
        self.actions = []
        
        if solution_node:
            self.path = solution_node.getPath()
            self.actions = solution_node.getSolution()
        else:
            self.path = [initial_state]
            self.actions = []
        
        self.animating = False
        self.animation_speed = 1.0  # seconds per move
        self.last_update = time.time()
    
    def draw_board(self, state):
        """Draw the game board with vehicles."""
        # Draw background
        self.screen.fill(self.BACKGROUND)
        
        # Draw exit indicator
        exit_y = self.board_height // 2 - 1
        exit_rect = pygame.Rect(
            self.MARGIN + self.board_width * self.CELL_SIZE - 5,
            self.MARGIN + exit_y * self.CELL_SIZE + self.CELL_SIZE // 4,
            10,
            self.CELL_SIZE // 2
        )
        pygame.draw.rect(self.screen, self.EXIT_COLOR, exit_rect)
        
        # Draw grid
        for row in range(self.board_height + 1):
            y = self.MARGIN + row * self.CELL_SIZE
            pygame.draw.line(self.screen, self.GRID_COLOR, 
                           (self.MARGIN, y), 
                           (self.MARGIN + self.board_width * self.CELL_SIZE, y), 2)
        
        for col in range(self.board_width + 1):
            x = self.MARGIN + col * self.CELL_SIZE
            pygame.draw.line(self.screen, self.GRID_COLOR, 
                           (x, self.MARGIN), 
                           (x, self.MARGIN + self.board_height * self.CELL_SIZE), 2)
        
        # Draw walls
        for wall_x, wall_y in state.walls:
            rect = pygame.Rect(
                self.MARGIN + wall_x * self.CELL_SIZE + 2,
                self.MARGIN + wall_y * self.CELL_SIZE + 2,
                self.CELL_SIZE - 4,
                self.CELL_SIZE - 4
            )
            pygame.draw.rect(self.screen, self.WALL_COLOR, rect)
        
        # Draw vehicles
        for vehicle in state.vehicles:
            vid = vehicle['id']
            x = vehicle['x']
            y = vehicle['y']
            orientation = vehicle['orientation']
            length = vehicle['length']
            
            # Choose color
            if vid == 'X':
                color = self.RED_CAR
            elif length == 3:
                color = self.TRUCK_COLOR
            else:
                color = self.DEFAULT_CAR_COLOR
            
            # Calculate rectangle
            if orientation == 'H':
                rect = pygame.Rect(
                    self.MARGIN + x * self.CELL_SIZE + 4,
                    self.MARGIN + y * self.CELL_SIZE + 4,
                    length * self.CELL_SIZE - 8,
                    self.CELL_SIZE - 8
                )
            else:
                rect = pygame.Rect(
                    self.MARGIN + x * self.CELL_SIZE + 4,
                    self.MARGIN + y * self.CELL_SIZE + 4,
                    self.CELL_SIZE - 8,
                    length * self.CELL_SIZE - 8
                )
            
            # Draw vehicle
            pygame.draw.rect(self.screen, color, rect, border_radius=8)
            
            # Draw vehicle ID
            text = self.font_medium.render(vid, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_info(self):
        """Draw information panel."""
        info_y = self.MARGIN + self.board_height * self.CELL_SIZE + 20
        
        # Algorithm name
        if self.algorithm_name:
            text = self.font_large.render(f"Algorithm: {self.algorithm_name}", True, self.TEXT_COLOR)
            self.screen.blit(text, (self.MARGIN, info_y))
        
        # Steps taken
        text = self.font_medium.render(f"Search Steps: {self.steps}", True, self.TEXT_COLOR)
        self.screen.blit(text, (self.MARGIN, info_y + 40))
        
        # Solution cost
        if self.solution_node:
            cost = self.solution_node.g
            text = self.font_medium.render(f"Solution Cost: {cost} moves", True, self.TEXT_COLOR)
            self.screen.blit(text, (self.MARGIN, info_y + 70))
        
        # Current move
        text = self.font_medium.render(
            f"Move: {self.current_state_index}/{len(self.path)-1}", 
            True, self.TEXT_COLOR
        )
        self.screen.blit(text, (self.MARGIN, info_y + 100))
        
        # Instructions
        if not self.animating:
            text = self.font_small.render("Press SPACE to animate | ARROW keys to step", True, self.TEXT_COLOR)
            self.screen.blit(text, (self.MARGIN + 300, info_y + 40))
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        # Toggle animation
                        self.animating = not self.animating
                        self.last_update = time.time()
                    
                    elif event.key == pygame.K_RIGHT and not self.animating:
                        # Next state
                        if self.current_state_index < len(self.path) - 1:
                            self.current_state_index += 1
                    
                    elif event.key == pygame.K_LEFT and not self.animating:
                        # Previous state
                        if self.current_state_index > 0:
                            self.current_state_index -= 1
                    
                    elif event.key == pygame.K_r:
                        # Reset to start
                        self.current_state_index = 0
                        self.animating = False
                    
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Animation update
            if self.animating:
                current_time = time.time()
                if current_time - self.last_update >= self.animation_speed:
                    if self.current_state_index < len(self.path) - 1:
                        self.current_state_index += 1
                        self.last_update = current_time
                    else:
                        self.animating = False
            
            # Draw everything
            current_state = self.path[self.current_state_index]
            self.draw_board(current_state)
            self.draw_info()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()


def visualize_solution(initial_state, solution_node, algorithm_name, steps):
    """
    Helper function to create and run the visualization.
    
    Parameters:
    - initial_state: Initial puzzle state
    - solution_node: Node containing the solution
    - algorithm_name: Name of the algorithm used
    - steps: Number of steps taken
    """
    game = RushHourGame(initial_state, solution_node, algorithm_name, steps)
    game.run()
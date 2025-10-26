import pygame
import sys
import time
import math

class RushHourGame:
    
    def __init__(self, initial_state, solution_node=None, algorithm_name="", steps=0):
        pygame.init()
        
        # Game settings 
        self.CELL_SIZE = 70
        self.MARGIN = 20
        self.INFO_HEIGHT = 130
        self.TITLE_HEIGHT = 45
        # spacing used above and below the board so they match
        self.BOARD_SPACING = 14
        # inset for grid lines so they don't reach the rounded corners
        self.FRAME_INSET = 8
        
        # Calculate window size
        self.board_width = initial_state.board_width
        self.board_height = initial_state.board_height
        
        self.WINDOW_WIDTH = self.board_width * self.CELL_SIZE + 2 * self.MARGIN
        # add +40 to make the window taller (adjust as needed)
        self.WINDOW_HEIGHT = self.board_height * self.CELL_SIZE + 2 * self.MARGIN + self.INFO_HEIGHT + self.TITLE_HEIGHT + 40
        
        # Create window
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Rush Hour Puzzle")
        
        # Enhanced color palette 
        self.BACKGROUND = (30, 30, 40)  # Dark blue-gray
        self.BOARD_BG = (245, 245, 250)  # Light gray
        self.GRID_COLOR = (200, 200, 210)
        self.RED_CAR = (220, 53, 69)  # Vibrant red
        self.BLUE_CAR = (52, 152, 219)  # Blue
        self.WALL_COLOR = (60, 60, 70)
        self.WALL_HIGHLIGHT = (80, 80, 90)
        self.TEXT_COLOR = (240, 240, 245)
        self.TEXT_SHADOW = (20, 20, 30)
        self.EXIT_COLOR = (255, 193, 7)  # Amber/Gold
        self.EXIT_GLOW = (255, 235, 59)
        self.ACCENT_COLOR = (139, 69, 255)  # Purple accent
        
        # Fonts - consistent everywhere
        self.font_title = pygame.font.Font(None, 38)
        self.font_info = pygame.font.Font(None, 20)  
        self.font_vehicle = pygame.font.Font(None, 24) 
        
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
        self.animation_speed = 0.5
        self.last_update = time.time()
        
        self.exit_pulse = 0
    
    def get_vehicle_color(self, vid, length):
        """Get color for vehicle."""
        if vid == 'X':
            return self.RED_CAR
        else:
            return self.BLUE_CAR
    
    def draw_gradient_rect(self, surface, color1, color2, rect):
        """Draw a vertical gradient."""
        for i in range(rect.height):
            ratio = i / rect.height
            r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
            g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
            b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
            pygame.draw.line(surface, (r, g, b), 
                           (rect.x, rect.y + i), 
                           (rect.x + rect.width, rect.y + i))
    
    def draw_text_with_shadow(self, text, font, color, x, y, shadow=True):
        """Draw text with shadow."""
        if shadow:
            shadow_surf = font.render(text, True, self.TEXT_SHADOW)
            self.screen.blit(shadow_surf, (x + 2, y + 2))
        text_surf = font.render(text, True, color)
        self.screen.blit(text_surf, (x, y))
    
    def draw_board(self, state):
        """Draw the game board - original style with new cars."""
        # Background
        self.screen.fill(self.BACKGROUND)
        
        # Title bar with gradient
        title_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, self.TITLE_HEIGHT)
        self.draw_gradient_rect(self.screen, self.ACCENT_COLOR, (100, 50, 200), title_rect)
        
        # Center the title properly
        title_text = "RUSH HOUR PUZZLE"
        title_surface = self.font_title.render(title_text, True, self.TEXT_COLOR)
        title_x = (self.WINDOW_WIDTH - title_surface.get_width()) // 2
        self.draw_text_with_shadow(title_text, self.font_title, self.TEXT_COLOR, title_x, 8)
        
        # Board with NO border frame - just the board itself with more space from title
        board_x = self.MARGIN
        board_y = self.MARGIN + self.TITLE_HEIGHT + self.BOARD_SPACING  # use unified spacing
        
        # Only draw the board background - NO FRAME
        board_rect = pygame.Rect(
            board_x,
            board_y,
            self.board_width * self.CELL_SIZE,
            self.board_height * self.CELL_SIZE
        )
        pygame.draw.rect(self.screen, self.BOARD_BG, board_rect, border_radius=10)
        
        # Rounded border matching board
        # Slightly thicker outer frame
        pygame.draw.rect(self.screen, self.GRID_COLOR, board_rect, 4, border_radius=10)

        # Internal grid lines only, inset so they don't show at rounded corners
        inset = self.FRAME_INSET
        inner_left = board_x + inset
        inner_right = board_x + self.board_width * self.CELL_SIZE - inset
        inner_top = board_y + inset
        inner_bottom = board_y + self.board_height * self.CELL_SIZE - inset

        for row in range(1, self.board_height):
            y = board_y + row * self.CELL_SIZE
            pygame.draw.line(self.screen, self.GRID_COLOR,
                             (inner_left, y),
                             (inner_right, y), 2)

        for col in range(1, self.board_width):
            x = board_x + col * self.CELL_SIZE
            pygame.draw.line(self.screen, self.GRID_COLOR,
                             (x, inner_top),
                             (x, inner_bottom), 2)
        
        # Exit indicator 
        exit_y = self.board_height // 2 - 1
        self.exit_pulse += 0.05
        
        # Glow effect
        for i in range(3):
            alpha_surface = pygame.Surface((15 + i * 5, self.CELL_SIZE // 2 + i * 10), pygame.SRCALPHA)
            alpha_color = (*self.EXIT_GLOW, 80 - i * 20)
            pygame.draw.rect(alpha_surface, alpha_color, alpha_surface.get_rect(), border_radius=5)
            self.screen.blit(alpha_surface, (
                board_x + self.board_width * self.CELL_SIZE - 8 - i * 2,
                board_y + exit_y * self.CELL_SIZE + self.CELL_SIZE // 4 - i * 5
            ))
        
        # Exit arrow
        exit_rect = pygame.Rect(
            board_x + self.board_width * self.CELL_SIZE - 5,
            board_y + exit_y * self.CELL_SIZE + self.CELL_SIZE // 4,
            12,
            self.CELL_SIZE // 2
        )
        pygame.draw.rect(self.screen, self.EXIT_COLOR, exit_rect, border_radius=3)
        
        # Walls 
        for wall_x, wall_y in state.walls:
            wall_rect = pygame.Rect(
                board_x + wall_x * self.CELL_SIZE + 3,
                board_y + wall_y * self.CELL_SIZE + 3,
                self.CELL_SIZE - 6,
                self.CELL_SIZE - 6
            )
            # Shadow
            shadow_rect = wall_rect.copy()
            shadow_rect.x += 2
            shadow_rect.y += 2
            pygame.draw.rect(self.screen, (30, 30, 35), shadow_rect, border_radius=8)
            
            # Main wall
            pygame.draw.rect(self.screen, self.WALL_COLOR, wall_rect, border_radius=8)
            
            # Highlight
            highlight_rect = pygame.Rect(wall_rect.x + 5, wall_rect.y + 5, 
                                        wall_rect.width - 10, wall_rect.height // 2 - 5)
            pygame.draw.rect(self.screen, self.WALL_HIGHLIGHT, highlight_rect, border_radius=5)
        
        # Vehicles 
        for vehicle in state.vehicles:
            vid = vehicle['id']
            x = vehicle['x']
            y = vehicle['y']
            orientation = vehicle['orientation']
            length = vehicle['length']
            
            color = self.get_vehicle_color(vid, length)
            
            # Calculate rectangle
            if orientation == 'H':
                rect = pygame.Rect(
                    board_x + x * self.CELL_SIZE + 6,
                    board_y + y * self.CELL_SIZE + 6,
                    length * self.CELL_SIZE - 12,
                    self.CELL_SIZE - 12
                )
            else:
                rect = pygame.Rect(
                    board_x + x * self.CELL_SIZE + 6,
                    board_y + y * self.CELL_SIZE + 6,
                    self.CELL_SIZE - 12,
                    length * self.CELL_SIZE - 12
                )
            
            # Draw vehicle - solid color with border
            pygame.draw.rect(self.screen, color, rect, border_radius=14)
            
            # Subtle inner border for depth
            inner_rect = rect.inflate(-4, -4)
            lighter = (min(255, color[0] + 40), min(255, color[1] + 40), min(255, color[2] + 40))
            pygame.draw.rect(self.screen, lighter, inner_rect, 2, border_radius=12)
            
            # Vehicle ID
            text = self.font_vehicle.render(vid, True, (255, 255, 255))
            text_rect = text.get_rect(center=rect.center)
            self.screen.blit(text, text_rect)
    
    def draw_info(self):
        """Draw information panel - original style."""
        # use the same board spacing above and below the board
        board_y = self.MARGIN + self.TITLE_HEIGHT + self.BOARD_SPACING
        info_y = board_y + self.board_height * self.CELL_SIZE + self.BOARD_SPACING
         
         # Info background
         # add a few pixels to the info height for extra inner padding
        info_bg = pygame.Rect(self.MARGIN, info_y - 5, 
                              self.WINDOW_WIDTH - 2 * self.MARGIN, self.INFO_HEIGHT - 8)
        pygame.draw.rect(self.screen, (50, 50, 65), info_bg, border_radius=10)
        pygame.draw.rect(self.screen, self.ACCENT_COLOR, info_bg, 2, border_radius=10)
        
        # Algorithm name - NO RECTANGLE, just text
        algo_y = info_y + 5
        if self.algorithm_name:
            self.draw_text_with_shadow(f"Algorithm: {self.algorithm_name}", 
                                     self.font_info, self.EXIT_COLOR, 
                                     self.MARGIN + 12, algo_y)
        
        # Stats in two columns
        stats_y = algo_y + 26
        
        # Left column
        self.draw_text_with_shadow(f"Steps: {self.steps}", 
                                  self.font_info, self.TEXT_COLOR, 
                                  self.MARGIN + 12, stats_y)
        
        # Right column
        if self.solution_node:
            cost = self.solution_node.g
            cost_x = self.WINDOW_WIDTH // 2 + 10
            self.draw_text_with_shadow(f"Cost: {cost} moves", 
                                      self.font_info, self.TEXT_COLOR, 
                                      cost_x, stats_y)
        
        # Progress
        progress_y = stats_y + 26
        if len(self.path) > 1:
            progress_text = f"Move: {self.current_state_index} / {len(self.path) - 1}"
            self.draw_text_with_shadow(progress_text, self.font_info, self.TEXT_COLOR,
                                      self.MARGIN + 12, progress_y)
            
            # Progress bar
            bar_width = self.WINDOW_WIDTH - 2 * self.MARGIN - 24
            bar_height = 12
            bar_x = self.MARGIN + 12
            bar_y = progress_y + 22
            
            # Background
            pygame.draw.rect(self.screen, (30, 30, 40), 
                           (bar_x, bar_y, bar_width, bar_height), border_radius=7)
            
            # Progress
            if len(self.path) > 1:
                progress_ratio = self.current_state_index / (len(self.path) - 1)
                progress_width = int(bar_width * progress_ratio)
                if progress_width > 0:
                    progress_rect = pygame.Rect(bar_x, bar_y, progress_width, bar_height)
                    pygame.draw.rect(self.screen, self.EXIT_COLOR, progress_rect, border_radius=7)
        
        # Instructions - much more space to avoid overlap
        # move instructions up a bit so there's more space between them and the purple frame
        inst_y = progress_y + 36
        inst_text = "SPACE: Play  |  Arrows: Step  |  R: Reset  |  ESC: Exit"
        self.draw_text_with_shadow(inst_text, self.font_info, (180, 180, 190),
                                  self.MARGIN + 12, inst_y, shadow=False)
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.animating = not self.animating
                        self.last_update = time.time()
                    
                    elif event.key == pygame.K_RIGHT and not self.animating:
                        if self.current_state_index < len(self.path) - 1:
                            self.current_state_index += 1
                    
                    elif event.key == pygame.K_LEFT and not self.animating:
                        if self.current_state_index > 0:
                            self.current_state_index -= 1
                    
                    elif event.key == pygame.K_r:
                        self.current_state_index = 0
                        self.animating = False
                    
                    elif event.key == pygame.K_ESCAPE:
                        running = False
            
            # Animation
            if self.animating:
                current_time = time.time()
                if current_time - self.last_update >= self.animation_speed:
                    if self.current_state_index < len(self.path) - 1:
                        self.current_state_index += 1
                        self.last_update = current_time
                    else:
                        self.animating = False
            
            # Draw
            current_state = self.path[self.current_state_index]
            self.draw_board(current_state)
            self.draw_info()
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()


def visualize_solution(initial_state, solution_node, algorithm_name, steps):
    """Create and run the visualization."""
    game = RushHourGame(initial_state, solution_node, algorithm_name, steps)
    game.run()
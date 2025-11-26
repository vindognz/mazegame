# imports
import pygame

class MazeEditor:
    def __init__(self, grid_size=16, cell_size=32):
        # grid stuff
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.window_size = grid_size * cell_size
        
        # maze array - 0 = walkable, 1 = wall
        self.maze = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Maze Painter")
        
        self.running = True
    
    def handle_input(self):
        # check for window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # save on 's' key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    self.export_maze()
        
        # mouse drawing
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] or mouse_pressed[2]:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // self.cell_size
            grid_y = mouse_y // self.cell_size
            
            # make sure we're in bounds
            if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                if mouse_pressed[0]:  # left click = wall
                    self.maze[grid_y][grid_x] = 1
                elif mouse_pressed[2]:  # right click = erase
                    self.maze[grid_y][grid_x] = 0
    
    def draw(self):
        # draw the grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                color = (255, 255, 255) if self.maze[y][x] == 0 else (0, 0, 0)
                pygame.draw.rect(self.screen, color, 
                               (x * self.cell_size, y * self.cell_size, 
                                self.cell_size, self.cell_size))
        
        pygame.display.flip()
    
    # main loop
    def run(self):
        while self.running:
            self.handle_input()
            self.draw()
        
        pygame.quit()

    def export_maze(self):
        # save maze to file
        with open('maze_grid.txt', 'w') as f:
            f.write('grid = [\n')
            for row in self.maze:
                f.write(f'    {row},\n')
            f.write(']\n')
        print('saved to maze_grid.txt')

    
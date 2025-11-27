# imports
import pygame
import json

class MazeEditor:
    def __init__(self, grid_size=16, cell_size=32):
        # grid stuff
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.window_size = grid_size * cell_size
        
        # maze array - 0 = walkable, 1 = wall
        self.maze = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        
        # start and end positions
        self.start_pos = None
        self.end_pos = None

        self.path = []
        
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Maze Painteir")
        
        self.running = True
    
    def handle_input(self):
        # check for window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # keyboard controls
            if event.type == pygame.KEYDOWN:
                # clear path on any keypress except G
                if event.key != pygame.K_g:
                    self.path = []
                
                if event.key == pygame.K_s:
                    self.export_maze()
                elif event.key == pygame.K_q:  # q = place start
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // self.cell_size
                    grid_y = mouse_y // self.cell_size
                    if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                        if self.maze[grid_y][grid_x] != 3:  # can't be same as end
                            # remove old start if it exists
                            for y in range(self.grid_size):
                                for x in range(self.grid_size):
                                    if self.maze[y][x] == 2:
                                        self.maze[y][x] = 0
                            self.maze[grid_y][grid_x] = 2
                elif event.key == pygame.K_e:  # e = place end
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    grid_x = mouse_x // self.cell_size
                    grid_y = mouse_y // self.cell_size
                    if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                        if self.maze[grid_y][grid_x] != 2:  # can't be same as start
                            # remove old end if it exists
                            for y in range(self.grid_size):
                                for x in range(self.grid_size):
                                    if self.maze[y][x] == 3:
                                        self.maze[y][x] = 0
                            self.maze[grid_y][grid_x] = 3
                elif event.key == pygame.K_g:  # g = solve!
                    # find start and end in the grid
                    start = None
                    end = None
                    for y in range(self.grid_size):
                        for x in range(self.grid_size):
                            if self.maze[y][x] == 2:
                                start = (x, y)
                            elif self.maze[y][x] == 3:
                                end = (x, y)
                    
                    # make sure we have both start and end
                    if start and end:
                        from algorithms import BFS
                        solver = BFS(self.maze, start, end)
                        path = solver.solve()
                        if path:
                            print(f"Path found! Length: {len(path)}")
                            self.path = path
                        else:
                            print("No path found :(")
                    else:
                        print("Need both start and end points!")
                elif event.key == pygame.K_c:  # c = clear walls
                    for y in range(self.grid_size):
                        for x in range(self.grid_size):
                            if self.maze[y][x] == 1:
                                self.maze[y][x] = 0
                elif event.key == pygame.K_l:  # l = load maze
                    try:
                        import json
                        with open('maze_grid.json', 'r') as f:
                            loaded_grid = json.load(f)
                            
                            # make sure it's the right size
                            if len(loaded_grid) == self.grid_size and len(loaded_grid[0]) == self.grid_size:
                                self.maze = loaded_grid
                                print("Maze loaded!")
                            else:
                                print(f"Grid size mismatch! Expected {self.grid_size}x{self.grid_size}")
                    except FileNotFoundError:
                        print("No saved maze found :(")
                    except Exception as e:
                        print(f"Error loading maze: {e}")
        
        # mouse drawing
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] or mouse_pressed[2]:
            self.path = []  # clear path when drawing
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = mouse_x // self.cell_size
            grid_y = mouse_y // self.cell_size
            
            # make sure we're in bounds
            if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                # don't draw over start/end tiles
                if self.maze[grid_y][grid_x] not in [2, 3]:
                    if mouse_pressed[0]:  # left click = wall
                        self.maze[grid_y][grid_x] = 1
                    elif mouse_pressed[2]:  # right click = erase
                        self.maze[grid_y][grid_x] = 0
    
    def draw(self):
        # draw the grid
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # check if this tile is in the path
                if (x, y) in self.path:
                    color = (255, 0, 0)  # red path
                elif self.maze[y][x] == 2:
                    color = (0, 255, 0)  # green start
                elif self.maze[y][x] == 3:
                    color = (255, 255, 0)  # yellow end
                elif self.maze[y][x] == 0:
                    color = (255, 255, 255)  # white walkable
                else:
                    color = (0, 0, 0)  # black wall
                
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
        with open('maze_grid.json', 'w') as f:
            json.dump(self.maze, f)
        print('saved to maze_grid.json')

    
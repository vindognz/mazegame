# make sure you're running the right file
if __name__ == "__main__":
    print("Run gui.py silly.")
    exit()

# imports
import pygame
import json
import easygui
import os

from algorithms import *

class MazeEditor:
    def __init__(self, grid_size=16, cell_size=32):
        # grid stuff
        self.grid_size = grid_size
        self.cell_size = cell_size
        self.maze_size = grid_size * cell_size
        self.border_width = 8
        self.window_size = self.maze_size + (self.border_width * 2)
        
        # maze array - 0 = walkable, 1 = wall
        self.maze = [[0 for _ in range(grid_size)] for _ in range(grid_size)]
        
        # start and end positions
        self.start_pos = None
        self.end_pos = None

        self.path = []

        # animation stuff
        self.animating = False
        self.animation_generator = None
        self.animation_speed = 5  # frames between steps
        self.animation_counter = 0
        self.explored = set()  # blue tiles
        
        # pygame setup
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Maze Painteir")
        pygame.mouse.set_visible(False)

        
        self.running = True
    
    def handle_input(self):
        # check for window close
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # keyboard controls
            if event.type == pygame.KEYDOWN:
                
                # escape cancels animation
                if event.key == pygame.K_ESCAPE:
                    self.animating = False
                    self.explored = set()
                    self.path = []
                    print("Animation cancelled")
                    continue
                
                if not self.animating:
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
                            solver = BFS(self.maze, start, end)
                            self.animation_generator = solver.solve()
                            self.animating = True
                            self.explored = set()
                            self.path = []
                            print("Starting animation...")
                        else:
                            print("Need both start and end points!")
                    elif event.key == pygame.K_c:  # c = clear walls
                        for y in range(self.grid_size):
                            for x in range(self.grid_size):
                                if self.maze[y][x] == 1:
                                    self.maze[y][x] = 0
                    elif event.key == pygame.K_l:  # l = load maze
                        try:
                            # get list of saved mazes
                            if not os.path.exists('mazes'):
                                print("No mazes folder found!")
                                continue
                            
                            maze_files = [f.replace('.json', '') for f in os.listdir('mazes') if f.endswith('.json')]
                            
                            if not maze_files:
                                print("No saved mazes found!")
                                continue
                            
                            # show selection menu
                            choice = easygui.choicebox("Select a maze to load:", "Load Maze", maze_files)
                            
                            if choice:
                                filepath = f'mazes/{choice}.json'
                                with open(filepath, 'r') as f:
                                    loaded_grid = json.load(f)
                                    
                                    # make sure it's the right size
                                    if len(loaded_grid) == self.grid_size and len(loaded_grid[0]) == self.grid_size:
                                        self.maze = loaded_grid
                                        print(f"Maze '{choice}' loaded!")
                                    else:
                                        print(f"Grid size mismatch! Expected {self.grid_size}x{self.grid_size}")
                        except Exception as e:
                            print(f"Error loading maze: {e}")
                    elif event.key == pygame.K_d:  # d = delete maze
                        try:
                            # get list of saved mazes
                            if not os.path.exists('mazes'):
                                print("No mazes folder found!")
                                continue
                            
                            maze_files = [f.replace('.json', '') for f in os.listdir('mazes') if f.endswith('.json')]
                            
                            if not maze_files:
                                print("No saved mazes found!")
                                continue
                            
                            # show selection menu
                            choice = easygui.choicebox("Select a maze to delete:", "Delete Maze", maze_files)
                            
                            if choice:
                                # confirm deletion
                                confirm = easygui.ynbox(f"Are you sure you want to delete '{choice}'?", "Confirm Delete")
                                if confirm:
                                    filepath = f'mazes/{choice}.json'
                                    os.remove(filepath)
                                    print(f"Deleted '{choice}'")
                        except Exception as e:
                            print(f"Error deleting maze: {e}")
                    elif event.key == pygame.K_h:  # h = solve with A*
                        # find start and end in the grid
                        start = None
                        end = None
                        for y in range(self.grid_size):
                            for x in range(self.grid_size):
                                if self.maze[y][x] == 2:
                                    start = (x, y)
                                elif self.maze[y][x] == 3:
                                    end = (x, y)
                        
                        if start and end:
                            solver = AStar(self.maze, start, end)
                            self.animation_generator = solver.solve()
                            self.animating = True
                            self.explored = set()
                            self.path = []
                            print("Starting A* animation...")
                        else:
                            print("Need both start and end points!")
        
        # mouse drawing
        mouse_pressed = pygame.mouse.get_pressed()
        if mouse_pressed[0] or mouse_pressed[2]:
            self.path = []
            mouse_x, mouse_y = pygame.mouse.get_pos()
            grid_x = (mouse_x - self.border_width) // self.cell_size
            grid_y = (mouse_y - self.border_width) // self.cell_size
            
            if not self.animating:  # only draw if not animating
                # make sure we're in bounds
                if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                    # don't draw over start/end tiles
                    if self.maze[grid_y][grid_x] not in [2, 3]:
                        if mouse_pressed[0]:  # left click = wall
                            self.maze[grid_y][grid_x] = 1
                        elif mouse_pressed[2]:  # right click = erase
                            self.maze[grid_y][grid_x] = 0

    def update(self):
        if self.animating and self.animation_counter >= self.animation_speed:
            self.animation_counter = 0
            try:
                status, pos, data = next(self.animation_generator)
                
                if status == 'exploring':
                    self.explored = set(data)
                elif status == 'path':
                    self.explored = set()  # clear the blue wave
                    self.path = data[:]
                elif status == 'done':
                    self.explored = set()  # make sure it's cleared
                    self.path = data
                    self.animating = False
                    print(f"Path found! Length: {len(self.path)}")
                elif status == 'no_path':
                    self.animating = False
                    print("No path found :(")
            except StopIteration:
                self.animating = False
        
        if self.animating:
            self.animation_counter += 1
    
    def draw(self):
        # fill background
        self.screen.fill((50, 50, 50))
        
        # draw the grid (offset by border)
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                # check colors
                if (x, y) in self.path:
                    color = (255, 0, 0)  # red path
                elif (x, y) in self.explored:
                    color = (100, 150, 255)  # light blue explored
                elif self.maze[y][x] == 2:
                    color = (0, 255, 0)  # green start
                elif self.maze[y][x] == 3:
                    color = (255, 255, 0)  # yellow end
                elif self.maze[y][x] == 0:
                    color = (255, 255, 255)  # white walkable
                else:
                    color = (0, 0, 0)  # black wall
                
                pygame.draw.rect(self.screen, color, 
                            (self.border_width + x * self.cell_size, 
                                self.border_width + y * self.cell_size, 
                                self.cell_size, self.cell_size))
        
        # draw custom pencil cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pygame.draw.rect(self.screen, (210, 140, 70), (mouse_x - 4, mouse_y - 20, 8, 24))
        pencil_tip = [(mouse_x, mouse_y + 8), (mouse_x - 4, mouse_y + 4), (mouse_x + 4, mouse_y + 4)]
        pygame.draw.polygon(self.screen, (50, 50, 50), pencil_tip)
        pygame.draw.rect(self.screen, (255, 150, 150), (mouse_x - 4, mouse_y - 24, 8, 4))
        
        pygame.display.flip()
    
    # main loop
    def run(self):
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
        
        pygame.quit()

    def export_maze(self):
        # create mazes directory if it doesn't exist
        os.makedirs('mazes', exist_ok=True)
        
        # ask for maze name
        name = easygui.enterbox("Enter maze name:", "Save Maze")
        if name:
            # save maze to file
            filepath = f'mazes/{name}.json'
            with open(filepath, 'w') as f:
                json.dump(self.maze, f)
            print(f'saved to {filepath}')

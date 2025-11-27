# imports
from collections import deque

class Algorithm:
    def __init__(self, grid, start, end):
        self.grid = grid
        self.start = start
        self.end = end
        self.path = []
        self.visited = set()
        
    def solve(self):
        # override this in child classes
        raise NotImplementedError
    
    def is_valid(self, pos):
        x, y = pos
        n = len(self.grid)
        return 0 <= x < n and 0 <= y < n and self.grid[y][x] in [0, 2, 3]
    
    def get_neighbours(self, pos):
        x, y = pos
        return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

class BFS(Algorithm):
    def solve(self):
        queue = deque([self.start])
        self.visited = {self.start}
        parent = {self.start: None}
        
        while queue:
            pos = queue.popleft()
            
            # yield current position being explored
            yield ('exploring', pos, list(self.visited))
            
            if pos == self.end:
                # reconstruct path
                path = []
                current = self.end
                while current is not None:
                    path.append(current)
                    # yield each step of path reconstruction
                    yield ('path', current, path[:])
                    current = parent[current]
                path.reverse()
                yield ('done', None, path)
                return
            
            for neighbour in self.get_neighbours(pos):
                if self.is_valid(neighbour) and neighbour not in self.visited:
                    queue.append(neighbour)
                    self.visited.add(neighbour)
                    parent[neighbour] = pos
        
        yield ('no_path', None, [])

# add more algorithms later like:
# class AStar(Algorithm):
# class DFS(Algorithm):
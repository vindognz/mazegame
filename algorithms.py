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
        return [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1),  # cardinal directions
            # (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)  # diagonals
        ]

    # FOR KNIGHT
    # def get_neighbours(self, pos):
    #     x, y = pos
    #     return [
    #         (x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),  # horizontal L's
    #         (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)   # vertical L's
    #     ]

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

import heapq

class AStar(Algorithm):
    def solve(self):
        # priority queue: (f_score, counter, position)
        counter = 0  # tie-breaker for equal f_scores
        start_h = self.heuristic(self.start, self.end)
        heap = [(start_h, counter, self.start)]
        counter += 1
        
        self.visited = {self.start}
        parent = {self.start: None}
        g_score = {self.start: 0}
        
        while heap:
            f, _, pos = heapq.heappop(heap)
            
            # yield current position being explored
            yield ('exploring', pos, list(self.visited))
            
            if pos == self.end:
                # reconstruct path
                path = []
                current = self.end
                while current is not None:
                    path.append(current)
                    yield ('path', current, path[:])
                    current = parent[current]
                path.reverse()
                yield ('done', None, path)
                return
            
            for neighbour in self.get_neighbours(pos):
                if self.is_valid(neighbour):
                    tentative_g = g_score[pos] + 1
                    
                    if neighbour not in g_score or tentative_g < g_score[neighbour]:
                        g_score[neighbour] = tentative_g
                        f_score = tentative_g + self.heuristic(neighbour, self.end)
                        heapq.heappush(heap, (f_score, counter, neighbour))
                        counter += 1
                        parent[neighbour] = pos
                        self.visited.add(neighbour)
        
        yield ('no_path', None, [])
    
    def heuristic(self, pos1, pos2):
        # manhattan distance for 4-directional
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        
        # euclidean for 8-directional/diagonals
        # return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5
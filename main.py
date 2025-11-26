from PIL import Image
from collections import deque

img = Image.open("maze.png")

img = img.convert('RGB')

width, height = img.size

if width != height:
    raise ValueError(f"Image must be square! Got {width}x{height}")

n = width
grid = []

for y in range(n):
    row = []
    for x in range(n):
        pixel = img.getpixel((x, y))

        # pure white = walkable tile
        # everything else = wall
        if pixel == (255, 255, 255):
            row.append(0)
        else:
            row.append(1)
    grid.append(row)

def isValid(pos, grid, n):
    x, y = pos
    return 0 <= x < n and 0 <= y < n and grid[y][x] == 0

def getNeighbours(pos):
    x, y = pos
    return [
        (x+1, y), (x, y+1),
        (x-1, y), (x, y-1)
    ]

def BFS(start, end, grid, n):
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    while len(queue) != 0:
        pos = queue.popleft()

        if pos == end:
            path = []
            current = end

            while current is not None:
                path.append(current)
                current = parent[current]

            path.reverse()
            return path
        
        for neighbour in getNeighbours(pos):
            if isValid(neighbour, grid, n) and neighbour not in visited:
                queue.append(neighbour)
                visited.add(neighbour)
                parent[neighbour] = pos
    
    return []

path = BFS((0, 0), (n-1, n-1), grid, n)

path_set = set(path)
for y in range(n):
    for x in range(n):
        if (x, y) in path_set:
            print('\033[42m' + '\033[1m' + ' ' + '\033[0m', end=' ')
        elif grid[y][x] == 1:
            print('+', end=' ')
        else:
            print('\033[41m' + '\033[1m' + ' ' + '\033[0m', end=' ')
    print()

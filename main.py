from PIL import Image
from collections import deque

# load image
img = Image.open("maze.png").convert('RGB')
width, height = img.size

if width != height:
    raise ValueError(f"Image must be square! Got {width}x{height}")

n = width

# convert image to grid
grid = []
for y in range(n):
    row = []
    for x in range(n):
        pixel = img.getpixel((x, y))
        row.append(0 if pixel == (255, 255, 255) else 1)  # 0 = walkable, 1 = wall
    grid.append(row)

# helper BFS functions
def isValid(pos, grid, n):
    x, y = pos
    return 0 <= x < n and 0 <= y < n and grid[y][x] == 0

def getNeighbours(pos):
    x, y = pos
    return [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]

def BFS(start, end, grid, n):
    queue = deque([start])
    visited = {start}
    parent = {start: None}

    while queue:
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

# create the output image
output = Image.new('RGB', (n, n))

for y in range(n):
    for x in range(n):
        if (x, y) in path_set:
            output.putpixel((x, y), (0, 255, 0))  # green path
        elif grid[y][x] == 1:
            output.putpixel((x, y), (0, 0, 0))    # black walls
        else:
            output.putpixel((x, y), (255, 255, 255))  # white walkable

# save solved maze image
output.save("solved_maze.png")
print("Saved solved_maze.png")

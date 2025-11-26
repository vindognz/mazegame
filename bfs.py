grid = [
    [0, 1, 0, 0, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 1, 0],
    [0, 1, 0, 1, 0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 1, 0]
]
n = len(grid)

def isValid(pos):
    x, y = pos
    return 0 <= x < n and 0 <= y < n and grid[y][x] == 0

def getNeighbours(pos):
    x, y = pos
    return [
        (x+1, y), (x-1, y),
        (x, y+1), (x, y-1)
    ]

def BFS(start, end):
    queue = [(start, 0)]
    visited = {start}
    parent = {start: None}
    
    while len(queue) != 0:
        pos, moves = queue.pop(0)

        if pos == end:
            path = []
            current = end

            while current is not None:
                path.append(current)
                current = parent[current]

            path.reverse()
            return moves, path
        
        for neighbour in getNeighbours(pos):
            if isValid(neighbour) and neighbour not in visited:
                queue.append((neighbour, moves+1))
                visited.add(neighbour)
                parent[neighbour] = pos
    
    return None, []

moves, path = BFS((0, 0), (8, 8))
print(f"Moves: {moves}")

path_set = set(path)
for y in range(n):
    for x in range(n):
        if (x, y) in path_set:
            print('\033[0;32m' + '\033[1m' + '*' + '\033[0m', end=' ')
        elif grid[y][x] == 1:
            print('+', end=' ')
        else:
            print('.', end=' ')
    print()
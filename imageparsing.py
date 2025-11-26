from PIL import Image

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

print("grid = [")
for row in grid:
    print(f"    {row},")
print("]")

print("\nVisualization:")
for row in grid:
    for cell in row:
        print('\033[0;32m' + '\033[1m' + '*' + '\033[0m' if cell == 0 else '.', end=' ')
    print()
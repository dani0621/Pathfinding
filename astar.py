# A* Pathfinding Algorithm
# user clicks two points, the first is the start node and the second is the end node
# press space for the path to be run, and press "r" to create a new map (different walls)
# followed tutorial on YouTube by Tech With Tim and made previous adjustments (visuals, creating random walls, "r" to make new map/grid, reset start/end nodes after path is found)
# https://www.youtube.com/watch?v=JtiK0DOeI4A
# ChatGPT was used to debug and help with making changes

import pygame
import random
import time
from queue import PriorityQueue

# constants, set up window, grid
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 50, 50
CELL_SIZE = WIDTH // COLS
WALL_FREQUENCY = 0.1 # probability of a cell being a wall

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BRIGHT_BLUE = (115, 232, 255)
GRAY = (200, 200, 200)
YELLOW = (255, 232, 115)
PURPLE = (216, 148, 255)

# initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Pathfinding")
clock = pygame.time.Clock()

# generate grid, blank cell is 0, wall is 1
def generate_grid():
    return [
        [1 if random.random() < WALL_FREQUENCY else 0 for _ in range(COLS)]
        for _ in range(ROWS)
    ]

# draw grid, start, end, visited cells, and path on the screen
def draw_grid(grid, start, end, path=set(), visited=set()):
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE
            if grid[r][c] == 1:
                color = BLACK  # wall color
            elif (r, c) in visited:
                color = RED  # visited nodes
            elif (r, c) in path:
                color = BRIGHT_BLUE  # Path found by A* algorithm
            pygame.draw.rect(screen, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw start and end
    if start:
        pygame.draw.rect(screen, YELLOW, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    if end:
        pygame.draw.rect(screen, PURPLE, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Draw grid lines
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

    pygame.display.update()

# Heuristic function- Manhattan distance
def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

# A* pathfinding Algorithm
def a_star(grid, start, end):
    open_set = PriorityQueue() # The open set (priority queue) stores nodes to be evaluated
    open_set.put((0, start))  # (f_score, node)
    came_from = {} # track the path (came from which node)
    g_score = {start: 0} # track the cost to reach each node from start
    f_score = {start: heuristic(start, end)} # Dictionary to track the estimated total cost (f = g + h)

    visited = set() # Set of visited nodes to avoid re-processing
    path_found = False # Flag to indicate if a path has been found

    while not open_set.empty(): # Continue searching until the open set is empty
        _, current = open_set.get() # Get the node with the lowest f-score

        if current in visited:
            continue # Skip nodes that have already been visited
        visited.add(current) # Mark the current node as visited

        if current == end: # stop the search once reach end node
            path_found = True
            break

        # Check neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dr, current[1] + dc)

            if (
                0 <= neighbor[0] < ROWS
                and 0 <= neighbor[1] < COLS
                and grid[neighbor[0]][neighbor[1]] == 0  # Ensure not a wall
            ):
                tentative_g_score = g_score[current] + 1 # cost to reach the neighbor

                if tentative_g_score < g_score.get(neighbor, float('inf')): # If this path is better, update
                    came_from[neighbor] = current # where we come from
                    g_score[neighbor] = tentative_g_score # Update g-score
                    f_score[neighbor] = tentative_g_score + heuristic(neighbor, end) # Update f-score
                    open_set.put((f_score[neighbor], neighbor))

        # update grid
        draw_grid(grid, start, end, visited=visited)
        time.sleep(0.01)  # slope loop down for better visuals

    # path from the end node back to the start node
    path = set()
    if path_found:
        current = end
        while current in came_from:
            path.add(current)
            current = came_from[current]
        path.add(start)

    return path, visited # Return the path and visited nodes

# Main loop
def main():
    running = True
    grid = generate_grid()
    start = None # no set start/end coordinates in the beginning
    end = None
    path = set()

    while running:
        screen.fill(WHITE) # Fill the screen with white before drawing the grid
        draw_grid(grid, start, end, path=path) # draw grids

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # ChatGPT helped with this
                if event.key == pygame.K_r:  # make another grid/map if user presses "r"
                    grid = generate_grid()
                    start = None
                    end = None
                    path = set()  # Clear the path
                elif event.key == pygame.K_SPACE and start and end:  # 'Space' to start the A* search
                    path, visited = a_star(grid, start, end) # Run A* algorithm
                    start = None  # Reset start after path
                    end = None    # Reset end after path
            # ChatGPT help with this too
            elif event.type == pygame.MOUSEBUTTONDOWN: # Mouse click events to set start and end
                pos = pygame.mouse.get_pos() # mouse position
                row, col = pos[1] // CELL_SIZE, pos[0] // CELL_SIZE # Convert to grid coordinates
                if not start:
                    start = (row, col)
                elif not end and (row, col) != start:
                    end = (row, col)

    pygame.quit()

if __name__ == "__main__":
    main()
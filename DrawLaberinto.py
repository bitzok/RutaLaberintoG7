import pygame
import random

pygame.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
CELL_SIZE = 15
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("G7-PROBLEMA LABERINTO")

# Camino libre = 0
# Camino ocupado = 1
def generate_maze(maze):
    start_x, start_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
    start_x = (start_x // 2) * 2
    start_y = (start_y // 2) * 2
    maze[start_y][start_x] = 0

    walls = [(start_x, start_y, dx, dy) for dx, dy in DIRECTIONS if 0 <= start_x + dx * 2 < GRID_WIDTH and 0 <= start_y + dy * 2 < GRID_HEIGHT]

    while walls:
        x, y, dx, dy = random.choice(walls)
        walls.remove((x, y, dx, dy))

        nx, ny = x + dx * 2, y + dy * 2
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and maze[ny][nx] == 1:
            maze[y + dy][x + dx] = 0
            maze[ny][nx] = 0

            walls += [(nx, ny, dx, dy) for dx, dy in DIRECTIONS if 0 <= nx + dx * 2 < GRID_WIDTH and 0 <= ny + dy * 2 < GRID_HEIGHT]

def draw_maze(maze):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

start_pos = (0, 0)
end_pos = (GRID_WIDTH - 2, GRID_HEIGHT - 2)

def draw_robot(position, color=BLUE):
    pygame.draw.rect(screen, color, (position[1] * CELL_SIZE, position[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def move_robot(maze, position, direction):
    x, y = position
    if direction == "up" and x > 0 and maze[x - 1][y] == 0:
        x -= 1
    elif direction == "down" and x < GRID_HEIGHT - 1 and maze[x + 1][y] == 0:
        x += 1
    elif direction == "left" and y > 0 and maze[x][y - 1] == 0:
        y -= 1
    elif direction == "right" and y < GRID_WIDTH - 1 and maze[x][y + 1] == 0:
        y += 1
    return (x, y)

def show_victory_screen():
    font = pygame.font.Font(None, 74)
    text = font.render("¡Ganaste!", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.fill(WHITE)
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.delay(2000)

def main():
    maze = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    generate_maze(maze)

    robot_pos = start_pos
    running = True
    clock = pygame.time.Clock()

    while running:
        screen.fill(WHITE)
        draw_maze(maze)
        draw_robot(robot_pos)
        pygame.draw.rect(screen, GREEN, (start_pos[1] * CELL_SIZE, start_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (end_pos[1] * CELL_SIZE, end_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

        if robot_pos == end_pos:
            show_victory_screen()
            running = False  # Salir del bucle principal

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    robot_pos = move_robot(maze, robot_pos, "up")
                elif event.key == pygame.K_DOWN:
                    robot_pos = move_robot(maze, robot_pos, "down")
                elif event.key == pygame.K_LEFT:
                    robot_pos = move_robot(maze, robot_pos, "left")
                elif event.key == pygame.K_RIGHT:
                    robot_pos = move_robot(maze, robot_pos, "right")

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()

import pygame
import random
import time
from algoritmoGenetico import GeneticAlgorithm

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

def generate_maze(maze, progress_callback=None):
    start_x, start_y = random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1)
    start_x = (start_x // 2) * 2
    start_y = (start_y // 2) * 2
    maze[start_y][start_x] = 0

    walls = [(start_x, start_y, dx, dy) for dx, dy in DIRECTIONS if 0 <= start_x + dx * 2 < GRID_WIDTH and 0 <= start_y + dy * 2 < GRID_HEIGHT]

    total_cells = GRID_WIDTH * GRID_HEIGHT // 2
    cleared_cells = 0

    while walls:
        x, y, dx, dy = random.choice(walls)
        walls.remove((x, y, dx, dy))

        nx, ny = x + dx * 2, y + dy * 2
        if 0 <= nx < GRID_WIDTH and 0 <= ny < GRID_HEIGHT and maze[ny][nx] == 1:
            maze[y + dy][x + dx] = 0
            maze[ny][nx] = 0
            cleared_cells += 1

            if progress_callback:
                progress_callback(cleared_cells / total_cells)

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
    if direction in ["up", "w"] and x > 0 and maze[x - 1][y] == 0:
        x -= 1
    elif direction in ["down", "s"] and x < GRID_HEIGHT - 1 and maze[x + 1][y] == 0:
        x += 1
    elif direction in ["left", "a"] and y > 0 and maze[x][y - 1] == 0:
        y -= 1
    elif direction in ["right", "d"] and y < GRID_WIDTH - 1 and maze[x][y + 1] == 0:
        y += 1
    return (x, y)

def show_victory_screen(simulation_time, steps_taken):
    font = pygame.font.Font(None, 74)
    small_font = pygame.font.Font(None, 36)

    text = font.render("¡PRUEBA FINALIZADA!", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    
    time_text = small_font.render(f"Tiempo de Simulación: {simulation_time:.2f} segundos", True, BLACK)
    time_text_rect = time_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    steps_text = small_font.render(f"Pasos Dados: {steps_taken}", True, BLACK)
    steps_text_rect = steps_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))

    screen.fill(WHITE)
    screen.blit(text, text_rect)
    screen.blit(time_text, time_text_rect)
    screen.blit(steps_text, steps_text_rect)

    pygame.display.flip()
    pygame.time.delay(3000)

def show_loading_screen(progress):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 36)
    
    loading_text = font.render("Generando laberinto...", True, BLACK)
    loading_text_rect = loading_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
    screen.blit(loading_text, loading_text_rect)
    
    bar_width = 400
    bar_height = 30
    progress_width = int(bar_width * progress)
    pygame.draw.rect(screen, BLACK, [(SCREEN_WIDTH - bar_width) // 2, SCREEN_HEIGHT // 2, bar_width, bar_height], 2)
    pygame.draw.rect(screen, GREEN, [(SCREEN_WIDTH - bar_width) // 2, SCREEN_HEIGHT // 2, progress_width, bar_height])

    pygame.display.flip()

def main():
    maze = [[1 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    
    def update_progress(progress):
        show_loading_screen(progress)
    
    generate_maze(maze, progress_callback=update_progress)

    genetic_algo = GeneticAlgorithm(maze, start_pos, end_pos)
    start_time = time.time()
    best_path = genetic_algo.evolve()
    steps_taken = 0

    robot_pos = start_pos
    for move in best_path:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        robot_pos = move_robot(maze, robot_pos, move)
        steps_taken += 1
        draw_maze(maze)
        draw_robot(robot_pos)
        pygame.draw.rect(screen, GREEN, (start_pos[1] * CELL_SIZE, start_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (end_pos[1] * CELL_SIZE, end_pos[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(100)

        if robot_pos == end_pos:
            end_time = time.time()
            simulation_time = end_time - start_time
            show_victory_screen(simulation_time, steps_taken)
            break

    pygame.quit()

if __name__ == "__main__":
    main()

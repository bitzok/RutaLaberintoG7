import pygame
import random


class Laberinto:
    DIRECCIONES = [(0, -1), (0, 1), (-1, 0), (1, 0)]
    BLANCO = (255, 255, 255)
    NEGRO = (0, 0, 0)
    VERDE = (0, 255, 0)

    def __init__(self, ancho, alto, tamano_celda):
        self.ancho = ancho
        self.alto = alto
        self.tamano_celda = tamano_celda
        self.grid_ancho = ancho // tamano_celda
        self.grid_alto = alto // tamano_celda
        self.mapa = [[1 for _ in range(self.grid_ancho)] for _ in range(self.grid_alto)]
        self.screen = pygame.display.set_mode((ancho, alto))
        pygame.display.set_caption("G7-PROBLEMA LABERINTO")

    def generar(self):
        start_x, start_y = random.randint(0, self.grid_ancho - 1), random.randint(0, self.grid_alto - 1)
        start_x = (start_x // 2) * 2
        start_y = (start_y // 2) * 2
        self.mapa[start_y][start_x] = 0
        walls = [(start_x, start_y, dx, dy) for dx, dy in self.DIRECCIONES if 0 <= start_x + dx * 2 < self.grid_ancho and 0 <= start_y + dy * 2 < self.grid_alto]

        total_cells = (self.grid_ancho * self.grid_alto) // 2
        cleared_cells = 0

        while walls:
            x, y, dx, dy = random.choice(walls)
            walls.remove((x, y, dx, dy))

            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < self.grid_ancho and 0 <= ny < self.grid_alto and self.mapa[ny][nx] == 1:
                self.mapa[y + dy][x + dx] = 0
                self.mapa[ny][nx] = 0
                cleared_cells += 1

                self.mostrar_pantalla_carga(cleared_cells / total_cells)

                walls += [(nx, ny, dx, dy) for dx, dy in self.DIRECCIONES if 0 <= nx + dx * 2 < self.grid_ancho and 0 <= ny + dy * 2 < self.grid_alto]

    def mostrar_pantalla_carga(self, progreso):
        self.screen.fill(self.BLANCO)
        font = pygame.font.Font(None, 36)

        loading_text = font.render("Generando laberinto...", True, self.NEGRO)
        loading_text_rect = loading_text.get_rect(center=(self.ancho // 2, self.alto // 2 - 50))
        self.screen.blit(loading_text, loading_text_rect)

        bar_width = 400
        bar_height = 30
        progress_width = int(bar_width * progreso)

        pygame.draw.rect(self.screen, self.NEGRO, [(self.ancho - bar_width) // 2, self.alto // 2, bar_width, bar_height], 2)
        pygame.draw.rect(self.screen, self.VERDE, [(self.ancho - bar_width) // 2, self.alto // 2, progress_width, bar_height])

        pygame.display.flip()

    def dibujar(self):
        for y in range(self.grid_alto):
            for x in range(self.grid_ancho):
                color = self.BLANCO if self.mapa[y][x] == 0 else self.NEGRO
                pygame.draw.rect(self.screen, color, (x * self.tamano_celda, y * self.tamano_celda, self.tamano_celda, self.tamano_celda))

    def obtener_matriz(self):
        return self.mapa

import random
import pygame

class Laberinto:
    DIRECCIONES = [(0, -1), (0, 1), (-1, 0), (1, 0)]

    def __init__(self, ancho, alto, tamano_celda):
        self.ancho = ancho
        self.alto = alto
        self.tamano_celda = tamano_celda
        self.ancho_celdas = ancho // tamano_celda
        self.alto_celdas = alto // tamano_celda
        self.mapa = [[1 for _ in range(self.ancho_celdas)] for _ in range(self.alto_celdas)]
        self.posicion_inicio = (0, 0)
        self.posicion_fin = (self.ancho_celdas - 2, self.alto_celdas - 2)
        self.generar_laberinto()

    def generar_laberinto(self):
        inicio_x, inicio_y = random.randint(0, self.ancho_celdas - 1), random.randint(0, self.alto_celdas - 1)
        inicio_x = (inicio_x // 2) * 2
        inicio_y = (inicio_y // 2) * 2
        self.mapa[inicio_y][inicio_x] = 0

        muros = [(inicio_x, inicio_y, dx, dy) for dx, dy in self.DIRECCIONES if 0 <= inicio_x + dx * 2 < self.ancho_celdas and 0 <= inicio_y + dy * 2 < self.alto_celdas]

        while muros:
            x, y, dx, dy = random.choice(muros)
            muros.remove((x, y, dx, dy))

            nx, ny = x + dx * 2, y + dy * 2
            if 0 <= nx < self.ancho_celdas and 0 <= ny < self.alto_celdas and self.mapa[ny][nx] == 1:
                self.mapa[y + dy][x + dx] = 0
                self.mapa[ny][nx] = 0

                muros += [(nx, ny, dx, dy) for dx, dy in self.DIRECCIONES if 0 <= nx + dx * 2 < self.ancho_celdas and 0 <= ny + dy * 2 < self.alto_celdas]

    def dibujar_laberinto(self, pantalla, colores):
        for y in range(self.alto_celdas):
            for x in range(self.ancho_celdas):
                color = colores['BLANCO'] if self.mapa[y][x] == 0 else colores['NEGRO']
                pygame.draw.rect(pantalla, color, (x * self.tamano_celda, y * self.tamano_celda, self.tamano_celda, self.tamano_celda))

    def es_camino_libre(self, x, y):
        return 0 <= x < self.alto_celdas and 0 <= y < self.ancho_celdas and self.mapa[x][y] == 0

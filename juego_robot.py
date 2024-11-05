import pygame
from algoritmo_genetico import GeneticAlgorithm

class JuegoRobot:
    COLORES = {
        "BLANCO": (255, 255, 255),
        "NEGRO": (0, 0, 0),
        "VERDE": (0, 255, 0),
        "AZUL": (0, 0, 255),
        "ROJO": (255, 0, 0),
    }
    def __init__(self, laberinto):
        self.pantalla = pygame.display.set_mode((laberinto.ancho, laberinto.alto))
        pygame.display.set_caption("G7-PROBLEMA LABERINTO")
        self.laberinto = laberinto
        self.posicion_robot = laberinto.posicion_inicio
        self.reloj = pygame.time.Clock()
        self.jugando = True
        self.mejor_ruta = []
        self.indice_movimiento = 0
        self.contador_pasos = 0
        start_pos = self.laberinto.posicion_inicio
        end_pos = self.laberinto.posicion_fin
        algoritmo_genetico = GeneticAlgorithm(
            maze=laberinto.mapa,
            start_pos=start_pos,
            end_pos=end_pos,
            population_size=200,
            mutation_rate=0.04,
            max_generations=1000
        )
        self.mejor_ruta = algoritmo_genetico.evolve()
        self.indice_movimiento = 0

    def dibujar_elementos(self):
        self.pantalla.fill(self.COLORES["BLANCO"])
        self.laberinto.dibujar_laberinto(self.pantalla, self.COLORES)
        self.dibujar_robot()
        pygame.draw.rect(self.pantalla, self.COLORES["VERDE"],
                         (self.laberinto.posicion_inicio[1] * self.laberinto.tamano_celda, self.laberinto.posicion_inicio[0] * self.laberinto.tamano_celda, self.laberinto.tamano_celda, self.laberinto.tamano_celda))
        pygame.draw.rect(self.pantalla, self.COLORES["ROJO"],
                         (self.laberinto.posicion_fin[1] * self.laberinto.tamano_celda, self.laberinto.posicion_fin[0] * self.laberinto.tamano_celda, self.laberinto.tamano_celda, self.laberinto.tamano_celda))
    def dibujar_robot(self):
        pygame.draw.rect(self.pantalla, self.COLORES["AZUL"],
                         (self.posicion_robot[1] * self.laberinto.tamano_celda, self.posicion_robot[0] * self.laberinto.tamano_celda, self.laberinto.tamano_celda, self.laberinto.tamano_celda))

    def mover_robot(self):
        # Mover el robot siguiendo la mejor ruta encontrada por el algoritmo genético
        if self.indice_movimiento < len(self.mejor_ruta):
            direccion = self.mejor_ruta[self.indice_movimiento]
            x, y = self.posicion_robot

            # Comprobar la dirección y si el movimiento es posible
            if direccion == "up" and self.laberinto.es_camino_libre(x - 1, y):
                x -= 1
            elif direccion == "down" and self.laberinto.es_camino_libre(x + 1, y):
                x += 1
            elif direccion == "left" and self.laberinto.es_camino_libre(x, y - 1):
                y -= 1
            elif direccion == "right" and self.laberinto.es_camino_libre(x, y + 1):
                y += 1

            # Actualizar la posición del robot
            self.posicion_robot = (x, y)
            self.indice_movimiento += 1
            self.contador_pasos += 1
    def mostrar_pantalla_victoria(self):
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render(f"¡Ganaste! Pasos: {self.contador_pasos}", True, self.COLORES["NEGRO"])  # Mostrar pasos
        rect_texto = texto.get_rect(center=(self.laberinto.ancho // 2, self.laberinto.alto // 2))
        self.pantalla.fill(self.COLORES["BLANCO"])
        self.pantalla.blit(texto, rect_texto)
        pygame.display.flip()
        pygame.time.delay(2000)

    def ejecutar(self):
        while self.jugando:
            self.dibujar_elementos()

            # Mover el robot automáticamente
            if self.posicion_robot != self.laberinto.posicion_fin:
                self.mover_robot()
            else:
                self.mostrar_pantalla_victoria()
                self.jugando = False

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jugando = False

            pygame.display.flip()
            self.reloj.tick(10)

        pygame.quit()
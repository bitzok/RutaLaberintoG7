import pygame
import time
from algoritmo_genetico import GeneticAlgorithm

class JuegoRobot:
    BLUE = (0, 0, 255)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)

    def _init_(self, laberinto):
        self.laberinto = laberinto
        self.start_pos = (0, 0)
        self.end_pos = (self.laberinto.grid_ancho - 2, self.laberinto.grid_alto - 2)
        self.robot_pos = self.start_pos
        self.genetic_algo = GeneticAlgorithm(self.laberinto.obtener_matriz(), self.start_pos, self.end_pos)

    def dibujar_robot(self, posicion):
        pygame.draw.rect(self.laberinto.screen, self.BLUE, (posicion[1] * self.laberinto.tamano_celda, posicion[0] * self.laberinto.tamano_celda, self.laberinto.tamano_celda, self.laberinto.tamano_celda))

    def mover_robot(self, direccion):
        x, y = self.robot_pos
        maze = self.laberinto.obtener_matriz()
        if direccion == "up" and x > 0 and maze[x - 1][y] == 0:
            x -= 1
        elif direccion == "down" and x < self.laberinto.grid_alto - 1 and maze[x + 1][y] == 0:
            x += 1
        elif direccion == "left" and y > 0 and maze[x][y - 1] == 0:
            y -= 1
        elif direccion == "right" and y < self.laberinto.grid_ancho - 1 and maze[x][y + 1] == 0:
            y += 1
        self.robot_pos = (x, y)

    def mostrar_pantalla_victoria(self, tiempo_simulacion, pasos_dados):
        font = pygame.font.Font(None, 74)
        small_font = pygame.font.Font(None, 36)

        text = font.render("¡PRUEBA FINALIZADA!", True, (0, 0, 0))
        time_text = small_font.render(f"Tiempo de Simulación: {tiempo_simulacion:.2f} segundos", True, (0, 0, 0))
        steps_text = small_font.render(f"Pasos Dados: {pasos_dados}", True, (0, 0, 0))

        self.laberinto.screen.fill((255, 255, 255))
        self.laberinto.screen.blit(text, text.get_rect(center=(self.laberinto.ancho // 2, self.laberinto.alto // 2 - 50)))
        self.laberinto.screen.blit(time_text, time_text.get_rect(center=(self.laberinto.ancho // 2, self.laberinto.alto // 2 + 20)))
        self.laberinto.screen.blit(steps_text, steps_text.get_rect(center=(self.laberinto.ancho // 2, self.laberinto.alto // 2 + 60)))

        pygame.display.flip()
        pygame.time.delay(3000)

    def ejecutar(self):
        self.laberinto.generar()
        best_path = self.genetic_algo.evolve()
        start_time = time.time()
        pasos_dados = 0

        for move in best_path:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            self.mover_robot(move)
            pasos_dados += 1

            self.laberinto.dibujar()
            self.dibujar_robot(self.robot_pos)
            pygame.draw.rect(self.laberinto.screen, self.GREEN, (self.start_pos[1] * self.laberinto.tamano_celda, self.start_pos[0] * self.laberinto.tamano_celda, self.laberinto.tamano_celda, self.laberinto.tamano_celda))
            pygame.draw.rect(self.laberinto.screen, self.RED, (self.end_pos[1] * self.laberinto.tamano_celda, self.end_pos[0] * self.laberinto.tamano_celda, self.laberinto.tamano_celda, self.laberinto.tamano_celda))

            pygame.display.flip()
            pygame.time.delay(100)

            if self.robot_pos == self.end_pos:
                simulation_time = time.time() - start_time
                self.mostrar_pantalla_victoria(simulation_time, pasos_dados)
                break

        pygame.quit()
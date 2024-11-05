import pygame
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
    def mover_robot(self, direccion):
        x, y = self.posicion_robot
        if direccion == "arriba" and self.laberinto.es_camino_libre(x - 1, y):
            x -= 1
        elif direccion == "abajo" and self.laberinto.es_camino_libre(x + 1, y):
            x += 1
        elif direccion == "izquierda" and self.laberinto.es_camino_libre(x, y - 1):
            y -= 1
        elif direccion == "derecha" and self.laberinto.es_camino_libre(x, y + 1):
            y += 1
        self.posicion_robot = (x, y)
    def mostrar_pantalla_victoria(self):
        fuente = pygame.font.Font(None, 74)
        texto = fuente.render("¡Ganaste!", True, self.COLORES["NEGRO"])
        rect_texto = texto.get_rect(center=(self.laberinto.ancho // 2, self.laberinto.alto // 2))
        self.pantalla.fill(self.COLORES["BLANCO"])
        self.pantalla.blit(texto, rect_texto)
        pygame.display.flip()
        pygame.time.delay(2000)
    def ejecutar(self):
        while self.jugando:
            self.dibujar_elementos()
            if self.posicion_robot == self.laberinto.posicion_fin:
                self.mostrar_pantalla_victoria()
                self.jugando = False
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.jugando = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        self.mover_robot("arriba")
                    elif evento.key == pygame.K_DOWN:
                        self.mover_robot("abajo")
                    elif evento.key == pygame.K_LEFT:
                        self.mover_robot("izquierda")
                    elif evento.key == pygame.K_RIGHT:
                        self.mover_robot("derecha")
            pygame.display.flip()
            self.reloj.tick(10)
        pygame.quit()
import pygame
from laberinto import Laberinto
from juego_robot import JuegoRobot

def main():
    pygame.init()
    laberinto = Laberinto(ancho=600, alto=600, tamano_celda=15)
    juego = JuegoRobot(laberinto)
    juego.ejecutar()

if __name__ == "__main__":
    main()

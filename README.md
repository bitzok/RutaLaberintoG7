# AUTOMATIZACIÓN DE LABERINTOS - GRUPO 7

Este proyecto, **Automatización de Laberintos**, ha sido desarrollado como parte de la asignatura de AUTOMATIZACIÓN Y CONFIGURACIÓN DE SOFTWARE a cargo de la profesora ROSAS CUEVA YESSICA en la UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS. El objetivo de este proyecto es construir un sistema que permita la generación y resolución automática de laberintos, explorando algoritmos de generación y búsqueda en estructuras de laberintos.

## Integrantes del Equipo

- **Ames Camayo, Daniel Ames**
- **Cjumo Chumbes, Jose Carlos**
- **Ortiz Quispe, Akcel Eduardo**
- **Ramirez Alvarado, Piero Jaime**
- **Santa Cruz Pachas, Edward Grover**

## Descripción del Proyecto

El objetivo principal de este proyecto es resolver el problema clásico de navegación en laberintos mediante algoritmos genéticos. Simulamos a un robot que busca la mejor ruta para salir del laberinto, evaluando la factibilidad de cada ruta en función de la longitud del camino, la cantidad de giros y los obstáculos presentes. 

### Características

- **Definición del Laberinto**: Representación en cuadrícula con celdas que especifican posiciones libres y obstáculos.
- **Algoritmo Genético para Planificación de Rutas**:
  - **Genotipo**: Estructura de caminos posibles en una cuadrícula de filas y columnas.
  - **Función de Fitness**: Evalúa la calidad de cada camino en función de su longitud, la factibilidad (evitación de obstáculos) y la cantidad de giros.
  - **Operadores Genéticos**: Se utilizan operadores de selección, cruce y mutación para mejorar sucesivamente las rutas generadas.
- **Análisis de Resultados**: Evolución de la ruta óptima a través de las generaciones y observación de la eficiencia de los operadores genéticos en laberintos complejos.
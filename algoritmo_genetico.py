import random

class GeneticAlgorithm:
    def __init__(self, maze, start_pos, end_pos, population_size=200, mutation_rate=0.04, max_generations=1000):
        """
        Inicializa el algoritmo genético con los parámetros necesarios.
        
        Precondiciones:
            - maze: matriz de enteros, donde 0 representa caminos libres y 1 paredes.
            - start_pos: tupla con la posición inicial del robot (x, y).
            - end_pos: tupla con la posición objetivo (x, y).
            - population_size: tamaño de la población de rutas (opcional).
            - mutation_rate: tasa de mutación de las rutas (opcional).
            - max_generations: número máximo de generaciones para la evolución (opcional).

        Poscondiciones:
            - Se inicializa una población aleatoria de rutas.
        """
        self.maze = maze
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.path_length = 3000  # Longitud máxima de cada ruta
        self.population = self.initialize_population()

    def initialize_population(self):
        """
        Inicializa la población de rutas de forma aleatoria.
        
        Poscondiciones:
            - Devuelve una lista de rutas, cada una de las cuales es una lista de movimientos aleatorios.
        """
        return [self.random_path() for _ in range(self.population_size)]

    def random_path(self):
        """
        Genera una ruta aleatoria.
        
        Poscondiciones:
            - Devuelve una lista de movimientos aleatorios (direcciones).
        """
        return [random.choice(["up", "down", "left", "right"]) for _ in range(self.path_length)]

    def fitness(self, path):
        """
        Calcula el valor de aptitud (fitness) de una ruta dada.
        
        Precondiciones:
            - path: lista de movimientos (direcciones) que representa una ruta.
        
        Poscondiciones:
            - Devuelve un valor de aptitud basado en la distancia al objetivo.
            - Si la ruta llega al objetivo, devuelve 'inf' como aptitud máxima.
        """
        x, y = self.start_pos
        for move in path:
            if move == "up" and x > 0 and self.maze[x - 1][y] == 0:
                x -= 1
            elif move == "down" and x < len(self.maze) - 1 and self.maze[x + 1][y] == 0:
                x += 1
            elif move == "left" and y > 0 and self.maze[x][y - 1] == 0:
                y -= 1
            elif move == "right" and y < len(self.maze[0]) - 1 and self.maze[x][y + 1] == 0:
                y += 1

            if (x, y) == self.end_pos:
                return float('inf')  # Máxima aptitud si se alcanza el objetivo

        # Distancia Manhattan como penalización si no se alcanza el objetivo
        distance = abs(x - self.end_pos[0]) + abs(y - self.end_pos[1])
        return 1 / (1 + distance)

    def selection(self):
        """
        Selecciona a los mejores individuos (rutas) de la población.
        
        Poscondiciones:
            - La población se reduce a la mitad, reteniendo a los individuos con mayor aptitud.
        """
        weighted_population = [(self.fitness(individual), individual) for individual in self.population]
        weighted_population.sort(reverse=True, key=lambda x: x[0])
        self.population = [ind for _, ind in weighted_population[:self.population_size // 2]]

    def crossover(self, parent1, parent2):
        """
        Realiza el cruce entre dos rutas (individuos).
        
        Precondiciones:
            - parent1 y parent2: listas de movimientos (direcciones).
        
        Poscondiciones:
            - Devuelve una nueva ruta resultante del cruce de los padres.
        """
        split = random.randint(1, len(parent1) - 1)
        return parent1[:split] + parent2[split:]

    def mutate(self, path):
        """
        Realiza la mutación en una ruta con una probabilidad dada.
        
        Precondiciones:
            - path: lista de movimientos (direcciones).
        
        Poscondiciones:
            - Devuelve la ruta modificada después de aplicar la mutación.
        """
        for i in range(len(path)):
            if random.random() < self.mutation_rate:
                path[i] = random.choice(["up", "down", "left", "right"])
        return path

    def evolve(self):
        """
        Ejecuta el proceso de evolución hasta alcanzar la generación máxima o el objetivo.
        
        Poscondiciones:
            - Devuelve la mejor ruta encontrada o una ruta que alcanza el objetivo.
        """
        for generation in range(self.max_generations):
            self.selection()
            next_generation = []

            while len(next_generation) < self.population_size:
                parent1, parent2 = random.sample(self.population, 2)
                child = self.crossover(parent1, parent2)
                child = self.mutate(child)
                next_generation.append(child)

            self.population = next_generation

            best_path = max(self.population, key=self.fitness)
            if self.fitness(best_path) == float('inf'):
                print(f"Objetivo alcanzado en generación {generation}")
                return best_path

        return max(self.population, key=self.fitness)

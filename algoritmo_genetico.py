import random


class GeneticAlgorithm:
    def __init__(self, maze, start_pos, end_pos, population_size=200, mutation_rate=0.05, max_generations=1000):
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
        self.path_length = 1000  # Longitud máxima de cada ruta
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
        distance_traveled = 0
        turns = 0
        last_move = None

        for move in path:
            if move == "up" and x > 0 and self.maze[x - 1][y] == 0:
                x -= 1
            elif move == "down" and x < len(self.maze) - 1 and self.maze[x + 1][y] == 0:
                x += 1
            elif move == "left" and y > 0 and self.maze[x][y - 1] == 0:
                y -= 1
            elif move == "right" and y < len(self.maze[0]) - 1 and self.maze[x][y + 1] == 0:
                y += 1

            distance_traveled += 1
            if last_move and last_move != move:
                turns += 1
            last_move = move

        # console log
        if (x, y) == self.end_pos:
            print(f"Objetivo alcanzado en la posición ({x}, {y}) con pasos: {distance_traveled}")
            return float('inf')  # Solo retornar inf si realmente se alcanza el objetivo

        manhattan_distance = abs(x - self.end_pos[0]) + abs(y - self.end_pos[1])
        return 1 / (1 + distance_traveled + turns * 2 + manhattan_distance * 5)

    def selection(self):
        """
        Selecciona a los mejores individuos (rutas) de la población.

        Poscondiciones:
            - La población se reduce a la mitad, reteniendo a los individuos con mayor aptitud.
        """
        weighted_population = sorted([(self.fitness(ind), ind) for ind in self.population], reverse=True)
        return [ind for _, ind in weighted_population[:self.population_size // 2]]

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
        return [random.choice(["up", "down", "left", "right"]) if random.random() < self.mutation_rate else step for
                step in path]

    def evolve(self):
        """
        Ejecuta el proceso de evolución hasta alcanzar la generación máxima o el objetivo.

        Poscondiciones:
            - Devuelve la mejor ruta encontrada o una ruta que alcanza el objetivo.
        """
        for generation in range(self.max_generations):
            selected = self.selection()
            next_gen = []
            num_crossovers = 0
            num_mutations = 0

            while len(next_gen) < self.population_size:
                parent1, parent2 = random.sample(selected, 2)
                child = self.crossover(parent1, parent2)
                num_crossovers += 1
                mutated_child = self.mutate(child)
                num_mutations += sum(1 for i in range(len(child)) if child[i] != mutated_child[i])
                next_gen.append(mutated_child)

            self.population = next_gen
            best_path = max(self.population, key=self.fitness)
            best_fitness = self.fitness(best_path)

            if best_fitness == float('inf'):
                distance_to_goal = 0
            else:
                x, y = self.start_pos
                for move in best_path:
                    if move == "up" and x > 0 and self.maze[x - 1][y] == 0:
                        x -= 1
                    elif move == "down" and x < len(self.maze) - 1 and self.maze[x + 1][y] == 0:
                        x += 1
                    elif move == "left" and y > 0 and self.maze[x][y - 1] == 0:
                        y -= 1
                    elif move == "right" and y < len(self.maze[0]) - 1 and self.maze[x][y + 1] == 0:
                        y += 1
                distance_to_goal = abs(x - self.end_pos[0]) + abs(y - self.end_pos[1])

            # console log
            print(f"Generación {generation + 1}:")
            print(f"  Mejor fitness: {best_fitness}")
            print(f"  Pasos del mejor camino: {len(best_path)}")
            print(f"  Distancia restante al objetivo: {distance_to_goal}")
            print(f"  Cruces realizados: {num_crossovers}, Mutaciones realizadas: {num_mutations}\n")

            if best_fitness == float('inf'):
                print(f"Objetivo alcanzado en generación {generation + 1} con el camino óptimo.")
                return best_path

        return max(self.population, key=self.fitness)
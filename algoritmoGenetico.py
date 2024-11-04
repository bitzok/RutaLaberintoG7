import random

class GeneticAlgorithm:
    def __init__(self, maze, start_pos, end_pos, population_size=200, mutation_rate=0.04, max_generations=1000):
        self.maze = maze
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.path_length = 1000
        self.population = self.initialize_population()

    def initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = self.random_path()
            population.append(individual)
        return population

    def random_path(self):
        return [random.choice(["up", "down", "left", "right"]) for _ in range(self.path_length)]

    def fitness(self, path):
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
                return float('inf')

        distance = abs(x - self.end_pos[0]) + abs(y - self.end_pos[1])
        return 1 / (1 + distance)

    def selection(self):
        weighted_population = [(self.fitness(individual), individual) for individual in self.population]
        weighted_population.sort(reverse=True, key=lambda x: x[0])
        self.population = [ind for _, ind in weighted_population[:self.population_size // 2]]

    def crossover(self, parent1, parent2):
        split = random.randint(1, len(parent1) - 1)
        return parent1[:split] + parent2[split:]

    def mutate(self, path):
        for i in range(len(path)):
            if random.random() < self.mutation_rate:
                path[i] = random.choice(["up", "down", "left", "right"])
        return path

    def evolve(self):
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

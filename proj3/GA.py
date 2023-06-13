import random
import pandas as pd
import numpy as np
from deap import algorithms, base, creator, tools

# Load the distance matrix from an Excel file
dist_df = pd.read_excel("../Project3_DistancesMatrix.xlsx", sheet_name="Sheet1", index_col=0)
# Path:  [0, 43, 82, 79, 18, 53, 75, 73, 83, 86, 94, 95, 5, 40, 54, 9, 7, 46, 6, 59, 20, 41, 63, 66, 61, 26, 25, 68,
# 48, 47, 49, 29, 15, 90, 78, 74, 51, 39, 91, 36, 85, 69, 62, 92, 31, 70, 16, 52, 23, 89, 19, 65, 10, 11, 84, 72, 12,
# 30, 60, 1, 37, 35, 80, 21, 33, 81, 28, 55, 2, 96, 27, 76, 77, 64, 87, 58, 57, 45, 17, 34, 22, 4, 71, 99, 97, 32,
# 88, 8, 50, 42, 38, 93, 24, 56, 13, 44, 98, 3, 14, 67, 0]
# Fitness:  94.00000000000003
distance_matrix = dist_df.to_numpy()

creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
# Attribute generator
toolbox.register("indices", random.sample, range(0, len(distance_matrix)), len(distance_matrix))
# Structure initializers
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.indices)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)


# Define the fitness function
def fitness(path):
    # Remove 0 from middle of path
    a = list(path)
    a.remove(0)
    # Calculate the sum of distances between consecutive positions
    dist = 0
    for i in range(len(a) - 1):
        dist += distance_matrix[a[i]][a[i + 1]]

    dist += distance_matrix[0][a[0]] + distance_matrix[a[-1]][0]
    return dist,


toolbox.register("evaluate", fitness)
toolbox.register("mate", tools.cxOrdered)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.1)
toolbox.register("select", tools.selTournament, tournsize=3)

if __name__ == "__main__":
    # random.seed(42)
    # Initialize the population
    pop = toolbox.population(n=300)

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB, NGEN = 0.5, 0.2, 10000

    # Run the GA
    for g in range(NGEN):
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        # Replace the old population with the offspring
        pop[:] = offspring

    # Sort the population by fitness
    pop = sorted(pop, key=lambda ind: ind.fitness.values)

    best_individual = [0] + [item for item in pop[0] if item != 0] + [0]
    # Print the best individual (path)
    print("Path: ", best_individual)
    print("Fitness: ", pop[0].fitness.values[0])

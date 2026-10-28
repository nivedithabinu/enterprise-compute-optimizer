import numpy as np 
import pandas as pd 

# Loading the static dataset that was engineered in Week 1
load = pd.read_csv('../data/mac_performance.csv')

costs = load['estimated_market_price'].to_numpy()
scores = load['geekbench6_multi_core'].to_numpy()

# We will now use 2D NumPy arrays to represent the population of hardware fleets, completely avoiding hash maps or Python dictionaries
# Rows = individual fleets
# Columns = quantity of each Mac model
def initializePopulation(popSize, numGenes, maxQuantity_per_mac=5):
    return np.random.randint(0, maxQuantity_per_mac, size=(popSize, numGenes))

def calculateFitness(population, costs, scores, budget):
    # Total Cost + Total Score via Matrix Multiplication
    totalCosts = np.dot(population, costs)
    totalScores = np.dot(population, scores)
    
    # Business Constraint: zero out fitness if the fleet exceeds the budget
    validMask = totalCosts <= budget
    return totalScores*validMask

def selection(population, fitnessScores):
    populationSize = len(population)
    tournaments = np.random.randint(0, populationSize, size=(populationSize,2))
    tournamentFitness = fitnessScores[tournaments]
    
    # Finding the winner of each tournament and returning the selected parents
    best_indices = tournaments[np.arange(populationSize), np.argmax(tournamentFitness, axis=1)]
    return population[best_indices]

def crossover(parents, crossover_rate=0.8):
    populationSize, numGenes = parents.shape
    children = parents.copy()
    
    for i in range(0, populationSize, 2):
        if i+1 < populationSize and np.random.rand() < crossover_rate:
            crossoverPoint = np.random.randint(1, numGenes)
            
            # Swap the arrays beyond the crossover point
            children[i, crossoverPoint:] = parents[i+1, crossoverPoint:]
            children[i+1, crossoverPoint:] = parents[i, crossoverPoint:]
    return children

def mutation(children, mutation_rate=0.05, maxQuantity_per_mac=3):
    mask = np.random.rand(*children.shape) < mutation_rate
    random_genes = np.random.randint(0, maxQuantity_per_mac, size=children.shape)
    children[mask] = random_genes[mask]
    return children
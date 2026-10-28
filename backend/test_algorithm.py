import numpy as np 
import pandas as pd 

from genetic_algorithm import initializePopulation, calculateFitness, selection, crossover, mutation

# 1. Loading the exact data
load = pd.read_csv('../data/mac_performance.csv')

costs = load['estimated_market_price'].to_numpy()
scores = load['geekbench6_multi_core'].to_numpy()

numGenes = len(costs)

# 2. Defining test constraints
budget = 15000
popSize = 500
generations = 100

print(f"--- Starting {generations}-Generation Optimization ---")
population = initializePopulation(popSize, numGenes, maxQuantity_per_mac=3)

best_overall_score = 0
best_overall_cost = 0

for i in range(generations):
    fitnessScores = calculateFitness(population, costs, scores, budget)
    
    # Track the best performing valid fleet
    current_best_idx = np.argmax(fitnessScores)
    current_best_score = fitnessScores[current_best_idx]
    
    if current_best_score>best_overall_score:
        best_overall_score = current_best_score
        best_overall_cost = np.dot(population[current_best_idx], costs)
        print(f"Generation {i+1}: New Best Score = {best_overall_score:,.0f} | Cost: ${best_overall_cost:,.2f}")
        
    # Evolve to the next generation using pure matrix operations
    parents = selection(population, fitnessScores)
    children = crossover(parents, crossover_rate=0.8)
    population = mutation(children, mutation_rate=0.05, maxQuantity_per_mac=3)

print("\n--- Optimization Complete ---")
print(f"Final Optimal Compute Score: {best_overall_score:,.0f}")
print(f"Total Budget Used: ${best_overall_cost:,.2f} / ${budget:,.2f}")
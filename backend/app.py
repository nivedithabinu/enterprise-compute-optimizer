import numpy as np 
import pandas as pd 

from flask import Flask, request, jsonify
from genetic_algorithm import initializePopulation, calculateFitness, selection, crossover, mutation

app = Flask(__name__)

# Loading static data into memory
load = pd.read_csv('../data/mac_performance.csv')

costs = load['estimated_market_price'].to_numpy()
scores = load['geekbench6_multi_core'].to_numpy()

numGenes = len(costs)

@app.route('/optimize', methods=['POST'])
def optimizeFleet():
    # Receive constraints from the frontend
    payload = request.json
    budget = payload.get('budget', 15000)
    
    popSize = 100
    generations = 100
    
    population = initializePopulation(popSize, numGenes, maxQuantity_per_mac=3)
    
    best_overall_score = 0
    best_overall_cost = 0
    best_fleet = None
    
    for _ in range(generations):
        fitnessScores = calculateFitness(population, costs, scores, budget)
        
        current_best_idx = np.argmax(fitnessScores)
        current_best_score = fitnessScores[current_best_idx]
        
        if current_best_score>current_best_idx:
            best_overall_score = float(current_best_score)
            best_overall_cost = float(np.dot(population[current_best_idx],costs))
            best_fleet = population[current_best_idx].tolist()
        
        parents = selection(population,fitnessScores)
        children = crossover(parents,crossover_rate=0.8)
        population = mutation(children, mutation_rate=0.05, maxQuantity_per_mac=3)
    
    return jsonify(
        {
            'optimal_score': best_overall_score,
            'total_cost': best_overall_cost,
            'fleet_configuration': best_fleet
        }
    )

if __name__ == '__main__':
    app.run(port=5000, debug=True)
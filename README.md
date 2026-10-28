# Enterprise Compute Optimizer 💻⚙️

An open-source full-stack machine learning and data science pipeline that utilizes a custom genetic algorithm to determine the optimal fleet of Apple Mac computers for enterprise environments. The optimization engine maximizes total Geekbench computational performance while strictly adhering to a user-defined financial budget constraint.

This project bridges the gap between raw algorithmic data science and accessible full-stack software engineering, providing a responsive interface for complex matrix-based computations.

## 🚀 Key Features
* **Custom Genetic Algorithm:** Engineered a high-performance evolutionary algorithm using pure NumPy operations (crossover, mutation, and tournament selection) without relying on heavy external ML libraries.
* **RESTful Backend Architecture:** Designed a lightweight Python/Flask server to process optimization parameters and serve JSON payloads directly to the frontend.
* **Modern React UI:** Built a blazing-fast single-page application using Vite and React, styled seamlessly with Tailwind CSS v4 for a responsive, dark-mode data dashboard.
* **Data-Driven Insights:** Leverages a Kaggle dataset (`mac_performance.csv`) to parse real-world market pricing and Geekbench multi-core metrics.
* **CORS-Free Proxy Routing:** Configured Vite's internal server proxy to securely route API requests to the Flask backend without exposing ports or requiring external API keys.

## 🛠️ Technology Stack

**Frontend**
* React.js (Vite)
* Tailwind CSS v4
* JavaScript (ES6+)

**Backend & Data Science**
* Python 3
* Flask (REST API)
* NumPy (Matrix Operations & Evolutionary Logic)
* Pandas (Dataset Processing)

## 🧠 Algorithmic Approach

The core engine relies on a genetic algorithm simulating natural selection to solve a bounded knapsack-style optimization problem:

1. **Initialization:** A population of random fleet arrays is generated. Each array index represents a specific Mac model, and the integer value represents the quantity to purchase.
2. **Fitness Function:** The algorithm evaluates each fleet by calculating: `Total Score = Σ (Geekbench Score_i * Quantity_i)`.
3. **Budget Constraint:** Any fleet where `Total Cost = Σ (Market Price_i * Quantity_i) > Budget` is heavily penalized or discarded.
4. **Evolution:** The population undergoes Tournament Selection, Uniform Crossover, and Random Mutation across 100 generations to mathematically converge on the highest performing hardware configuration.

## 🔌 API Reference

### `POST /optimize`
Calculates the optimal fleet configuration based on the provided financial constraint.

**Request Body:**
```json
{
  "budget": 20000
}

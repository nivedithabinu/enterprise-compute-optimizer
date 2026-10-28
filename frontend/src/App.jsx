import { useState } from 'react'

export default function App() {
  const [budget, setBudget] = useState(20000)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState(null)

  const handleOptimize = async (e) => {
    e.preventDefault()
    setLoading(true)
    
    try {
      const response = await fetch('/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ budget: Number(budget) })
      })

      const data = await response.json()
      setResults(data)
    }

    catch (error) {
      console.error("Optimization failed:", error)
    } 
    
    finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 p-8 font-sans">
      <div className="max-w-4xl mx-auto space-y-8">
        <header className="border-b border-gray-800 pb-4">
          <h1 className="text-3xl font-bold text-blue-400">Enterprise Compute Optimizer</h1>
          <p className="text-gray-400 mt-2">Genetic algorithm fleet selection utilizing pure NumPy</p>
        </header>
        <form onSubmit={handleOptimize} className="bg-gray-900 p-6 rounded-lg border border-gray-800 flex gap-4 items-end">
          <div className="flex-1">
            <label className="block text-sm font-medium text-gray-400 mb-2">Total Budget ($)</label>
            <input type="number" value={budget} onChange={(e) => setBudget(e.target.value)} className="w-full bg-gray-950 border border-gray-700 rounded p-3 text-white focus:outline-none focus:border-blue-500" required/>
          </div>
          <button type="submit" disabled={loading} className="bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 px-8 rounded transition-colors disabled:opacity-50">
            {loading ? 'Evolving Fleet...' : 'Optimize Compute'}
          </button>
        </form>

        {results && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-gray-900 p-6 rounded-lg border border-gray-800">
              <h2 className="text-xl font-semibold mb-4 text-emerald-400">Performance Metrics</h2>
              <div className="space-y-4">
                <div>
                  <p className="text-gray-400 text-sm">Optimal Geekbench Score</p>
                  <p className="text-3xl font-bold">{results.optimal_score.toLocaleString()}</p>
                </div>
                <div>
                  <p className="text-gray-400 text-sm">Total Fleet Cost</p>
                  <p className="text-3xl font-bold">${results.total_cost.toLocaleString()}</p>
                </div>
              </div>
            </div>

            <div className="bg-gray-900 p-6 rounded-lg border border-gray-800">
              <h2 className="text-xl font-semibold mb-4 text-blue-400">Fleet Distribution</h2>
              <div className="h-48 overflow-y-auto pr-2 text-sm text-gray-300">
                <p>Raw Quantity Array (Index = Mac Model ID):</p>
                <div className="bg-gray-950 p-4 rounded mt-2 font-mono break-words border border-gray-800">
                  [{results.fleet_configuration.join(', ')}]
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
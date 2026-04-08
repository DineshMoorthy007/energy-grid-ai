import React, { useState, useEffect, useCallback } from 'react';
import { predictDemand } from '../services/api';
import MetricsCard from './MetricsCard';
import DemandChart from './DemandChart';
import GridVisualizer from './GridVisualizer';

const Dashboard = () => {
  // State
  const [hour, setHour] = useState(12);
  const [temperature, setTemperature] = useState(25);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);
  const [isAutoRefresh, setIsAutoRefresh] = useState(false);

  // Fetch data function
  const fetchData = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await predictDemand(hour, temperature);
      setData({ ...result, hour, temperature }); // Attach current inputs for charts
    } catch (err) {
      setError("Failed to connect to backend AI & Quantum engine.");
    } finally {
      setLoading(false);
    }
  }, [hour, temperature]);

  // Initial fetch and auto-refresh logic
  useEffect(() => {
    fetchData();
  }, [hour, temperature]); // Fetch when inputs change manually

  // Auto-refresh simulation
  useEffect(() => {
    let interval;
    if (isAutoRefresh) {
      interval = setInterval(() => {
        // Simulate real-time changes
        setHour((prev) => (prev + 1) % 24);
        setTemperature((prev) => {
           const change = (Math.random() * 4) - 2;
           const newTemp = prev + change;
           return Math.max(-10, Math.min(40, newTemp)); // restrict range
        });
      }, 5000);
    }
    return () => clearInterval(interval);
  }, [isAutoRefresh]);

  // UI Helpers
  const getActionColor = (action) => {
    switch (action) {
      case 'NORMAL': return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
      case 'OPTIMIZED': return 'text-sky-400 border-sky-500/30 bg-sky-500/10';
      case 'CRITICAL': return 'text-rose-400 border-rose-500/30 bg-rose-500/10';
      case 'LOW_DEMAND': return 'text-purple-400 border-purple-500/30 bg-purple-500/10';
      default: return 'text-slate-400 border-slate-500/30 bg-slate-500/10';
    }
  };

  return (
    <div className="space-y-6">
      {/* Controls & Metrics Row */}
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Control Panel */}
        <div className="lg:col-span-1 border border-slate-800 bg-slate-900/40 rounded-2xl p-6 shadow-lg backdrop-blur-sm">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-lg font-semibold text-slate-200">Simulation Controls</h2>
            <button 
              onClick={() => setIsAutoRefresh(!isAutoRefresh)}
              className={`px-3 py-1 rounded-full text-xs font-medium transition-colors ${
                isAutoRefresh 
                ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/50' 
                : 'bg-slate-800 text-slate-400 border border-slate-700 hover:bg-slate-700'
              }`}
            >
              {isAutoRefresh ? 'Auto-pilot ON' : 'Auto-pilot OFF'}
            </button>
          </div>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-2">
                <label className="text-sm font-medium text-slate-400">Time of Day (Hour)</label>
                <span className="text-sm font-bold text-cyan-400">{hour}:00</span>
              </div>
              <input 
                type="range" 
                min="0" max="23" 
                value={hour} 
                onChange={(e) => {
                  setHour(parseInt(e.target.value));
                  setIsAutoRefresh(false);
                }}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
              />
            </div>
            
            <div>
              <div className="flex justify-between mb-2">
                <label className="text-sm font-medium text-slate-400">Temperature (°C)</label>
                <span className="text-sm font-bold text-rose-400">{temperature.toFixed(1)}°</span>
              </div>
              <input 
                type="range" 
                min="-10" max="40" step="0.5"
                value={temperature} 
                onChange={(e) => {
                  setTemperature(parseFloat(e.target.value));
                  setIsAutoRefresh(false);
                }}
                className="w-full h-2 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-rose-400"
              />
            </div>

            <button
              onClick={fetchData}
              disabled={loading}
              className="w-full py-3 rounded-lg bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white font-medium transition-all shadow-lg shadow-blue-500/25 active:scale-95 flex justify-center items-center"
            >
              {loading ? (
                <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
              ) : (
                "Run Prediction & Optimization"
              )}
            </button>
          </div>
        </div>

        {/* Metrics */}
        <div className="lg:col-span-3 grid grid-cols-1 md:grid-cols-3 gap-6">
          <MetricsCard 
            title="Predicted AI Demand" 
            value={data ? data.predicted_demand : '---'} 
            unit="MW"
            icon={
              <svg className="w-12 h-12 text-cyan-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
            }
          />
          <MetricsCard 
            title="Grid Status" 
            value={data ? data.grid_status : '---'} 
            unit=""
            colorClass={data ? (data.grid_status.includes('CRITICAL') ? 'from-rose-900 to-slate-900 border-rose-500/50' : 'from-slate-800 to-slate-900') : "from-slate-800 to-slate-900"}
            icon={
              <svg className="w-12 h-12 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
              </svg>
            }
          />
          <MetricsCard 
            title="Overloaded Nodes (Post-Opt)" 
            value={data?.grid_state ? data.grid_state.nodes.filter(n => n.overloaded).length : '---'} 
            unit=""
            icon={
              <svg className="w-12 h-12 text-amber-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
            }
          />
        </div>
      </div>

      {/* Error State */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/50 text-rose-400 flex items-start gap-3">
          <svg className="w-5 h-5 flex-shrink-0 mt-0.5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <p>{error}</p>
        </div>
      )}

      {/* Main Visuals Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Graph & Explanation */}
        <div className="lg:col-span-2 space-y-6">
          <div className="border border-slate-800 bg-slate-900/40 rounded-2xl p-6 shadow-lg backdrop-blur-sm relative h-[500px] flex flex-col">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-semibold text-slate-200">Quantum Grid Topology Optimization</h2>
              {data && (
                <div className={`px-3 py-1 rounded-full text-xs font-medium border ${getActionColor(data.action)}`}>
                  {data.action}
                </div>
              )}
            </div>
            
            <div className="flex-1 bg-slate-950/50 rounded-xl overflow-hidden border border-slate-800/50 relative">
              {loading && !data && (
                <div className="absolute inset-0 z-10 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center">
                   <div className="w-8 h-8 rounded-full border-t-2 border-r-2 border-cyan-400 animate-spin"></div>
                </div>
              )}
              {data?.grid_state && (
                <GridVisualizer gridData={data.grid_state} />
              )}
            </div>
          </div>
        </div>

        {/* AI Explanation & Demand Chart */}
        <div className="lg:col-span-1 space-y-6">
          {/* AI Explanation & Recommendation */}
          <div className="border border-slate-800 bg-slate-900/40 rounded-2xl p-6 shadow-lg backdrop-blur-sm">
            <h2 className="text-lg font-semibold text-slate-200 mb-4 flex items-center gap-2">
              <svg className="w-5 h-5 text-indigo-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              AI Engine Explanation
            </h2>
            <div className="bg-slate-950/50 rounded-xl p-4 border border-slate-800/50 text-slate-300 text-sm leading-relaxed mb-4 min-h-[80px]">
              {loading ? (
                <div className="flex items-center gap-3 text-slate-500 animate-pulse">
                  <div className="w-4 h-4 rounded-full border-2 border-slate-600 border-t-indigo-500 animate-spin"></div>
                  Quantum analysis in progress...
                </div>
              ) : (
                data ? data.explanation : "Awaiting data input to run AI models and Quantum optimization."
              )}
            </div>

            <h3 className="text-sm font-semibold text-slate-400 mb-2 mt-4 flex items-center gap-2">
              <svg className="w-4 h-4 text-emerald-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              Recommendation
            </h3>
            <div className="bg-emerald-900/20 rounded-xl p-3 border border-emerald-500/30 text-emerald-300/90 text-sm">
              {data ? data.recommendation : "---"}
            </div>
          </div>

          {/* Demand Chart */}
          <div className="border border-slate-800 bg-slate-900/40 rounded-2xl p-6 shadow-lg backdrop-blur-sm">
            <h2 className="text-lg font-semibold text-slate-200 mb-4">Demand Forecast</h2>
            <DemandChart data={data} />
          </div>
          
          {/* Quantum states debugging */}
          {data?.optimized_routes && (
             <div className="border border-slate-800 bg-slate-900/40 rounded-2xl p-6 shadow-lg backdrop-blur-sm">
              <h2 className="text-sm font-semibold text-slate-400 mb-2 font-mono flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-fuchsia-500"></span>
                Qubit Vector Details
              </h2>
              <div className="flex flex-wrap gap-2">
                {data.optimized_routes.map((route) => (
                  <span key={route.route_id} className={`px-2 py-1 text-xs font-mono rounded ${route.quantum_state === 1 ? 'bg-fuchsia-500/20 text-fuchsia-300 border border-fuchsia-500/50' : 'bg-slate-800 text-slate-400 border border-slate-700'}`}>
                    Q{route.route_id}: {route.quantum_state}
                  </span>
                ))}
              </div>
             </div>
          )}

        </div>
      </div>
    </div>
  );
};

export default Dashboard;

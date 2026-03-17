import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Area, AreaChart } from 'recharts';

const DemandChart = ({ data }) => {
  // Generate a mock 24h curve based on the current data point for visualization
  // In a real app, this would come from historical/forecast API endpoints
  const chartData = Array.from({ length: 24 }).map((_, i) => {
    let baseLoad = 40 + (Math.sin((i - 6) * Math.PI / 12) + 1) * 20;
    
    // If it's the currently predicted hour, use the actual data
    if (i === data?.hour) {
      return {
        hour: `${i}:00`,
        demand: data.demand,
        isCurrent: true
      };
    }
    
    return {
      hour: `${i}:00`,
      demand: baseLoad + (Math.random() * 5 - 2.5),
      isCurrent: false
    };
  });

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-slate-900 border border-slate-700 p-3 rounded-lg shadow-xl">
          <p className="text-slate-300 text-sm font-medium mb-1">{`Time: ${label}`}</p>
          <p className="text-cyan-400 font-bold">
            {`Demand: ${payload[0].value.toFixed(1)} MW`}
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="h-64 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
          <defs>
            <linearGradient id="colorDemand" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#22d3ee" stopOpacity={0.3}/>
              <stop offset="95%" stopColor="#22d3ee" stopOpacity={0}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
          <XAxis 
            dataKey="hour" 
            stroke="#94a3b8" 
            fontSize={12} 
            tickLine={false}
            axisLine={false}
            interval={3}
          />
          <YAxis 
            stroke="#94a3b8" 
            fontSize={12} 
            tickLine={false}
            axisLine={false}
            tickFormatter={(value) => `${value}`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Area 
            type="monotone" 
            dataKey="demand" 
            stroke="#22d3ee" 
            strokeWidth={2}
            fillOpacity={1} 
            fill="url(#colorDemand)" 
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};

export default DemandChart;

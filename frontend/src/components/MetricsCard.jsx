import React from 'react';

const MetricsCard = ({ title, value, unit, icon, trend, colorClass = "from-slate-800 to-slate-900" }) => {
  return (
    <div className={`relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-br ${colorClass} p-6 shadow-lg shadow-black/20`}>
      <div className="absolute top-0 right-0 p-4 opacity-10">
        {icon}
      </div>
      <h3 className="text-sm font-medium text-slate-400 mb-2">{title}</h3>
      <div className="flex items-baseline gap-2">
        <span className="text-3xl font-bold tracking-tight text-white">{value}</span>
        {unit && <span className="text-sm font-medium text-slate-500">{unit}</span>}
      </div>
      {trend && (
        <div className={`mt-2 flex items-center text-xs font-medium ${trend.isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
          {trend.isPositive ? (
            <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
            </svg>
          ) : (
            <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
            </svg>
          )}
          {trend.value}
        </div>
      )}
    </div>
  );
};

export default MetricsCard;

import React from 'react';

const MetricsCard = ({ title, value, unit, icon, trend, colorClass = "from-slate-800 to-slate-900" }) => {
  // Format strings like "REDISTRIBUTE_ENERGY" to "Redistribute Energy"
  const formattedValue = typeof value === 'string' 
    ? value.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ')
    : value;

  return (
    <div className={`relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-br ${colorClass} p-6 shadow-lg shadow-black/20 flex flex-col justify-between min-h-[160px]`}>
      <div className="absolute top-0 right-0 p-4 opacity-10">
        {icon}
      </div>
      <div className="flex flex-col">
        <h3 className="text-xs font-semibold text-slate-500 mb-2 uppercase tracking-widest">{title}</h3>
        <div className="flex items-baseline gap-2 flex-wrap">
          <span className={`font-extrabold tracking-tight text-white break-words ${
            typeof formattedValue === 'string' && formattedValue.length > 12 
              ? 'text-lg sm:text-xl' 
              : 'text-2xl sm:text-3xl'
          }`}>
            {formattedValue}
          </span>
          {unit && <span className="text-sm font-medium text-slate-500">{unit}</span>}
        </div>
      </div>
      {trend && (
        <div className={`mt-4 flex items-center text-xs font-medium ${trend.isPositive ? 'text-emerald-400' : 'text-rose-400'}`}>
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

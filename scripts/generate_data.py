import pandas as pd
import numpy as np
import os

def generate_synthetic_data(num_days=365, output_file="backend/data/synthetic_demand.csv"):
    # Ensure directory exists
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    np.random.seed(42)
    
    data = []
    
    for day in range(num_days):
        # Base daily temp varies between winter and summer roughly
        base_temp = np.random.uniform(5, 35) 
        
        for hour in range(24):
            # Hour temp varies: coldest at 4am, hottest at 2pm (14:00)
            temp_variation = -5 * np.cos((hour - 4) * np.pi / 12)
            temperature = base_temp + temp_variation
            
            # Base grid demand
            base_demand = 100.0
            
            # Peak hour boost 
            if 17 <= hour <= 22: # evening
                peak_boost = np.random.uniform(50, 80)
            elif 6 <= hour <= 9: # morning
                peak_boost = np.random.uniform(20, 40)
            elif 0 <= hour <= 5: # night low
                peak_boost = np.random.uniform(-40, -10)
            else: # daytime normal
                peak_boost = np.random.uniform(0, 15)
                
            # Temperature factor: high AC usage in heat, high heating in cold
            temp_factor = 0
            if temperature > 25:
                temp_factor = (temperature - 25) * 5.5
            elif temperature < 15:
                temp_factor = (15 - temperature) * 3.0
                
            # Add some random noise for realism
            noise = np.random.normal(0, 5)
            
            demand = base_demand + peak_boost + temp_factor + noise
            
            data.append({
                "hour": hour,
                "temperature": round(temperature, 2),
                "demand": round(demand, 2)
            })
            
    df = pd.DataFrame(data)
    df.to_csv(output_file, index=False)
    print(f"Generated {len(df)} synthetic data records at {output_file}")
    return df

if __name__ == "__main__":
    generate_synthetic_data()

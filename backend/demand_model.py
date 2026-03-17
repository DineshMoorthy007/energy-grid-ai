import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

class DemandPredictor:
    def __init__(self):
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self._train_model()

    def _generate_synthetic_data(self):
        # Generate synthetic data for training
        np.random.seed(42)
        # 1000 samples
        hours = np.random.randint(0, 24, 1000)
        # Temperature from -10 to 40 Celsius
        temperatures = np.random.uniform(-10, 40, 1000)
        
        # Base demand pattern: higher during day (hours 8-20), lower at night
        # Temperature effect: high demand when very hot (AC) or very cold (heating)
        demand = 50 + \
                 (np.sin(hours * np.pi / 12 - np.pi/2) + 1) * 30 + \
                 (temperatures - 15)**2 * 0.1 + \
                 np.random.normal(0, 5, 1000)
        
        df = pd.DataFrame({
            'hour': hours,
            'temperature': temperatures,
            'demand': demand
        })
        return df

    def _train_model(self):
        df = self._generate_synthetic_data()
        X = df[['hour', 'temperature']]
        y = df['demand']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        self.model.fit(X_train, y_train)
        
        # We could print the score here, but for this app we just need the model ready
        # print(f"Model R^2 Score: {self.model.score(X_test, y_test)}")

    def predict_demand(self, hour: int, temperature: float) -> float:
        """
        Predicts total energy demand for a given hour and temperature.
        """
        prediction = self.model.predict([[hour, temperature]])
        return float(prediction[0])

# Singleton instance for the app to use
demand_model = DemandPredictor()

def predict_demand(hour: int, temperature: float) -> float:
    return demand_model.predict_demand(hour, temperature)

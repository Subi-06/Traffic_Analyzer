import joblib
import os
import numpy as np

import pandas as pd

class TrafficPredictor:
    def __init__(self, model_path='ai_model/congestion_model.pkl'):
        self.model_path = model_path
        self.model = None
        self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            self.model = joblib.load(self.model_path)
            print("AI Model loaded successfully.")
        else:
            print(f"Warning: Model not found at {self.model_path}")

    def predict(self, traffic, latency, bandwidth, packet_loss):
        if self.model is None:
            return 0
        
        # Create DataFrame to match training feature names
        features = pd.DataFrame([{
            'traffic': traffic,
            'latency': latency,
            'bandwidth': bandwidth,
            'packet_loss': packet_loss
        }])
        return int(self.model.predict(features)[0])

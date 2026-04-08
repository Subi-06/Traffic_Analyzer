import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import os

class CongestionTrainer:
    def __init__(self, data_path='ai_model/network_traffic.csv'):
        self.data_path = data_path
        self.model = LogisticRegression()

    def train(self):
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset not found at {self.data_path}")

        df = pd.read_csv(self.data_path)
        X = df[['traffic', 'latency', 'bandwidth', 'packet_loss']]
        y = df['congestion']

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        
        predictions = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, predictions)
        print(f"Model Accuracy: {accuracy * 100:.2f}%")
        
        joblib.dump(self.model, 'ai_model/congestion_model.pkl')
        print("Model saved as ai_model/congestion_model.pkl")
        return accuracy

if __name__ == "__main__":
    trainer = CongestionTrainer()
    trainer.train()

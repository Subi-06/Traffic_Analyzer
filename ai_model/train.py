import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Bidirectional, Dropout
import os

def generate_synthetic_data(samples=1000, seq_length=10):
    # Features: packets_per_sec, latency, drop_rate
    X = np.random.rand(samples, seq_length, 3)
    y = np.zeros((samples, 1))
    
    for i in range(samples):
        # A simple relationship: higher packets and latency = higher congestion
        # Add some noise and patterns
        packets = X[i, :, 0].mean()
        latency = X[i, :, 1].mean()
        y[i] = min(1.0, (packets * 0.6 + latency * 0.4) + np.random.normal(0, 0.05))
    
    return X, y

def build_model(input_shape):
    model = Sequential([
        Bidirectional(LSTM(64, return_sequences=True), input_shape=input_shape),
        Dropout(0.2),
        Bidirectional(LSTM(32)),
        Dropout(0.2),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    return model

if __name__ == "__main__":
    X, y = generate_synthetic_data()
    model = build_model((X.shape[1], X.shape[2]))
    
    print("Training Bi-LSTM model...")
    model.fit(X, y, epochs=10, batch_size=32, validation_split=0.2)
    
    # Ensure the directory exists
    os.makedirs(os.path.dirname('ai_model/model.h5'), exist_ok=True)
    model.save('ai_model/model.h5')
    print("Model saved to ai_model/model.h5")

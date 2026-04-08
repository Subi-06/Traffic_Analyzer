import pandas as pd
import numpy as np
import os

def generate_csv(filepath='ai_model/network_traffic.csv', samples=2000):
    np.random.seed(42)
    
    # Features: traffic (0-100), latency (0-100ms), bandwidth (0-1000Mbps), packet_loss (0-10%)
    traffic = np.random.randint(0, 100, samples)
    latency = np.random.randint(0, 100, samples)
    bandwidth = np.random.randint(10, 1000, samples)
    packet_loss = np.random.uniform(0, 10, samples)
    
    # Target: Congestion (1 if conditions are poor, 0 otherwise)
    # Logic: if traffic > 80 or (latency > 60 and packet_loss > 5) or bandwidth < 100 and traffic > 50
    congestion = ((traffic > 80) | 
                  ((latency > 60) & (packet_loss > 5)) | 
                  ((bandwidth < 200) & (traffic > 60))).astype(int)
    
    df = pd.DataFrame({
        'traffic': traffic,
        'latency': latency,
        'bandwidth': bandwidth,
        'packet_loss': packet_loss,
        'congestion': congestion
    })
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    df.to_csv(filepath, index=False)
    print(f"Dataset generated at {filepath}")

if __name__ == "__main__":
    generate_csv()

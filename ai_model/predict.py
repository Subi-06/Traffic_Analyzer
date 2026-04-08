import tensorflow as tf
import numpy as np

import os

model = None

def load_ai_model(path=None):
    global model
    if path is None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'ai_model', 'model.h5')
    model = tf.keras.models.load_model(path)

def predict_congestion(data_sequence):
    # data_sequence: (seq_length, 3)
    if model is None:
        return 0.5
    
    input_data = np.expand_dims(data_sequence, axis=0)
    prediction = model.predict(input_data)
    return float(prediction[0][0])

import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
import re
import os
import asyncio
import tensorflow as tf
import logging
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
# Your TensorFlow code here

logging.getLogger('tensorflow').setLevel(logging.ERROR)

class ToxicityModel:
    def __init__(self, model_path):
        self.model_path = model_path
        self.model = None
        self.max_len = 100

    def load_model_async(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError(f"Model file not found: {self.model_path}")
        
        loop = asyncio.get_event_loop()
        self.model = loop.run_in_executor(None, load_model, self.model_path)

    def preprocess(self, text):
        text = re.sub(r'[^\w\s]', '', text)
        text = text.lower().split()
        text = ' '.join(text[:self.max_len])
        return text

    def predict(self, text):
        if self.model is None:
            raise ValueError("Model is not loaded. Please load the model before making predictions.")
        
        preprocessed_text = self.preprocess(text)
        input_text = tf.keras.preprocessing.sequence.pad_sequences(
            [preprocessed_text], maxlen=self.max_len)
        prediction = self.model.predict(input_text)
        return prediction[0] > 0.5

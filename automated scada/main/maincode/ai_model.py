# ai_model.py
import os
from data_acquisition import RaspberryPiSensor  
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score, StratifiedKFold
import pandas as pd
import joblib
import time
import logging

class AIModel:
    DEFAULT_DATASET_PATH = os.path.join(os.path.dirname(__file__), 'lol.csv')

    def __init__(self, dataset_path=None):
        self.sensor = RaspberryPiSensor()  
        self.logger = self._setup_logger()

        if dataset_path is None:
            dataset_path = self.DEFAULT_DATASET_PATH

        self._initialize_model()
        self._load_dataset(dataset_path)
        self._train_model()
        self._evaluate_model()

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def _acquire_sensor_data(self):
        try:
            sensor_data = self.sensor.read_sensor_data()
            if sensor_data:
                temperature, ph_level = map(float, sensor_data.split(','))  
                return temperature, ph_level
            else:
                return None, None
        except Exception as e:
            self.logger.error(f"Error acquiring sensor data: {e}")
            return None, None

    def _load_dataset(self, dataset_path):
        try:
            self.logger.info("Loading dataset...")
            data = pd.read_csv(dataset_path)
            if 'label' not in data.columns:
                raise ValueError("The dataset must contain the 'label' column for training.")
            
            self.features = data[['temperature', 'ph_level']]
            self.labels = data['label']
        except Exception as e:
            self.logger.error(f"Error loading dataset: {e}")
            raise

    def _initialize_model(self):
        self.logger.info("Initializing the model...")
        self.model = RandomForestClassifier(random_state=42)

    def _train_model(self):
        try:
            self.logger.info("Training the model...")
            self.model.fit(self.features, self.labels)
        except Exception as e:
            self.logger.error(f"Error training the model: {e}")
            raise

    def _evaluate_model(self):
        self.logger.info("Evaluating the model...")
        try:
            skf = StratifiedKFold(n_splits=min(4, self.labels.nunique()), shuffle=True, random_state=42)
            scores = cross_val_score(self.model, self.features, self.labels, cv=skf)
            accuracy = scores.mean()
            self.logger.info(f"Cross-validated Accuracy: {accuracy:.2f}")
        except Exception as e:
            self.logger.error(f"Error evaluating the model: {e}")
            raise

    def save_model(self, model_path='trained_model.joblib'):
        self.logger.info(f"Saving the trained model to {model_path}...")
        try:
            joblib.dump(self.model, model_path)
        except Exception as e:
            self.logger.error(f"Error saving the model: {e}")
            raise

    def predict(self, temperature, ph_level):
        self.logger.info("Making predictions...")
        input_data = pd.DataFrame([[temperature, ph_level]], columns=['temperature', 'ph_level'])
        prediction = self.model.predict(input_data)[0]
        return prediction

if __name__ == "__main__":
    ai_model = AIModel()

    try:
        while True:
            temperature, ph_level = ai_model._acquire_sensor_data()

            if temperature is not None and ph_level is not None:
                prediction = ai_model.predict(temperature, ph_level)
                ai_model.logger.info(f"AI Prediction: {prediction}")

            time.sleep(10)
    except KeyboardInterrupt:
        ai_model.logger.info("AI model stopped.")

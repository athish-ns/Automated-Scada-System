# monitoring_system.py
import time
import logging
from data_acquisition import RaspberryPiSensor  
from ai_model import AIModel

class RaspberryPiMonitoringSystem:
    def __init__(self):
        self.ai_model = AIModel()
        self.sensor = RaspberryPiSensor()  
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def run(self):
        self.logger.info("Monitoring system is active...")
        try:
            while True:
                sensor_data = self.sensor.read_sensor_data()

                if sensor_data is not None:
                    temperature, ph_level = sensor_data
                    try:
                        prediction = self.ai_model.predict(temperature, ph_level)
                        self.logger.info(f"AI Prediction: {prediction}")
                    except Exception as e:
                        self.logger.error(f"Error making AI prediction: {e}")

                time.sleep(10)
        except KeyboardInterrupt:
            self.logger.info("Monitoring system stopped.")
        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    monitoring_system = RaspberryPiMonitoringSystem()  
    monitoring_system.run()  

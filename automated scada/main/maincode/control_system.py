# control_system.py
import time
import random
import logging
from monitoring import RaspberryPiMonitoringSystem  

class ControlSystem:
    def __init__(self, monitoring_system):
        self.logger = self._setup_logger()
        self.sodium_hydroxide_dripper = False
        self.hydrochloric_acid_dripper = False
        self.initial_ph_level = random.uniform(6.5, 8.5)
        self.automatic_mode = False
        self.monitoring_system = monitoring_system

    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def _simulate_dripper_control(self, dripper_type, action):
        action_str = "on" if action else "off"
        dripper_name = "Sodium hydroxide" if dripper_type == 'sodium' else "Hydrochloric acid"
        self.logger.info(f"Turning {action_str} the dripper of {dripper_name}.")
        if dripper_type == 'sodium':
            self.sodium_hydroxide_dripper = action
        elif dripper_type == 'hydrochloric':
            self.hydrochloric_acid_dripper = action

    def start_automatic_mode(self):
        self.logger.info("Automatic mode started")
        self.automatic_mode = True

    def stop_automatic_mode(self):
        self.logger.info("Automatic mode stopped")
        self.automatic_mode = False

    def adjust_ph_level(self):
        try:
            sensor_data = self.monitoring_system.sensor.read_sensor_data()

            if sensor_data is not None:
                temperature, ph_level = sensor_data
                if self.automatic_mode:
                    if ph_level < 7.0:
                        self.logger.info("pH level is below 7.0. Turning on Sodium hydroxide to raise pH...")
                        self._simulate_dripper_control('sodium', True)
                        time.sleep(5)
                        self._simulate_dripper_control('sodium', False)

                    elif ph_level > 8.0:
                        self.logger.info("pH level is above 8.0. Turning on Hydrochloric acid to lower pH...")
                        self._simulate_dripper_control('hydrochloric', True)
                        time.sleep(5)
                        self._simulate_dripper_control('hydrochloric', False)

                    else:
                        self.logger.info("pH level is within the acceptable range. Maintaining pH level.")

                else:
                    if ph_level < 6.5:
                        self.logger.info("pH level is below 6.5. Turning on Sodium hydroxide to raise pH...")
                        self._simulate_dripper_control('sodium', True)
                        time.sleep(5)
                        if self.is_ph_stable(ph_level):
                            self._simulate_dripper_control('sodium', False)

                    elif ph_level > 8.5:
                        self.logger.info("pH level is above 8.5. Turning on Hydrochloric acid to lower pH...")
                        self._simulate_dripper_control('hydrochloric', True)
                        time.sleep(5)
                        if self.is_ph_stable(ph_level):
                            self._simulate_dripper_control('hydrochloric', False)

                    else:
                        self.logger.info("pH level is within the acceptable range. Maintaining pH level.")

        except Exception as e:
            self.logger.error(f"Error adjusting pH level: {e}")

    def is_ph_stable(self, ph_level):
        return abs(ph_level - self.initial_ph_level) < 0.2

if __name__ == "__main__":
    monitoring_system = RaspberryPiMonitoringSystem() 
    control_system = ControlSystem(monitoring_system)

    try:
        while True:
            control_system.adjust_ph_level()
            time.sleep(10)

    except KeyboardInterrupt:
        control_system.logger.info("Control system stopped.")



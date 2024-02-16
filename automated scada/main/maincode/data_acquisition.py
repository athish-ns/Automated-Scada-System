# raspberry_pi_sensor.py
import time
import logging
import board
import busio
from digitalio import DigitalInOut
from adafruit_mcp3xxx.mcp3008 import MCP3008
from adafruit_mcp3xxx.analog_in import AnalogIn

class RaspberryPiSensor:
    def __init__(self):
        self.spi = busio.SPI(clock=board.SCK, MISO=board.MISO, MOSI=board.MOSI)
        self.cs = DigitalInOut(board.D22)  
        self.mcp = MCP3008(self.spi, self.cs)
        self.logger = self.setup_logger()

    def setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch = logging.StreamHandler()
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        return logger

    def read_sensor_data(self):
        try:
            temperature, ph_level = self._read_actual_sensor_data()
            return temperature, ph_level
        except Exception as e:
            self.logger.error(f"Error reading sensor data: {e}")
            return None

    def _read_actual_sensor_data(self):
        temperature = self.read_adc(0)
        ph_level = self.read_adc(1)
        return temperature, ph_level

    def read_adc(self, channel):
        try:
            analog_in = AnalogIn(self.mcp, getattr(self.mcp, f"PIN_{channel}"))
            return analog_in.value
        except Exception as e:
            self.logger.error(f"Error reading ADC for channel {channel}: {e}")
            return None

if __name__ == "__main__":
    sensor = RaspberryPiSensor()

    try:
        while True:
            sensor_data = sensor.read_sensor_data()

            if sensor_data:
                print(f"Sensor Data - Temperature: {sensor_data[0]}, pH Level: {sensor_data[1]}")

            time.sleep(1)
    except KeyboardInterrupt:
        print("Data acquisition stopped.")

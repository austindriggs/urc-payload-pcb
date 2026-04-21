from machine import I2C
import time

class BME688_Air:
    def __init__(self, i2c, addr=0x76):
        self.i2c = i2c
        self.addr = addr

        # Query device info
        self.chip_id = self._read_reg(0x00,1)
        print("Chip ID:", self.chip_id)

        self._init_sensor()

    def _read_reg(self, reg, length):
        try:
            return self.i2c.readfrom_mem(self.addr, reg, length)
        except OSError as e:
            print("Read error:", e)
            return None

    def _write_reg(self, reg, data):
        try:
            self.i2c.writeto_mem(self.addr, reg, bytes([data]))
        except OSError as e:
            print("Write error:", e)

    def _init_sensor(self):
        # Soft reset
        self._write_reg(0xE0, 0xB6)
        time.sleep(0.1)

        # Set sensor to forced mode
        # based on Bosch BME688 AI guidance:
        self._write_reg(0x74, 0x10)  # config
        self._write_reg(0x75, 0x10)  # ctrl_meas

    def read_all(self):
        # Trigger measurement
        self._write_reg(0x74, 0x10)
        time.sleep(0.05)

        # Bulk read of raw data registers
        data = self._read_reg(0x1F, 15)
        if not data:
            return None

        # parse temp, press, humidity
        raw_t = (data[5] << 12) | (data[6] << 4) | (data[7] >> 4)
        raw_p = (data[2] << 12) | (data[3] << 4) | (data[4] >> 4)
        raw_h = (data[8] << 8) | data[9]

        # convert to human values (approx.)
        temp = raw_t / 100.0
        press = raw_p / 100.0
        hum = raw_h / 1024.0

        return temp, press, hum
from machine import Pin, I2C
import time
import math

# =============================
# I2C Setup
# =============================
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
BME680_ADDR = 0x77

print("I2C devices:", [hex(x) for x in i2c.scan()])

# =============================
# Minimal BME680 Config
# =============================

# Soft reset
i2c.writeto_mem(BME680_ADDR, 0xE0, b'\xB6')
time.sleep(0.5)

# Humidity oversampling x1
i2c.writeto_mem(BME680_ADDR, 0x72, b'\x01')

# Temperature + Pressure oversampling x1
i2c.writeto_mem(BME680_ADDR, 0x74, b'\x25')

print("BME680 configured")

def read_raw_data():
    data = i2c.readfrom_mem(BME680_ADDR, 0x1F, 15)
    return data

while True:
    try:
        raw = read_raw_data()

        pres_raw = (raw[2] << 12) | (raw[3] << 4) | (raw[4] >> 4)
        temp_raw = (raw[5] << 12) | (raw[6] << 4) | (raw[7] >> 4)
        hum_raw  = (raw[8] << 8)  | raw[9]

        print("\n--- BME680 RAW DATA ---")
        print("Temp Raw:", temp_raw)
        print("Pressure Raw:", pres_raw)
        print("Humidity Raw:", hum_raw)

    except Exception as e:
        print("Error:", e)

    time.sleep(2)

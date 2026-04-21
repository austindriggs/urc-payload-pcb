# ==============================
# PICO SCIENCE FIRMWARE (DEBUG SAFE)
# ==============================

import machine
from machine import Pin, I2C, PWM
from Old.bme680 import BME680_I2C
import time
import sys
import select

print("\n=== PICO SCIENCE BOOT ===")

# ==============================
# I2C BUS
# ==============================
try:
    i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
    print("I2C Initialized")
except Exception as e:
    print("I2C ERROR:", e)

# ==============================
# BME680 SENSORS
# ==============================
bme1 = None
bme2 = None

try:
    bme1 = BME680_I2C(i2c, address=0x76)
    print("BME680 #1 OK (0x76)")
except Exception as e:
    print("BME680 #1 FAILED:", e)

try:
    bme2 = BME680_I2C(i2c, address=0x77)
    print("BME680 #2 OK (0x77)")
except Exception as e:
    print("BME680 #2 FAILED:", e)

# ==============================
# PWM
# ==============================
def init_pwm(pin):
    try:
        pwm = PWM(Pin(pin))
        pwm.freq(50)
        pwm.duty_u16(0)
        print("PWM OK on pin", pin)
        return pwm
    except Exception as e:
        print("PWM FAIL on pin", pin, e)
        return None

soil_collector1 = init_pwm(2)
soil_collector2 = init_pwm(3)
probe_signal    = init_pwm(4)
drill_pwm       = init_pwm(5)

# ==============================
# RELAYS
# ==============================
halogen = Pin(22, Pin.OUT)
halogen.value(0)
print("Halogen relay OK")

u2d2 = Pin(21, Pin.OUT)
u2d2.value(1)
print("U2D2 relay OK")

# ==============================
# STREAM CONTROL
# ==============================
STREAM_INTERVAL = 1.0
last_stream = time.ticks_ms()

# ==============================
# SERIAL POLLING
# ==============================
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

print("Entering main loop...")

while True:

    # ----- STREAM -----
    if time.ticks_diff(time.ticks_ms(), last_stream) > STREAM_INTERVAL * 1000:

        try:
            if bme1:
                t1 = bme1.temperature
                p1 = bme1.pressure
                h1 = bme1.humidity
            else:
                t1 = p1 = h1 = 0.0

            if bme2:
                t2 = bme2.temperature
                p2 = bme2.pressure
                h2 = bme2.humidity
            else:
                t2 = p2 = h2 = 0.0

            print("{:.6f},{:.6f},{:.6f},{:.6f},{:.6f},{:.6f}".format(
                t1, p1, h1, t2, p2, h2
            ))

        except Exception as e:
            print("STREAM ERROR:", e)

        last_stream = time.ticks_ms()

    # ----- COMMANDS -----
    if poller.poll(0):
        cmd = sys.stdin.readline().strip()
        print("CMD:", cmd)

        if cmd == "hbon":
            halogen.value(1)
            print("Halogen ON")

        elif cmd == "hboff":
            halogen.value(0)
            print("Halogen OFF")

        elif cmd == "reset":
            print("Resetting...")
            machine.reset()

        else:
            print("Unknown command")

    time.sleep(0.01)
    
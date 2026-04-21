# ==============================
# PICO SCIENCE FIRMWARE (NUMERIC ONLY)
# ==============================

import machine
from machine import Pin, I2C, PWM
from Old.bme680 import BME680_I2C
import time
import sys
import select

# ==============================
# I2C BUS
# ==============================
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)

# ==============================
# BME680 SENSORS (NO PRINTS)
# ==============================
try:
    bme1 = BME680_I2C(i2c, address=0x76)
except:
    bme1 = None

try:
    bme2 = BME680_I2C(i2c, address=0x77)
except:
    bme2 = None


# ==============================
# PWM ACTUATORS
# ==============================
def init_pwm(pin):
    pwm = PWM(Pin(pin))
    pwm.freq(50)
    pwm.duty_u16(0)
    return pwm

soil_collector1 = init_pwm(2)
soil_collector2 = init_pwm(3)
probe_signal    = init_pwm(4)
drill_pwm       = init_pwm(5)

def set_pwm_from_float(pwm, val, base=3300, scale=3300):
    duty = int(val * scale) + base
    pwm.duty_u16(duty)


# ==============================
# RELAYS
# ==============================
halogen = Pin(22, Pin.OUT) #22
halogen.value(0)

u2d2 = Pin(21, Pin.OUT) #21
u2d2.value(1)


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


# ==============================
# SAFE SENSOR READ (ALWAYS RETURNS NUMBERS)
# ==============================
def read_bme(sensor):
    if sensor:
        try:
            return (
                sensor.temperature,
                sensor.pressure,
                sensor.humidity
            )
        except:
            return (0.0, 0.0, 0.0)
    return (0.0, 0.0, 0.0)


# ==============================
# MAIN LOOP
# ==============================
while True:

    # ----- STREAM DATA -----
    if time.ticks_diff(time.ticks_ms(), last_stream) > STREAM_INTERVAL * 1000:

        t1, p1, h1 = read_bme(bme1)
        t2, p2, h2 = read_bme(bme2)

        # ALWAYS EXACTLY 6 NUMBERS
        print("{:.6f},{:.6f},{:.6f},{:.6f},{:.6f},{:.6f}".format(
            t1, p1, h1, t2, p2, h2
        ))

        last_stream = time.ticks_ms()


    # ----- HANDLE COMMANDS -----
    if poller.poll(0):

        cmd = sys.stdin.readline().strip()

        try:
            if cmd == "sc1":
                val = float(sys.stdin.readline().strip())
                set_pwm_from_float(soil_collector1, val)

            elif cmd == "sc2":
                val = float(sys.stdin.readline().strip())
                set_pwm_from_float(soil_collector2, val)

            elif cmd == "probe":
                val = float(sys.stdin.readline().strip())
                set_pwm_from_float(probe_signal, val)

            elif cmd == "drill":
                val = float(sys.stdin.readline().strip())
                duty = int(val * 2583) + 3630
                drill_pwm.duty_u16(duty)

            elif cmd == "hbon":
                halogen.value(1)

            elif cmd == "hboff":
                halogen.value(0)

            elif cmd == "u2d2on":
                u2d2.value(0)

            elif cmd == "u2d2off":
                u2d2.value(1)

            elif cmd == "reset":
                machine.reset()

        except:
            pass

    time.sleep(0.01)
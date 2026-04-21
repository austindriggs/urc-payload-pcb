from machine import Pin, I2C, PWM
from Old.bme680 import BME680_I2C
import time
import sys
import select

print("\n=== PAYLOAD SYSTEM BOOT ===")

# -------------------------------------------------
# I2C BUS
# -------------------------------------------------
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=100000)
print("I2C devices:", [hex(x) for x in i2c.scan()])

# -------------------------------------------------
# BME680 SENSOR
# -------------------------------------------------
bme = BME680_I2C(i2c, address=0x77)

# -------------------------------------------------
# QWIIC SOIL MOISTURE SENSOR (0x28)
# -------------------------------------------------
SOIL_ADDR = 0x28
COMMAND_GET_VALUE = 0x05
COMMAND_LED_ON = 0x01
COMMAND_LED_OFF = 0x00

def soil_connected():
    return SOIL_ADDR in i2c.scan()

def soil_read_raw():
    data = i2c.readfrom_mem(SOIL_ADDR, COMMAND_GET_VALUE, 2)
    return data[1] << 8 | data[0]

def soil_led_on():
    i2c.writeto(SOIL_ADDR, bytes([COMMAND_LED_ON]))

def soil_led_off():
    i2c.writeto(SOIL_ADDR, bytes([COMMAND_LED_OFF]))

def soil_percent(raw, dry=200, wet=1000):
    if raw < dry:
        raw = dry
    if raw > wet:
        raw = wet
    return round((raw - dry) * 100 / (wet - dry), 2)

# -------------------------------------------------
# ACTUATOR (PWM)
# -------------------------------------------------
actuator = PWM(Pin(2))
actuator.freq(50)

def set_actuator_us(pulse_us):
    duty = int((pulse_us / 20000) * 65535)
    actuator.duty_u16(duty)

def extend():
    set_actuator_us(2000)

def retract():
    set_actuator_us(1000)

def stop():
    set_actuator_us(1500)

# -------------------------------------------------
# DIGITAL INPUTS
# -------------------------------------------------
exp1 = Pin(6, Pin.IN, Pin.PULL_UP)
exp2 = Pin(7, Pin.IN, Pin.PULL_UP)
limit1 = Pin(14, Pin.IN, Pin.PULL_UP)
limit2 = Pin(15, Pin.IN, Pin.PULL_UP)
can_int = Pin(20, Pin.IN, Pin.PULL_UP)

# -------------------------------------------------
# RELAYS
# -------------------------------------------------
relay1 = Pin(21, Pin.OUT)
relay2 = Pin(22, Pin.OUT)

# -------------------------------------------------
# LEDS
# -------------------------------------------------
led_status = Pin(10, Pin.OUT)
led_error  = Pin(11, Pin.OUT)

# -------------------------------------------------
# SYSTEM STATE
# -------------------------------------------------
telemetry_enabled = False
last_print = time.ticks_ms()

print("\nTelemetry is OFF by default.")
print("Type 'help' for command list.\n")

# -------------------------------------------------
# COMMAND HANDLER
# -------------------------------------------------
def handle_command(cmd):
    global telemetry_enabled

    cmd = cmd.strip().lower()

    if cmd == "extend":
        print("Extending actuator")
        extend()

    elif cmd == "retract":
        print("Retracting actuator")
        retract()

    elif cmd == "stop":
        print("Stopping actuator")
        stop()

    elif cmd.startswith("move"):
        try:
            val = int(cmd.split()[1])
            if 1000 <= val <= 2000:
                set_actuator_us(val)
                print("Moving actuator to", val, "us")
            else:
                print("Range: 1000–2000")
        except:
            print("Usage: move 1500")

    elif cmd == "telemetry on":
        telemetry_enabled = True
        print("Telemetry ENABLED")

    elif cmd == "telemetry off":
        telemetry_enabled = False
        print("Telemetry DISABLED")

    elif cmd == "soil read":
        if soil_connected():
            raw = soil_read_raw()
            percent = soil_percent(raw)
            print("Soil Raw:", raw)
            print("Soil Moisture:", percent, "%")
        else:
            print("Soil sensor not detected!")

    elif cmd == "soil led on":
        soil_led_on()
        print("Soil LED ON")

    elif cmd == "soil led off":
        soil_led_off()
        print("Soil LED OFF")

    elif cmd == "status":
        print("\nSystem Status:")
        print("Telemetry:", telemetry_enabled)
        print("Limit1:", limit1.value())
        print("Limit2:", limit2.value())
        print("EXP1:", exp1.value())
        print("EXP2:", exp2.value())
        print("CAN_INT:", can_int.value())
        print("Soil Connected:", soil_connected())

    elif cmd == "help":
        print("""
================ COMMANDS ================

ACTUATOR:
  extend
  retract
  stop
  move <1000-2000>

SOIL SENSOR:
  soil read
  soil led on
  soil led off

TELEMETRY:
  telemetry on
  telemetry off

SYSTEM:
  status
  help

==========================================
""")

    else:
        print("Unknown command. Type 'help'.")

# -------------------------------------------------
# MAIN LOOP
# -------------------------------------------------
poller = select.poll()
poller.register(sys.stdin, select.POLLIN)

while True:

    # -------- TELEMETRY --------
    if telemetry_enabled and time.ticks_diff(time.ticks_ms(), last_print) > 2000:
        try:
            temperature = bme.temperature
            pressure = bme.pressure
            humidity = bme.humidity
            gas = bme.gas

            soil_raw = None
            soil_moisture = None

            if soil_connected():
                soil_raw = soil_read_raw()
                soil_moisture = soil_percent(soil_raw)

            led_status.toggle()

            print("\n--- TELEMETRY ---")
            print("Temp:", round(temperature,2), "°C")
            print("Pressure:", round(pressure,2), "hPa")
            print("Humidity:", round(humidity,2), "%")
            print("Gas:", gas, "Ohms")

            if soil_raw is not None:
                print("Soil Raw:", soil_raw)
                print("Soil Moisture:", soil_moisture, "%")

            print("Limit1:", limit1.value(), "Limit2:", limit2.value())

        except Exception as e:
            print("Sensor error:", e)
            led_error.on()

        last_print = time.ticks_ms()

    # -------- COMMAND INPUT --------
    if poller.poll(0):
        cmd = sys.stdin.readline()
        handle_command(cmd)

    time.sleep(0.01)

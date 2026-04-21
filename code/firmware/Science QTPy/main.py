from machine import Pin, I2C
import onewire
import ds18x20
import time
import sys
import select

# -------------------------
# ACTUATOR SETUP
# -------------------------

IN1 = Pin(4, Pin.OUT)
IN2 = Pin(6, Pin.OUT)
EN1 = Pin(5, Pin.OUT)

def stop():
    EN1.value(0)
    IN1.value(0)
    IN2.value(0)

def retract():
    EN1.value(1)
    IN1.value(1)
    IN2.value(0)

def extend():
    EN1.value(1)
    IN1.value(0)
    IN2.value(1)

# Start OFF
stop()

# -------------------------
# Soil Moisture Sensor (I2C1)
# -------------------------

i2c = I2C(1, sda=Pin(22), scl=Pin(23), freq=100000)
soil_addr = 0x28

print("I2C scan:", i2c.scan())

# -------------------------
# DS18B20 Temperature
# -------------------------

dat = Pin(26)
ow = onewire.OneWire(dat)
ds = ds18x20.DS18X20(ow)

roms = ds.scan()
print("Temp sensor ROM:", roms)

# -------------------------
# Non-blocking serial check
# -------------------------

def read_command():
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        cmd = sys.stdin.readline().strip()
        return cmd
    return None

# -------------------------
# Main loop
# -------------------------

while True:

    # ---- Check for command ----
    cmd = read_command()
    if cmd:
        print("CMD:", cmd)

        if cmd == "extend":
            extend()
        elif cmd == "retract":
            retract()
        elif cmd == "stop":
            stop()
        else:
            print("Unknown command")

    # ---- Temperature ----
    ds.convert_temp()
    time.sleep(1)

    temp = None
    for rom in roms:
        temp = round(ds.read_temp(rom), 2)

    # ---- Moisture ----
    moisture = None
    try:
        data = i2c.readfrom_mem(soil_addr, 0x05, 2)
        moisture = data[1] << 8 | data[0]
    except:
        print("Moisture sensor read error")

    # ---- Print results ----
    print(f"{moisture}, {temp}")

    time.sleep(1)
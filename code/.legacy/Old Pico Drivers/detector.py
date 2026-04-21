from machine import Pin, I2C
import time

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

print("Scanning I2C bus...")

while True:
    devices = i2c.scan()
    if devices:
        print("Devices found:")
        for d in devices:
            print("  Address:", hex(d))
    else:
        print("No devices found")
    time.sleep(2)

    from machine import Pin, I2C
import struct
import time

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

TMP117_ADDR = 0x4C

while True:
    raw = i2c.readfrom_mem(TMP117_ADDR, 0x0F, 2)
    val = struct.unpack(">H", raw)[0]
    print("TMP117 Device ID:", hex(val))
    time.sleep(2)


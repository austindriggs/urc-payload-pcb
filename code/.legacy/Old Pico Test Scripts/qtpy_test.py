from machine import Pin, I2C

i2c = I2C(1, sda=Pin(22), scl=Pin(23), freq=100000)

print("Scan:", i2c.scan())

try:
    i2c.writeto(0x76, b'\xD0')
    print("Write succeeded")
except Exception as e:
    print("Write failed:", e)

try:
    data = i2c.readfrom(0x76, 1)
    print("Read succeeded:", data)
except Exception as e:
    print("Read failed:", e)
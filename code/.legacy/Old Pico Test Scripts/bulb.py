from machine import Pin
import time

# Initialize pins
pin21 = Pin(21, Pin.OUT)
pin22 = Pin(22, Pin.OUT)

# Start LOW
pin21.value(0)
pin22.value(0)

print("Starting AUTO TEST for GP21 and GP22")

while True:

    print("GP21 HIGH")
    pin21.value(1)
    time.sleep(3)
    pin21.value(0)
    print("GP21 LOW")

    time.sleep(1)

    print("GP22 HIGH")
    pin22.value(1)
    time.sleep(3)
    pin22.value(0)
    print("GP22 LOW")

    time.sleep(1)
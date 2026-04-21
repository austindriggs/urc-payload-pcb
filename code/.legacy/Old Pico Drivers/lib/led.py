from machine import Pin, PWM
from utime import sleep


def init():
    led_onboard = Pin(25, Pin.OUT)
    led_onboard.value(1)
    heartbeat()
    resolved()
    led_onboard.value(0)

    return led_onboard


def heartbeat():
    print("Normal system operation")
    led_status = Pin(10, Pin.OUT)
    led_status.value(1)


def failure():
    print("System error detected")
    led_error = Pin(11, Pin.OUT)
    led_error.value(1)


def critical():
    print("Critical error detected")
    led_error = PWM(Pin(11))
    led_error.freq(10)
    led_error.duty_u16(32768)


def resolved():
    print("System error resolved")
    temp_pwm = PWM(Pin(11))
    temp_pwm.deinit()
    led_error = Pin(11, Pin.OUT)
    led_error.value(0)


def test():
    print("--- Starting LED Hardware Test ---")

    print("Step 0: Testing On-Board LED (Pin 25 ON)")
    led_onboard = Pin(25, Pin.OUT)
    led_onboard.value(1)
    sleep(1)
    led_onboard.value(0)

    print("Step 1: Setting Heartbeat (Pin 10 ON)")
    heartbeat()
    sleep(2)

    print("Step 2: Simulating Failure (Pin 11 ON)")
    failure()
    sleep(2)

    print("Step 3: Simulating Critical Error (Pin 11 FLICKER)")
    critical()
    sleep(3)

    print("Step 4: Resolving Errors (Pin 11 OFF)")
    resolved()
    sleep(1)
    
    print("--- LED Hardware Test Complete ---")
    init()


if __name__ == "__main__":
    test()

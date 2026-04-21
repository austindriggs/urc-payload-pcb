import machine

def lsw_init(pin_number):
    """
    Initializes a limit switch on the given pin number.
    The pin is configured as an input with a pull-up resistor
    for an active-low limit switch.
    """
    return machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)

def is_lsw_pressed(lsw_pin):
    """
    Checks if the limit switch is pressed (active).
    For an active-low switch, pressed means the pin is LOW (0).
    Returns True if pressed, False otherwise.
    """
    return lsw_pin.value() == 0

def is_lsw_released(lsw_pin):
    """
    Checks if the limit switch is not pressed (inactive).
    For an active-low switch, not pressed means the pin is HIGH (1).
    Returns True if not pressed, False otherwise.
    """
    return lsw_pin.value() == 1

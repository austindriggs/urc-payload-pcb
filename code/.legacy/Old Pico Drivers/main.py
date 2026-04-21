import select, sys, time, machine, gc
from collections import deque
import onewire
import ds18x20
import _thread
#import pca
#import multicore
#import old.hardware as hardware

import lib.pwm as pwm
import lib.led as led
import manipulator
import science

#125 MHz clock freq
machine.freq(125000000)

# Set up the poll object
poll_obj = select.poll()
poll_obj.register(sys.stdin, select.POLLIN)

# queue for communication between cores, max size is kind of arbitrary at this point
# for now the messages are as follows:
# '5' means open the claw
# '6' is an explicit stop command, but shouldn't be necessary
# '7' means close the claw

# '1' means activate the solenoid
# '0' means deactivate the solenoid, with no power it automatically retracts, so no reversal necessary
#q = deque([], 15)
#validMsgs = ['5', '6', '7', '1', '0']

# I2C for communicating with GPIO extenders and PWM extenders
# might need delay between init and use, or after writing
i2c = machine.I2C(0, scl = machine.Pin(1), sda = machine.Pin(0), freq = 400000)
devs = i2c.scan()
sys.stdout.write("I2C devices:" + str(devs) + '\n')


# initialize other things
led_onboard = led.init()
#pca.pca_init_all_out(pca.pca0, i2c)
wdt = machine.WDT(timeout=6000)

science.init_bme680(i2c)

# Current mode, can be toggled via 'switch' command in mission
current_mode = 'science'

# Main loop to run the appropriate mission based on current_mode
while True:
    if current_mode == 'science':
        science.mission(poll_obj, wdt, i2c)
    elif current_mode == 'manipulator':
        manipulator.mission(poll_obj, wdt, i2c)    

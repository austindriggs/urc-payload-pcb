import machine
import onewire
import ds18x20
from machine import Pin, ADC
import lib.led as led








    
#Manipulator Stuff




#Science Stuff
def lin_act_init(pin: int):
    lin_act_pwm = machine.PWM(Pin(pin), freq = 50, duty_u16 = 0)
    return lin_act_pwm

#soil collector 1 servo will be on pin 2 / servo 1 on the pcb schematic
def soil_collector1_lin_act_init():
    return lin_act_init(2)

#soil collector 2 servo will be on pin 3 / servo 2 on the pcb schematic
def soil_collector2_lin_act_init():
    return lin_act_init(3)

#temperature and moisture probe, signal still needs to be like 5V RC control
def probe_signal_init():
    return lin_act_init(4)

#drill actuator 
def drill_lin_act_init():
    return lin_act_init(5)

#Halogen bulb will be on 22
def halogen_bulb_init():
    halogen_pin = Pin(22, Pin.OUT)
    return halogen_pin

def moisture_sens_ADC_init():
    return ADC(Pin(26))

def temp_ow_init():
    return onewire.OneWire(Pin(27))

def temp_init(ow):
    return ds18x20.DS18X20(ow)




#This is specifically a one wire temp sensor
def temp_sens_ds_init(ow):
    return ds18x20.DS18X20(ow)

#Relay for the dynamixel control unit
def u2d2_relay_init():
    return Pin(21, Pin.OUT)







import machine
import onewire
import ds18x20
from machine import Pin, ADC
import lib.led as led

import lib.pwm as pwm

import time
import sys

from bme680 import BME680_I2C

bme = None

def init_bme680(i2c):
    global bme
    try:
        bme = BME680_I2C(i2c)
        sys.stdout.write("BME680 initialized\n")
    except Exception as e:
        sys.stdout.write(f"BME680 init failed: {e}\n")



def lin_act_init(pin: int):
    lin_act_pwm = machine.PWM(Pin(pin), freq = 50, duty_u16 = 0)
    return lin_act_pwm



#soil collector 1 servo will be on GPIO2 (physical pin 4) / SERVO1_PICO
#soil collector 2 servo will be on GPIO3 (physical pin 5) / SERVO2_PICO
def soil_collector_lin_act_init():
    return lin_act_init(2), lin_act_init(3)



#temperature and moisture probe, signal still needs to be like 5V RC control on GPIO4 (physical pin 6) / SERVO3_PICO
def probe_signal_init():
    return lin_act_init(4)



#drill actuator on GPIO5 (physical pin 7) / SERVO4_PICO
def drill_lin_act_init():
    return lin_act_init(5)



#Halogen bulb will be on GPIO22 (physical pin 29) / Digital_Relay2
def halogen_bulb_init():
    halogen_pin = Pin(22, Pin.OUT)
    halogen_pin.value(0)
    return halogen_pin



def moisture_sens_ADC_init():
    # GPIO26 (physical pin 31) / ADC0
    return ADC(Pin(26))



def temp_ow_init():
    # GPIO27 (physical pin 32) / ADC1
    return onewire.OneWire(Pin(27))



def temp_init(ow):
    return ds18x20.DS18X20(ow)



#Relay for the dynamixel control unit on GPIO21 (physical pin 27) / Digital_Relay1
def u2d2_relay_init():
    return Pin(21, Pin.OUT)



def timee(activeMaybe):
        if(activeMaybe == False):
            led.failure()
        else:
            activeMaybe = False



def temp_moist(moisture_adc, temp_sens):
    try:
        moisture_val = str(moisture_adc.read_u16())
        #After calling convert temp you need to give time for the sensor to actually convert its data
        temp_sens.convert_temp()
        temp_dev_id = temp_sens.scan()[0]
        time.sleep_ms(750)
        temperature = temp_sens.read_temp(temp_dev_id)
        sys.stdout.write(f"{moisture_val},{temperature}\n")
    except:
        return



def halogen_bulb_safety(halogen_pin, hb_active, hb_extender):
    if(hb_extender != 3):
        hb_extender = hb_extender + 1
        return
    else:
        halogen_pin.value(0)
        hb_active = False            



def input_flush(poll_obj):
    poll_result = poll_obj.poll(0)
    while (poll_result != []):
        poll_result = poll_obj.poll(0)
        dump = sys.stdin.readline()
    return







def mission(poll_obj, wdt, i2c):
    sys.stdout.write("Science!")
    activeMaybe = False
    
    soil_collector1_pwm, soil_collector2_pwm = soil_collector_lin_act_init()
    probe_pwm_signal = probe_signal_init()
    drill_pwm = drill_lin_act_init()
    halogen_pin = halogen_bulb_init()
    hb_extender = 0
    hb_active = False
    u2d2_pin = u2d2_relay_init()
    moisture_adc = moisture_sens_ADC_init()
    temp_ow = temp_ow_init()
    temp_sens = temp_init(temp_ow)


    pwm.set_pwm_duty(3300, soil_collector1_pwm)
    pwm.set_pwm_duty(3300, soil_collector2_pwm)
    pwm.set_pwm_duty(3300, probe_pwm_signal)
    pwm.set_pwm_duty(3630, drill_pwm)

    # emergencyTim = machine.Timer(-1)
    # emergencyTim.init(period = 100, mode = machine.Timer.PERIODIC, callback = lambda t: timee(activeMaybe))
    temp_moist_data_timer = machine.Timer(-1)
    temp_moist_data_timer.init(period = 4000, mode = machine.Timer.PERIODIC, callback = lambda t: temp_moist(moisture_adc, temp_sens))
    #hb_safety_timer = machine.Timer(period = 6500, mode = machine.Timer.PERIODIC, callback = halogen_bulb_safety(hb_active, hb_extender))
    input_flush_timer = machine.Timer(-1)
    input_flush_timer.init(period = 5000, mode = machine.Timer.PERIODIC, callback = lambda t: input_flush(poll_obj))
    
    while True:
        poll_result = poll_obj.poll(5)
        wdt.feed()
        if (poll_result == []):
            continue
        data = sys.stdin.readline().strip("\n")

        #science controls
        if(data == "sc1"):
            #led.value(1)
            data2 = sys.stdin.readline().strip("\n")
            try:
                duty = float(data2)
                pwm.set_pwm_duty((int(duty * 3300) + 3300), soil_collector1_pwm)
            except:
                continue

        elif(data == "sc2"):
            #led.value(1)
            data2 = sys.stdin.readline().strip("\n")
            try:
                duty = float(data2)
                pwm.set_pwm_duty((int(duty * 3300) + 3300), soil_collector2_pwm)
            except:
                continue

        elif(data == "probe"):
            #led.value(1)
            data2 = sys.stdin.readline().strip("\n")
            try:
                duty = float(data2)
                pwm.set_pwm_duty((int(duty * 3300) + 3300), probe_pwm_signal)
            except:
                continue

        #drill goes from 1.1 ms to 1.9 ms for retracted and extended instead of 1 ms and 2 ms like the other actuators
        elif(data == "drill"):
            #led.value(1)
            data2 = sys.stdin.readline().strip("\n")
            try:
                duty = float(data2)
                pwm.set_pwm_duty((int(duty * 2583) + 3630), drill_pwm)
            except:
                continue


        elif(data == "moist"):
            #led.value(1)
            moisture_val = str(moisture_adc.read_u16())
            sys.stdout.write(f"{moisture_val}\n")

        elif(data == "temp"):
            #led.value(1)
            #After calling convert temp you need to give time for the sensor to actually convert its data
            temp_sens.convert_temp()
            temp_dev_id = temp_sens.scan()
            time.sleep_ms(750)
            temperature = temp_sens.read_temp(temp_dev_id)
            sys.stdout.write(f"{temperature}\n")


        #halogen bulb control
        elif(data == "hbon"):
            if(hb_active == True):
                continue
            hb_active = True
            halogen_pin.value(1)
            hb_safety_timer = machine.Timer(-1)
            hb_safety_timer.init(period = 6500, mode = machine.Timer.ONE_SHOT, callback = halogen_bulb_safety(halogen_pin, hb_active, hb_extender))
    
        elif(data== "hboff"):
            hb_active = False
            halogen_pin.value(0)

        #u2d2 relay stuff goes here
        elif(data == "u2d2on"):
            #led.value(1)
            u2d2_pin.value(0)
    
        elif(data== "u2d2off"):
            #led.value(0)
            u2d2_pin.value(1)


        elif(data == "bme680"):
            if bme:
                temp = bme.temperature
                hum = bme.humidity
                pres = bme.pressure
                gas = bme.gas
                sys.stdout.write(f"Temperature: {temp:.2f} C, Humidity: {hum:.2f} %, Pressure: {pres:.2f} hPa, Gas: {gas} ohms\n")
            else:
                sys.stdout.write("BME680 not initialized\n")

        elif(data=='reset'):
            machine.reset()

        else:
            #led.value(0)
            continue

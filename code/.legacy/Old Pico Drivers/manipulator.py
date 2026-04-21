import machine
import onewire
import ds18x20
from machine import Pin, ADC
import lib.led as led
import sys
import lib.pwm as pwm
import select



def claw_init():
    claw_pwm = machine.PWM(Pin(12), freq = 1000, duty_u16 = 0)
    return claw_pwm

def solenoid_init():
    solenoid_pin = Pin(22, Pin.OUT)
    return solenoid_pin

def fsr_init():
    fsr_adc0 = ADC(Pin(26))
    fsr_adc1 = ADC(Pin(27))
    return fsr_adc0, fsr_adc1
    

def timee(activeFlagClaw, activeFlagSolenoid, solenoid_pin, claw_pwm):

        if(activeFlagClaw == False):
            #led.value(0)
            pwm.stop_claw(claw_pwm)
        else:
            activeFlagClaw = False
        if(activeFlagSolenoid == False):
            #led.value(0)
            solenoid_pin.value(0)
        else:
            activeFlagSolenoid = False
        
        
def send_FSR(adc0, adc1):
    adcstr0 = str(adc0.read_u16())
    adcstr1 = str(adc1.read_u16())

    fullstring = str(adcstr0) + "," + str(adcstr1) + '\r'

    sys.stdout.write(fullstring)


def input_flush(poll_obj):
    poll_result = poll_obj.poll(0)
    while (poll_result != []):
        poll_result = poll_obj.poll(0)
        dump = sys.stdin.readline()
    return


def create_timers(activeFlagClaw, activeFlagSolenoid, solenoid_pin,claw_pwm, poll_obj):
    emergencyTim = machine.Timer(-1) 
    emergencyTim.init(period=100, 
                      mode=machine.Timer.PERIODIC, 
                      callback=timee(activeFlagClaw, activeFlagSolenoid, solenoid_pin,claw_pwm)
                    )

    input_flush_timer = machine.Timer(-1)
    input_flush_timer.init(period=100, 
                           mode=machine.Timer.PERIODIC, 
                           callback=input_flush(poll_obj)
                           )

    return emergencyTim, input_flush_timer


def mission(poll_obj, wdt, i2c):
    sys.stdout.write("Manipulation!")
    activeFlagClaw = False
    activeFlagSolenoid = False
    
    #arm stuff
    claw_pwm = claw_init()
    solenoid_pin = solenoid_init()
    fsr_adc0, fsr_adc1 = fsr_init()
    
    pwm.stop_claw(claw_pwm)
    solenoid_pin.value(0)
    
    emergencyTim, input_flush_timer = create_timers(activeFlagClaw, activeFlagSolenoid, solenoid_pin,claw_pwm, poll_obj)
    
    while True:
        poll_result = poll_obj.poll(5)
        wdt.feed()
        if (poll_result == []):
            continue
        data = sys.stdin.readline().strip("\n")

        # messages 1, 0, 5, 6, 7 are all used for the manipulator (numbers)
        # science messages will be all letters, not car
        # sudo udevadm info -a /dev/ttyACM0
        # need to use 1 piece from first info then 1 other, entire block
        #.install udevrules script?

        if(data == '5'):
            #led.value(1)
            #pca.set_claw_dir_open(i2c)
            if(activeFlagClaw):
                activeFlagClaw = True
                continue
            else:
                activeFlagClaw = True
                pwm.ramp_claw_speed(claw_pwm)
            
        elif(data == '6'):
            #led.value(0)
            pwm.stop_claw(claw_pwm)
            activeFlagClaw = True
        elif(data == '7'):
            #led.value(1)
            #pca.set_claw_dir_close(i2c)
            if(activeFlagClaw):
                activeFlagClaw = True
                continue
            else:
                activeFlagClaw = True
                pwm.ramp_claw_speed(claw_pwm)

        elif(data == '1'):
            #led.value(1)
            solenoid_pin.value(1)
            activeFlagSolenoid = True
        elif(data == '0'):
            #led.value(0)
            solenoid_pin.value(0)
            activeFlagSolenoid = True

        elif(data=='reset'):
            machine.reset()
            
        else:
            #led.value(0)
            pwm.stop_claw(claw_pwm)
            solenoid_pin.value(0)

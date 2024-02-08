# IMPORTS

from pyiArduinoI2Cexpander import *     
from time import sleep    
import Adafruit_DHT     
from gpiozero import LineSensor, DigitalOutputDevice, TonalBuzzer  
from gpiozero.tones import Tone
import paho.mqtt.publish as publish
import json
# import RPi.GPIO as GPIO
from pyfirmata import Arduino, ArduinoMega, util


# DEFS

def beep(frequency, time):
    if doBeep:
        beeper.play(Tone(frequency))
        sleep(time)
        beeper.stop()
    else: pass

def multi_beep(frequency, time, amount, interval):
    for i in range(amount):
        beep(frequency, time)
        sleep(interval)

def custom_map(x, fromLow, fromHigh, toLow, toHigh):
    return (x - fromLow) * (toHigh - toLow) / (fromHigh - fromLow) + toLow

def readPH(pin, zeroshift):
    adcSensor = board.analog[pin].read() * 1024
    voltageSensor = adcSensor * 5.02 / 1023
    fin = round(3.5 * voltageSensor + zeroshift, 1)
    return fin 

def sensors_read():
    # LUMINANCE - measure
    luminance = round(1024 - board.analog[1].read() * 1024, 0)                    
    print('Luminance sensor: ', luminance)

    # Automation
    if not(lum_low <= luminance) and not relay3.is_active:
        relay3.on()
    elif lum_low <= luminance and relay3.is_active:
        relay3.off()
    check_relay(3)

    # Uploading
    publish.single('logger/luminance', str(luminance), hostname='localhost')


    #SOIL HUMIDITY - measurement
    soilhum = round(board.analog[0].read() * 1024, 0)
    newValue = custom_map(soilhum, 630, 330, 0, 100)
    print('Soil humidity sensor: ', newValue)

    # Automation
    if not(soilhum_low <= soilhum <= soilhum_high) and not relay1.is_active:
        relay1.on()
    elif soilhum_low <= soilhum <= soilhum_high and relay1.is_active:
        relay1.off()
    check_relay(1)

    # Uploading
    publish.single('logger/soil_humidity', str(newValue), hostname='localhost')
    

    # AIR TEMPERATURE & HUMIDITY - measurement
    while True:
        airhum, airtemp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4, retries=5, delay_seconds=2)
        if airhum != None and airtemp != None:
                break

    print('Air temperature: ', airtemp)
    print('Air humidity: ', airhum)

    # Automation - FOR TEMPERATURE
    if not(airtemp_low <= airhum <= airtemp_high) and not relay2.is_active:
        relay2.on()
    elif airtemp_low <= airhum <= airtemp_high and relay2.is_active:
        relay2.off()
    check_relay(2)

    # Automation - FOR HUMIDITY
    if not(airhum_low <= airhum <= airhum_high) and not relay4.is_active:
        relay4.on()
    elif airhum_low <= airhum <= airhum_high and relay4.is_active:
        relay4.off()
    check_relay(4)

    # Uploading
    publish.single("logger/air_temperature", str(airtemp), hostname='localhost')
    publish.single('logger/air_humidity', str(airhum), hostname='localhost') 


    # WATER PRESENCE - measurement
    isWater = water_sensor.is_active  
    print("Water presence: ", isWater)

    # Automation

    # Uploading
    publish.single('logger/water_presence', str(isWater), hostname='localhost')


    ph = readPH(2, -0.7)
    print('pH: ', ph)
    # print('pH level: ', ph)
    # # if not(ph_low <= ph):
    # #     publish.single('alerts/pH', 'Low acidity', hostname='localhost')
    # # elif not(ph <= ph_high):
    # #     publish.single('alerts/pH', 'High acidity', hostname='localhost')
    # # else:
    # #     publish.single('alerts/pH', 'OK', hostname='localhost')
    # publish.single('logger/pH', str(ph), hostname='localhost')

    print('')   

def check_relay(num):
    if num == 1:
        relay1_status = relay1.is_active  
        print("Relay 1 is active: ", relay1_status)
        publish.single('logger/relay1', str(relay1_status), hostname='localhost')
    elif num == 2:
        relay2_status = relay2.is_active  
        print("Relay 2 is active: ", relay2_status)
        publish.single('logger/relay2', str(relay2_status), hostname='localhost')
    elif num == 3:
        relay3_status = relay3.is_active  
        print("Relay 3 is active: ", relay3_status)
        publish.single('logger/relay3', str(relay3_status), hostname='localhost')
    elif num == 4:
        relay4_status = relay4.is_active  
        print("Relay 4 is active: ", relay4_status)
        publish.single('logger/relay4', str(relay4_status), hostname='localhost')
    
# ------------------------------------------------------------------------------------------

with open('/home/pi/PythonScripts/final/testfile.json') as settings:
    data = json.load(settings)

soilhum_low = data['soilhum_low_threshold']
airtemp_low = data['airtemp_low_threshold']
airhum_low = data['airhum_low_threshold']
ph_low = data['ph_low_threshold']
lum_low = data['luminance_low_threshold']

soilhum_high = data['soilhum_high_threshold']
airtemp_high = data['airtemp_high_threshold']
airhum_high = data['airhum_high_threshold']
ph_high = data['ph_high_threshold']

doBeep = data['buzzer_on']

board = ArduinoMega('/dev/ttyACM0')
board.analog[0].enable_reporting()
board.analog[1].enable_reporting()
board.analog[2].enable_reporting()
it = util.Iterator(board)
it.start()




water_sensor = LineSensor(9)
beeper = TonalBuzzer(12)

relay1 = DigitalOutputDevice(0, active_high=False) # Soil pump
relay2 = DigitalOutputDevice(1, active_high=False) # Ventilation fan
relay3 = DigitalOutputDevice(2, active_high=False) # UV lights
relay4= DigitalOutputDevice(3, active_high=False) # Sprinkler pump

relay1.off()
relay2.off()
relay3.off()
relay4.off()

beep(550.0, 0.25)

while True:         
    sensors_read()
    beep(500.0, 0.1)
    sleep(1)                             
 
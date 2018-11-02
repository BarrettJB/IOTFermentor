import time
import Adafruit_ADS1x15 as ads1x15
import numpy as np
import RPi.GPIO as GPIO
from math import log

#Takes value from ADC and returns temperature
def calculate_temperature(val)
    T0 = 298.15
    B = 3950
    R0 = 10000
    volt = num*(5/32768)
    Rt = (volt*10000)/(5-volt)
    T_inv = (1/T0) + (1/B)*log(Rt/10000)
    T = 1/T_inv
    return T;

adc = ads1x15.ADS1115()
GAIN = 1

#setup relay GPIO pin
GPIO.setup(25, GPIO.OUT)
GPIO.output(25, GPIO.HIGH)

#timer for data points
start = time.clock()

#file to write data into
file = open('tempData.txt','w')

print('Starting temperature controlled relay')
print('Measured Temperature')
shouldLoop = True

while shouldLoop:
    #take 10 measurements and average for better precision
    temps = np.zeros(10)
    for i in range(0,10):
        num = adc.read_adc(0,gain=GAIN)
        temps[i] = calculate_temperature(val)
    
    #get data and write to file
    avgTemp = np.mean(temps)
    ts = time.clock() - start;
    file.write("%f,\t%f" %(ts,avgTemp))
    print("%f,\t%f" %(ts,avgTemp))
    
    print(avgTemp)
    if (avgTemp > 40):
        shouldLoop = False
        
        
print('Temperature target reached')
GPIO.output(25,GPIO.LOW)
file.close()


    


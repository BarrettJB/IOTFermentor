import time
import Adafruit_ADS1x15 as ads1x15
import numpy as np
import RPi.GPIO as GPIO
from math import log

#Takes value from ADC and returns temperature
def calculate_temperature(val):
    T0 = 298.15
    Tk = 273.15
    B = 3950
    R0 = 10000
    volt = num*(5.0/32768)
    Rt = (volt*10000)/(5-volt)
    T_inv = (1.0/T0) + (1.0/B)*log(Rt/10000)
    T = (1.0/T_inv)-Tk 
    #print('|  %2.2fC | %5.1f | %1.5f |' % (T,Rt,volt))
    return T;

adc = ads1x15.ADS1115()
GAIN = 1

#setup relay GPIO pin
GPIO.setmode(GPIO.BCM)
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
        temps[i] = calculate_temperature(num)
    
    #get data and write to file
    avgTemp = np.mean(temps)
    ts = time.clock() - start;
    file.write("%f,\t%f\n" %(ts,avgTemp))
    print("%f,\t%f" %(ts,avgTemp))
    
    if (avgTemp > 65):
        shouldLoop = False;


        
print('Temperature target reached')
file.write("Tempreached")
GPIO.output(25,GPIO.LOW)
TimeStop = ts*2

while (ts < TimeStop):
    #take 10 measurements and average for better precision
    temps = np.zeros(10)
    for i in range(0,10):
        num = adc.read_adc(0,gain=GAIN)
        temps[i] = calculate_temperature(num)
    
    #get data and write to file
    avgTemp = np.mean(temps)
    ts = time.clock() - start;
    file.write("%f,\t%f\n" %(ts,avgTemp))
    print("%f,\t%f" %(ts,avgTemp))

file.close()


    


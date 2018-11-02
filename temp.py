import time
import Adafruit_ADS1x15 as ads1x15
from math import log

adc = ads1x15.ADS1115()
GAIN = 1

print('Reading out temperature, resistance, and voltage values')
print('|  Temp  |   R    |  Volt  |')

T0 = 298.15
Tk = 273.15
B = 3950
R0 = 10000

while True:
    num = adc.read_adc(0,gain=GAIN)
    volt = num*(5.0/32768)
    Rt = (volt*10000)/(5-volt)
    T_inv = (1.0/T0) + (1.0/B)*log(Rt/10000)
    T = (1.0/T_inv)-Tk
    print('|  %2.2fC | %5.1f | %1.5f |' % (T,Rt,volt))
    time.sleep(0.5)
    

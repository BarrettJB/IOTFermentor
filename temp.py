import time
import Adafruit_ADS1x15 as ads1x15
from math import log

adc = ads1x15.ADS1115()
GAIN = 1

print('Reading out temperature, resistance, and voltage values')
print('|  Temp  |   R    |  Volt  |')

T0 = 298.15
B = 3950
R0 = 10000

while True:
    num = adc.read(0,gain=GAIN)
    volt = num*(5/32768)
    Rt = (volt*10000)/(5-volt)
    T_inv = (1/T0) + (1/B)*log(Rt/10000)
    T = 1/T_inv
    print('|  %2.2f  | %5.1f | %1.5f |' % (T,Rt,volt))
    

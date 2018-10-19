import RPi.GPIO as GPIO
from flask import Flask, render_template, request

app = Flask(__name__)

GPIO.setmode(GPIO.BCM)

#Dictionary that holds pin number and state
pins = {
    23 : {'name' : 'Blue LED', 'state' : GPIO.LOW},
    24 : {'name' : 'Red LED', 'state' : GPIO.LOW},
    25 : {'name' : 'Relay', 'state' : GPIO.LOW}
    }
    
#Set each pin to output mode and lower
for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    
@app.route('/')
def main():
    #Read pin state and store in the dict
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
        
    templateData = {
        'pins' : pins
    }
    
    #pass pin data to the html file
    return render_template('main.html',**templateData)
 
@app.route('/<changePin>/<action>')
def action(changePin, action):
    changePin = int(changePin)
    deviceName = pins[changePin]['name']
    #if action in URL is on then
    if action == 'on':
        GPIO.output(changePin, GPIO.HIGH)
        message = "Turned " + deviceName + " on."
        
    if action == 'off':
        GPIO.output(changePin,GPIO.LOW)
        message = "Turned " + deviceName + " off."
        
    #update states
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    
    templateData = {
        'pins' : pins
    }
    
    #pass pin data to the html file
    return render_template('main.html',**templateData)
   
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
  
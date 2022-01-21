#All imports
from flask import Flask,redirect,render_template
import time, argparse, board, neopixel
from rpi_ws281x import *
from math import *

###############################################
#
#   Raspberry Pi - ws2812 led strip controller
#
#   Author : Allan R.
#   Version : v1.0
#   
#
#   Variable you need to change :
LED_COUNT      = 143                # Number of leds that your strip have
LED_PIN        = 18                 # GPIO pin where your strip is plugged
piHost         = "192.168.1.116"    # IP / Hostname of the raspberry that host this script
###############################################

#Set needed variable
app= Flask(__name__)
isOn = False
isStopped = False
whileOn = True


temp = True
pixels = neopixel.NeoPixel(board.D18, 143)

# Define function to do a wipe animation
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Define function to show a static color without animation
def colorStatic(color):
    pixels.fill((color))

# Define function that generate rainbow colors for the rainbow effect
def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

# Define function for the rainbow effect
def rainbow(strip, wait_ms=20, iterations=1):
    for j in range(256*iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i+j) & 255))
        strip.show()
        time.sleep(wait_ms/1000.0)
    print(str(whileOn) + "7")
    if whileOn == False:
        print(str(whileOn) + "8")
        return True

# Define main function that manage all leds effects calls
def ledControl(action, isOn, brightness, last, rgbColors=None):
    print(str(whileOn) + "1")
    if isOn:
        whileOn = True
    else:
        whileOn = False

    def stopCheck(stopVar, actualStop=True):
        if stopVar == "check":
            return actualStop

    def stopFunc():
        return stopCheck("check")

    #When OFF button pressed
    if action == "off":
        whileOn = False
        print(str(whileOn) + "3")
        #ledControl("w-bluepurple", False, None, None)
        #ledControl("rainbow", False, None, None)
        pixels.fill((0, 0, 0))

    #When brightness is changed
    if brightness != None:
        floatBr = float(brightness / 255)
        strip.setBrightness(brightness)
        pixels.brightness = floatBr
        strip.begin()
        return redirect("/"+last, code=302)

    #When static color buttons pressed
    if action == "red":
        colorStatic(Color(255, 0, 0))
    if action == "green":
        colorStatic(Color(0, 255, 0))
    if action == "blue":
        colorStatic(Color(0, 0, 255))

    #When Rainbow effect button pressed
    if action == "rainbow":
        print(str(whileOn) + "4")
        while whileOn:
            rainbow(strip)
            whileOn = stopCheck("check", isOn)
            
    #When wipe between blue and purple effect button pressed
    if action == "w-bluepurple":
        while whileOn:
            colorWipe(strip, Color(50, 50, 255))
            colorWipe(strip, Color(230, 0, 255))

    #When RGB color sliders are set manually
    if action == "RGB":
        colorStatic(rgbColors)

# LED strip configuration. Normally you don't need to change anything :
LED_FREQ_HZ    = 800000     # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10         # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50         # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0          # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Main program logic follows:
if __name__ == '__main__':
    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

# Listen to all GET requests to customs URLs and call needed functions
@app.route('/')
def index(): return render_template('webpage.html')

@app.route('/A')
def routeA(): ledControl("red", False, None, None); return render_template('webpage.html')

@app.route('/a')
def routea(): ledControl("green", False, None, None); return render_template('webpage.html')

@app.route('/B')
def routeB(): ledControl("blue", False, None, None); return render_template('webpage.html')

@app.route('/b')
def routeb(): ledControl("w-bluepurple", True, None, None); return render_template('webpage.html')

@app.route('/C')
def routeC(): ledControl("rainbow", True, None, None); return render_template('webpage.html')

@app.route('/c')
def routec(): ledControl("off", False, None, None); return render_template('webpage.html')

@app.route('/bri/<brightness>/<last>')
def routeBri(brightness, last): ledControl("blue", False, int(brightness), last); return render_template('webpage.html')

@app.route('/rgb/<r>-<g>-<b>')
def routeRGB(r, g, b): ledControl("RGB", False, None, None, Color(int(r), int(g), int(b))); return render_template('webpage.html')

#Start the Flask website
if __name__=="__main__":
    print("Start")
    app.run(debug=False, host=piHost)

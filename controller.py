from flask import Flask
from flask import render_template
import time
from rpi_ws281x import *
import argparse

app= Flask(__name__)
isOn = False


# LED strip configuration:
LED_COUNT      = 143      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
#LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 50     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000.0)

# Main program logic follows:
if __name__ == '__main__':
    # Process arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--clear', action='store_true', help='clear the display on exit')
    args = parser.parse_args()

    # Create NeoPixel object with appropriate configuration.
    strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()

    print ('Press Ctrl-C to quit.')
    if not args.clear:
        print('Use "-c" argument to clear LEDs on exit')

@app.route('/')
def index():
    return render_template('webpage.html')

@app.route('/A')
def led1on():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, (255, 0, 0))
        strip.show()
        time.sleep(0/1000.0)
    return render_template('webpage.html')

@app.route('/a')
def led1off():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, (0, 255, 0))
        strip.show()
        time.sleep(0/1000.0)
    return render_template('webpage.html')

@app.route('/B')
def led2on():
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, (0, 0, 255))
        strip.show()
        time.sleep(0/1000.0)
    return render_template('webpage.html')

@app.route('/b')
def led2off():
    isOn = True
    while isOn:
        print ('Color wipe animations.')
        colorWipe(strip, Color(50, 50, 255))  # Violet wipe
        colorWipe(strip, Color(230, 0, 255))  # Blue wipe
    return render_template('webpage.html')

@app.route('/C')
def led3on():
    return render_template('webpage.html')

@app.route('/c')
def led3off():
    isOn = False
    colorWipe(strip, Color(0,0,0), 5)
    return render_template('webpage.html')

if __name__=="__main__":
    print("Start")
    app.run(debug=True, host='192.168.1.116')

# rpiLedWebController

Raspberry Led Web Controller is simply a webpage that can command your Neopixel led strip (or any another ws2812 led strip).

## Prerequisites

- Python 3
- PIP3

##Wiring guide

**add images**

## Installation
### Part 1 (Prerequisites for the ledstrip)

**1.** Update package list
```bash
sudo apt-get update
```

**2.** Install needed package to compile needed files
```bash
sudo apt-get install gcc make build-essential python-dev git scons swig
```

**3.** Disable the Audio output (mandatory idk why) :  
Edit this conf file
```bash
sudo nano /etc/modprobe.d/snd-blacklist.conf
```
And add this line on it. Save it and close it
```bash
blacklist snd_bcm2835
```

**4.** Disable the Audio output on the Boot conf file too :  
Edit this conf file
```bash
sudo nano /boot/config.txt
```

Search these lines and un-comment the 2nd line. it should look like this :
```bash
# Enable audio (loads snd_bcm2835)
dtparam=audio=on
```
Save it and close it

**5.** Reboot the system
```bash
sudo reboot
```

**6.** Download the needed library to use the ws281x led strips :
```bash
git clone https://github.com/jgarff/rpi_ws281x
```

**7.** Compile the library :
```bash
cd rpi_ws281x/
sudo scons
```
**8.** Install the python libray
```bash
cd python
sudo python3 setup.py build 
sudo python3 setup.py install 
sudo pip3 install adafruit-circuitpython-neopixel
```

### Part 2 (Webserver)

**1.** Clone this repository
```bash
git clone https://github.com/resal1510/rpiLedWebController.git
```
**TO CONTINUE**

## Usage

```python
python3 controller.py

Please have a look at https://github.com/AndresGarelli/Larva_Tracking_OpenCV for a new code that simultaneously records and tracks larval behavior.


This is a modification of FlyPi, a Raspberry Pi based platform for imaging experiments (https://github.com/amchagas/Flypi original article: http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.2002702)

FlyPi-Pupariation was designed to allow monitoring of Drosophila larval behavior over long periods of time. The platform has been adapted for optogenetic manipulation of individual larvae.

The RPi controls the camera and LED illumination (optogenetics, Campari and white and IR illumination), making an aditional Arduino microcontroller unnecessary.

FlyPi and FlyPi-pupariation had been designed for and tested in Raspberry Pi 3 and 4 running Raspberry Pi OS.

Download all the files as a single zip file clicking on the green "Code" button on the right hand side of the main page.
That file will also contain an example video of Drosophila larvae expressing GCAMP in muscle cells.

INSTALLATION

The installation of FlyPi is straightforward and should take no more than 5-10 minutes.

1- Install the picamera and w1thermsensor packages usign apt in a terminal window with the following commands:

- sudo apt-get update
- sudo apt-get install python3-picamera
- sudo apt-get install python3-w1thermsensor

2- Copy all files, except Flypi.desktop, in a folder somewhere in your disc.

3- Copy Flypi.desktop in the desktop. Open Flypi.desktop in text editor and modify the line reading Exec=/home/pi/Desktop/Flypi-master/Python/run.py to indicate the path to the file "run.py" in your RPi.

You need to make run.py executable. Open terminal, go to the folder where you placed run.py and write sudo chmod +x run.py

(or Google for instructions)

4- Enable GPIO and 1-wire in the "interfaces" menu of configuration of your RPi: Preferences menu>>Interfaces

5- If you are using a DS18B20 temperature sensor, connect the DATA pin to pin 7 of Raspberry connector (GPIO4) and to 5V with a  4.7 kOhm pull-up resistor. You can change to other pin modifying in /boot/config.txt this line: dtoverlay=w1-gpio to this dtoverlay=w1-gpio,gpiopin=x changing x for the GPIO number you choose.(use GPIO number, not the number of pin in the connector). You can get the GPIO numbers googling "raspberry pinout"
Connect the Vin and GND pins of the sensor to any 5V and GND pins of the board.
You can find more information on w1thermsensor package here:https://github.com/timofurrer/w1thermsensor/blob/master/README.md
Connecting a DS18B20 sensor (step 5) is not mandatory. The software will still run if it does not find a sensor.

6- Once you completed these steps, you should be able to open Flypi-Pupariation from the icon in the desktop

in order to block the message asking what to do with the file when you open Flypi, open the file manager (the yellow icon with two folders), Edit, preferences, General and select the option "no mostrar opciones al abrir archivos ejecutables" (do not show options when opening executable files, or something like that)

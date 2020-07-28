# FlyPi-Pupariation

This is a modification of the FlyPi platform for imaging experiments (https://github.com/amchagas/Flypi original article: http://journals.plos.org/plosbiology/article?id=10.1371/journal.pbio.2002702)

The RPi controls the camera and LED illumination (optogenetics, Campari and white and IR illumination), making an aditional Arduino microcontroller unnecessary. 

INSTALLATION

copy all files, except Flypi.desktop, in a folder somewhere in your disc.

copy Flypi.desktop in the desktop
open Flypi.desktop in text editor and modify accordingly:

[Desktop Entry]
Name=FlyPi
Comment= FlyPi will control the camera and LEDs
Icon=/usr/share/pixmaps/openbox.xpm (you should indicate here the path to some image)
Exec=/home/pi/Desktop/Flypi-master/Python/run.py  (indicate the path to the file "run.py")
Type=Application
Encoding=UTF-8
Terminal=false
Categories=None;

you need to make run.py executable. 
open terminal, go to the folder and write sudo chmod +x run.py

or Google for instructions

enable GPIO in the "interfaces" menu of configuration of your RPi:
Preferences menu>>Interfaces


TEMPERATURE SENSOR

install w1thermsensor writing the following line in a terminal window:
sudo apt-get install python3-w1thermsensor

enable GPIO and 1-wire in the "interfaces" menu of configuration:
Preferences menu>>Interfaces
connect the DATA pin of the DS18B20 temperature sensor to pin 7 of Raspberry connector (GPIO4). You can change to other pin modifying in /boot/config.txt this line:
dtoverlay=w1-gpio
to this
dtoverlay=w1-gpio,gpiopin=x.

changing x for the GPIO number you choose.(use GPIO number, not the number of pin in the connector). You can get the GPIO numbers googling "raspberry pinout"

more information here:https://github.com/timofurrer/w1thermsensor/blob/master/README.md



Once you completed these steps, you should be able to open Flypi-Pupariation from the icon in the desktop



in order to block the message asking what to do with the file when you open Flypi, open the file manager (the yellow icon with two folders), Edit, preferences, General and select the option "no mostrar opciones al abrir archivos ejecutables" (do not show options when opening executable files, or something like that)

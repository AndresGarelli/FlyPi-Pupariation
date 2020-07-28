    ######################################## Mockup
import tkinter as tk
#from tkinter import*
import RPi.GPIO as GPIO
import time
import tkinter.font


class Illumination:

    def __init__(self, parent="none", label="White",
                 prot=False, protFrame="",
                 #ser=""
                 ):

        #bare minimum 
        self.label = label
       
        self.IlluminationLabel = tk.Label(master=parent, text=self.label)
        self.IlluminationLabel.pack(fill="y")
        #include ability to interact with serial port
        #self.ser = ser

        #create buttons or other tools for GUI
#        self.onButt = tk.Button(master=parent,
#                                   text="ON", fg="green",
#                                   command=self.on)
#
#        self.onButt.pack(fill="x")
#
#        self.offButt = tk.Button(master=parent,
#                                    text="OFF",
#                                    fg="RED",
#                                    command=self.off)
#
#        self.offButt.pack(fill="x")
        
        LedBlancoInf = 17 #physical 11 # pin11
        LedBlancoSup = 18 #physical 12
        LedIR = 27 #physical 13
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # We are accessing GPIOs according to their physical location
        chan_list = [17,18,27]
        GPIO.setup(chan_list, GPIO.OUT) # We have set our LED pin mode to output
        GPIO.output(chan_list, GPIO.LOW) # When it will start then LED will be OFF
        #Font1 = tkinter.font.Font(family = 'Calibri', size = 10, weight = 'bold')

        #self.Text1 = tk.Label(master=parent,text='LED blanco superior', font = Font1, fg='black', padx = 10, pady = 10)
        
        self.Scale1= tk.Scale (master=parent, from_=0, to = 100, orient = tk.HORIZONTAL, resolution = 10, command = self.pwmBlancoSup)
        #self.Scale1.grid (row=0, column=1)
        self.Scale1.pack (fill="y") 
        self.Text1 = tk.Label(master=parent,text='White TOP\npin12', fg='black', padx = 5, pady = 5)
#self.Text1.grid(row=0,column=0)
        self.Text1.pack(fill="y")
        
        
        self.Scale2= tk.Scale (master=parent, from_=0, to = 100, orient = tk.HORIZONTAL, resolution = 10, command = self.pwmBlancoInf)
        #self.Scale2.grid (row=1, column=1)
        self.Scale2.pack (fill="y")
#        self.Text2 = tk.Label(master=parent,text='LED blanco inferior', font = Font1, fg='black', padx = 10, pady = 10)
        self.Text2 = tk.Label(master=parent,text='White BOTTOM\npin11', fg='black', padx = 5, pady = 5)
        #self.Text2.grid(row=1,column=0)
        self.Text2.pack(fill="y")

        self.Scale3= tk.Scale (master=parent, from_=0, to = 100, orient = tk.HORIZONTAL, resolution = 10, command = self.pwmIR)
        #self.Scale2.grid (row=1, column=1)
        self.Scale3.pack (fill="y")
#        self.Text2 = tk.Label(master=parent,text='LED blanco inferior', font = Font1, fg='black', padx = 10, pady = 10)
        self.Text3 = tk.Label(master=parent,text='IR - pin13', fg='black', padx = 5, pady = 5)
        #self.Text2.grid(row=1,column=0)
        self.Text3.pack(fill="y")


        self.PwmValue1 = GPIO.PWM(LedBlancoSup, 1000)
        self.PwmValue1.start (0)

        self.PwmValue2 = GPIO.PWM(LedBlancoInf, 1000)
        self.PwmValue2.start (0)

        self.PwmValue3 = GPIO.PWM(LedIR, 1000)
        self.PwmValue3.start (0)

    def pwmBlancoSup(self,valor):
        valor=self.Scale1.get()
        self.PwmValue1.ChangeDutyCycle(valor)

    def pwmBlancoInf(self,valor2):
        valor2=self.Scale2.get()
        self.PwmValue2.ChangeDutyCycle(valor2)

    def pwmIR(self,valor3):
        valor3=self.Scale3.get()
        self.PwmValue3.ChangeDutyCycle(valor3)
        
#def botonSalir():
#    GPIO.cleanup()
#    arena.destroy()


        
#    #callbacks for buttons
#
#    def on(self):
#        output = "on button pressed"
#        print(output)
#        #return 
#    
#    def off(self):
#        output = "off button pressed"
#        print(output)
#        #return 

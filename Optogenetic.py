    ######################################## Mockup
import tkinter as tk
#from tkinter import*
import RPi.GPIO as GPIO
import time
import tkinter.font
import threading


class Optogenetic:

    def __init__(self, parent="none", label="OPTOGENETIC",
                 prot=False, protFrame="",
                 #ser=""
                 ):

        self.LEDVar= tk.IntVar()
        #bare minimum
        
        self.optoParent = parent
        ###frames for all opto controls
        self.frame1 = tk.Frame(master=self.optoParent, bd=2, relief="ridge")
        self.frame1.grid(row=0, column=0,
                            columnspan=4, rowspan=4,
                            sticky="N")
        frame2 = tk.Frame(master=self.frame1 , bd=2, relief="ridge")
        frame2.grid(row=1, column=0, columnspan=6, rowspan=3, sticky="S")
        
        
#        
        self.label = label
       
        self.OptogeneticLabel = tk.Label(master=self.frame1, text=self.label)
        self.OptogeneticLabel.grid(row=0,column=0, columnspan=1, sticky="ESN")

        self.ScaleLEDs= tk.Scale (master=self.frame1, from_=0, to = 100, orient = tk.HORIZONTAL, resolution = 10)
        self.ScaleLEDs.grid (row=0, column=4, sticky="W")
        self.ScaleLEDs.set(100)
        
        self.TextLEDs = tk.Label(master=self.frame1,text='intensity', fg='black', padx = 5, pady = 5)
        self.TextLEDs.grid(row=0,column=3, sticky="SE")
        
      #create buttons or other tools for GUI

#        self.emptyLabel = tk.Label(master=self.frame1, text=" ")
#        self.emptyLabel.grid(row=1, column=1, sticky="s")        

        self.Fila1ONLabel = tk.Label(master=frame2, text="ON (sec)")
        self.Fila1ONLabel.grid(row=1, column=0, sticky="e")
        
        self.Fila1cycleLabel = tk.Label(master=frame2, text="cycle (sec)")
        self.Fila1cycleLabel.grid(row=2, column=0, sticky="e")

        self.Fila1repeatLabel = tk.Label(master=frame2, text="repeat (0=24hr)")
        self.Fila1repeatLabel.grid(row=3, column=0, sticky="e")

        self.emptyLabel = tk.Label(master=frame2, text=" ")
        self.emptyLabel.grid(row=4, rowspan=2, column=0, sticky="WE")        

        self.emptyLabel3 = tk.Label(master=frame2, text=" ")
        self.emptyLabel3.grid(row=7,  column=4, sticky="WE")
        
        self.emptyLabel2 = tk.Label(master=frame2, text=" ")
        self.emptyLabel2.grid(row=6, columnspan=5, column=0, sticky="WE")
        
        self.Fila2ONLabel = tk.Label(master=frame2, text="ON (sec)")
        self.Fila2ONLabel.grid(row=8, column=0, sticky="e")
        
        self.Fila2cycleLabel = tk.Label(master=frame2, text="cycle (sec)")
        self.Fila2cycleLabel.grid(row=9, column=0, sticky="e")

        self.Fila2repeatLabel = tk.Label(master=frame2, text="repeat (0=24hr)")
        self.Fila2repeatLabel.grid(row=10, column=0, sticky="e")
        
        #GPIO
        
        self.LED1 = 13 #physical 33 # pin11
        self.LED2 = 19 #physical 35
        self.LED3 = 26 #physical 37
        self.LED4= 16 #physical 36
        self.LED5 = 20 #physical 38
        self.LED6= 21 #physical 40
        
        
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        # We are accessing GPIOs according to their physical location
        
        chan_list = [13,19,26,16,20,21]
        GPIO.setup(chan_list, GPIO.OUT) # We have set our LED pin mode to output
        GPIO.output(chan_list, GPIO.LOW) # When it will start then LED will be OFF

        self.PWMLED1 = GPIO.PWM(self.LED1,1000)
        self.PWMLED2 = GPIO.PWM(self.LED2,1000)
        self.PWMLED3 = GPIO.PWM(self.LED3,1000)
        self.PWMLED4 = GPIO.PWM(self.LED4,1000)
        self.PWMLED5 = GPIO.PWM(self.LED5,1000)
        self.PWMLED6 = GPIO.PWM(self.LED6,1000)
        

#

        #LED1
        self.LED1Label = tk.Label(master=frame2, text="LED1\n[pin 33]",fg="blue")
        self.LED1Label.grid(row=0, column=1, columnspan=1,sticky="N")
    
        self.LED1ON = tk.Entry(master=frame2, width=4)
        self.LED1ON.grid(row=1, column=1, sticky="N")
        self.LED1ON.insert(0, 0.25)
        
        self.LED1cycle = tk.Entry(master=frame2, width=4)
        self.LED1cycle.grid(row=2, column=1, sticky="N")
        self.LED1cycle.insert(0, 1)        
        
        self.LED1repeat = tk.Entry(master=frame2, width=4)
        self.LED1repeat.grid(row=3, column=1, sticky="N")
        self.LED1repeat.insert(0, 1)
        
        self.LED1button = tk.Button(master=frame2,
                                  text="START", fg="black",
                                  command=self.threadBotonLED1)
        self.LED1button.grid(row=4, column=1, columnspan=1,sticky="WEN")
        
        self.stop1=tk.IntVar()
        self.LED1STOPbutton = tk.Checkbutton(master=frame2,
                                  text="STOP", fg="black",variable=self.stop1, indicatoron=False)
        self.LED1STOPbutton.grid(row=5, column=1, columnspan=1,sticky="WE")

        #LED2

        self.LED2Label = tk.Label(master=frame2, text="LED2\n[pin 35]",fg="blue")
        self.LED2Label.grid(row=0, column=2, columnspan=1,sticky="N")
    
        self.LED2ON = tk.Entry(master=frame2, width=4)
        self.LED2ON.grid(row=1, column=2, sticky="N")
        self.LED2ON.insert(0, 0.25)
        
        self.LED2cycle = tk.Entry(master=frame2, width=4)
        self.LED2cycle.grid(row=2, column=2, sticky="N")
        self.LED2cycle.insert(0, 1)        
        
        self.LED2repeat = tk.Entry(master=frame2, width=4)
        self.LED2repeat.grid(row=3, column=2, sticky="N")
        self.LED2repeat.insert(0, 1)
        
        self.LED2button = tk.Button(master=frame2,
                                  text="START", fg="black",
                                  command=self.threadBotonLED2)
        self.LED2button.grid(row=4, column=2, columnspan=1,sticky="WEN")
        
        self.stop2=tk.IntVar()
        self.LED2STOPbutton = tk.Checkbutton(master=frame2,
                                  text="STOP", fg="black",variable=self.stop2, indicatoron=False)
        self.LED2STOPbutton.grid(row=5, column=2, columnspan=1,sticky="WE")
        
        #LED3

        self.LED3Label = tk.Label(master=frame2, text="LED3\n[pin 37]",fg="blue")
        self.LED3Label.grid(row=0, column=3, columnspan=1,sticky="N")
    
        self.LED3ON = tk.Entry(master=frame2, width=4)
        self.LED3ON.grid(row=1, column=3, sticky="N")
        self.LED3ON.insert(0, 0.25)
        
        self.LED3cycle = tk.Entry(master=frame2, width=4)
        self.LED3cycle.grid(row=2, column=3, sticky="N")
        self.LED3cycle.insert(0, 1)        
        
        self.LED3repeat = tk.Entry(master=frame2, width=4)
        self.LED3repeat.grid(row=3, column=3, sticky="N")
        self.LED3repeat.insert(0, 1)
        
        self.LED3button = tk.Button(master=frame2,
                                  text="START", fg="black",
                                  command=self.threadBotonLED3)
        self.LED3button.grid(row=4, column=3, columnspan=1,sticky="WEN")
        
        self.stop3=tk.IntVar()
        self.LED3STOPbutton = tk.Checkbutton(master=frame2,
                                  text="STOP", fg="black",variable=self.stop3, indicatoron=False)
        self.LED3STOPbutton.grid(row=5, column=3, columnspan=1,sticky="WE")
        
        #LED4     

        self.LED4Label = tk.Label(master=frame2, text="LED4\n[pin 36]",fg="blue")
        self.LED4Label.grid(row=7, column=1, columnspan=1,sticky="N")
    
        self.LED4ON = tk.Entry(master=frame2, width=4)
        self.LED4ON.grid(row=8, column=1, sticky="N")
        self.LED4ON.insert(0, 0.25)
        
        self.LED4cycle = tk.Entry(master=frame2, width=4)
        self.LED4cycle.grid(row=9, column=1, sticky="N")
        self.LED4cycle.insert(0, 1)        
        
        self.LED4repeat = tk.Entry(master=frame2, width=4)
        self.LED4repeat.grid(row=10, column=1, sticky="N")
        self.LED4repeat.insert(0, 1)
        
        self.LED4button = tk.Button(master=frame2,
                                  text="START", fg="black",
                                  command=self.threadBotonLED4)
        self.LED4button.grid(row=11, column=1, columnspan=1,sticky="WEN")
        
        self.stop4=tk.IntVar()
        self.LED4STOPbutton = tk.Checkbutton(master=frame2,
                                  text="STOP", fg="black",variable=self.stop4, indicatoron=False)
        self.LED4STOPbutton.grid(row=12, column=1, columnspan=1,sticky="WE")

        
        #LED5
        
        self.LED5Label = tk.Label(master=frame2, text="LED5\n[pin 38]",fg="blue")
        self.LED5Label.grid(row=7, column=2, columnspan=1,sticky="N")
    
        self.LED5ON = tk.Entry(master=frame2, width=4)
        self.LED5ON.grid(row=8, column=2, sticky="N")
        self.LED5ON.insert(0, 0.25)
        
        self.LED5cycle = tk.Entry(master=frame2, width=4)
        self.LED5cycle.grid(row=9, column=2, sticky="N")
        self.LED5cycle.insert(0, 1)        
        
        self.LED5repeat = tk.Entry(master=frame2, width=4)
        self.LED5repeat.grid(row=10, column=2, sticky="N")
        self.LED5repeat.insert(0, 1)
        
        self.LED5button = tk.Button(master=frame2,
                                  text="START", fg="black",
                                  command=self.threadBotonLED5)
        self.LED5button.grid(row=11, column=2, columnspan=1,sticky="WEN")
        
        self.stop5=tk.IntVar()
        self.LED5STOPbutton = tk.Checkbutton(master=frame2,
                                  text="STOP", fg="black",variable=self.stop5, indicatoron=False)
        self.LED5STOPbutton.grid(row=12, column=2, columnspan=1,sticky="WE")        
        
        
        #LED6

        self.LED6Label = tk.Label(master=frame2, text="LED6\n[pin 40]",fg="blue")
        self.LED6Label.grid(row=7, column=3, columnspan=1,sticky="N")
    
        self.LED6ON = tk.Entry(master=frame2, width=4)
        self.LED6ON.grid(row=8, column=3, sticky="N")
        self.LED6ON.insert(0, 0.25)
        
        self.LED6cycle = tk.Entry(master=frame2, width=4)
        self.LED6cycle.grid(row=9, column=3, sticky="N")
        self.LED6cycle.insert(0, 1)        
        
        self.LED6repeat = tk.Entry(master=frame2, width=4)
        self.LED6repeat.grid(row=10, column=3, sticky="N")
        self.LED6repeat.insert(0, 1)
        
        self.LED6button = tk.Button(master=frame2,
                                  text="START", fg="black",
                                  command=self.threadBotonLED6)
        self.LED6button.grid(row=11, column=3, columnspan=1,sticky="WEN")
        
        self.stop6=tk.IntVar()
        self.LED6STOPbutton = tk.Checkbutton(master=frame2,
                                  text="STOP", fg="black",variable=self.stop6, indicatoron=False)
        self.LED6STOPbutton.grid(row=12, column=3, columnspan=1,sticky="WE")
        
        
        
        #START ALL button
        self.Allbutton = tk.Button(master=frame2,
                                  text="START\nALL", fg="green",
                                  command=self.ThreadALL)
        self.Allbutton.grid(row=1, column=4, rowspan=5,sticky="NS")
        
        
        #STOP ALL button
        self.StopAllbutton = tk.Button(master=frame2,
                                  text="STOP\nALL", fg="red",command=self.stopALL)
        self.StopAllbutton.grid(row=8, column=4,rowspan=5, columnspan=1,sticky="NS")
#        self.onButt = tk.Button(master=self.optoFrame1,
#                                   text="ON", fg="green",
#                                   command=self.on)
#
#        self.onButt.pack(fill="x")
#
#        self.offButt = tk.Button(master=self.optoFrame1,
#                                    text="OFF",
#                                    fg="RED",
#                                    command=self.off)
#
#        self.offButt.pack(fill="x")
#        
#
#        self.PwmValue1 = GPIO.PWM(LedBlancoSup, 1000)
#        self.PwmValue1.start (0)
#
#        self.PwmValue2 = GPIO.PWM(LedBlancoInf, 1000)
#        self.PwmValue2.start (0)

#Functions for LED1    
    def LED1start(self):
        valON=float(self.LED1ON.get())
        valCycle=float(self.LED1cycle.get())
        valRepeat=int(self.LED1repeat.get())
        if valRepeat==0:
            valRepeat=86400
        print(valON,valCycle,valRepeat)
        OFFtime=valCycle - valON
        cycle=0
        self.stop1.set(False)
        stop=self.stop1.get()
        while cycle < valRepeat and stop==False:
            intensidad=self.ScaleLEDs.get()
            print(intensidad)
            self.PWMLED1.start(intensidad)
            time.sleep(float(valON))
            self.PWMLED1.stop()
            time.sleep(OFFtime)
            cycle +=1
            stop=self.stop1.get()
        time.sleep(1)
        self.stop1.set(False)
        print("FIN LED1")
          
    def threadBotonLED1(self):
        threading.Thread(target=self.LED1start).start()
        
 
#Functions for LED2    
    def LED2start(self):
        valON=float(self.LED2ON.get())
        valCycle=float(self.LED2cycle.get())
        valRepeat=int(self.LED2repeat.get())
        if valRepeat==0:
            valRepeat=86400
        print(valON,valCycle,valRepeat)
        OFFtime=valCycle - valON
        cycle=0
        self.stop2.set(False)
        stop=self.stop2.get()
        while cycle < valRepeat and stop==False:    
            intensidad=self.ScaleLEDs.get()
            print(intensidad)
            self.PWMLED2.start(intensidad)
            time.sleep(float(valON))
            self.PWMLED2.stop()
            time.sleep(OFFtime)
            cycle +=1
            stop=self.stop2.get()
        time.sleep(1)
        self.stop2.set(False)
        print("FIN LED2")
          
    def threadBotonLED2(self):
        threading.Thread(target=self.LED2start).start()

    
#Functions for LED3    
    def LED3start(self):
        valON=float(self.LED3ON.get())
        valCycle=float(self.LED3cycle.get())
        valRepeat=int(self.LED3repeat.get())
        if valRepeat==0:
            valRepeat=86400
        print(valON,valCycle,valRepeat)
        OFFtime=valCycle - valON
        cycle=0
        self.stop3.set(False)
        stop=self.stop3.get()
        while cycle < valRepeat and stop==False:    
            intensidad=self.ScaleLEDs.get()
            print(intensidad)
            self.PWMLED3.start(intensidad)
            time.sleep(float(valON))
            self.PWMLED3.stop()
            time.sleep(OFFtime)
            cycle +=1
            stop=self.stop3.get()
        time.sleep(1)
        self.stop3.set(False)
        print("FIN LED3")
          
    def threadBotonLED3(self):
        threading.Thread(target=self.LED3start).start()  
    
    
#Functions for LED4    
    def LED4start(self):
        valON=float(self.LED4ON.get())
        valCycle=float(self.LED4cycle.get())
        valRepeat=int(self.LED4repeat.get())
        if valRepeat==0:
            valRepeat=86400
        print(valON,valCycle,valRepeat)
        OFFtime=valCycle - valON
        cycle=0
        self.stop4.set(False)
        stop=self.stop4.get()
        while cycle < valRepeat and stop==False:    
            intensidad=self.ScaleLEDs.get()
            print(intensidad)
            self.PWMLED4.start(intensidad)
            time.sleep(float(valON))
            self.PWMLED4.stop()
            time.sleep(OFFtime)
            cycle +=1
            stop=self.stop4.get()
        time.sleep(1)
        self.stop4.set(False)
        print("FIN LED4")
          
    def threadBotonLED4(self):
        threading.Thread(target=self.LED4start).start()   
    
    
#Functions for LED5    
    def LED5start(self):
        valON=float(self.LED5ON.get())
        valCycle=float(self.LED5cycle.get())
        valRepeat=int(self.LED5repeat.get())
        if valRepeat==0:
            valRepeat=86400
        print(valON,valCycle,valRepeat)
        OFFtime=valCycle - valON
        cycle=0
        self.stop5.set(False)
        stop=self.stop5.get()
        while cycle < valRepeat and stop==False:    
            intensidad=self.ScaleLEDs.get()
            print(intensidad)
            self.PWMLED5.start(intensidad)
            time.sleep(float(valON))
            self.PWMLED5.stop()
            time.sleep(OFFtime)
            cycle +=1
            stop=self.stop5.get()
        time.sleep(1)
        self.stop5.set(False)
        print("FIN LED5")
          
    def threadBotonLED5(self):
        threading.Thread(target=self.LED5start).start()    
    
    
#Functions for LED6    
    def LED6start(self):
        valON=float(self.LED6ON.get())
        valCycle=float(self.LED6cycle.get())
        valRepeat=int(self.LED6repeat.get())
        if valRepeat==0:
            valRepeat=86400
        print(valON,valCycle,valRepeat)
        OFFtime=valCycle - valON
        cycle=0
        self.stop6.set(False)
        stop=self.stop6.get()
        while cycle < valRepeat and stop==False:    
            intensidad=self.ScaleLEDs.get()
            print(intensidad)
            self.PWMLED6.start(intensidad)
            time.sleep(float(valON))
            self.PWMLED6.stop()
            time.sleep(OFFtime)
            cycle +=1
            stop=self.stop6.get()
        time.sleep(1)
        self.stop6.set(False)
        print("FIN LED6")
          
    def threadBotonLED6(self):
        threading.Thread(target=self.LED6start).start()
    
    
    
    
    def ThreadALL(self):
        threading.Thread(target=self.LED1start).start()
        threading.Thread(target=self.LED2start).start()
        threading.Thread(target=self.LED3start).start()
        threading.Thread(target=self.LED4start).start()
        threading.Thread(target=self.LED5start).start()
        threading.Thread(target=self.LED6start).start()
        
    def stopALL(self):
        self.stop1.set(True)
        self.stop2.set(True)
        self.stop3.set(True)
        self.stop4.set(True)        
        self.stop5.set(True)
        self.stop6.set(True)        
    
 
#        
#        
#    def pwmBlancoSup(self,valor):
#        valor=self.Scale1.get()
#        self.PwmValue1.ChangeDutyCycle(valor)
#
#    def pwmBlancoInf(self,valor2):
#        valor2=self.Scale2.get()
#        self.PwmValue2.ChangeDutyCycle(valor2)



#def botonSalir():
#    GPIO.cleanup()
#    arena.destroy()


        
    #callbacks for buttons


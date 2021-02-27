import tkinter as tk
from tkinter import *
import RPi.GPIO as GPIO
import os
import time
#import serial module
try:
    import serial
    serialAvail = True

except ImportError:
    serialAvail = False
    print ("serial module not available!")
    print ("user interface will not control flypi!")


var2 = 0

class App:

    def __init__(self, master):

        frame = tk.Frame(master)
        frame.pack()

        self.var = IntVar()
        self.c = Checkbutton(frame, text="Check box to use CAMPARI setup or\n leave unchecked for standard setup", variable=self.var, command=self.setup)
        self.var.set(0)
        self.c.pack()
        
        self.button = Button(
            frame, text="CONTINUE", fg="red", command=frame.quit
            )
        self.button.pack(side=BOTTOM)
        #global var


    
    def setup(self):
        global var2
        var2= self.var.get()
        #print(self.var)
        print(var2)
        
#print(var2)
root = tk.Tk()

app = App(root)

root.mainloop()
root.destroy()

class flypiApp:
    #global ser
    #filepath for output:
    basePath = '/home/pi/Desktop/LARVAS/'


    #use these flags to make whole pieces of the GUI disappear
    if var2 == 0:
        Optogenetic = 1
        CAMPARI = 0
    elif var2 == 1:
        Optogenetic = 0
        CAMPARI = 1
        
    cameraFlag = 1
    ringFlag = 0
    led1Flag = 0
    led2Flag = 0
    matrixFlag = 0
    #Optogenetic =1
    peltierFlag = 0
    autofocusFlag = 0
    Illumination=1
    mockupFlag = 0
    protocolFlag = 0
    quitFlag = 1

    if (ringFlag == 0 and led1Flag == 0 and led2Flag == 0 and led2Flag == 0 and matrixFlag == 0 and peltierFlag == 0 and autofocusFlag ==0 ):
        print("no need for arduino")
        loadSerial = 0
    else:
        print("load arduino")
        loadSerial = 1

    #############adresses for all arduino components:
    #timing address
    timeAdd = "TIM"

    ##LED1##
    led1OnAdd = "LD1<1>>"
    led1OffAdd = "LD1<0>>"
    led1ZapDurAdd = "LZ1"

    ##LED2##
    led2OnAdd = "LD2<1>>"
    led2OffAdd = "LD2<0>>"
    led2ZapDurAdd = "LZ2"

    ##MATRIX##
    matOffAdd = "MAT<0>>"
    matPat1Add = "MAT<1>>"
    matPat2Add = "MAT<2>>"
    matPat3Add = "MAT<3>>"
    matPat4Add = "MAT<4>>"
    matBrightAdd = "MAB"

    ##RING##
    ringOnAdd = "RIN<1>>"
    ringOffAdd = "RIN<0>>"
    ringRedAdd = "RRE"
    ringGreenAdd = "RGR"
    ringBlueAdd = "RBL"
    ringAllAdd = "RAL"
    ringZapAdd = "RZA"
    ringRotAdd = "RRT"

    ##PELTIER##
    peltOnAdd = "PEL<1>>"
    peltOffAdd = "PEL<0>>"
    peltTempAdd = "TEM"

    ##autofocus##
    autoFocusAdd = "SER"
    autoFocusOffAdd = "SER<0>>"

    allCalls = list()
    #row4Frame = tk.Frame()
    def __init__(self, master, ser="",loadSerial=loadSerial):


        #create base path for storing files, temperature curves, etc:
        if not os.path.exists(self.basePath):
            #os.chdir('/home/pi/Desktop/')
            os.mkdir(self.basePath)
            os.chown(self.basePath, 1000, 1000)

        #create dictionary to store all classes that will be used

        usedClasses = dict()

        usedClasses["app"] = self
        ##create the mainframe
        frame = tk.Frame()
        self.frame = frame

        frame.grid(row=0, column=0, rowspan=1, columnspan=1)

        row1Frame = tk.Frame(master=frame, bd=2, relief="ridge")
        row2Frame = tk.Frame(master=frame, bd=2, relief="ridge")
        row3Frame = tk.Frame(master=frame, bd=2, relief="ridge")
        row4Frame = tk.Frame(master=frame, bd=2, relief="ridge")
        row5Frame = tk.Frame(master=frame, bd=2, relief="ridge")

        #####callback for menus
        #self.test_rec()
        if self.loadSerial == 1:
            if serialAvail == True:
                # for Arduino Uno from RPi
                #self.ser = serial.Serial('/dev/ttyACM0', 115200)
                # for Arduino Nano from RPi
                self.ser = serial.Serial('/dev/ttyUSB0', 115200)
#            ser = serial.Serial('/dev/ttyUSB0', 4800,timeout=0.05)
        ##show the pieces of the GUI
        ##depending on which flags are on (see above):



        ###CAMERA###
        if self.cameraFlag == 1:

            
            import Camera
            self.frameCam = tk.Frame(master=row2Frame, bd=3)
            self.frameCam.pack(side="top")
            self.Camera = Camera.Camera(parent=self.frameCam,
                                        label="CAMERA",
                                        basePath=self.basePath)

            usedClasses["camera"] = self.Camera
        else:
            usedClasses["camera"] = 0
        ###LED1###
        if self.led1Flag == 1:
            import LED

            self.frameLed1 = tk.Frame(row1Frame, bd=3)
            self.frameLed1.grid(row=0, column=0, sticky="NW")

            self.LED1 = LED.LED(parent=self.frameLed1, label="LED 1",
                          onAdd=self.led1OnAdd, offAdd=self.led1OffAdd,
                          zapDurAdd=self.led1ZapDurAdd, #ser=self.ser,
                          #prot=self.prot,
                          #protFrame=self.frameProt,
                          )
            led1Off = self.led1OffAdd
            if self.loadSerial == 1:
                self.ser.write(led1Off.encode('utf-8'))

#            usedClasses["led1"] = self.LED1
            usedClasses["led1"] = 1
            #print (self.LED1)
        else:
            usedClasses["led1"] = 0
        ###LED2###
        if self.led2Flag == 1:
            import LED
            self.frameLed2 = tk.Frame(row1Frame, bd=3)
            self.frameLed2.grid(row=0, column=1, sticky="NW")
            self.LED2 = LED.LED(parent=self.frameLed2, label="LED 2",
                          onAdd=self.led2OnAdd, offAdd=self.led2OffAdd,
                          zapDurAdd=self.led2ZapDurAdd, ser=self.ser,

                          #prot=self.prot, protFrame=self.frameProt,
                          )
            led2Off = self.led2OffAdd
            if self.loadSerial == 1:
                self.ser.write(led2Off.encode('utf-8'))
#            usedClasses["led2"] = self.LED2
            usedClasses["led2"] = 1
        else:
            usedClasses["led2"] = 0


        ###MATRIX###
        if self.matrixFlag == 1:
            import Matrix
            self.frameMatrix = tk.Frame(row1Frame, bd=3)
            self.frameMatrix.grid(row=0, column=2, sticky="W",)
            self.Matrix = Matrix.Matrix(parent=self.frameMatrix, label="MATRIX",
                               pat3Add=self.matPat3Add,pat4Add=self.matPat4Add, offAdd=self.matOffAdd,
                               pat1Add=self.matPat1Add, pat2Add=self.matPat2Add,
                               brightAdd=self.matBrightAdd,

                               #ser=self.ser
                               )
            matOff = self.matOffAdd
            if self.loadSerial == 1:
                self.ser.write(matOff.encode('utf-8'))
            usedClasses["matrix"] = 1

        else:

            usedClasses["matrix"] = 0

        ###RING###
        if self.ringFlag == 1:
            import Ring
            self.frameRing = tk.Frame(row1Frame, bd=3)
            self.frameRing.grid(row=1, column=0, sticky="NW",
                                columnspan=3, rowspan=1)

            self.Ring = Ring.Ring(parent=self.frameRing, label="RING",
                             ringOnAdd=self.ringOnAdd,
                             ringOffAdd=self.ringOffAdd,
                             ringZapAdd=self.ringZapAdd,
                             redAdd=self.ringRedAdd,
                             greenAdd=self.ringGreenAdd,
                             blueAdd=self.ringBlueAdd,
                             #allAdd=self.ringAllAdd,
                             #rotAdd=self.ringRotAdd,

                             )

            ringOff=self.ringOffAdd
            if self.loadSerial == 1:
                self.ser.write(ringOff.encode('utf-8'))

            usedClasses["ring"] = self.Ring
        else:

            usedClasses["ring"] = 0

        ###PELTIER###
        if self.peltierFlag == 1:
            import Peltier
            self.framePelt = tk.Frame(row4Frame, bd=3)
            self.framePelt.pack(side="left")
            self.Peltier = Peltier.Peltier(parent=self.framePelt,
                                           label="PELTIER",
                                           onAdd=self.peltOnAdd,
                                           offAdd=self.peltOffAdd,
                                           tempAdd=self.peltTempAdd,
                                           basePath=self.basePath,
                                           #ser=self.ser
                                           )
            peltOff = self.peltOffAdd
            if self.loadSerial == 1:
                self.ser.write(peltOff.encode('utf-8'))
            usedClasses["peltier"] = 1#self.Peltier

        else:
            usedClasses["peltier"] = 0


        ###Auto Focus###
        if self.autofocusFlag == 1:
            import AutoFocus
            self.frameAuto = tk.Frame(row4Frame, bd=3)
            self.frameAuto.pack(side="left")
            self.AutoFocus = AutoFocus.AutoFocus(parent=self.frameAuto,
                                           label="Focus",
                                           velAdd=self.autoFocusAdd,
                                           ser=self.ser)

            autoFocusOffAdd = self.autoFocusOffAdd
            if self.loadSerial == 1:
                self.ser.write(autoFocusOffAdd.encode('utf-8'))

        else:

            usedClasses["autofocus"] = 0
        ###Protocol###
        if self.protocolFlag == 1:
            import Protocol

            self.frameProt = tk.Frame(master=row3Frame,
                                      bd=3,
                                      relief="ridge")
            self.frameProt.pack(side="top")
            self.Protocol = Protocol.Protocol(parent = self.frameProt,
                                              usedClasses=usedClasses,
                                              basePath = self.basePath+"/protocol/",
                                              label="Protocols",#ser=self.ser,
                                              timingAdd=self.timeAdd)


        else:
            self.frameProt = ""
            self.prot = False

    ##Illumination##
        if self.Illumination == 1:
            import Illumination
            self.frameIllumination = tk.Frame(row3Frame, bd=3)
            self.frameIllumination.pack(side="left")
            self.Illumination= Illumination.Illumination(parent=self.frameIllumination,
                                           label="LEDs control",
#                                         ser=self.ser
                                         )

        ####optogenetics
            
        if self.Optogenetic == 1:
            import Optogenetic
            self.frameOptogenetic = tk.Frame(row3Frame, bd=3)
            self.frameOptogenetic.pack(fill="y")
            self.Optogenetic= Optogenetic.Optogenetic(parent=self.frameOptogenetic,
                                           label="OPTOGENETICS",
#                                         ser=self.ser
                                         )

#######CAMPARI
        if self.CAMPARI == 1:
            import CAMPARI
            self.frameOptogenetic = tk.Frame(row3Frame, bd=3)
            self.frameOptogenetic.pack(fill="y")
            self.CAMPARI= CAMPARI.Optogenetic(parent=self.frameOptogenetic,
                                           label="CAMPARI     ;P",
#                                         ser=self.ser
                                         )
##mock up###
        if self.mockupFlag == 1:
            import Mock_up
            self.frameMock = tk.Frame(row4Frame, bd=3)
            self.frameMock.pack(side="left")
            self.Mockup= Mock_up.Mock_up(parent=self.frameMock,
                                           label="mock_up",
#                                         ser=self.ser
                                         )

        ####
        ###QUIT###
        if self.quitFlag == 1:
            self.frameQuit = tk.Frame(master=row4Frame)
            self.frameQuit.pack(fill="both")
#            (side="right")
            #self.frameQuit.grid(row=5, column=2, sticky="NW")
            self.quitAPP(parent=self.frameQuit)

        #draw all frames on screen
        row4Frame.grid(row=5, column=0, sticky="NWE", columnspan=1)
        row1Frame.grid(row=1, column=0, sticky="NWE", columnspan=1)
        row3Frame.grid(row=1, column=0, sticky="NWE")
        row2Frame.grid(row=0, column=0, sticky="NWE", columnspan=1)

        #####callback for menus
#        self.test_rec()
    ######################################## QUIT

    def quitAPP(self, parent="none"):
        ##callback to close the program and close serial port
        def quitNcloseSerial():
            if self.peltierFlag == 1 and self.Peltier.peltFlag1 == 1:
                print("close pelt file")
                self.Peltier.fh.close()
            if serialAvail == True:

                #self.ser.flush()
                #self.ser.readline()
                if self.loadSerial == 1:
                    self.ser.close()
            #print(self.Matrix.ser.isOpen())
            self.quit.quit()
            GPIO.cleanup()
            

        self.quit = tk.Button(master=parent, text="EXIT PROGRAM",
                              fg="red", command=quitNcloseSerial)

        self.quit.pack(fill="both")

        return


    def waittime(self,time1=100):
        output = str(self.timeAdd)+"<"+str(time1)+">>"
        print("wait time " + str(time1))
        if self.loadSerial == 1:
            self.ser.write(output.encode("utf-8"))
        self.lockwait()
        #self.allcalls.append(output.encode("utf-8"))

        return


    def lockwait(self,waitString="<wtd>>"):
        output = list()
        flag=True
        while flag== True:
            #if there is something to read on the serial port
            if self.loadSerial == 1:
                test=self.ser.in_waiting
            

                if test>0:
                    #read line
                    dummie=self.ser.readline()
                    dummie = str(dummie)#.decode("utf-8")

                    #if the line is "waited" get out of the waiting while loop

                    if waitString in str(dummie):
                        flag = False
                    else:
                        output.append(dummie)


                return output
            else:
                return






    def create_folder(self,
                      folderPath="/home/pi/Desktop/flypi_output/",
                      folderName="output1"):
        absPath = folderPath+folderName+"/"
        if not os.path.exists(absPath):
            #if not, create it:
            os.makedirs(absPath)
            os.chown(absPath, 1000, 1000)
        return

    def create_file(self,
                    filePath="/home/pi/Desktop/flypi_output/output1/",
                    fileName="file1"+time.strftime('%Y-%m-%d') + ".txt"):
        #check if the file already exists
        if os.path.isfile(filePath + fileName) == False:
            #if it does not exist, create it
            fh = open(filePath + fileName, "w")
        else:
            #open file and append to it
            fh = open(filePath + fileName, "a")



        return fh


    ######################################## CAMERA
import tkinter as tk
import os
import time
import subprocess
import threading
from tkinter.filedialog import askopenfilename
try:
    from w1thermsensor import W1ThermSensor
except ModuleNotFoundError:
    print("w1thermsensor not found. Install module with sudo apt-get install python3-w1thermsensor")
    pass

#sensor.set_resolution(9)
#import warnings
#warnings.filterwarnings('default', category=DeprecationWarning)

class Camera:

    def __init__(self, parent="none",
                 label="CAMERA", basePath="~/Desktop/"):
        
        self.nosensor = 0
        try:
            global sensor
            sensor = W1ThermSensor()
        except: 
            pass
            print("No sensor Found")
            self.nosensor = 1 
        
        try:
            # picamera module
            import picamera 
            #picameraAvail = True
            ##setup camera
            self.cam = picamera.PiCamera()
            self.cam.led = False
            self.cam.exposure_mode = "auto"
            self.cam.exposure_compensation = 0
            self.cam.brightness = 50
            self.cam.awb_mode = "auto"
            self.cam.framerate =10

        except ImportError:
            #picameraAvail = False
            print ("picamera module not available!")

        self.camParent = parent
        self.basePath = basePath

#        self.autoExpVar = tk.IntVar()

        self.flipVar = tk.IntVar()
        self.flipVal = 0
        self.MeasTempVar = tk.IntVar()
        self.MeasTempVal = 0
        self.TempDisplayVar = tk.StringVar()
        if self.nosensor == 1:
            self.TempDisplayVar.set("No sensor")
        elif self.nosensor == 0:
            self.TempDisplayVar.set("")    
        self.TempDisplayVal = ""
        self.zoomVar = tk.DoubleVar(value=1.0)
        self.zoomVal = 1.0
        self.FPSVar = tk.IntVar()
        self.FPSVal = 10
        self.bitRate = 1000000
        self.binVar = tk.IntVar()
        self.binVal = 0

        self.sizeVar = tk.IntVar()
        self.sizeVal = 800
        self.previewVar = tk.IntVar()
        self.previewVal = 240
        self.horVar = tk.DoubleVar()
        self.horVal = 1
        self.verVar = tk.DoubleVar()
        self.verVal = 1
        self.brightVar = tk.IntVar()
        self.brightVal = 50
        self.contVar = tk.IntVar()
        self.contVal = 50
        self.expVar = tk.IntVar()
        self.expVal = 0
        self.rotVar = tk.IntVar()
        self.rotVal = 180
        self.camallcalls = list()
        self.ARvar = tk.StringVar()
        self.ARval = "4:3"
        self.RedGainVar = tk.DoubleVar()
        self.RedGainVal = 0
        self.BlueGainVar = tk.DoubleVar()
        self.BlueGainVal =0
        self.height =tk.IntVar()
        self.pheight =tk.IntVar()
        self.PrintTempVar =tk.IntVar()
        self.PrintTempVal = 0
        self.PrintTempValold = 0
#        self.cycle = tk.IntVar()
#        self.cycle.set(0) =0
#        self.numVideos =IntVar()
#        selfr.numVideos.set(0)
        cycle=0
        #TT="-"
        numVideos=0
        ###frames for all camera controls
        self.camFrame1 = tk.Frame(master=self.camParent, bd=2)
        self.camFrame1.grid(row=0, column=0,
                            columnspan=1, rowspan=2,
                            sticky="N")

        frame2 = tk.Frame(master=self.camParent, bd=2)
        frame2.grid(row=0, column=1, sticky="NW", columnspan=2)
        frame3 = tk.Frame(master=frame2, bd=2, relief="ridge")
        frame3.grid(row=8, column=0, columnspan=3, rowspan=4, sticky="S")
        ####
        ####variables for the dropdown menus
        self.camAWVar = tk.StringVar(master=self.camFrame1)
        self.camAWVal = "auto"
        self.camModVar = tk.StringVar(master=self.camFrame1)
        self.camExpModeVar = tk.StringVar(master=self.camFrame1)
        self.camExpModeVal = "auto"
        self.resVar = tk.StringVar()
        self.resVal = "larva"
        self.camBitRateVar = tk.IntVar()
        self.camBitRateVal = 1
        #self.BR = tk.IntVar()
        self.BR = int(self.camBitRateVal*1000000)

        ####

        self.label = label
        #self.parent = parent
        self.camLabel = tk.Label(master=self.camFrame1, text=self.label)
        self.camLabel.pack()

        self.camOnButt = self.camButton(parent=self.camFrame1,
                            rowIndx=1, colIndx=0, fill="x",
                            buttText="ON", color="green", func=self.camOn)

        self.camOffButt = self.camButton(parent=self.camFrame1,
                            rowIndx=1, colIndx=1, fill="x",
                            buttText="OFF", color="red", func=self.camOff)
        self.camConvbutt = self.camButton(parent=self.camFrame1,
                            rowIndx=1, colIndx=2, fill="x",
                            buttText="to AVI", color="blue", func=self.camConv2)

        self.camARlabel = tk.Label(master=self.camFrame1,
                                    text=" AR ")

        self.camARlabel.pack(fill="x")
        self.camARmenu = tk.OptionMenu(self.camFrame1,
                                       self.ARvar,
                                       '4:3', '16:9',
                                       )
        self.ARvar.set("4:3")
        self.camARmenu.pack(fill="x")
        self.camARmenu.pack_propagate(flag=False)
        
        self.camResLabel = tk.Label(master=self.camFrame1,
                                    text=" Settings ")

        self.camResLabel.pack(fill="x")
        self.camResMenu = tk.OptionMenu(self.camFrame1,
                                       self.resVar, "none","IR","larva", "larva-GFP",
                                       '2592x1944', '1920x1080',
                                       '1296x972', '1296x730', '640x480')
        self.resVar.set("none")
        self.camResMenu.pack(fill="x")
        self.camResMenu.pack_propagate(flag=False)
        
        
        
        self.camAWLabel = tk.Label(master=self.camFrame1,
                                   text=" White balance ")
        self.camAWLabel.pack(fill="x")
        self.camAWMenu = tk.OptionMenu(self.camFrame1,
                                       self.camAWVar,
                                       'off', 'auto', 'green',
                                       'red', 'blue', 'sunlight', 'cloudy',
                                       'shade', 'tungsten', 'fluorescent',
                                       'incandescent',
                                       'flash', 'horizon')
        self.camAWVar.set("auto")
        self.camAWval = "auto"
        self.camAWMenu.pack(fill="x")
        self.camAWMenu.pack_propagate(flag=False)
        
        self.camModLabel = tk.Label(master=self.camFrame1, text="Image Effect")
        self.camModLabel.pack(fill="x")
        self.camModes = tk.OptionMenu(self.camFrame1,
                                      self.camModVar,
                                      "none", "negative", "solarize", "sketch",
                                      "denoise", "emboss", "oilpaint", "hatch",
                                      "gpen", "pastel", "watercolor", "film",
                                      "blur", "saturation", "colorswap",
                                      "washedout",
                                      "posterise", "colorpoint",
                                      "colorbalance", "cartoon",
                                      "deinterlace1", "deinterlace2")
        self.camModVar.set("none")
        self.camModes.pack(fill="x")
        
        self.camExpModeLabel = tk.Label(master=self.camFrame1,
                                       text="Exposure Mode")
        self.camExpModeLabel.pack(fill="x")
        self.camExpMode = tk.OptionMenu(self.camFrame1,
                                       self.camExpModeVar,
                                      "off",
                                      "snow", "auto", "night", "nightpreview", "backlight", "spotlight", "sports","beach","verylong","fixedfps", "antishake","fireworks")
        self.camExpMode.pack(fill="x")
        self.camExpModeVar.set("auto")
        self.camExpMode.pack_propagate(flag=False)
        
        
        self.camBitRateLabel = tk.Label(master=self.camFrame1,
                                       text="Bit Rate x1M")
        self.camBitRateLabel.pack(fill="x")
        self.camBitRate = tk.Scale(self.camFrame1, from_=0.5, to=25, resolution=0.5, orient=tk.HORIZONTAL)
#        self.camBitRate.pack(fill="x")
        self.camBitRate.pack()
        #self.camBitRate.set(1)
        self.camBitRate.set(self.camBitRateVal)
        
        self.camBitRate.pack_propagate(flag=False)
        
        
        
                
#        self.camARMenu = tk.OptionMenu(frame2, self.ARvar,"4:3","16:9")
#        self.resVar.set("4:3")
#        self.camResMenu.pack(fill="x")
#        self.camResMenu.pack_propagate(flag=False)

        self.camFPS = self.camSlider(parent=frame2, label_="FPS",
                                   var=self.FPSVar, len=90,
                                   rowIndx=0, colIndx=2, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=10, to__=90,
                                   res=2, set_=self.FPSVal)

        #self.camBin = self.camSlider(parent=frame2, label_="Binning",
        #                           var=self.binVar, len=90,
        #                           rowIndx=0, colIndx=2, sticky="",
        #                           orient_="horizontal",
        #                           colSpan=1, from__=0, to__=4, res=2, set_=0)

        self.camPreview = self.camSlider(parent=frame2, label_="preview",
                                   var=self.previewVar,
                                   rowIndx=0, colIndx=0, sticky="",
                                   orient_="horizontal", len=90,
                                   colSpan=1, from__=150, to__=1000,
                                   res=10, set_=self.previewVal)

        self.camWidth = self.camSlider(parent=frame2, label_="width (px)",
                                   var=self.sizeVar, len=90,
                                   rowIndx=1, colIndx=0, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=150,
                                   to__=1330, res=10, set_=self.sizeVal)

        self.camHor = self.camSlider(parent=frame2, label_="Horiz. Offset",
                                   var=self.horVar, len=90,
                                   rowIndx=2, colIndx=0, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=1, to__=100,
                                   res=5, set_=1)

        self.camVer = self.camSlider(parent=frame2, label_="Verti. Offset",
                                   var=self.verVar, len=90,
                                   rowIndx=2, colIndx=1, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=1,
                                   to__=100, res=5, set_=1)

        self.camBright = self.camSlider(parent=frame2, label_="Brightness",
                                   var=self.brightVar, len=90,
                                   rowIndx=1, colIndx=2, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=0, to__=100,
                                   res=5, set_=50)

        self.camCont = self.camSlider(parent=frame2, label_="Contrast",
                                   var=self.contVar, len=90,
                                   rowIndx=1, colIndx=1, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=0, to__=100,
                                   res=5, set_=50)

        self.camExp = self.camSlider(parent=frame2, label_="Exp compensation",
                                   var=self.expVar, len=90,
                                   rowIndx=2, colIndx=2, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=-25, to__=25,
                                   res=5, set_=0)

        self.camRot = self.camSlider(parent=frame2, label_="Rotation",
                                   var=self.rotVar, len=90,
                                   rowIndx=0, colIndx=1, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=0, to__=270,
                                   res=90, set_=180)
        
        self.BlueGain = self.camSlider(parent=frame2, label_="Blue gain",
                                   var=self.BlueGainVar, len=90,
                                   rowIndx=3, colIndx=0, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=0, to__=8,
                                   res=0.1, set_=self.BlueGainVal)

        self.RedGain = self.camSlider(parent=frame2, label_="Red gain",
                                   var=self.RedGainVar, len=90,
                                   rowIndx=3, colIndx=1, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=0, to__=8,
                                   res=0.1, set_=self.RedGainVal)
  
  
        self.camExp = self.camSlider(parent=frame2, label_="Exposure",
                                   var=self.expVar, len=90,
                                   rowIndx=2, colIndx=2, sticky="",
                                   orient_="horizontal",
                                   colSpan=1, from__=-25, to__=25,
                                   res=5, set_=0)
        

#        self.autoExposure = tk.Checkbutton(master=frame2,
#                                           text="auto expos.",
#                                           variable=self.autoExpVar,
#                                           onvalue=1, offvalue=0)
#        self.autoExpVar.set(1)
#        self.autoExposure.grid(row=4, column=0, sticky="N")

        self.flip = tk.Checkbutton(master=frame2,
                                   text="Flip image",
                                   variable=self.flipVar,
                                   onvalue=1, offvalue=0)

        self.flipVar.set(0)
        self.flip.grid(row=3, column=2, sticky="S")
        
        self.EmptyLabel = tk.Label(master=frame2, text=" ")
        self.EmptyLabel.grid(row=5, column=0,columnspan=5)
#        
#        self.EmptyLabel2 = tk.Label(master=frame2, text=" ")
#        self.EmptyLabel2.grid(row=6, column=0,columnspan=5)
#        
#        self.EmptyLabel3 = tk.Label(master=frame2, text=" ")
#        self.EmptyLabel3.grid(row=7, column=0,columnspan=5)
        #########Time lapse/video/photo####################

        self.TLLabel = tk.Label(master=frame3, text="ACQUIRE")
        self.TLLabel.grid(row=0, column=0,columnspan=5)

        self.camRecButt = tk.Button(master=frame3,
                                  text="short video", fg="black",
                                  command=self.camRec)
        self.camRecButt.grid(row=1, column=0, sticky="WEN")

        self.camTLButt = tk.Button(master=frame3,
                                 text="timelapse", fg="black",
                                 command=self.camTL)
        self.camTLButt.grid(row=1, column=1, sticky="WES")

        self.camSnapButt = tk.Button(master=frame3,
                                   text="photo", fg="black",
                                   command=self.camSnap)
        self.camSnapButt.grid(row=1, column=2,rowspan=5, sticky="WESN")

        self.TLdurLabel = tk.Label(master=frame3, text="DUR (sec)")
        self.TLdurLabel.grid(row=2, column=0, sticky="E")

        self.TLdur = tk.Entry(master=frame3, width=8)
        self.TLdur.grid(row=2, column=1, sticky="WN")
        self.TLdur.insert(0, 0)

        self.TLinterLabel = tk.Label(master=frame3, text="INTERVAL (sec)")
        self.TLinterLabel.grid(row=3, column=0, sticky="E")

        self.TLinter = tk.Entry(master=frame3, width=8)
        self.TLinter.insert(0, 0)
        self.TLinter.grid(row=3, column=1, sticky="NW")




        
        self.camLongRecButt = tk.Button(master=frame3,
                                  text="long video", fg="black",
                                  command=self.threadCamLongRec)
        self.camLongRecButt.grid(row=1, column=3, columnspan=2,sticky="WE")

        self.SegmentDurLabel = tk.Label(master=frame3, text="split (min)")
        self.SegmentDurLabel.grid(row=2, column=3, sticky="E")

        self.SegmentDur = tk.Entry(master=frame3, width=3)
        self.SegmentDur.insert(0, 5)
        self.SegmentDur.grid(row=2, column=4, sticky="NE")

        self.LongDurLabel = tk.Label(master=frame3, text="total length (hr)")
        self.LongDurLabel.grid(row=3, column=3, sticky="E")
        self.TotalLength = tk.Entry(master=frame3, width=3)
        self.TotalLength.insert(0, 24)
        self.TotalLength.grid(row=3, column=4, sticky="NE")
        
        self.nameLabel = tk.Label(master=frame3, text="name")
        self.nameLabel.grid(row=4, column=3, columnspan=2)

        self.name = tk.Entry(master=frame3, width=18)
        self.name.grid(row=5, column=3, columnspan=2)
        
        self.stopCamLongRec=tk.IntVar()
        self.stopCamLongRecbutton = tk.Checkbutton(master=frame3,
                                  text="STOP", fg="black",variable=self.stopCamLongRec, indicatoron=False)
        self.stopCamLongRecbutton.grid(row=6, column=3, columnspan=2,sticky="WE")   
        
        self.videoprogressVar = tk.StringVar()
        self.videoprogressVar.set('recording video ' + str(cycle) + ' of ' +str(numVideos))
        self.progress = self.videoprogressVar.get()
        print(self.progress)
        self.nameLabel = tk.Label(master=frame3, textvariable= self.videoprogressVar)
        self.nameLabel.grid(row=7, column=3, columnspan=2)
        
        self.Measure = tk.Checkbutton(master=frame3,
                                   text="Measure Temp",
                                   variable=self.MeasTempVar, command=self.threadMeasTemp,
                                   onvalue=1, offvalue=0)
        self.MeasTempVar.set(0)
        self.Measure.grid(row=4, column=0, sticky="SE")


        self.nameLabel = tk.Label(master=frame3, textvariable= self.TempDisplayVar)
        self.nameLabel.grid(row=4, column=1, stick="SNWE")
        
        self.Print = tk.Checkbutton(master=frame3,
                                   text="Print Temp",
                                   variable=self.PrintTempVar,
                                   onvalue=1, offvalue=0)
        self.PrintTempVar.set(0)
        self.Print.grid(row=5, column=0, sticky="SW")
        ####callback for menus
        self.camGetMenus()
        ####
        
        
        
    ########callback for menus
    def camGetMenus(self):
        #this is a recursive function that will call itself
        #with a minimum interval of 700ms.
        #upon calling it will get the value of three variables
        #white balance, mode and color effect
        self.camFrame1.after(400, self.camGetMenus)
        

        if self.camAWVal != self.camAWVar.get():         
            self.camAWVal = self.camAWVar.get()
            
            
            if self.camAWVal != "":
                if self.camAWVal == "green":
                    self.cam.awb_mode = "off"
                    self.cam.awb_gains = (1, 1)
                    self.BlueGainVar.set(1)
                    self.RedGainVar.set(1)
                elif self.camAWVal == "red":
                    self.cam.awb_mode = "off"
                    self.cam.awb_gains = (8.0, 0.9)
                    self.BlueGainVar.set(0.9)
                    self.RedGainVar.set(8)
                elif self.camAWVal == "blue":
                    self.cam.awb_mode = "off"
                    self.cam.awb_gains = (0.9, 8.0)
                    self.BlueGainVar.set(8)
                    self.RedGainVar.set(0.9)
                    
                elif self.camAWVal == "off":
                    self.cam.awb_mode = self.camAWVal
                    self.RedGainVal = self.RedGainVar.get()
                    self.BlueGainVal = self.BlueGainVar.get()
                    self.cam.awb_gains =(self.RedGainVal,self.BlueGainVal)
                    time.sleep(0.1)
                    print(self.camAWVar.get())
                    print(self.camAWVal)
                    print(self.cam.awb_mode)
                    print(self.cam.awb_gains)
                else:
                    self.cam.awb_mode = self.camAWVal
                    print(self.camAWVar.get())
                    print(self.camAWVal)
                    print(self.cam.awb_mode)
                    print(self.cam.awb_gains)

        if self.cam.image_effect != self.camModVar.get():
            self.camModVal = self.camModVar.get()
            if self.camModVal != "":
                self.cam.image_effect = self.camModVal
#
#        if self.ccamColEffValamColEffVal != self.camColEffVar.get():
#            self.camColEffVal = self.camColEffVar.get()
#            if self.camColEffVal != "":
#                if self.camColEffVal == "BW":
#                    self.cam.color_effects = (128, 128)
#                elif self.camColEffVal == "RED":
#                    self.cam.color_effects = (0, 255)
#                elif self.camColEffVal == "BLUE":
#                    self.cam.color_effects = (255, 0)
#                elif self.camColEffVal == "GREEN":
#                    self.cam.color_effects = (0, 0)
#                else:
#                    self.cam.color_effects = None
        #ce = self.camColEffVar.get()

#        autoExp = self.autoExpVar.get()
#        if autoExp == 0:
#            self.cam.exposure_mode = "off"
#        else:
#            self.cam.exposure_mode = "auto"

        #flip= self.flipVar.get()
        #print(type(flip1))
        if self.flipVal != self.flipVar.get():
            self.flipVal = self.flipVar.get()
            if self.flipVal == 1:
                self.cam.hflip = True
            else:
                self.cam.hflip = False
        
        if  self.camExpModeVal !=  self.camExpModeVar.get():
             self.camExpModeVal = self.camExpModeVar.get()
             self.cam.exposure_mode = (self.camExpModeVal)
             
        if self.FPSVal != self.FPSVar.get():
            self.FPSVal = self.FPSVar.get()
            self.cam.framerate = (self.FPSVal)

        if self.brightVal != self.brightVar.get():
            self.brightVal = self.brightVar.get()
            self.cam.brightness = (self.brightVal)

        if self.contVal != self.contVar.get():
            self.contVal = self.contVar.get()
            self.cam.contrast = (self.contVal)

        if self.expVal != self.expVar.get():
            self.expVal = self.expVar.get()
            self.cam.exposure_compensation = (self.expVal)

        if self.camBitRateVal != self.camBitRate.get():
            self.camBitRateVal = self.camBitRate.get()
            self.BR = int(self.camBitRateVal*1000000)

        if self.TempDisplayVal != self.TempDisplayVar.get():
                self.TempDisplayVal = self.TempDisplayVar.get()
                

        if self.PrintTempVar.get() ==1:
            self.PrintTempValold = self.PrintTempVar.get()
            self.cam.annotate_text = (self.TempDisplayVal)
            #self.cam.annotate_background = Color('blue')
            #self.cam.annotate_foreground = Color('white')
        elif self.PrintTempVar.get() == 0 and self.PrintTempValold ==1:
            self.PrintTempValold = self.PrintTempVar.get()
            self.cam.annotate_text = ""
                
        if self.BlueGainVal != self.BlueGainVar.get():
            self.BlueGainVal = self.BlueGainVar.get()
        if self.RedGainVal != self.RedGainVar.get():
            self.RedGainVal = self.RedGainVar.get()
        
              
        if self.camAWVal == "off":
#            self.cam.awb_mode = "off"
            self.RedGainVal = self.RedGainVar.get()
            self.BlueGainVal = self.BlueGainVar.get()
            self.cam.awb_gains =(self.RedGainVal,self.BlueGainVal)          
        
#        if self.cam.awb_mode == "off":
#            self.cam.awb_gains =(self.RedGainVal,self.BlueGainVal)
            

            
        if self.ARval != self.ARvar.get():
            self.ARval = self.ARvar.get()
            if self.ARval=="4:3":
                self.heigth = int(self.sizeVal*3/4)
                self.pheigth = int(self.previewVal*3/4)
            elif self.ARval=="16:9":
                self.heigth = int(self.sizeVal*9/16)
                self.pheigth = int(self.previewVal*9/16)
            self.cam.resolution =(self.sizeVal, self.heigth)
            self.cam.preview_window = (50, 50, self.previewVal, self.pheigth)

        if self.sizeVal != self.sizeVar.get():
            self.sizeVal = self.sizeVar.get()
            if self.ARval=="4:3":
                self.heigth = int(self.sizeVal*3/4)
#                pheigth = int(self.previewVal*3/4)
            elif self.ARval=="16:9":
                self.heigth = int(self.sizeVal*9/16)
#                pheigth = int(self.previewVal*9/16)
            self.cam.resolution =(self.sizeVal, self.heigth)
#            self.cam.preview_window = (50, 50, self.previewVal, pheigth)

        if self.previewVal != self.previewVar.get():
            self.previewVal = self.previewVar.get()
            if self.ARval=="4:3":
                self.pheigth = int(self.previewVal*3/4)
            elif self.ARval=="16:9":
                self.pheigth = int(self.previewVal*9/16)
            self.cam.preview_window = (50, 50, self.previewVal, self.pheigth)


        if self.rotVal != self.rotVar.get():
            self.rotVal = self.rotVar.get()
            self.cam.rotation = self.rotVal

        if self.resVal != self.resVar.get():
            self.resVal = self.resVar.get()
            
            if self.resVal == "larva":
                self.sizeVar.set(800)
#                self.cam.resolution = (800, 600)
#                self.cam.framerate = (self.FPSVal)
                self.camBitRate.set(1)
                #self.camBitRateVal = self.camBitRate.get()
                #self.BR = int(self.camBitRateVal*1000000)
                self.FPSVar.set(10)
                self.binVar.set(0)
                self.BlueGainVar.set(1.6)
                self.RedGainVar.set(1.4)
                self.camExpModeVar.set("snow")
                self.camAWVar.set("off")
                
            elif self.resVal == "IR":
                self.sizeVar.set(800)
#                self.cam.resolution = (800, 600)
#                self.cam.framerate = (self.FPSVal)
                self.camBitRate.set(1)
                #self.camBitRateVal = self.camBitRate.get()
                #self.BR = int(self.camBitRateVal*1000000)
                self.FPSVar.set(10)
                self.binVar.set(0)
#                Scale3.set(20)
                self.BlueGainVar.set(1.0)
                self.RedGainVar.set(1.0)
                self.camExpModeVar.set("night")
                self.camAWVar.set("off")
                
            elif self.resVal == "larva-GFP":
                self.sizeVar.set(1330)
#                self.cam.resolution = (800, 600)
#                self.cam.framerate = (self.FPSVal)
                self.camBitRate.set(1)
#                self.camBitRateVal = self.camBitRate.get()
#                self.BR = int(self.camBitRateVal*1000000)
                self.FPSVar.set(10)
                self.binVar.set(0)
                self.BlueGainVar.set(2)
                self.RedGainVar.set(0.1)
                self.camExpModeVar.set("snow")
                self.camAWVar.set("off")
            
            
            elif self.resVal == "2592x1944":
                self.cam.resolution = (2592, 1944)
                self.cam.framerate = (15)
                self.FPSVar.set(15)
                self.binVar.set(0)
                #self.cam.zoom(0)
                self.zoomVar.set(1)
            elif self.resVal == "1920x1080":
                self.cam.resolution = (1920, 1080)
                self.cam.framerate = (30)
                self.FPSVar.set(30)
                self.binVar.set(0)
                #self.zoomVar.set(3)
            elif self.resVal == "1296x972":
                self.cam.resolution = (1296, 972)
                self.cam.framerate = (42)
                self.FPSVar.set(42)
                self.binVar.set(2)
            elif self.resVal == "1296x730":
                self.cam.resolution = (1296, 730)
                self.cam.framerate = (49)
                self.FPSVar.set(49)
                self.binVar.set(2)
            elif self.resVal == "640x480":
                self.cam.resolution = (640, 480)
                self.cam.framerate = (90)
                self.FPSVar.set(90)
                self.binVar.set(4)
                #self.zoomVar.set(5)

        if self.zoomVal != self.zoomVar.get() or \
           self.horVal != self.horVar.get() or \
           self.verVal != self.verVar.get() or \
           self.resVal != self.resVar.get():# or \
           #self.binVal != self.binVar.get():
            self.zoomVal = self.zoomVar.get()
            self.horVal = self.horVar.get()
            self.verVal = self.verVar.get()
            self.resVal = self.resVar.get()
            #self.binVal = self.binVar.get()
            if self.zoomVal == 1:
                self.cam.zoom = (0, 0, 1, 1)
                self.horVar.set(50)
                self.verVar.set(50)
            else:
                zoomSide = 1 / self.zoomVal
                edge = (1 - zoomSide)#*0.5
                self.cam.zoom = ((self.horVal / 100.0) * edge,
                               (self.verVal / 100.0) * edge,
                               1 / self.zoomVal,
                               1 / self.zoomVal)

    #general function to create buttons
    def camButton(self, parent="none", fill="", side="top",
                  rowIndx=1, colIndx=0, sticky="",
                  buttText="button", color="black",
                  func="none"):

        button = tk.Button(master=parent,
                           text=buttText,
                           fg=color, command=func)
        button.pack(fill=fill, side=side)
        return
    #general function for slider
    def camSlider(self, parent="none", label_="empty", len=90,
                   var="", rowIndx=1, colIndx=0,
                   sticky="", orient_="vertical",
                   colSpan=1, from__=100, to__=0,
                   res=1, set_=0):

        Slider = tk.Scale(master=parent, from_=from__, to=to__,
                          resolution=res, label=label_, length=90,
                          variable=var, orient=orient_)
        Slider.set(set_)
        Slider.grid(row=rowIndx, column=colIndx, columnspan=colSpan)
        return
    ##################callbacks for buttons
    def camOn(self):

        print ("cam on")
        res = self.resVar.get()
        size = self.sizeVar.get()
        if self.ARvar.get()=="4:3":
            heigth = int(size*3/4)
        elif self.ARvar.get()=="16:9":
            heigth = int(size*9/16)
        self.cam.resolution = (size, heigth)
        self.cam.preview_window = (50, 50, self.previewVal, self.previewVal)
        self.zoomVar.set(1)
        self.horVar.set(0)
        self.verVar.set(0)
        self.cam
        self.cam.rotation = self.rotVal
        self.cam.zoom = (self.horVar.get(),
                       self.verVar.get(),
                       self.zoomVar.get(),
                       self.zoomVar.get())
        self.cam.start_preview()
        self.cam.preview.fullscreen = False
        #self.cam.annotate_text = "Temp 25.0 C"
        #self.cam.annotate_size = 60 
        #self.cam.annotate_background = Color('black')
        #self.cam.annotate_foreground = Color('black')
        #self.cam.annotate_background = Color('white')
        
        
        #wait a second so the camera adjusts
        time.sleep(1)
        return

    def camOff(self):
        print ("cam Off")
        self.cam.stop_preview()
        return

    def camConv(self):
        #tk().withdraw()
        opts = dict()
        opts["filetypes"] = [('h264 files','.h264'),('all files','.*')]
        opts["initialdir"] = [self.basePath]

        fileName = askopenfilename(**opts)
        if fileName == '':
            print ('no files selected')
            return
        fps = self.FPSVar.get()
        fps = "-r" + str(fps)
#        fps = int(fps)
        print (fileName)
        print ("converting video to avi")
        outname = os.path.splitext(fileName)[0]+".avi"
        lastInd=fileName.rindex("/")
        files = os.listdir(fileName[0:lastInd])
        outCore = outname.rindex("/")
        print ("out:" + outname[outCore:])
        if outname[outCore+1:] in files:
            print ("file is already converted! Skipping...")
            print("done.")
            return
        
        command = ['avconv', '-i', fileName,"-b",str(self.bitRate) ,"-c:v","copy", outname]
        #command = ['ffmpeg', '-i', fileName,"-b",str(self.bitRate) ,"-pix_fmt","nv12","-f:v","-vcodec rawvideo", outname]
        subprocess.call(command,shell=False)
        print("done.")
        return

    def camConv2(self):
        #tk().withdraw()
        opts = dict()
        opts["filetypes"] = [('h264 files','.h264'),('all files','.*')]
        opts["initialdir"] = [self.basePath]

        fileName = askopenfilename(**opts)
        if fileName == '':
            print ('no files selected')
            return
        fps = self.FPSVar.get()
        fps = "-r" + str(fps)
#        fps = int(fps)
        print (fileName)
        print ("converting video to avi")
        outname = os.path.splitext(fileName)[0]+".avi"
        lastInd=fileName.rindex("/")
        files = os.listdir(fileName[0:lastInd])
        outCore = outname.rindex("/")
        print ("out:" + outname[outCore:])
        if outname[outCore+1:] in files:
            print ("file is already converted! Skipping...")
            print("done.")
            return
        
        command = ['MP4Box', '-add', fileName, outname]
        #command = ['ffmpeg', '-i', fileName,"-b",str(self.bitRate) ,"-pix_fmt","nv12","-f:v","-vcodec rawvideo", outname]
        subprocess.call(command,shell=False)
        print("done.")
        return
    
    def camRec(self,dur=None):
        if dur == None:
            dur = self.TLdur.get()


        videoPath = self.basePath + '/videos/'
        if not os.path.exists(videoPath):
            #if not, create it:
            os.makedirs(videoPath)
            os.chown(videoPath, 1000, 1000)
        #it seems that the raspi-cam doesn't like shooting videos at full res.
        #so the softw. will automatically use a lower resolution for videos
        if self.resVal == "2592x1944":
            self.resVar.set ("1920x1080")
            self.cam.resolution = (1920, 1080)
            if self.FPSVar.get()<30:
                self.FPSVar.set(30)
            print ("impossible to record at 2592X1944,")
            print ("due to camera limitations.")
            print("dropping to next possible resolution")


        print("recording for: " + str(dur) + " secs")
        print("FPS: " + str(self.FPSVal))
        self.cam.start_recording(output = videoPath +
                                'video_' +
                                time.strftime('%Y-%m-%d-%H-%M-%S') + '.h264',
                                format = "h264",bitrate=self.BR)
                                #resize = (1920,1080))
        self.cam.wait_recording(float(dur))
        self.cam.stop_recording()
        print("done.")
        #here we restore the preview resolution if it was the maximal one.
        if self.resVal == "2592x1944":
            self.cam.resolution = (2592, 1944)
        return

    def camLongRec(self,split=None):
        if split == None:
            split = float(self.SegmentDur.get())
        splitSeg = int(split*60)
        
        horas = float(self.TotalLength.get())
        num = (horas*60/split)
        numVideos = int(num)
#        print(num)
#        print(numVideos)
        if numVideos < num:
            numVideos = numVideos+1
            
#        print(numVideos)
        filename = self.name.get()
        
        videoPath = self.basePath 
        if not os.path.exists(videoPath):
            #if not, create it:
            os.makedirs(videoPath)
            os.chown(videoPath, 1000, 1000)
        #it seems that the raspi-cam doesn't like shooting videos at full res.
        #so the softw. will automatically use a lower resolution for videos
        if self.resVal == "2592x1944":
            self.resVar.set ("1920x1080")
            self.cam.resolution = (1920, 1080)
            if self.FPSVar.get()<30:
                self.FPSVar.set(30)
            print ("impossible to record at 2592X1944,")
            print ("due to camera limitations.")
            print("dropping to next possible resolution")

#        if self.resVal == "larva":
            
        print("recording for: " + str(horas) + " hs. Splitting every " + str(split) + " minutes")
        print(str(numVideos)+ " files will be created" )
        print(self.BR)
        print(self.camBitRateVal)
        print("fps: "+ str(self.FPSVal))
        cycle =1
        j= numVideos+1
        self.videoprogressVar.set('recording video ' + str(cycle) + ' of ' +str(numVideos))
         
        self.cam.start_recording(output = videoPath + str(filename) + "-0001"+ '.h264', bitrate= self.BR)
        #                                ,format = "h264",)
                                #resize = (1920,1080))
        self.cam.wait_recording(splitSeg)
        #for i in range (2, numCorrected):
        
        cycle=2
        self.stopCamLongRec.set(False)
        stop=self.stopCamLongRec.get()
        while cycle < j and stop == False:
#        for i in range(2, j):
            self.videoprogressVar.set('recording video ' + str(cycle) + ' of ' +str(numVideos))
            self.cam.split_recording(output = videoPath + str(filename) + '-%04d.h264' % cycle)
            self.cam.wait_recording(splitSeg)
            print (time.strftime('%H:%M:%S')  + " video " +str(cycle))
            cycle +=1
            stop=self.stopCamLongRec.get()
        self.cam.stop_recording()
        self.stopCamLongRec.set(False)
        cycle= 0
        numVideos=0
        self.videoprogressVar.set('recording video ' + str(cycle) + ' of ' +str(numVideos))
        print("done.")
        
        
        

        
        
        #here we restore the preview resolution if it was the maximal one.
        if self.resVal == "2592x1944":
            self.cam.resolution = (2592, 1944)
        return

    def threadCamLongRec(self):
        threading.Thread(target=self.camLongRec).start()
    
    def camTL(self):
        dur = self.TLdur.get()
        interval = self.TLinter.get()
        tlPath = self.basePath + '/time_lapse/'

        #check to see if the time lapse output folder is present:
        if not os.path.exists(tlPath):
            #if not, create it:
            os.makedirs(tlPath)
            os.chown(tlPath, 1000, 1000)

        #get the present time, down to seconds
        tlFold = time.strftime("%Y-%m-%d-%H-%M-%S")

        #make a new folder to store all time lapse photos
        os.makedirs(tlPath + tlFold)
        os.chown(tlPath + tlFold, 1000, 1000)
        #os.chdir(tlPath+tlFold)

        shots = int(int(dur) / int(interval))
        if shots <= 0:
            print("something wrong with time specifications!")
        else:
            print('time lapse:')
            print('number of shots: ' + str(shots))
            for i in range(0, shots):
                print("TL " + str(i + 1) + "/" + str(shots))
                self.cam.capture(tlPath + tlFold + "/TL_" + str(i + 1) + ".jpg")
                time.sleep(float(interval))
            print("done.")
        return
    def camSnap(self):
        photoPath = self.basePath + '/snaps/'
        #check to see if the snap output folder is present:
        if not os.path.exists(photoPath):
            #if not, create it:
            os.makedirs(photoPath)
            os.chown(photoPath, 1000, 1000)



        # Camera warm-up time
        time.sleep(1)
        self.cam.capture(photoPath + 'snap_' +
                        time.strftime("%Y-%m-%d-%H-%M-%S") + '.jpg')
        return
    
    def threadMeasTemp(self):
        threading.Thread(target=self.MeasTempstart).start()
    
    def MeasTempstart(self):
        seguir = self.MeasTempVar.get()
        if seguir == 0:
            self.TempDisplayVar.set("")
        if seguir == 1:
            t0=time.time()
            try:
                temperature = sensor.get_temperature()
                TT= round(temperature,1)
                self.TempDisplayVar.set(str(TT)+" C")
                print("comienzo")
                print("La temperatura es %s ºC" % TT)
            except NameError:
                print("No sensor")
                self.TempDisplayVar.set("No sensor")
            
        #seguir = 1
            while seguir ==1:
                if time.time()-t0 >= 5.0:
                    t0=time.time()
                    try:
                        temperature = sensor.get_temperature()
                        TT= round(temperature,1)
                        self.TempDisplayVar.set(str(TT)+" C")
                        #print("La temperatura es %s ºC" % TT)
                        seguir = self.MeasTempVar.get()
                    except NameError:
                        pass
        #else:
            self.TempDisplayVar.set("")
            print("Stop temp sensor")
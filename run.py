#!/usr/bin/env python3


#import "global" libraries
import tkinter as tk
#import os
#import time


#################PROGRAM EXECUTION
from flypiApp import *

#create a root
root = tk.Tk()
root.title("Fly Pi - Pupariation")

flypiApp(root)


#dummie.title("test")
root.resizable(width=False, height=True)
root.mainloop()

root.destroy()

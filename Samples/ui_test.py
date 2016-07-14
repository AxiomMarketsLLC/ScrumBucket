#!/usr/bin/python 

from Tkinter import *
top = Tk()

var = StringVar()
if(True):
	colour = "green"
else:
 	colour  = "red" 
label = Label(top, textvariable=var, width=100, height=50, bg=colour)

def changeColour():
    label.configure(bg="red")
    top.after(2000,changeColour)
var.set("App Works")
label.pack() 

top.after(1000,changeColour)
top.mainloop() 

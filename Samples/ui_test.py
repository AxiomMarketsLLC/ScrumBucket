#!/usr/bin/python 

from Tkinter import *
top = Tk()

var = StringVar()
colour = "green"


label = Label(top, textvariable=var, width=100, height=50, bg=colour)

menu = Spinbox(top,values=[ "10 secs","20 secs", "1 min", "15 mins","30 mins"])
menu.pack()


def changeColour():
    label.configure(bg="red")
    top.after(2000,changeColour)
var.set("App Works")
label.pack() 

top.after(1000,changeColour)
top.mainloop() 
 

import decimal
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinter.colorchooser, tkinter.messagebox
from PIL import Image, ImageTk
import numpy as np
import math

window=tk.Tk()
window.title('GBSpriter')
window.configure(bg='#FFFFFF')
window.geometry("720x800+0+0")


#this is for the module
x_len=0
y_len=0
screen_x=0
screen_y=0
pixel_x=0
pixel_y=0
mouse_x=0
mouse_y=0
mouse_colour="#000000"

pixels=[]
data_array=[0]*16

class Pixel():
 def __init__(self, window_name, color, pixel_name, outline):
  self.window_name=window_name
  self.color=color
  self.pixel_name=pixel_name
  self.outline=outline
  self.color_tag=0
 def stamp(self):
  tk.canvas.itemconfigure(self.pixel_name, fill=self.color, outline=self.outline) 

def qdee(window_name, scrn_x, scrn_y, pixl_x, pixl_y):
 global x_len
 global y_len
 global pixel_x
 global pixel_y
 global screen_x
 global screen_y
 screen_x=scrn_x
 screen_y=scrn_y
 pixel_x=pixl_x
 pixel_y=pixl_y
 x_len=screen_x/pixel_x
 y_len=screen_y/pixel_y
 pixels.clear()
 tk.canvas=Canvas(window_name, height=screen_y, width=screen_x)
 tk.canvas.pack(fill=BOTH, side=BOTTOM)
 for i in range(pixel_y):
  for q in range(pixel_x):
   pixel_name=str(q)+'-'+str(i)
   pixel_name=tk.canvas.create_rectangle(q*x_len, screen_y-((i+1)*y_len), q*x_len+x_len, screen_y-((i+1)*y_len-y_len), fill = 'black', outline = 'white', width = 1) 
   pixel_name=Pixel(window_name, '#ffffff', pixel_name, 'green')
   pixel_name.stamp()
   pixels.append(pixel_name)
 
def paint():
 global mouse_colour
 pixels[math.floor((mouse_x)/7.371)+8*(math.floor((mouse_y+8)/7.371))].color=mouse_colour
 if mouse_colour=="#FFFFFF":
  pixels[math.floor((mouse_x)/7.371)+8*(math.floor((mouse_y+8)/7.371))].color_tag=0
 elif mouse_colour=="#AAAAAA":
  pixels[math.floor((mouse_x)/7.371)+8*(math.floor((mouse_y+8)/7.371))].color_tag=1
 elif mouse_colour=="#555555":
  pixels[math.floor((mouse_x)/7.371)+8*(math.floor((mouse_y+8)/7.371))].color_tag=2
 elif mouse_colour=="#000000":
  pixels[math.floor((mouse_x)/7.371)+8*(math.floor((mouse_y+8)/7.371))].color_tag=3
 pixels[math.floor((mouse_x)/7.371)+8*(math.floor((mouse_y+8)/7.371))].stamp()

def mouse_move(event):
 x, y=event.x, event.y
 global mouse_x
 global mouse_y
 mouse_x, mouse_y=round(x/12-0.5), round((screen_y-y-100)/12)

def clip():
    global data_array
    global okwtf
    okwtf=""
    for i in data_array:
        okwtf+=i+','
    okwtf=okwtf[:-1]
    print(okwtf)

def colour4(event):
    global mouse_colour
    mouse_colour="#FFFFFF"
    paint()
def colour3(event):
    global mouse_colour
    mouse_colour="#AAAAAA"
    paint()
def colour2(event):
    global mouse_colour
    mouse_colour="#555555"
    paint()
def colour1(event):
    global mouse_colour
    mouse_colour="#000000"
    paint()

def load_sprite():
    spriteset=loadsprite.get()
    chunks = spriteset.split(',')
    for i in range(len(chunks)):
        chunks[i]=int(chunks[i],16)
    
    for i in range(8):
        for q in range(8):
            pixels[(7-i)*8+q].color_tag=0
            if chunks[2*i]>=2**(7-q):
                chunks[2*i]-=2**(7-q)
                pixels[(7-i)*8+q].color_tag+=1
            if chunks[2*i+1]>=2**(7-q):
                chunks[2*i+1]-=2**(7-q)
                pixels[(7-i)*8+q].color_tag+=2

    for i in range(64):
        if pixels[i].color_tag==0:
            pixels[i].color="#FFFFFF"
        elif pixels[i].color_tag==1:
            pixels[i].color="#AAAAAA"
        elif pixels[i].color_tag==2:
            pixels[i].color="#555555"
        elif pixels[i].color_tag==3:
            pixels[i].color="#000000"
        pixels[i].stamp()

qdee(window, 720, 720, 8, 8)
tk.canvas.bind('<Motion>', mouse_move)
window.bind("4", colour4)
window.bind("3", colour3)
window.bind("2", colour2)
window.bind("1", colour1)
data=Label(window, text="ff")
data.place(x=5, y=35)
thebutton = tk.Button(window, text ="Clip", command = clip)
thebutton.place(x=8, y=12)
loadsprite=Entry(window, width=20)
loadsprite.insert(0,'')
loadsprite.place(x=400, y=12)
theotherotherbutton=Button(window, text="Load", command=load_sprite)
theotherotherbutton.place(x=350, y=15)

while True:
 data_array=[0]*16
 data_number=""
 for i in range(8):
     for q in range(8):
        if pixels[i*8+(7-q)].color_tag==1:
            data_array[-i*2-2]+=2**q
        elif pixels[i*8+(7-q)].color_tag==2:
            data_array[-i*2-1]+=2**q
        elif pixels[i*8+(7-q)].color_tag==3:
            data_array[-i*2-2]+=2**q
            data_array[-i*2-1]+=2**q
 
 for i in range(len(data_array)):
     data_array[i]=str(hex(data_array[i]))
     if len(data_array[i])==3:
         data_array[i]=data_array[i][:2]+'0'+data_array[i][2:]
 data_number=str(data_array)
 data.config(text=data_number)
 window.update()
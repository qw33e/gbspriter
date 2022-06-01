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
window.geometry("1200x850+0+0")

x_len=0
y_len=0
screen_x=0
screen_y=0
pixel_x=0
pixel_y=0
mouse_x=0
mouse_y=0
x_pos=0
y_pos=0
version=0

#list of the data for each tile
tilelist=[0]*32
for i in range(32):
    tilelist[i]=[]
chunks=[0]*64
#list of each tile on the map
pixel_array=[0]*18
for i in range(18):
    pixel_array[i]=[0]*40
pixels=[]

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
   pixel_name=Pixel(window_name, '#ffffff', pixel_name,'')
   pixel_name.stamp()
   pixels.append(pixel_name)
 
def paint(event):
 if mouse_x<67 and mouse_y<52:
  global chunks
  global x_pos
  global y_pos
  global pixel_array
  global version
  chunks2=chunks.copy()
  pos=int(math.floor((mouse_x)/0.413)/8)*8+160*int((math.floor((mouse_y+8)/0.413))/8)*8
  pixel_array[int((math.floor((mouse_y+8)/0.413))/8)+y_pos][(int(math.floor((mouse_x)/0.413)/8)+x_pos)*2]=int(tileslut.get())
  pixel_array[int((math.floor((mouse_y+8)/0.413))/8)+y_pos][(int(math.floor((mouse_x)/0.413)/8)+x_pos)*2+1]=version
  for i in range(8):
    for q in range(8):
        pixels[pos+q+160*(7-i)].color_tag=0
        if chunks2[2*i]>=2**(7-q):
            chunks2[2*i]-=2**(7-q)
            pixels[pos+q+160*(7-i)].color_tag+=1
        if chunks2[2*i+1]>=2**(7-q):
            chunks2[2*i+1]-=2**(7-q)
            pixels[pos+q+160*(7-i)].color_tag+=2
        if pixels[pos+q+160*(7-i)].color_tag==0:
            pixels[pos+q+160*(7-i)].color="#FFFFFF"
        elif pixels[pos+q+160*(7-i)].color_tag==1:
            pixels[pos+q+160*(7-i)].color="#AAAAAA"
        elif pixels[pos+q+160*(7-i)].color_tag==2:
            pixels[pos+q+160*(7-i)].color="#555555"
        elif pixels[pos+q+160*(7-i)].color_tag==3:
            pixels[pos+q+160*(7-i)].color="#000000"
        pixels[pos+q+160*(7-i)].stamp()

def mouse_move(event):
 x, y=event.x, event.y
 global mouse_x
 global mouse_y
 mouse_x, mouse_y=round(x/12-0.5), round((screen_y-y-100)/12)

def clip():
    global pixel_array
    global tilelist
    dimension=dimensions.get()
    dimension=dimension.split('x')
    dimension[0]=eval(dimension[0])
    dimension[1]=eval(dimension[1])
    file=open('map_map.c', 'w')
    text="#define map_mapWidth "+str(dimension[0])+"\n#define map_mapHeight "+str(dimension[1])+"\n#define map_mapBank 0\n#define map_map map_mapPLN0\nconst unsigned char bigmap_mapPLN0[] =\n{\n"
    for i in range(dimension[1]):
        for q in range(dimension[0]):
            chunk=hex(pixel_array[-i-1][2*q]+32*pixel_array[-i-1][2*q+1])
            if len(chunk)==3:
                chunk=chunk[:2]+'0'+chunk[2:]
            text+=chunk+","
        text+="\n"
    text=text[:-2]
    text+="\n};"
    file.write(text)
    file.close()

    file=open('map_map.h','w')
    text="#ifndef __map_map_h_INCLUDE\n#define __map_map_h_INCLUDE\n\n#define map_mapWidth "+str(dimension[0])+"\n#define map_mapHeight "+str(dimension[1])+"\n#define map_mapBank 0\n\n#define map_map map_mapPLN0\nextern const unsigned char map_mapPLN0[];\n\n#endif"
    file.write(text)
    file.close()

    file=open('map_tiles.h','w')
    text="#ifndef __map_tiles_h_INCLUDE\n#define __map_tiles_h_INCLUDE\n\n#define map_tilesBank 0\nextern const unsigned char map_tiles[];\n\n#endif"
    file.write(text)
    file.close()

    file=open('map_tiles.c', 'w')
    text="const unsigned char map_tiles[] =\n{\n"
    for i in range(8):
        for q in range(32):
            if len(tilelist[q])>i:
                text+=tilelist[q][i]+",\n"
            else:
                break
    text=text[:-2]
    text+="\n};"
    file.write(text)
    file.close()
        

def load_sprite(event):
    global chunks
    global tilelist
    global version
    tileselect=int(tileslut.get())
    spriteset=eval("t"+str(tileselect)).get()
    if spriteset not in tilelist[tileselect]:
     tilelist[tileselect].append(spriteset)
    eval("t"+str(tileselect))['values']=tilelist[tileselect]
    version=eval("t"+str(tileselect)).current()
    chunks = spriteset.split(',')
    for i in range(len(chunks)):
        chunks[i]=int(chunks[i],16)

def set_dimension():
    global pixel_array
    print(pixel_array)
    dimension=dimensions.get()
    dimension=dimension.split('x')
    dimension[0]=eval(dimension[0])
    dimension[1]=eval(dimension[1])
    if 2*dimension[0]<len(pixel_array[0]):
        dif=len(pixel_array[0])-2*dimension[0]
        for i in range(len(pixel_array)):
            pixel_array[i]=pixel_array[i][:-dif]
    elif 2*dimension[0]>len(pixel_array[0]):
        dif=2*dimension[0]-len(pixel_array[0])
        for i in range(len(pixel_array)):
            for q in range(dif):
                pixel_array[i].append(0)
    if dimension[1]<len(pixel_array):
        dif=len(pixel_array)-dimension[1]
        pixel_array=pixel_array[:-dif]
    elif dimension[1]>len(pixel_array):
        dif=dimension[1]-len(pixel_array)
        for i in range(dif):
            pixel_array.insert(0,[0])
            pixel_array[0]=[0]*2*dimension[0]
    print(pixel_array)

def left(event):
    global x_pos
    x_pos-=1
    reload()
def right(event):
    global x_pos
    x_pos+=1
    reload()
def up(event):
    global y_pos
    y_pos+=1
    reload()
def down(event):
    global y_pos
    y_pos-=1
    reload()

def reload():
  global chunks
  global x_pos
  global y_pos
  global pixel_array
  global tilelist
  data.config(text=str(x_pos)+","+str(-y_pos))
  for b in range(18):
   for d in range(20):
    chunks2=tilelist[pixel_array[b+y_pos][2*(d+x_pos)]][pixel_array[b+y_pos][2*(d+x_pos)+1]].split(",")
    for i in range(len(chunks2)):
        chunks2[i]=int(chunks2[i],16)
    pos=d*8+160*8*b
    for i in range(8):
     for q in range(8):
        pixels[pos+q+160*(7-i)].color_tag=0
        if chunks2[2*i]>=2**(7-q):
            chunks2[2*i]-=2**(7-q)
            pixels[pos+q+160*(7-i)].color_tag+=1
        if chunks2[2*i+1]>=2**(7-q):
            chunks2[2*i+1]-=2**(7-q)
            pixels[pos+q+160*(7-i)].color_tag+=2
        if pixels[pos+q+160*(7-i)].color_tag==0:
            pixels[pos+q+160*(7-i)].color="#FFFFFF"
        elif pixels[pos+q+160*(7-i)].color_tag==1:
            pixels[pos+q+160*(7-i)].color="#AAAAAA"
        elif pixels[pos+q+160*(7-i)].color_tag==2:
            pixels[pos+q+160*(7-i)].color="#555555"
        elif pixels[pos+q+160*(7-i)].color_tag==3:
            pixels[pos+q+160*(7-i)].color="#000000"
        pixels[pos+q+160*(7-i)].stamp()

qdee(window, 800, 720, 160, 144)
tk.canvas.bind('<Motion>', mouse_move)
window.bind("<Button-1>", paint)
window.bind("<Return>", load_sprite)
window.bind('a', left)
window.bind('d', right)
window.bind('w', up)
window.bind('s', down)
data=Label(window, text="0,0")
data.place(x=5, y=35)
thebutton = tk.Button(window, text ="Clip", command = clip)
thebutton.place(x=8, y=12)
dimensions=Entry(window, width=20)
dimensions.insert(0,'20x18')
dimensions.place(x=150, y=12)
theotherotherbutton=Button(window, text="dimension", command=set_dimension)
theotherotherbutton.place(x=70, y=15)
tileslut=Entry(window, width=20)
tileslut.insert(0,'0')
tileslut.place(x=900, y=20)

for i in range(32):
    exec("t"+str(i)+" = ttk.Combobox(window, values = tilelist[i])")
    eval("t"+str(i)).set("Select Tile")
    eval("t"+str(i)).place(x=900, y=25*i+50)
    exec("d"+str(i)+"=Label(window, text=str(i))")
    eval("d"+str(i)).place(x=870, y=25*i+50)

while True:
 window.update()
#IMPORTS
import math
import tkinter as tk
import random
import time

#VARIABLES
x=[1,2,4,7]
y=[1,2,4,5]
z=[1,2,4,5]
focal_lenght=150
camx=0
camy=0
camz=-10
pitch=0
yaw=0
sizex=300
sizey=300
ot = time.time()

#SETUP_WINDOW
window = tk.Tk()
window.title("BLEH")
window.geometry(str(sizex)+"x"+str(sizey))
canvas = tk.Canvas(window, width=(sizex), height=(sizey), bg="white")
canvas.pack(fill="both", expand=True)
canvas.pack()


#rendering
def render():

    #getting and setting varibles
    global x,y,z,focal_lenght,camx,camy,camz,pitch,yaw,sizex,sizey,ot
    ot = time.time()
    weg=0
    for i in range(int(len(x)/4)):
        xscreen= []
        yscreen= []

        #reseting screen
        canvas.delete("all")

        for i in range(4):
            #set screen position
            x1 =  (x[weg]-camx)*math.cos(yaw)+(z[weg]-camz)*math.sin(yaw)
            z1 = -(x[weg]-camx)*math.sin(yaw)+(z[weg]-camz)*math.cos(yaw)
            y1 =  (y[weg]-camy)
            y2 = y1 * math.cos(pitch) - z1 * math.sin(pitch)
            z2 = y1 * math.sin(pitch) + z1 * math.cos(pitch)
            x2 = x1
            xscreen.append((sizex/2)+focal_lenght * x2 / (z2))
            yscreen.append((sizey/2)-focal_lenght * y2 / (z2))
            weg+=1
        #check for the point
        #make poligons
        canvas.create_polygon(
        xscreen[3], yscreen[3],
        xscreen[1], yscreen[1],
        xscreen[2], yscreen[2],
        fill="blue", outline="blue")
        canvas.create_polygon(
        xscreen[0], yscreen[0],
        xscreen[1], yscreen[1],
        xscreen[2], yscreen[2],
        fill="skyblue", outline="skyblue")
    #INFO
    plotter=0
    tt = time.time() - ot
    if plotter==0:
        print("RENDER   INFO: "+str(math.floor(tt))+ "sec and "+ str(round(tt * 1000 - math.floor(tt) * 1000, 2))+ "ms","FPS:",round(1 / (tt+0.001)),"OBJEKTS:",int(len(x)/4))
        print("PLAYER   INFO: x:",camx,"y:",camy,"z:",camz,"pitch",pitch* (360 / 6.283185307),"yaw",yaw* (360 / 6.283185307))
        print("SCREEN   INFO: sizes:",sizex,sizey,"FOV:",focal_lenght)
        print()
    else:
        print((camx,camy,camz,pitch,yaw))


#keys detect
def move(event):
    global cx, cy,camx,camy,camz,pitch,yaw

    if event.keysym == "w":
        camx+=math.sin(-yaw)
        camz+=math.cos(-yaw)
    elif event.keysym == "s":
        camx+=math.sin(-(yaw+3))
        camz+=math.cos(-(yaw+3))
    elif event.keysym == "a":
        camx+=math.sin(-(yaw+1.5))
        camz+=math.cos(-(yaw+1.5))
    elif event.keysym == "d":
        camx+=math.sin(-(yaw+4.5))
        camz+=math.cos(-(yaw+4.5))
    elif event.keysym == "space":
        camy+=0.5
    elif event.keysym in ("Shift_L"):
        camy-=0.5
    elif event.keysym == "Up":
        pitch += 0.1
    elif event.keysym == "Down":
        pitch -= 0.1
    elif event.keysym == "Left":
        yaw += 0.1
    elif event.keysym == "Right":
        yaw -= 0.1

    #ROUNDING STUFF FOR SETESFYINES OR SOMETHING LIKE THAT
    rp=10000000000000000000    #roundingpower
    #camx= (round(camx*rp))/rp
    #camz= (round(camz*rp))/rp
    #camy= (round(camy*rp))/rp
    yaw= (round(yaw*rp))/rp
    pitch= (round(pitch*rp))/rp
    render()
window.bind("<Key>", move)

#sets the new window size
def sizewindow():
    global sizex,sizey
    # size to window
    window.update()
    if window.winfo_width() != sizex or window.winfo_height() != sizey:
        sizex = window.winfo_width()
        sizey = window.winfo_height()
        render()
    window.after(1000, sizewindow)

def offscreen_distance(x, y, sizex, sizey):
    dx = 0
    dy = 0
    if x < 0:
        dx = x
    elif x > sizex:
        dx = x - sizex
    if y < 0:
        dy = y
    elif y > sizey:
        dy = y - sizey
    dist = math.sqrt(dx*dx + dy*dy)
    return dist, dx, dy

#WINDOW LOOPS
render()
sizewindow()
window.mainloop()
'''
FEATURES:
500cubes max if you want max fps
MOVES WITH WINDOW
3D rendering
movment
rotation
custom window lenght hight


NOTES
2.MAKe the backwork grafik work
4.level system
5.gravity and colision
6.make a few levels
#optimis the rendering stuff probably fixed with 2.

'''

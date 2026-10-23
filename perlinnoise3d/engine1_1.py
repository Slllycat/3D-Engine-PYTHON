import tkinter as tk
import math
#version 1.1

class Camera:
    def __init__(self, position:tuple, yaw:float, pitch:float, fov:float):
        self.pos = position
        self.yaw = yaw
        self.pitch = pitch
        self.fov = fov

class Mesh():
    def __init__(self,vertices:list[list,tuple],triangles:list[list,tuple],color="white",tag:str=None):
        self.vert=vertices
        self.tri=triangles
        self.color=color
        self.tag=tag

def make_line_with_points(points2,color="white",tag:str=None):
    m=Mesh(
        vertices=points2,
        triangles=[(0,1,0)],
        color=color,
        tag=tag
    )
    return m

def make_triangle_with_points(points3,color="white",tag:str=None):
    m=Mesh(
        vertices=points3,
        triangles=[(0,1,2)],
        color=color,
        tag=tag
    )
    return m

def make_rectangle_with_points(points4,color="white",tag:str=None):
    m=Mesh(
        vertices=points4,
        triangles=[(0,1,2),(0,2,3)],
        color=color,
        tag=tag
    )
    return m

def make_rectangle_with_stats(origin,lenght,hight,color="white",tag:str=None):
    vert=[]
    vert.append(origin)
    vert.append(addtopoint(origin,lenght,[0]))
    vert.append(addtopoint(origin,hight,[1]))
    vert.append(addtopoint(addtopoint(origin,lenght,[0]),hight,[1]))
    m=Mesh(
        vertices=vert,
        triangles=[(0,1,2),(0,2,3)],
        color=color,
        tag=tag
    )
    return m

def visualsetup(size,title0="bleh",backg="black"):
    global canvas,window
    #window setup
    window = tk.Tk()
    window.title(title0)
    window.geometry(str(size)+"x"+str(size))
    canvas=tk.Canvas(window,width=size,height=size,bg=backg)
    canvas.pack()

def make3d2d(point,pos,yaw,pitch,fov):
    #move it to origin
    cx,cy,cz=pos
    x0,y0,z0=point
    x0-=cx
    y0-=cy
    z0-=cz

    cyaw=math.cos(yaw)
    syaw=math.sin(yaw)
    x1=x0*cyaw-z0*syaw
    y1=y0
    z1=x0*syaw+z0*cyaw

    cp=math.cos(pitch)
    sp=math.sin(pitch)
    x2=x1
    y2=y1*cp-z1*sp
    z2=y1*sp+z1*cp

    if z2>0:
        return x2*fov/z2,y2*fov/z2

def bindtocam(size,sx,sy):
    sx+=size/2
    sy=size/2-sy
    return sx,sy

def addtopoint(point,add,ind=None):
    if ind is None:
        return tuple([i+add for i in point])
    else:
        tmp=list(point)
        for i in ind:
            tmp[i]=point[i]+add
        return tuple(tmp)

def draw2point(size,sx,sy,color="white",psize=3,tag=None):
    sx,sy=bindtocam(size,sx,sy)
    canvas.create_rectangle(sx,sy,sx+psize,sy+psize,fill=color,tags=tag)

def draw3point(size,point,cam,color="white",psize=3,tag=None):
    a=make3d2d(point,cam.pos,cam.yaw,cam.pitch,cam.fov)
    if a is None:
        return "OFF SCREEN"
    sx,sy=a
    draw2point(size,sx,sy,color,psize,tag)

def rendermesh(size,mesh:Mesh,cam):
    p=[make3d2d(i,cam.pos,cam.yaw,cam.pitch,cam.fov) for i in mesh.vert]
    for i in p:
        if i is None:
            return "OFFSCREEN"
    p=[bindtocam(size,*i)for i in p]
    for i in mesh.tri:
        canvas.create_polygon(p[i[0]],p[i[1]],p[i[2]],fill=mesh.color,tags=mesh.tag)


def clear(tag="all"):
    canvas.delete(tag)

def run():
    window.mainloop()
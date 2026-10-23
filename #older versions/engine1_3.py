import tkinter as tk
import math
#version 1.3

class Camera:
    def __init__(self, position:list[float], yaw:float, pitch:float, fov:float):
        self.pos=position
        self.yaw=yaw
        self.pitch=pitch
        self.fov=fov
    
    def setpos(self,pos:list[float]):
        self.pos=pos
    
    def movepos(self,amount:list[float]):
        self.pos=[i+i2 for i,i2 in zip(self.pos,amount)]

    def setrotation(self,yaw=0,pitch=0):
        self.yaw=yaw
        self.pitch=pitch

    def rotate(self,yaw=0,pitch=0):
        self.yaw+=yaw
        self.pitch+=pitch
        
    

class Mesh:
    def __init__(self,vertices:list[list[float]],triangles:list[list[float]],color:list[str]=[],wire:bool=False,tag:str=None):
        if len(color)==0:
            color=["white" for _ in range(len(triangles))]
        elif len(color)==1:
            color=[color[0] for _ in range(len(triangles))]
        self.vert=vertices
        self.tri=triangles
        self.color=color
        self.tag=tag
        self.wire=wire
    
    def meshtoorigin(self,pos:list[float]):
        return Mesh(
            vertices=[[j+j2 for j,j2 in zip(i,pos)] for i in self.vert],
            triangles=self.tri,
            color=self.color,
            tag=self.tag,
            wire=self.wire)

    def scalemesh(self,scale:list[float]):
        return Mesh(
            vertices=[[j*j2 for j,j2 in zip(i,scale)] for i in self.vert],
            triangles=self.tri,
            color=self.color,
            tag=self.tag,
            wire=self.wire)

    def rotatemesh(self,rotation:list[float]):
        return Mesh(
            vertices=[rotatepoint(i,rotation)for i in self.vert],
            triangles=self.tri,
            color=self.color,
            tag=self.tag,
            wire=self.wire)

class Object3d():
    def __init__(self,mesh:Mesh,pos:list[float]=[0,0,0],rotation:list[float]=[0,0,0],scale:list[float]=[1,1,1]):
        self.mesh=mesh
        self.pos=pos
        self.rot=rotation
        self.getscale=scale

    def scale(self,scale:list[float]):
        self.mesh=self.mesh.scalemesh(scale)

    def setrotate(self,rotation:list[float]):
        self.rot=rotation
    
    def rotate(self,rotation:list[float]):
        self.rot=[i+i2 for i,i2 in zip(self.rot,rotation)]

    def setpos(self,pos:list[float]):
        self.pos=pos
    
    def move(self,pos:list[float]):
        self.pos=[i+i2 for i,i2 in zip(self.pos,pos)]

class Mouse:
    def __init__(self,mousex,mousey):
        self.mx=mousex
        self.my=mousey

class Input:
    def __init__(self):
        self.keys=set()
        self.mousebuttons=set()
        self.mousepos=Mouse(0, 0)
    
    def keydown(self, event):
        self.keys.add(event.keysym)
    
    def keyup(self,event):
        self.keys.discard(event.keysym)
    
    def mousedown(self,event):
        self.mousebuttons.add(event.num)
    
    def mouseup(self,event):
        self.mousebuttons.discard(event.num)
    
    def mousemove(self,event):
        self.mousepos.mx=event.x
        self.mousepos.my=event.y
    
    def isdown(self,key):
        return key in self.keys

    def mouseisdown(self, button):
        return button in self.mousebuttons

def inputsetup():
    global input
    input=Input()
    window.bind("<KeyPress>",input.keydown)
    window.bind("<KeyRelease>",input.keyup)
    canvas.bind("<ButtonPress>",input.mousedown)
    canvas.bind("<ButtonRelease>",input.mouseup)
    canvas.bind("<Motion>",input.mousemove)

def meshtriangle(color:list[str]=[],tag:str=None):
    m=Mesh(
        vertices=[[0,0,0],[1,0,0],[1,1,0]],
        triangles=[[0,1,2]],
        color=color,
        tag=tag
    )
    return m

def objecttriangle(pos:list[float]=[0,0,0],rot:list[float]=[0,0,0],scale:list[float]=[1,1,1],color:list[str]=[],tag:str=None):
    m=Mesh(
        vertices=[[0,0,0],[1,0,0],[1,1,0]],
        triangles=[[0,1,2]],
        color=color,
        tag=tag
    )
    o=Object3d(
        mesh=m,
        pos=pos,
        rotation=rot,
        scale=scale
    )
    return o

def meshrectangle(color:list[str]=[],tag:str=None):
    m=Mesh(
        vertices=[[0,0,0],[0,1,0],[1,1,0],[1,0,0]],
        triangles=[[0,1,2],[0,2,3]],
        color=color,
        tag=tag
    )
    return m

def objectrectangle(pos:list[float]=[0,0,0],rot:list[float]=[0,0,0],scale:list[float]=[1,1,1],color:list[str]=[],tag:str=None):
    m=Mesh(
        vertices=[[0,0,0],[0,1,0],[1,1,0],[1,0,0]],
        triangles=[[0,1,2],[0,2,3]],
        color=color,
        tag=tag
    )
    o=Object3d(
        mesh=m,
        pos=pos,
        rotation=rot,
        scale=scale
    )
    return o

def meshcube(color:list[str]=[],tag:str=None):
    m=Mesh(
        vertices=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],
        triangles=[[0,1,2],[0,2,3],[4,6,5],[4,7,6],[0,4,5],[0,5,1],[2,6,7],[2,7,3],[0,3,7],[0,7,4],[1,5,6],[1,6,2]],
        color=color,
        tag=tag
    )
    return m

def objectcube(pos:list[float]=[0,0,0],rot:list[float]=[0,0,0],scale:list[float]=[1,1,1],color:list[str]=[],tag:str=None):
    m=Mesh(
        vertices=[[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],
        triangles=[[0,1,2],[0,2,3],[4,6,5],[4,7,6],[0,4,5],[0,5,1],[2,6,7],[2,7,3],[0,3,7],[0,7,4],[1,5,6],[1,6,2]],
        color=color,
        tag=tag
    )
    o=Object3d(
        mesh=m,
        pos=pos,
        rotation=rot,
        scale=scale
    )
    return o

def visualsetup(size:int,title0:str="bleh",backg:str="black"):
    global canvas,window
    #window setup
    window = tk.Tk()
    window.title(title0)
    window.geometry(str(size)+"x"+str(size))
    canvas=tk.Canvas(window,width=size,height=size,bg=backg)
    canvas.pack()

def make3d2d(point:list[float],pos:list[float],yaw:float,pitch:float,fov:float):
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

def mergeobject(obj1:Object3d,obj2:Object3d):
    return Object3d(
        mesh=mergemesh(obj1.mesh,obj2.mesh),
        pos=obj1.pos,
        rotation=obj1.rot,
        scale=obj1.getscale)

def mergemesh(mesh1:Mesh,mesh2:Mesh):
    return Mesh(
        vertices=mesh1.vert+mesh2.vert,
        triangles=mesh1.tri+[[i2+len(mesh1.vert) for i2 in i] for i in mesh2.tri],
        color=mesh1.color+mesh2.color,
        tag=mesh1.tag,
        wire=mesh1.wire)

def bindtocam(size:int,sx:float,sy:float):
    sx+=size/2
    sy=size/2-sy
    return sx,sy

def addtopoint(point:list[float],add:float,ind:list=None):
    if ind is None:
        return [i+add for i in point]
    else:
        tmp=list(point)
        for i in ind:
            tmp[i]=point[i]+add
        return tmp

def rotatepoint(point:list[float],rotation:list[float]):
    x,y,z=point
    rx,ry,rz=rotation
    # X rotation
    cx=math.cos(rx)
    sx=math.sin(rx)
    y2=y*cx-z*sx
    z2=y*sx+z*cx
    y=y2
    z=z2
    #Y rotation
    cy=math.cos(ry)
    sy=math.sin(ry)
    x2=x*cy+z*sy
    z2=-x*sy+z*cy
    x=x2
    z=z2
    #Z rotation
    cz=math.cos(rz)
    sz=math.sin(rz)
    x2=x*cz-y*sz
    y2=x*sz+y*cz
    x=x2
    y=y2
    return[x,y,z]

def draw2point(size:int,sx:float,sy:float,color:str="white",psize:int=3,tag:str=None):
    sx,sy=bindtocam(size,sx,sy)
    canvas.create_rectangle(sx,sy,sx+psize,sy+psize,fill=color,tags=tag)

def draw3point(size:int,point:list[float],cam:Camera,color:str="white",psize:int=3,tag:str=None):
    a=make3d2d(point,cam.pos,cam.yaw,cam.pitch,cam.fov)
    if a is None:
        return "OFF SCREEN"
    sx,sy=a
    draw2point(size,sx,sy,color,psize,tag)

def rendermesh(size:str,mesh:Mesh,cam:Camera):
    p=[make3d2d(i,cam.pos,cam.yaw,cam.pitch,cam.fov) for i in mesh.vert]
    for i in p:
        if i is None:
            return "OFFSCREEN"
    p=[bindtocam(size,*i)for i in p]
    for i in range(len(mesh.tri)):
        canvas.create_polygon(p[mesh.tri[i][0]],p[mesh.tri[i][1]],p[mesh.tri[i][2]],fill=mesh.color[i],tags=mesh.tag)

def renderobject(size:int,obj:Object3d,cam:Camera,hidefully:bool=False):
    mesh=obj.mesh.scalemesh(obj.getscale)
    mesh=mesh.rotatemesh(obj.rot)
    mesh=mesh.meshtoorigin(obj.pos)
    p=[make3d2d(i,cam.pos,cam.yaw,cam.pitch,cam.fov) for i in mesh.vert]
    if hidefully:
        for i in p:
            if i is None:
                return "OFFSCREEN"
        p=[bindtocam(size,*i)for i in p]
        for i in range(len(mesh.tri)):
            if not mesh.wire:
                canvas.create_polygon(p[mesh.tri[i][0]],p[mesh.tri[i][1]],p[mesh.tri[i][2]],fill=mesh.color[i],tags=mesh.tag)
            else:
                canvas.create_polygon(p[mesh.tri[i][0]],p[mesh.tri[i][1]],p[mesh.tri[i][2]],outline=mesh.color[i],fill="",tags=mesh.tag)
    else:
        for i in range(len(mesh.tri)):
                if not(p[mesh.tri[i][0]] is None or p[mesh.tri[i][1]] is None or p[mesh.tri[i][2]] is None):
                    p1,p2,p3=bindtocam(size,*p[mesh.tri[i][0]]),bindtocam(size,*p[mesh.tri[i][1]]),bindtocam(size,*p[mesh.tri[i][2]])
                    if not mesh.wire:
                        canvas.create_polygon(p1,p2,p3,fill=mesh.color[i],tags=mesh.tag)
                    else:
                        canvas.create_polygon(p1,p2,p3,outline=mesh.color[i],fill="",tags=mesh.tag)        

def clear(tag:str="all"):
    canvas.delete(tag)

def run():
    window.mainloop()
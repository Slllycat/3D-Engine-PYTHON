import math
import engine1_4 as e
zoom=5             #5       5
depth=1            #10     10
cl=1                #1/0    1/0
biggnes=10           #25     10
size=50            #30    50
dist=30             #30     30
delay=1            #1      1

scale3d=10           #5      10
fill=False
cam=e.Camera(position=(size,size,-dist),yaw=0,pitch=0,fov=90)


def rad(s):
    import random
    rad=[]
    for _ in range(s**2):
        rad.append(math.radians(random.randint(0,359)))
    return rad

def fade(t):
    return t*t*t*(t*(t*6-15)+10)

def dotp(x,y,v,s):
    i=math.floor(x)+math.floor(y)*(s+1)
    xs,ys=x%1,y%1
    a=v[i]
    dx=-xs*math.cos(a)
    dy=-ys*math.sin(a)
    d1=dx+dy

    a=v[i+1]
    dx=(1-xs)*math.cos(a)
    dy=-ys*math.sin(a)
    d2=dx+dy

    a=v[i+(s+1)]
    dx=-xs*math.cos(a)
    dy=(1-ys)*math.sin(a)
    d3=dx+dy

    a=v[i+(s + 1)+1]
    dx=(1-xs)*math.cos(a)
    dy=(1-ys)*math.sin(a)
    d4=dx+dy
    u = fade(xs)
    v2 = fade(ys)
    lx1=(1-u)*d1+u*d2
    lx2=(1-u)*d3+u*d4
    l=(1-v2)*lx1+v2*lx2
    return l

def perlinpoint(x,y,v,s):
    p=dotp(x,y,v,s)
    return p


def perlinnoise(vsize,asize):
    v=rad(vsize+1)
    points=[]
    x,y=0,0
    for _ in range(asize):
        for _ in range(asize):
            points.append(perlinpoint(x,y,v,vsize))
            x+=(vsize/asize)
        x=0
        y+=(vsize/asize)
    return points

def multiperlinnoise(vsize,asize,depth):
    creat=0.5   # persistence
    amp=1.0
    vs=vsize
    points=[]
    for i in range(depth):
        v=rad(vsize+1)
        a=0
        x,y=0,0
        for _ in range(asize):
            for _ in range(asize):
                p = perlinpoint(x, y, v, vsize) * amp
                if i ==0:
                    points.append(p)
                else:
                    points[a] += p
                x+=(vsize/asize)
                a+=1
            x=0
            y+=(vsize/asize)
        vsize = vs*(i+2) # higher frequency
        amp *= creat                # lower strength
    return points

def valuetocolor(v,cl): #bleb RGB
    if cl==True:
        if v <= 0:
            c = int((v + 1) * 255)
            return f"#{0:02x}{0:02x}{c:02x}"
        elif v<0.1:
            c = int((v+0.1)*5*255)
            return f"#{c:02x}{c:02x}{0:02x}"
        else:
            c = int(255-(v* 255))
            return f"#{0:02x}{c:02x}{0:02x}"
    else:
        gray = int((v + 1) / 2 * 255)
        return f"#{gray:02x}{gray:02x}{gray:02x}"

e.visualsetup(size * biggnes)
a=multiperlinnoise(zoom,size,depth)
vertices = []
faces = []
colors = []

# Create each vertex ONCE
for y in range(size):
    for x in range(size):
        i = y * size + x

        vertices.append((
            x*2,
            -a[i]*scale3d,
            y*2
        ))
for y in range(size-1):
    for x in range(size-1):
        i=y*size+x
        faces.append([i,i+1,i+size+1])
        faces.append([i,i+size+1,i+size])
        color=valuetocolor(a[i],cl)
        colors.append(color)
        colors.append(color)

obj = e.Object3d(
    e.Mesh(vertices,faces, colors)
)
obj.mesh.wire=False
print(len(obj.mesh.tri))

e.inputsetup()
def mainloop():
    global cam,obj
    e.clear()
    e.renderobject(size*biggnes,obj,cam)
    if e.input.isdown("Left"):cam.movepos([-1,0,0])
    if e.input.isdown("Right"):cam.movepos([1,0,0])
    if e.input.isdown("Up"):cam.movepos([0,0,1])
    if e.input.isdown("Down"):cam.movepos([0,0,-1])
    if e.input.isdown("Shift_L"):cam.movepos([0,1,0])
    if e.input.isdown("space"):cam.movepos([0,-1,0])
    e.window.after(delay,mainloop)
    
mainloop()
e.run()
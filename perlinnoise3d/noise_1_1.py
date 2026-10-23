import math
import engine1_1 as e
zoom=4             #5       5       4
depth=10            #10     10      10
cl=1                #1/0    1/0     1
biggnes=10           #10     5       2
size=100            #100    200     400
dist=40             #40     40     100
delay =1            #1      1       1

scale3d=10           #5      5      10
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
x,y,weg=0,0,0
for i in range(size):
    for i2 in range(size):
        color=valuetocolor(a[weg],cl)
        if i2!=size-1 and i!=size-1:
            m=e.make_rectangle_with_points(
                [
                    (i*2,i2*2,-a[weg]*scale3d),
                    (i*2+2,i2*2,-a[weg+size]*scale3d),
                    (i*2+2,i2*2+2,-a[weg+size+1]*scale3d),
                    (i*2,i2*2+2,-a[weg+1]*scale3d)
                ]
                ,color)
            e.rendermesh(size*biggnes,m,cam)
        x+=biggnes
        weg+=1
    y+=biggnes
    x=0

e.run()
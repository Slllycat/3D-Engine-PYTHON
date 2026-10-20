import engine1_5 as e
import random

size=700
cam=e.Camera(position=[5,1,-20],yaw=0,pitch=0,fov=1000)

def makerooms(l):
    mesh=e.Mesh([],[],[])
    for z in range(l):
        for x in range(l):
            if random.randint(0,4)==0:
                m=e.Mesh([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],[[0,1,2],[0,2,3],[4,6,5],[4,7,6],[0,3,7],[0,7,4],[1,5,6],[1,6,2]],["#C8B95A","#C8B95A","#C8B95A","#C8B95A","#C8B95A","#C8B95A","#C8B95A","#C8B95A"])
                m=m.meshtoorigin([x*2,0,z*2])
                mesh=e.mergemesh(mesh,m)
            else:
                m=e.Mesh([[-1,-1,-1],[1,-1,-1],[1,1,-1],[-1,1,-1],[-1,-1,1],[1,-1,1],[1,1,1],[-1,1,1]],[[0,4,5],[0,5,1],[2,6,7],[2,7,3]],["#6B5942","#6B5942","#D6C96A","#D6C96A"])
                m=m.meshtoorigin([x*2,0,z*2])
                mesh=e.mergemesh(mesh,m)
    return mesh


mesh=makerooms(15)
mesh.wire=False
print("Truangles",len(mesh.tri))
objt1=e.Object3d(mesh)
objt1.scale([5,5,5])
a,s=0,0
e.visualsetup(size)
def mainloop():
    global objt1,cam,a,s
    e.clear()
    e.renderobject(size,objt1,cam)
    if e.input.isdown("a"):cam.movepos([-0.1,0,0])
    if e.input.isdown("d"):cam.movepos([0.1,0,0])
    if e.input.isdown("w"):cam.movepos([0,0,0.1])
    if e.input.isdown("s"):cam.movepos([0,0,-0.1])
    if e.input.isdown("e"):cam.movepos([0,0.1,0])
    if e.input.isdown("q"):cam.movepos([0,-0.1,0])
    if e.input.isdown("up"):cam.rotate(0,0.004)
    if e.input.isdown("down"):cam.rotate(0,-0.004)
    if e.input.isdown("left"):cam.rotate(-0.004,0)
    if e.input.isdown("right"):cam.rotate(0.004,0)
    s+=e.getfps()
    a+=1
    if a>100:
        print(s//a)
        a=0
        s=0
e.loop(mainloop)
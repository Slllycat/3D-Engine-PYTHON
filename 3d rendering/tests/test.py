import engine1_5 as e
import random,time

debug=True
if debug:
    import cProfile
    import pstats

    profiler = cProfile.Profile()
    profiler.enable()

size=700
cam=e.Camera(position=[5,1,-20],yaw=0,pitch=0,fov=500)

a=[]
aaa=10
for x in range(aaa):
    for y in range(aaa):
        for z in range(aaa):
            b=e.objectcube(pos=[x*4,y*4,10+z*4],scale=[1,1,1],color=["violet"])
            b.mesh.wire=True
            a.append(b)

e.visualsetup(size)
def mainloop():
    global a,cam
    e.clear()
    for i in a:
        e.renderobject(size,i,cam)
        i.rotate([random.randint(1,400)/10000,random.randint(1,400)/10000,random.randint(1,400)/10000])
    if e.input.isdown("left"):cam.movepos([-0.1,0,0])
    if e.input.isdown("right"):cam.movepos([0.1,0,0])
    if e.input.isdown("up"):cam.movepos([0,0,0.1])
    if e.input.isdown("down"):cam.movepos([0,0,-0.1])
    if e.input.isdown("q"):cam.movepos([0,0.1,0])
    if e.input.isdown("e"):cam.movepos([0,-0.1,0])
    print(e.getfps())
    time.sleep(0.016)
e.loop(mainloop)
if debug:
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats("cumtime").print_stats(20)

import engine1_5 as e
import random
import math


def applemesh():
    vertices = []
    triangles = []
    colors = []

    # Apple body: horizontal rings
    rings = [
        (-0.95, 0.12),
        (-0.82, 0.48),
        (-0.55, 0.76),
        (-0.15, 0.88),
        (0.25, 0.82),
        (0.55, 0.65),
        (0.73, 0.40),
        (0.68, 0.12)
    ]

    segments = 3

    for y, radius in rings:
        for i in range(segments):
            angle = 2 * math.pi * i / segments

            # Slight lobes make it look more like an apple
            r = radius * (1 + 0.06 * math.cos(angle * 5))

            vertices.append([
                r * math.cos(angle),
                y,
                r * math.sin(angle)
            ])

    # Connect the rings using triangles
    for ring in range(len(rings) - 1):
        for i in range(segments):
            a = ring * segments + i
            b = ring * segments + (i + 1) % segments
            c = (ring + 1) * segments + i
            d = (ring + 1) * segments + (i + 1) % segments

            triangles.append([a, c, b])
            triangles.append([b, c, d])

            # Different reds for a little visual variation
            colors.extend([
                random.choice(["red", "firebrick", "crimson"]),
                random.choice(["red", "firebrick", "crimson"])
            ])

    # Bottom center
    bottom = len(vertices)
    vertices.append([0, -0.94, 0])

    for i in range(segments):
        a = i
        b = (i + 1) % segments
        triangles.append([bottom, b, a])
        colors.append("firebrick")

    # Brown stem
    start = len(vertices)
    vertices.extend([
        [-0.045, 0.65, -0.045],
        [ 0.045, 0.65, -0.045],
        [ 0.045, 0.65,  0.045],
        [-0.045, 0.65,  0.045],
        [-0.025, 1.05, -0.025],
        [ 0.025, 1.05, -0.025],
        [ 0.025, 1.05,  0.025],
        [-0.025, 1.05,  0.025]
    ])

    stem_faces = [
        [0, 1, 5], [0, 5, 4],
        [1, 2, 6], [1, 6, 5],
        [2, 3, 7], [2, 7, 6],
        [3, 0, 4], [3, 4, 7],
        [4, 5, 6], [4, 6, 7]
    ]

    for face in stem_faces:
        triangles.append([start + i for i in face])
        colors.append("saddlebrown")

    # Green leaf
    start = len(vertices)
    vertices.extend([
        [0.0, 0.86, 0.0],
        [0.48, 1.08, 0.0],
        [0.27, 0.94, 0.12],
        [0.27, 0.94, -0.12]
    ])

    triangles.extend([
        [start, start + 1, start + 2],
        [start, start + 3, start + 1]
    ])

    colors.extend(["forestgreen", "green"])

    return e.Mesh(
        vertices=vertices,
        triangles=triangles,
        color=colors
    )


size = 700
cam = e.Camera(position=[5, 1, -20], yaw=0, pitch=0, fov=500)

a = []
aaa = 10

# Create the apple mesh only once!
mesh = applemesh()

for x in range(aaa):
    for y in range(aaa):
        for z in range(aaa):
            apple = e.Object3d(
                mesh=mesh,
                pos=[x * 4, y * 4, 25 + z * 4],
                scale=[0.7, 0.7, 0.7]
            )
            a.append(apple)

e.visualsetup(size, title0="Apple Engine 🍎")


def mainloop():
    global a, cam

    e.clear()

    for i in a:
        e.renderobject(size, i, cam)

        i.rotate([
            random.randint(1, 400) / 10000,
            random.randint(1, 400) / 10000,
            random.randint(1, 400) / 10000
        ])

    if e.input.isdown("left"):
        cam.movepos([-0.1, 0, 0])
    if e.input.isdown("right"):
        cam.movepos([0.1, 0, 0])
    if e.input.isdown("up"):
        cam.movepos([0, 0, 0.1])
    if e.input.isdown("down"):
        cam.movepos([0, 0, -0.1])
    if e.input.isdown("q"):
        cam.movepos([0, 0.1, 0])
    if e.input.isdown("e"):
        cam.movepos([0, -0.1, 0])

    print(e.getfps())


e.loop(mainloop)

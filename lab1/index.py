import ctypes
import os
import sys
sys.path.append('..')
import numpy as np

import pyglet
from pyglet.gl import *

from pywavefront import visualization
from pywavefront import Wavefront

# Create absolute path from this module
file_abspath = os.path.join(os.path.dirname(__file__), 'data/f16.obj')
meshes = Wavefront(file_abspath)

# camera rotation
rotation = 0.0
points = []
rotation_x = -140
rotation_y = 110
rotation_z = 330
starting_z_zoom = -80

visited_points = []

def readPoints(file):
    global points
    with open(file) as f:
        for line in f:
            points.append([int(x) for x in line.split()])
    return points
readPoints("data/spiral.txt")
# print(points)
combinedPoints = []
for point in points:
    combinedPoints.append(point[0])
    combinedPoints.append(point[1])
    combinedPoints.append(point[2])
# print(combinedPoints)

# points for Approximation uniform B-spline cubic curve
r0 = np.array(points[0])
r1 = np.array(points[1])
r2 = np.array(points[2])
r3 = np.array(points[3])
def get_R():
    return np.array([r0, r1, r2, r3])

Bi3 = 1.0/6 * np.array([[-1, 3, -3, 1],
                        [3, -6, 3, 0],
                        [-3, 0, 3, 0],
                        [1, 4, 1, 0]])
# print(Bi3)

t = 0.0
def get_t3():
    return np.array([t**3, t**2, t, 1])
def get_t3_d():
    return np.array([3*t**2, 2*t, 1, 0])

def calc_pos():
    return get_t3().T @ Bi3 @ get_R()

def calc_tangent():
    return get_t3_d().T @ Bi3 @ get_R()

f1_scale = 7
# current_orientation = np.array([0, 1, 0])

window = pyglet.window.Window(1024, 720, caption='Demo', resizable=True)
lightfv = ctypes.c_float * 4
label = pyglet.text.Label(
    'Hello, world',
    font_name='Times New Roman',
    font_size=12,
    x=800, y=700,
    anchor_x='center', anchor_y='center')

@window.event
def on_resize(width, height):
    viewport_width, viewport_height = window.get_framebuffer_size()
    glViewport(0, 0, viewport_width, viewport_height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(40.0, float(width) / height, 1.0, 100.0)
    glEnable(GL_DEPTH_TEST)
    glMatrixMode(GL_MODELVIEW)
    return True

def draw_tang():
    tang = calc_tangent()
    pos = calc_pos()
    # draw the tangent
    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    pyglet.graphics.draw(2, pyglet.gl.GL_LINES,
                            ('v3f', (0, 0, 0, tang[0], tang[1], tang[2])),
                            ('c3B', (255, 0, 0, 255, 0, 0))
                            )
    glPopMatrix()

def draw_curve():
    pyglet.gl.glPointSize(2)
    combined_visited_Points = []
    for point in visited_points:
        combined_visited_Points.append(point[0])
        combined_visited_Points.append(point[1])
        combined_visited_Points.append(point[2])
    pyglet.graphics.draw(len(visited_points), pyglet.gl.GL_POINTS,
                         ('v3f', combined_visited_Points ),
                        ('c3B', (0, 0, 255) * len(visited_points))
                         )


def draw_f1(mesh):
    global f1_scale, current_orientation, visited_points

    # update the position
    pos = calc_pos()

    s = np.array([0,0,1]) # current orientation
    e = calc_tangent() # goal orientation
    # print(f"s: {s}")
    # print(f"e: {e}")

    dot = np.dot(s, e)
    cosphi = dot / (np.linalg.norm(s) * np.linalg.norm(e))
    anglerad = np.arccos(cosphi)
    angle = np.degrees(anglerad)
    axis = np.cross(s, e)
    # print(f"dot product: {dot}")
    # print(f"cos phi: {cosphi}")
    # print(f"arc-cos rad: {anglerad}")
    # print(f"angle degree: {angle}")
    # print(f"axis: {axis}")

    glPushMatrix()
    glTranslatef(pos[0], pos[1], pos[2])
    glRotatef(angle, axis[0], axis[1], axis[2])
    glScalef(f1_scale, f1_scale, f1_scale)
    visualization.draw(mesh)
    glPopMatrix()

    # current_orientation = e

    visited_points.append(pos)


@window.event
def on_draw():
    window.clear()

    pyglet.gl.glPointSize(8)

    pyglet.graphics.draw(len(points), pyglet.gl.GL_POINTS,
                         ('v3f', combinedPoints ),
                        ('c3B', (255, 0, 0) * len(points))
                         )
    
    # draw the lines using points
    pyglet.graphics.draw(len(points), pyglet.gl.GL_LINE_STRIP,
                            ('v3f', combinedPoints ),
                            ('c3B', (0, 255, 0) * len(points))
                            )

    glLoadIdentity()

    # provide some light
    """ glLightfv(GL_LIGHT0, GL_POSITION, lightfv(-40.0, 200.0, 100.0, 0.0))
    glLightfv(GL_LIGHT0, GL_AMBIENT, lightfv(0.2, 0.2, 0.2, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightfv(0.5, 0.5, 0.5, 1.0))
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHTING) """

    glEnable(GL_COLOR_MATERIAL)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_MODELVIEW)

    glTranslated(-30, 20, starting_z_zoom)

    pyglet.gl.glRotatef(rotation_x, 1, 0, 0)
    pyglet.gl.glRotatef(rotation_y, 0, 1, 0)
    pyglet.gl.glRotatef(rotation_z, 0, 0, 1)

    # set background color to sky-bue
    glClearColor(225/255, 246/255, 255/255, 1)

    draw_tang()
    draw_f1(meshes)
    draw_curve()


# Function to update rotation angles based on key events
def update_rotation(symbol, modifiers):
    global rotation_x, rotation_y, rotation_z

    # Adjust rotation angles based on key events
    if symbol == pyglet.window.key.RIGHT:
        rotation_y += 10
    elif symbol == pyglet.window.key.LEFT:
        rotation_y -= 10
    elif symbol == pyglet.window.key.UP:
        rotation_x += 10
    elif symbol == pyglet.window.key.DOWN:
        rotation_x -= 10
    elif symbol == pyglet.window.key.A:
        rotation_z += 10
    elif symbol == pyglet.window.key.D:
        rotation_z -= 10
    elif symbol == pyglet.window.key.P:
        print(rotation_x, rotation_y, rotation_z)

# Set the update function for key events
window.push_handlers(on_key_press=update_rotation)

def shift_points():
    global r0, r1, r2, r3
    r0 = r1
    r1 = r2
    r2 = r3
    last_index = np.where(np.all(points==r2,axis=1))[0][0]
    # r3 = np.array(points[(last_index + 1)])
    r3 = np.array(points[(last_index + 1) % len(points)])
    # print(r0, r1, r2, r3)

def update_t(dt):
    global t
    t += dt
    if t > 1.0:
        t = 0.0
        shift_points()
    # print(t)

"""
for windows wsl, setup xlaunch with Clipboard=True, Primary Selection=True, 
Native OpenGL=False, Disable Access Control=True run this in terminal:
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
export LIBGL_ALWAYS_INDIRECT=0

"""

pyglet.clock.schedule(update_t)
pyglet.app.run()


import pyglet
from pyglet.gl import *
import random
from dataclasses import dataclass
import ctypes


window = pyglet.window.Window(1024, 720, caption='Demo', resizable=True)

@dataclass
class global_vars:
    MAX_PARTICLES: int = 100
    MAX_AGE: int = 200
    SPEED_FACTOR: float = 1
    SCALE_FACTOR: float = 0.15
    GRAVITY: float = 0.1

global_vars = global_vars()


class Particle:
    def __init__(self, x_origin, y_origin, z_origin):
        self.dx = random.random() * 2 - 1
        self.dy = random.random() * 2 - 1
        self.dz = random.random() * 2 - 1
        self.dz = 0
        self.age = 0
        self.x = x_origin
        self.y = y_origin
        self.z = z_origin
        self.consecutive_bounces = 0

    def update(self):
        self.x += self.dx * global_vars.SPEED_FACTOR
        self.y += self.dy * global_vars.SPEED_FACTOR
        self.z += self.dz * global_vars.SPEED_FACTOR
        self.dy -= global_vars.GRAVITY
        self.age += random.random()

        # elastic bounce
        if self.y < 0:
            # print('bounce')
            self.y = 0
            self.dy *= -1


        if self.age > global_vars.MAX_AGE:
            return True
        else:
            return False
    
    def draw(self):
        pyglet.graphics.draw(1, pyglet.gl.GL_POINTS,
         ('v3f', (self.x, self.y, self.z)),
         ('c3B', (255, 0, 0)))
    

particles = []

@window.event
def on_key_press(symbol, modifiers):
    global global_vars
    print(symbol, modifiers)

    # rotate and shift viewpoint
    if symbol == pyglet.window.key.LEFT:
        glTranslatef(-10, 0, 0)
    elif symbol == pyglet.window.key.RIGHT:
        glTranslatef(10, 0, 0)
    elif symbol == pyglet.window.key.UP:
        glTranslatef(0, 10, 0)
    elif symbol == pyglet.window.key.DOWN:
        glTranslatef(0, -10, 0)
    elif symbol == pyglet.window.key.PAGEUP:
        glTranslatef(0, 0, -1)
    elif symbol == pyglet.window.key.PAGEDOWN:
        glTranslatef(0, 0, 1)
    elif symbol == pyglet.window.key.A:
        glRotatef(-10, 0, 0, 1)
    elif symbol == pyglet.window.key.D:
        glRotatef(10, 0, 0, 1)
    elif symbol == pyglet.window.key.W:
        glRotatef(10, 1, 0, 0)
    elif symbol == pyglet.window.key.S:
        glRotatef(-10, 1, 0, 0)
    elif symbol == pyglet.window.key.Q:
        glRotatef(10, 0, 1, 0)
    elif symbol == pyglet.window.key.E:
        glRotatef(-10, 0, 1, 0)
    

    # zoom in and out
    elif symbol == pyglet.window.key.Z:
        glScalef(1.1, 1.1, 1.1)
    elif symbol == pyglet.window.key.X:
        glScalef(0.9, 0.9, 0.9)
    
    # reset view
    elif symbol == pyglet.window.key.R:
        glLoadIdentity()
    
@window.event
def on_draw():
    window.clear()
    pyglet.gl.glPointSize(8)
    # label.draw()

    # background color
    #glLoadIdentity()
    glClearColor(225/255, 246/255, 255/255, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # draw particles
    for particle in particles:
        particle.draw()
    

def update(dt):
    global particles
    # update particles
    for particle in particles:
        if particle.update():
            particles.remove(particle)
    
    # add new particles
    if len(particles) < global_vars.MAX_PARTICLES:
        particles.append(Particle(window.width//2, window.height//2, 0))
    # print(len(particles))

"""
for windows wsl, setup xlaunch with Clipboard=True, Primary Selection=True, 
Native OpenGL=False, Disable Access Control=True 

then run this in terminal:
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
export LIBGL_ALWAYS_INDIRECT=0

"""

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120)
    pyglet.app.run()

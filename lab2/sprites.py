import pyglet
from pyglet.gl import *
import random
from dataclasses import dataclass
import ctypes

window = pyglet.window.Window(1024, 720, caption='Demo', resizable=True)

@dataclass
class global_vars:
    MAX_PARTICLES: int = 200
    MAX_AGE: int = 100
    SPEED_FACTOR: float = 1
    SCALE_FACTOR: float = 0.15

global_vars = global_vars()

# load particle image bmp
particle_image = pyglet.resource.image('snow.bmp')
# set the anchor point of the image to the center 
particle_image.anchor_x = particle_image.width // 2
particle_image.anchor_y = particle_image.height // 2

particles = []
batch = pyglet.graphics.Batch()

class Particle:
    def __init__(self, batch=None, img=None, x_origin=0.0, y_origin=0.0
                ):
        self.dx = random.random() * 2 - 1
        self.dy = random.random() * 2 - 1
        self.age = 0
        self.sprite = pyglet.sprite.Sprite(img, x=x_origin, y=y_origin, batch=batch)
        self.sprite.scale = global_vars.SCALE_FACTOR

    def update(self):
        self.sprite.x += self.dx * global_vars.SPEED_FACTOR
        self.sprite.y += self.dy * global_vars.SPEED_FACTOR
        self.age += random.random()
        color_factor = self.age * 255 / global_vars.MAX_AGE
        self.sprite.color = (255,  color_factor,  color_factor)
        self.sprite.scale = global_vars.SCALE_FACTOR * (1 - self.age / global_vars.MAX_AGE)

        if self.age > global_vars.MAX_AGE:
            self.sprite.delete()
            return True
        else:
            return False
    
    def delete(self):
        # self.sprite.delete()
        pass

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
    
def billboardCheatSphericalBegin():
    modelview = (GLfloat * 16)()
    glPushMatrix()
    glGetFloatv(GL_MODELVIEW_MATRIX, modelview)
    # undo all rotations
    for i in range(3):
        for j in range(3):
            if i == j:
                modelview[i * 4 + j] = 1.0
            else:
                modelview[i * 4 + j] = 0.0
    # set the modelview with no rotations
    glLoadMatrixf(modelview)

def billboardCheatSphericalEnd():
    glPopMatrix()


@window.event
def on_draw():
    window.clear()
    # label.draw()

    # background color
    #glLoadIdentity()
    glClearColor(225/255, 246/255, 255/255, 1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    billboardCheatSphericalBegin()
    batch.draw()
    billboardCheatSphericalEnd()

def update(dt):
    global particles, batch
    if len(particles) < global_vars.MAX_PARTICLES:
        particles.append(Particle(batch=batch, img=particle_image, x_origin=window.width//3,
         y_origin=window.height//3))
        particles.append(Particle(batch=batch, img=particle_image, x_origin=window.width//2,
         y_origin=window.height//2))
    tmp_particles = particles
    for particle in particles:
        if particle.update():
            particle.delete()
            tmp_particles.remove(particle)
    particles = tmp_particles

"""
for windows wsl, setup xlaunch with Clipboard=True, Primary Selection=True, 
Native OpenGL=False, Disable Access Control=True 

then run this in terminal:
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
export LIBGL_ALWAYS_INDIRECT=0

"""

def main():
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()
    

if __name__ == "__main__":
    main()
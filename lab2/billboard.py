import pyglet
from pyglet.gl import *
import ctypes

window = pyglet.window.Window(1024, 720, caption='Demo', resizable=True)

# Load the texture
image = pyglet.image.load('snow.bmp')
texture = image.get_texture()
data = image.get_data()

# camera
rotation = 0
zoom = 0

quad1_coords_dict = {
    '1' : (0, 0, 0),
    '2' : (100, 0, 0),
    '3' : (100, 100, 0),
    '4' : (0, 100, 0)
}

quad2_coords_dict = {
    '1' : (-200, 0, 0),
    '2' : (-100, 0, 0),
    '3' : (-100, 100, 0),
    '4' : (-200, 100, 0)
}

def get_quad_coords(quad_coords_dict):
    quad_coords = []
    for coord in quad_coords_dict.values():
        quad_coords += coord
    return quad_coords


def draw_quad(quad_coords_dict):
    # glPushMatrix()
    # glLoadIdentity()
    # glTranslatef(window.width // 2, window.height // 2, 0)

    # set point size
    glPointSize(5)

    # draw the corners of the quad
    pyglet.graphics.draw(4, pyglet.gl.GL_POINTS,
        ('v3f', get_quad_coords(quad_coords_dict)),
        ('c3B', (255, 0, 0) * 4))
    
    # endable 2D textures
    glEnable(GL_TEXTURE_2D)
    # bind the texture to the quad
    glBindTexture(GL_TEXTURE_2D, texture.id)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0); glVertex2f(*quad_coords_dict['1'][0:2])    # Bottom left
    glTexCoord2f(1, 0); glVertex2f(*quad_coords_dict['2'][0:2])
    glTexCoord2f(1, 1); glVertex2f(*quad_coords_dict['3'][0:2])
    glTexCoord2f(0, 1); glVertex2f(*quad_coords_dict['4'][0:2])
    glEnd()
    # unbind the texture
    glBindTexture(GL_TEXTURE_2D, 0)
    # disable 2D textures
    glDisable(GL_TEXTURE_2D)

    # glPopMatrix()

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
    global rotation
    window.clear()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(-400, 400, -400, 400, -400, 400)
    
    glMatrixMode(GL_MODELVIEW)
    # glLoadIdentity()
    glRotatef(rotation, 0, 1, 0)
    # zoom in
    # glScalef(1 + zoom, 1 + zoom, 1 + zoom)


    # rotate viewpoint around z axis

    # glClearColor(225/255, 246/255, 255/255, 1)
    # glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    draw_quad(quad1_coords_dict)
    
    billboardCheatSphericalBegin()
    draw_quad(quad2_coords_dict)
    billboardCheatSphericalEnd()
    

    


def update(dt):
    global rotation, zoom

    rotation += 5 *  dt 
    # print(rotation)

    zoom += 0.1 * dt

    if zoom > 1:
        zoom = 0

    if rotation > 720.0:
        rotation = 0.0

"""
for windows wsl, setup xlaunch with Clipboard=True, Primary Selection=True, 
Native OpenGL=False, Disable Access Control=True 

then run this in terminal:
export DISPLAY=$(awk '/nameserver / {print $2; exit}' /etc/resolv.conf 2>/dev/null):0
export LIBGL_ALWAYS_INDIRECT=0

"""

if __name__ == '__main__':
    pyglet.clock.schedule(update)
    pyglet.app.run()
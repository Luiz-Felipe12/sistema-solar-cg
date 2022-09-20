import numpy

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image

global texture_index, sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune


# load images
def load_images():
    global sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune
    sun = read_texture('./textures/sun.jpg')
    mercury = read_texture('./textures/mercury.jpg')
    venus = read_texture('./textures/venus.jpg')
    earth = read_texture('./textures/earth.jpg')
    moon = read_texture('./textures/moon.jpg')
    mars = read_texture('./textures/mars.jpg')
    jupiter = read_texture('./textures/jupiter.jpg')
    saturn = read_texture('./textures/saturn.jpg')
    saturnRing = read_texture('./textures/saturnRing.jpg')  # sem referencia
    uranus = read_texture('./textures/uranus.jpg')
    uranusRing = read_texture('./textures/uranusRing.jpg')  # sem referencia
    neptune = read_texture('./textures/neptune.jpg')
    return sun, mercury, venus, earth, moon, mars, jupiter, saturn, saturnRing, uranus, uranusRing, neptune


def read_texture(filename):
    img = Image.open(filename)
    img_data = numpy.array(list(img.getdata()), numpy.int8)
    textID = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textID)
    # glPixelStorei(GL_UNPACK_ALIGNMENT, texture_index)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB,
                 img.size[0], img.size[1], 0, GL_RGB, GL_UNSIGNED_BYTE, img_data)
    return textID

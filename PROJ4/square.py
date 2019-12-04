# http://python-opengl-examples.blogspot.com/2009/04/basic-shading.html

from OpenGL.GL import *
from OpenGL.GLU import *
import pygame as pg
from pygame.locals import *
from PIL import Image


def create_1d_texture():
    tex = Image.new('RGB', (256, 1))
    for i in range(128):
        tex.putpixel((i, 0), (255, i * 2, i * 2))
        tex.putpixel((255 - i, 0), (255, i * 2, i * 2))
    tex.save('tex1d.png', 'PNG')


def wire_square():
    glBegin(GL_LINES)
    for edge in square_edges:
        for vertex in edge:
            glVertex2fv(square_vertices[vertex])
    glEnd()
    
    
def full_quad():

    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex2f(-1, -1)
    glTexCoord2f(1, 0)
    glVertex2f(1, -1)
    glTexCoord2f(1, 1)
    glVertex2f(1, 1)
    glTexCoord2f(0, 1)
    glVertex2f(-1, 1)
    glEnd()


def createAndCompileShader(type, source):
    shader=glCreateShader(type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    # get "compile status" - glCompileShader will not fail with
    # an exception in case of syntax errors

    result = glGetShaderiv(shader, GL_COMPILE_STATUS)

    if (result!=1): # shader didn't compile
        raise Exception("Couldn't compile shader\nShader compilation Log:\n"+str(glGetShaderInfoLog(shader)))
    return shader


def main():
    create_1d_texture()

    pg.init()
    pg.display.set_mode(window_size, DOUBLEBUF|OPENGL)

    gluPerspective(45, (window_size[0] / window_size[1]), 0.1, 50.0)

    # img = load_image('tex1d.png', 'r')
    # glTexImage1D(GL_TEXTURE_1D, 0, 4, 256, 0, GL_BGRA, GL_UNSIGNED_BYTE, img)
    #
    # glEnable(GL_TEXTURE_1D)

    vertex_shader = createAndCompileShader(GL_VERTEX_SHADER, vertex_shader_source)
    fragment_shader = createAndCompileShader(GL_FRAGMENT_SHADER, fragment_shader_source)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    try:
        glUseProgram(program)
    except OpenGL.error.GLError:
        print(glGetProgramInfoLog(program))
        raise

    glTranslatef(0.0, 0.0, -5)

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                quit()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        full_quad()
        pg.display.flip()
        pg.time.wait(10)


window_size = (1920, 1080)

square_vertices = (
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1)
)

square_edges = (
    (0, 1),
    (0, 2),
    (1, 3),
    (2, 3)
)

square_quads = (
    (0, 1, 2, 3)
)


vertex_shader_source = '''
attribute vec4 vPosition;
void main() {
    gl_Position = vPosition;
}
'''

use_smooth_shading = False
iterations = 100
antialias = 1
smooth_shading_scale = 1.0
use_double_precision = False

fragment_shader_source = """
#extension GL_EXT_gpu_shader4 : enable /*for "%"*/
#if """+str(int(use_double_precision))+"""
    #extension GL_ARB_gpu_shader_fp64 : enable
    #define FVEC2 dvec2
    #define FLOAT double
    #define LOG(X) FLOAT(log(float(X)))
#else
    #define FVEC2 vec2
    #define FLOAT float
    #define LOG(X) log(X)
#endif
#define NUM_COLORS 16
#define MAX_ITERS """+str(iterations)+"""
#define ANTIALIAS """+str(antialias)+"""
uniform FVEC2 bounds_x;
uniform FVEC2 bounds_y;
uniform FVEC2 screen_size;
vec3 get_color(int iter) {
    switch (iter%16) {
        case  0: return vec3(241,233,191);
        case  1: return vec3(248,201, 95);
        case  2: return vec3(255,170,  0);
        case  3: return vec3(204,108,  0);
        case  4: return vec3(153, 87,  0);
        case  5: return vec3(106, 52,  3);
        case  6: return vec3( 66, 30, 15);
        case  7: return vec3( 25,  7, 26);
        case  8: return vec3(  9,  1, 47);
        case  9: return vec3(  4,  4, 73);
        case 10: return vec3(  0,  7,100);
        case 11: return vec3( 12, 44,138);
        case 12: return vec3( 24, 82,177);
        case 13: return vec3( 57,125,209);
        case 14: return vec3(134,181,229);
        case 15: return vec3(211,236,248);
    }
}
int shade_index(int iter) {
	return iter;
}
FLOAT shadesmooth_index(int iter, FVEC2 position) {
	FLOAT normal_iter = FLOAT(iter) - LOG(LOG(length(position))) / LOG(2.0);
	return (normal_iter+0.5) * """+str(1.0/smooth_shading_scale)+""";
}
FVEC2 complex_sq(FVEC2 z) {
    FVEC2 temp1 = z * z;
    FLOAT temp2 = z.x * z.y;
    return FVEC2(temp1.x-temp1.y,temp2+temp2);
}
//FVEC2 complex_mul(FVEC2 a, FVEC2 b) {
//    return FVEC2(a.x*b.x-a.y*b.y,a.y*b.x+a.x*b.y);
//}
//FVEC2 complex_add(FVEC2 a, FVEC2 b) {
//    return a + b;
//}
vec3 sample(FVEC2 c) {
    FVEC2 z = c;
    for (int i=0;i<MAX_ITERS;++i) {
        //z = complex_add(complex_mul(z,z),c);
        z = complex_sq(z) + c;

        //Want to calculate if length(z)>some radius.  If it is, then we stop.
        //The minimum radius is 2.0, but smooth shading requires more to converge.
        FLOAT z_dot_z = dot(z,z); //z.x*z.x and z.y*z.y are also cool
        #if """+str(int(not use_smooth_shading))+""" //simple shading
            if (z_dot_z>2.0*2.0) {
                return vec3(get_color(shade_index(i))/255.0);
            }
        #else //smooth shading
            if (z_dot_z>8.0*8.0) {
                FLOAT index = shadesmooth_index(i,z);
                //gl_FragData[0] = vec4(vec3(index),1.0);
                int index2 = int(index);
                index -= FLOAT(index2);
                return vec3((get_color(index2)*(1.0-index)+get_color(index2+1)*index)/255.0);
            }
        #endif
    }
    return vec3(0.0,0.0,0.0);
}
void main(void) {
    vec4 color = vec4(0.0,0.0,0.0, 1.0);
    for (int y=0;y<ANTIALIAS;++y) {
        for (int x=0;x<ANTIALIAS;++x) {
            FVEC2 pixel = FVEC2(gl_FragCoord.xy) + FVEC2(-0.5+(FLOAT(x)+0.5)/FLOAT(ANTIALIAS),-0.5+(FLOAT(y)+0.5)/FLOAT(ANTIALIAS));
            FVEC2 c = pixel/screen_size * FVEC2(bounds_x.y-bounds_x.x,bounds_y.y-bounds_y.x) + FVEC2(bounds_x.x,bounds_y.x);
            color.rgb += sample(c);
        }
    }
    color.rgb /= float(ANTIALIAS*ANTIALIAS);
    gl_FragColor = color;
}
"""

if __name__ == "__main__":
    main()
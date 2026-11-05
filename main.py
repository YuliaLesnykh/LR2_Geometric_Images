import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import math
import sys

WIDTH, HEIGHT = 800, 600
CENTER_X, CENTER_Y = 0.0, 0.0
RADIUS = 0.8
MAX_VERTICES = 96

n_vertices = 3

# Краски
BG_COLOR = (1.0, 1.0, 1.0)
CIRCLE_COLOR = (0.3, 0.3, 0.3)
POLY_FILL_COLOR = (1.0, 0.75, 0.85)
POLY_LINE_COLOR = (0.9, 0.5, 0.7)
VERTEX_COLOR = (0.9, 0.5, 0.7)

def draw_circle(cx, cy, r, segments=100):
    glColor3f(*CIRCLE_COLOR)
    glLineWidth(3.0)
    glBegin(GL_LINE_LOOP)
    for i in range(segments):
        angle = 2.0 * math.pi * i / segments
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        glVertex2f(x, y)
    glEnd()
    glLineWidth(1.0)


def get_polygon_vertices(cx, cy, r, n):
    verts = []
    for i in range(n):
        angle = math.radians(90 + (360.0 / n) * i)
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        verts.append((x, y))
    return verts


def draw_polygon(cx, cy, r, n):
    if n < 3:
        return
    verts = get_polygon_vertices(cx, cy, r, n)

    # Заливка многоугольника
    glColor3f(*POLY_FILL_COLOR)
    glBegin(GL_POLYGON)
    for v in verts:
        glVertex2f(v[0], v[1])
    glEnd()

    # Контур многоугольника
    glColor3f(*POLY_LINE_COLOR)
    glLineWidth(3.0)
    glBegin(GL_LINE_LOOP)
    for v in verts:
        glVertex2f(v[0], v[1])
    glEnd()
    glLineWidth(1.0)

    # Точки границ многоугольника
    glPointSize(6.0)
    glColor3f(*VERTEX_COLOR)
    glBegin(GL_POINTS)
    for v in verts:
        glVertex2f(v[0], v[1])
    glEnd()
    glPointSize(1.0)


def main():
    global n_vertices

    pygame.init()
    display = (WIDTH, HEIGHT)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("ЛР1, Вписанный многоугольник")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    aspect = WIDTH / HEIGHT
    glOrtho(-aspect, aspect, -1.0, 1.0, -1.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glClearColor(*BG_COLOR, 1.0)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 15, bold=True)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_PAGEDOWN:
                    if n_vertices * 2 <= MAX_VERTICES:
                        n_vertices *= 2
                elif event.key == pygame.K_PAGEUP:
                    if n_vertices // 2 >= 3:
                        n_vertices //= 2

        glClear(GL_COLOR_BUFFER_BIT)
        draw_circle(CENTER_X, CENTER_Y, RADIUS)
        draw_polygon(CENTER_X, CENTER_Y, RADIUS, n_vertices)

        glMatrixMode(GL_PROJECTION)
        glPushMatrix()
        glLoadIdentity()
        glOrtho(0, WIDTH, HEIGHT, 0, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glPushMatrix()
        glLoadIdentity()

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        info = f"Вершин: {n_vertices}   |  PgUp - /2,  PgDn - x2,  ESC - выход"

        text_surface = font.render(info, True, (0, 0, 0))
        text_data = pygame.image.tostring(text_surface, "RGBA", True)
        tw, th = text_surface.get_size()

        tex_id = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, tex_id)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tw, th, 0, GL_RGBA, GL_UNSIGNED_BYTE, text_data)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        glEnable(GL_TEXTURE_2D)
        glColor3f(1, 1, 1)
        glBegin(GL_QUADS)
        glTexCoord2f(0, 1)
        glVertex2f(10, 10)
        glTexCoord2f(1, 1)
        glVertex2f(10 + tw, 10)
        glTexCoord2f(1, 0)
        glVertex2f(10 + tw, 10 + th)
        glTexCoord2f(0, 0)
        glVertex2f(10, 10 + th)
        glEnd()
        glDisable(GL_TEXTURE_2D)

        glDeleteTextures([tex_id])
        glDisable(GL_BLEND)

        glPopMatrix()
        glMatrixMode(GL_PROJECTION)
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
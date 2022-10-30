"""
Лабораторная работа N2 (4 часа). Тема: Каркасная визуализация выпуклого многогранника. Удаление невидимых линий.

Задание: Разработать формат представления многогранника и процедуру его каркасной отрисовки в ортографической и изометрической проекциях. Обеспечить удаление невидимых линий и возможность пространственных поворотов и масштабирования многогранника. Обеспечить автоматическое центрирование и изменение размеров изображения при изменении размеров окна.
Варианты многогранников:
1. Куб
2. Правильный октаэдр
3. Параллелепипед
4. Клин
5. Обелиск (усеченный клин)
6. Усеченный правильный тетраэдр (грани – правильные треугольники и шестиугольники)
7,8,9,10,11 - 4,5,6,8,10 – гранная прямая правильная призма
12 Прямая призма с основанием - правильный пятиугольник
13 Прямая призма с основанием - правильный 6-угольник
14 Прямая призма с основанием - правильный 7-угольник
15 Прямая призма с основанием - правильный 8-угольник
16 Наклонная призма с основанием - правильный пятиугольник
17 Наклонная призма с основанием - правильный 6-угольник
18 Наклонная призма с основанием - правильный 7-угольник
19 Наклонная призма с основанием - правильный 8-угольник
20 4 – гранная прямая правильная усеченная пирамида
21 5 – гранная прямая правильная усеченная пирамида
22 6 – гранная прямая правильная усеченная пирамида
23 8 – гранная прямая правильная усеченная пирамида
24 10 – гранная прямая правильная усеченная пирамида
25  Правильный додекаэдр
26. Правильный икосаэдр
27 Куб с покатой крышей
28 Куб + 4-гранная пирамида с основанием == грань куба


"""


from math import *
import pygame

def vec_length(vec):
    return sqrt(vec[0]**2+vec[1]**2+vec[2]**2)

def vec_norm(vec):
    length = vec_length(vec)
    if length == 0:
        return (0,0,0)
    norm = ( vec[0]/length , vec[1]/length , vec[2]/length )
    return norm

def cross_product(v1,v2):
    return (v1[1]*v2[2]-v1[2]*v2[1] , v1[2]*v2[0]-v1[0]*v2[2] , v1[0]*v2[1]-v1[1]*v2[0] )

def dot_product(v1, v2):
    ret = 0.0

    for i in range(len(v1)):
        ret += v1[i]*v2[i]

    return ret

ANGLE=pi/960
SCREEN_SIZE = (1024,800)
VECTORS = [(10,32),(20,47)]
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0, 255, 0)
LIGHT_GRAY=(220,220,220)

SCREEN_VEC1 = (1,0,0)
SCREEN_VEC2 = (0,1,0)
SCREEN_NORMAL = vec_norm(cross_product(SCREEN_VEC1, SCREEN_VEC2))
SHOW_INDICES = True
SHOW_NORMALS = True

SCALE = 100
CENTER = (SCREEN_SIZE[0]//2,SCREEN_SIZE[1]//2)

def kor_down(angle):
    return(cos(angle),sin(angle,0))

def kor_up(angle):
    return(cos(angle),sin(angle,2))

def prism(n,d1=2,d2=2,height=2):
    coords = []
    for i in range(n):
        angle = (2*pi/n)*i;
        x_low=cos(angle)*d1
        y_low=sin(angle)*d1
        coords.append( (x_low,y_low,-height/2) )
    for i in range(n):
        angle = (2*pi/n)*i;
        x_high=cos(angle)*d2
        y_high=sin(angle)*d2
        coords.append( (x_high,y_high,height/2) )

    faces = []
    for j in range(n):
        if j == (n-1):
            faces += [ [j,0, n, 2*n-1] ]
        else:
            faces += [ [j,j+1,j+n+1,j+n] ]
    faces += [ list(range(n-1,-1,-1)) ]
    faces += [ list(range(n,2*n)) ]

    return coords,faces



def pyramid(n):
  return prism(n, 2,1, 2)

def octahedron():
  coords = [(1,0,0), (0,-1,0), (-1,0,0), (0,1,0), (0,0,-1), (0,0,+1)]
  faces = [
    (0,1,5), (1,2,5), (2,3,5), (3,0,5),
    (0,4,1), (1,4,2), (2,4,3), (3,4,0),
  ]
  return coords, faces

def cube():
  return prism(4,sqrt(2),sqrt(2),2)
  coords = [
    (-1,-1,-1),
    ( 1,-1,-1),
    ( 1, 1,-1),
    (-1, 1,-1),
    (-1,-1, 1),
    ( 1,-1, 1),
    ( 1, 1, 1),
    (-1, 1, 1)
  ]

  faces = [
    (0, 3, 2, 1),
    (2, 3, 7, 6),
    (0, 4, 7, 3),
    (1, 2, 6, 5),
    (4, 5, 6, 7),
    (0, 1, 5, 4),
  ]
  return coords, faces

def truncated_tetrahedron():
  coords = [
    ( 3, 1, 1),( 1, 3, 1),( 1, 1, 3),
    (-3,-1, 1),(-1,-3, 1),(-1,-1, 3),
    (-3, 1,-1),(-1, 3,-1),(-1, 1,-3),
    ( 3,-1,-1),( 1,-3,-1),( 1,-1,-3),
  ]
  faces = [
    (0,1,2), (3,4,5), (6,7,8), (9,10,11),
    (9,11,8,7,1,0),
    (3,6,8,11,10,4),
    (1,7,6,3,5,2),
    (4,10,9,0,2,5),
  ]
  return coords, faces

MODELS = [
  (*cube(), "Cube"),
  (*octahedron(), "Octahedron"),
  (*truncated_tetrahedron(), "Truncated tetrahedron"),
  (*prism(4), "Prism 4"),
  (*prism(5), "Prism 5"),
  (*prism(6), "Prism 6"),
  (*prism(8), "Prism 8"),
  (*prism(10), "Prism 10"),
  (*pyramid(4), "Pyramid 4"),
  (*pyramid(5), "Pyramid 5"),
  (*pyramid(6), "Pyramid 6"),
  (*pyramid(8), "Pyramid 8"),
  (*pyramid(10), "Pyramid 10"),
  (*pyramid(12), "Pyramid 12"),
  (*pyramid(16), "Pyramid 16"),
  (*pyramid(24), "Pyramid 24"),
]





#MODELS = [prism(4,2,2,2), prism(12,2,1,2)]
CURRENT_MODEL = 0
VERTICES, FACES, NAME = MODELS[CURRENT_MODEL]

def next_model(direction):
    global VERTICES,FACES,CURRENT_MODEL, NAME
    CURRENT_MODEL = (CURRENT_MODEL + direction) % len(MODELS)
    VERTICES, FACES, NAME = MODELS[CURRENT_MODEL]

def normal(face):
    ver1=VERTICES[face[0]]
    ver2=VERTICES[face[1]]
    ver3=VERTICES[face[2]]
    vec1=(ver2[0]-ver1[0],ver2[1]-ver1[1],ver2[2]-ver1[2])
    vec2=(ver3[0]-ver2[0],ver3[1]-ver2[1],ver3[2]-ver2[2])
    return vec_norm(cross_product(vec1, vec2))

def is_visible_face(face):
    norm = normal(face)
    if dot_product(SCREEN_NORMAL, norm)<=0:
        return True
    else:
        return False


def filter_faces():
    visible= []
    invisible = []
    for face in FACES:
        if is_visible_face(face):
            visible += [face]
        else:
            invisible += [face]
    return visible, invisible

def matrix_rotate_x(angle):
    MX = [
        [1,0,0],
        [0,cos(angle),-sin(angle)],
        [0,sin(angle),cos(angle)]
            ]
    return MX

def matrix_rotate_y(angle):
    MY = [
        [cos(angle),0,sin(angle)],
        [0,1,0],
        [-sin(angle),0,cos(angle)]
            ]
    return MY

def matrix_rotate_z(angle):
    MZ = [
        [cos(angle),-sin(angle),0],
        [sin(angle),cos(angle),0],
        [0,0,1]
            ]
    return MZ

def rotate(angle, rot):
    m = rot(angle)
    for i in range(len(VERTICES)):
        VERTICES[i]=product(m, VERTICES[i])




def product(m,v):
    """ Matrix product """
    result = []
    for row in m:
        ret=0
        for i in range(0,len(row)):
            xm = row[i]
            xv = v[i]
            ret += xv*xm
        result.append(ret)
    return result


def to_scr(pos):
   x=pos[0]*SCALE + CENTER[0]
   y=pos[1]*SCALE + CENTER[1]
   return(x,y)

def orthogonal(pos):
    return(pos[0],pos[1])

def draw_wireframe_face(screen, color, face):
    for i in range(len(face)):
        a = VERTICES[face[i]]
        if (i+1) == len(face):
            b = VERTICES[face[0]]
        else:
            b = VERTICES[face[i+1]]
        ortho_a = orthogonal(a)
        screen_ortho_a = to_scr(ortho_a)
        ortho_b = orthogonal(b)
        screen_ortho_b = to_scr(ortho_b)
        pygame.draw.line(screen, color, screen_ortho_a, screen_ortho_b ,5)




def draw_wireframe(screen, color, faces):
    for face in faces:
        draw_wireframe_face(screen, color, face)



def draw_vec_center(screen, color, vec):
    x=vec[0]
    y=vec[1]
    pygame.draw.line(screen, color, CENTER, (SCREEN_SIZE[0]//2+x,SCREEN_SIZE[1]//2-y),3)
    return

def draw_vert_index(screen, font):
    if not SHOW_INDICES:
        return
    for i in range(len(VERTICES)):
        x = to_scr(orthogonal(VERTICES[i]))
        pic = font.render("%d"%i, False, BLACK)
        screen.blit(pic, x)

def draw_normals(screen):
    if not SHOW_NORMALS:
        return
    for face in FACES:
        norm = normal(face)
        mid = VERTICES[face[0]]
        norm = (mid[0]+norm[0],mid[1]+norm[1], mid[2]+norm[2])
        pygame.draw.line(screen, BLACK, to_scr(mid), to_scr(norm), 2)
    return

def main():
    global SCALE, SHOW_INDICES, SHOW_NORMALS
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((1024,800))
    font = pygame.font.SysFont('Sans', 32)
    title_font = pygame.font.SysFont('Sans', 48, bold=True)

    run = True
    x_rotation = False
    y_rotation = False
    z_rotation = False
    while run:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                run=False
            elif ev.type == pygame.KEYDOWN:
                sign = 1
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    sign = -1

                if ev.key==pygame.K_UP:
                    VECTORS[0]=(VECTORS[0][0],VECTORS[0][1]+10)
                elif ev.key == pygame.K_q:
                    run = False
                elif ev.key == pygame.K_x:
                    x_rotation = True
                elif ev.key == pygame.K_z:
                    z_rotation = True
                elif ev.key == pygame.K_y:
                    y_rotation = True
                elif ev.key == pygame.K_RIGHT:
                    SCALE = SCALE + 50
                elif ev.key == pygame.K_LEFT:
                    SCALE = SCALE - 50
                elif ev.key == pygame.K_i:
                   SHOW_INDICES = not SHOW_INDICES
                elif ev.key == pygame.K_n:
                    SHOW_NORMALS = not SHOW_NORMALS
                elif ev.key == pygame.K_m:
                     next_model(sign)
            elif ev.type == pygame.KEYUP:
                if ev.key == pygame.K_x:
                    x_rotation = False
                elif ev.key == pygame.K_z:
                    z_rotation = False
                elif ev.key == pygame.K_y:
                    y_rotation = False
        if x_rotation:
            rotate(sign*ANGLE, matrix_rotate_x)
        if y_rotation:
            rotate(sign*ANGLE,matrix_rotate_y)
        if z_rotation:
            rotate(sign*ANGLE,matrix_rotate_z)







        screen.fill(WHITE)
        title = title_font.render("%s"%NAME, False, BLACK)
        screen.blit(title,(0,0))
        pygame.draw.circle(screen, RED, to_scr((0,0,0)), 3)
        visible, invisible = filter_faces()
        draw_wireframe(screen, LIGHT_GRAY, invisible)
        draw_wireframe(screen, GREEN, visible)
        draw_vert_index(screen, font)
        draw_normals(screen)
        pygame.display.flip()
    pygame.quit()




if __name__=='__main__':
    try:
        main()
    except ArgumentError as error:
        print(error)
        pygame.quit()

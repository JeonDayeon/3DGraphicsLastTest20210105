
## 3D그래픽스 001분반 기말고사 20210105 전다연 ##


from OpenGL.GL import *
from OpenGL.GLU import *

import sys

from PyQt5.QtWidgets import QOpenGLWidget, QApplication, QMainWindow, QVBoxLayout, QWidget, QSlider
from PyQt5.QtCore import *

import numpy as np
import math
        
class MyGLWidget(QOpenGLWidget):

    def __init__(self, parent=None):
        super(MyGLWidget, self).__init__(parent)

        self.camloc = np.array([0.0, 3.0, 10.0])
        self.viewAngle = 3.141592
        self.direction = np.array([0, 0, -1])
        self.locz = 0.0
        self.angle= 0.0
        self.bending = -75
        self.tangle = 0.0


    def initializeGL(self):
        # ^{\it \color{gray}  OpenGL 그리기를 수행하기 전에 각종 상태값을 초기화}^
        glClearColor(0.8, 0.8, 0.6, 1.0)
        glPointSize(1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHT1)
        self.LightSet()

    def resizeGL(self, width, height):
        # ^{\it \color{gray}  카메라의 투영 특성을 여기서 설정}^
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60, width/height, 0.1, 1000)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        x, y, z = self.camloc
        cosine = math.cos(self.viewAngle)
        sine = math.sin(self.viewAngle)
        self.direction = np.array([sine, 0, cosine])
        tx, ty, tz = self.camloc + self.direction
        gluLookAt(x, y, z, tx, ty, tz, 0,1,0)

        cosine = math.cos(self.viewAngle)
        sine = math.sin(self.viewAngle)

        self.LightPosition()

        for row in range(100):
            for col in range(100):
                    glPushMatrix()
                    glTranslatef(row*20, 0, col*20)
                    glScalef(0.5, 0.5, 0.5)
                    draw_cube()
                    glPopMatrix()


        glColor3f(0.5, 0.5, 1.0)
        draw_plane(200, 200, 1.0)##바닥


        glRotatef(self.tangle, 30, 30, 0)
        glColor3f(1.0, 1.0, 1.0)
        glTranslatef(0, 1, self.locz)
        draw_cube()##전차 몸통

        glRotatef(self.angle, 0, 1, 0)
        glTranslatef(0, 1, 0) 
        glPushMatrix()
        glColor3f(1, 0, 0)
        glScalef(0.5, 0.5, 0.5) 
        draw_cube()
        glPopMatrix()  ##포탑

        glColor3f(1, 1, 0)
        glTranslatef(0, 0.5, 0) 
        glRotatef(self.bending, 1, 0, 0)
        glTranslatef(0, 3, 0)      
        glPushMatrix()
        glScalef(0.1, 3, 0.1)
        glColor3f(0, 1, 0)
        draw_cube()
        glPopMatrix() ##포

        glTranslatef(1.5, -4, -2) 
        glPushMatrix()
        glColor3f(1, 0, 0)
        glScalef(0.4, 0.4, 0.4) 
        draw_cube()
        glPopMatrix()##타이어 오른쪽

        glTranslatef(-3, 0, 0) 
        glPushMatrix()
        glColor3f(1, 0, 0)
        glScalef(0.4, 0.4, 0.4) 
        draw_cube()
        glPopMatrix()##타이어 왼쪽
    



        # ^{\it \color{gray}  그려진 프레임버퍼를 화면으로 송출}^
        glFlush()


    def LightSet(self):
        glMaterialfv(GL_FRONT, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glMaterialfv(GL_FRONT, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])
        glMaterialf(GL_FRONT, GL_SHININESS, 120)

        glLightfv(GL_LIGHT0, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 0.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])

        glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0, 0.0, 0.0, 1.0])


    def LightPosition(self) :
        glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, 1, 0])
        glLightfv(GL_LIGHT1, GL_POSITION, [-1, 1, -1, 0])

    def keyPressEvent(self, e):
        step = 0.8
        angle_step = 0.1
        k = e.key()

        ## 카메라
        if k == Qt.Key.Key_Up :
            self.camloc = self.camloc  + step * self.direction ##카메라 직진

        if k == Qt.Key.Key_Down :
            self.camloc = self.camloc  - step * self.direction ##카메라 후진

        if k == Qt.Key.Key_Left :
            self.viewAngle += angle_step ##카메라 좌회전

        if k == Qt.Key.Key_Right :
             self.viewAngle -= angle_step ##카메라 우회전


        ## 전차 이동
        if k == Qt.Key_W :
            self.locz -= 1.0##전차 전진
            self.camloc = self.camloc  + step * self.direction ##카메라 직진

        if k == Qt.Key_S :
            self.locz += 1.0 ##전차 후진
            self.camloc = self.camloc  - step * self.direction ##카메라 후진

        ## 포탑 회전
        if k == Qt.Key_A :
            self.angle += 10.0 ##왼쪽
            self.viewAngle += angle_step ##카메라 좌회전

        if k == Qt.Key_D :
            self.angle -= 10.0 ##오른쪽
            self.viewAngle -= angle_step ##카메라 우회전

        ## 포
        if k == Qt.Key_Q : 
            self.bending += 2 ##포 위로

        if k == Qt.Key_E :
            self.bending -= 2 ##포 아래로

        if k == Qt.Key_1 : 
            self.tangle -= 10 ## 방향전환(오류)

        if k == Qt.Key_2 : 
            self.tangle += 10

        self.update()

def main(argv = []):
    app = QApplication(sys.argv)

    win = MyGLWidget()
    win.show()

    app.exec()





def draw_plane(width, depth, interval):
    x, X = -width/2, width/2
    z, Z = -depth/2, depth/2
    cur = x
    glBegin(GL_LINE_LOOP)
    while cur <= X:
        glColor3f(1.0, 1.0, 1.0) 
        glVertex3f(cur, 0, z)
        glVertex3f(cur, 0, Z)
        cur += interval
    cur = z
    while cur <= Z: 
        glVertex3f(x, 0, cur)
        glVertex3f(X, 0, cur)
        cur += interval
    glEnd()

def draw_square():
    glBegin(GL_POLYGON)
    glVertex3f(-1,-1, 0)
    glVertex3f( 1,-1, 0)
    glVertex3f( 1, 1, 0)
    glVertex3f(-1, 1, 0)
    glEnd()

def draw_pentagon():
    glBegin(GL_POLYGON)
    glColor3f(1, 0, 0)

    glVertex3f(.0, .4, .0)
    glVertex3f(-.5, 0, .0)

    glVertex3f(-.3, -.5, .0)
    glVertex3f(.3, -.5, .0)

    glVertex3f(.3, -.5, .0)
    glVertex3f(.5, -.0, 0)

def draw_cube():

    glPushMatrix()
    glTranslatef(0, 0, 1)
    draw_square()

    glTranslatef(0, 0, -2)
    draw_square()

    glTranslatef(0, 0, 1)
    glRotatef(90, 0, 1, 0)
    glTranslatef(0, 0, 1)
    draw_square()

    glTranslatef(0, 0, -2)
    draw_square()

    glTranslatef(0, 0, 1)
    glRotatef(90, 1,0,0)
    glTranslatef(0, 0, 1)
    draw_square()
    
    glTranslatef(0, 0, -2)
    draw_square()

    glPopMatrix()

if __name__ == '__main__':
    main()
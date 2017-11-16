# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lab1ui.ui'
#
# Created: Sun Nov 12 14:46:14 2017
#      by: PyQt4 UI code generator 4.10
#
# WARNING! All changes made in this file will be lost!
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
#from Image import *
import dicom
import numpy as np
from PyQt4 import QtCore, QtGui, QtOpenGL
from PyQt4.QtCore import pyqtSignal, QSize, Qt
from PyQt4.QtGui import *
import sys
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

try:
    from OpenGL import GL
except ImportError:
    app = QtGui.QApplication(sys.argv)
    QtGui.QMessageBox.critical(None, "OpenGL hellogl",
            "PyOpenGL must be installed to run this example.")
    sys.exit(1)


plan=0;
ESCAPE = '\033'
x=y=w=h=0
WIDTH=HEIGHT=0
tr1=0
W=H=0
window = 0
IDs = []
IDs2 = []
IDs3=[]
index=30
inputdir='forlab7/'
spacing=0
slice=0
# rotation
X_AXIS = 1
Y_AXIS = 1
Z_AXIS = 1
rect1=[0,0,0,0]
rects=[]
lim1=[0,0,255,255]
rect2=[255,0,255,0]
lim2=[0,0,255,255]
rect3=[0,255,0,255]
lim3=[0,0,255,255]
index1=9
image1=image2=image3=0
imagesGlobal=[]

Lx=Ly=Lz=0



class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(700, 532)

        self.openGLWidget = GLWidget(Form)
        self.openGLWidget.setGeometry(QtCore.QRect(10, 10, 512, 512))
        self.openGLWidget.setObjectName("openGLWidget")

        self.horizontalSlider1 = QtGui.QSlider(Form)
        self.horizontalSlider1.setGeometry(QtCore.QRect(540, 10, 700-10-540, 22))
        self.horizontalSlider1.setMinimum(0)
        self.horizontalSlider1.setMaximum(19)
        self.horizontalSlider1.setValue(10)
        self.horizontalSlider1.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider1.setObjectName(_fromUtf8("horizontalSlider1"))
        self.horizontalSlider1.valueChanged.connect(self.openGLWidget.resetTextures)

        self.horizontalSlider2 = QtGui.QSlider(Form)
        self.horizontalSlider2.setGeometry(QtCore.QRect(540, 40, 700-10-540, 22))
        self.horizontalSlider2.setMinimum(0)
        self.horizontalSlider2.setMaximum(255)
        self.horizontalSlider2.setValue(125)
        self.horizontalSlider2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider2.setObjectName(_fromUtf8("horizontalSlider2"))
        #self.horizontalSlider2.valueChanged.connect(self.valuechange)
        self.horizontalSlider2.valueChanged.connect(self.openGLWidget.resetTextures)

        self.horizontalSlider3 = QtGui.QSlider(Form)
        self.horizontalSlider3.setGeometry(QtCore.QRect(540, 70, 700-10-540, 22))
        self.horizontalSlider3.setMinimum(0)
        self.horizontalSlider3.setMaximum(255)
        self.horizontalSlider3.setValue(125)
        self.horizontalSlider3.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider3.setObjectName(_fromUtf8("horizontalSlider3"))
        #self.horizontalSlider3.valueChanged.connect(self.valuechange)
        self.horizontalSlider3.valueChanged.connect(self.openGLWidget.resetTextures)

        self.addItem = QtGui.QPushButton(Form)
        self.addItem.setGeometry(QtCore.QRect(540 +(700-540)/2 +10, 100, (700-540)/2-10, 40))
        self.addItem.clicked.connect(self.addRect)
        self.addItem.setObjectName(_fromUtf8("addItem"))

        self.clear = QtGui.QPushButton(Form)
        self.clear.setGeometry(QtCore.QRect(540, 100, (700-540)/2-10, 40))
        self.clear.clicked.connect(self.clearRects)
        self.clear.setObjectName(_fromUtf8("clear"))



        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)
    def addRect(self):
        self.openGLWidget.add=1
    def clearRects(self):
        global rects
        rects=[];
        self.openGLWidget.setFocus()
    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.addItem.setText(_translate("Form", "add item", None))
        self.clear.setText(_translate("Form", "clear", None))
        self.openGLWidget.setFocus()

class GLWidget(QtOpenGL.QGLWidget):
    x=0
    y=0
    move=0
    rectIndex=0
    pointIndex=0
    add=0
    #xRotationChanged = QtCore.pyqtSignal(int)
    #yRotationChanged = QtCore.pyqtSignal(int)
    #zRotationChanged = QtCore.pyqtSignal(int)
    def resetTextures(self):
        global IDs, IDs2, IDs3, spacing, slice
        global lim1, lim2, lim3
        global image1, image2, image3, imagesGlobal
        global index1,Lx,Ly,Lz
        #Lz = (window.horizontalSlider1.value()+ (w - w / slice * spacing) / 2) * (w / slice * spacing) * len(imagesGlobal) - 1
        Lz = int(window.horizontalSlider1.value()* (w / slice * spacing)/ len(imagesGlobal)+(w - w / slice * spacing) / 2)
        #Lz = window.horizontalSlider1.value()
        Lx = window.horizontalSlider2.value()

        Ly = window.horizontalSlider3.value()
        tmp1 = (Lz - (w - w / slice * spacing) / 2) / (w / slice * spacing) * len(imagesGlobal) - 1
        index1 = int(window.horizontalSlider1.value())

        image = imagesGlobal
        ix = len(image[0])
        iy = len(image[0][0])

        COLORS = GL_LUMINANCE
        MODE = GL_UNSIGNED_BYTE
        k = 0
        imageK = []
        IDs2 = glGenTextures(2)
        ii = len(image[0][0])-Ly-1
        imageK.append(np.zeros([len(image), len(image[0][ii])]));
        imageK[0].fill(255)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][127])):
                imageK[0][i][y] = image[i][ii][y]
        glBindTexture(GL_TEXTURE_2D, IDs2[0]);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(image[0][ii]), len(image), 0, COLORS, MODE, imageK[0])
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image2 = imageK[0]

        ii = Lx
        IDs3 = glGenTextures(3)
        imageS = (np.zeros([len(image), len(image[0][ii])]));
        imageS.fill(255)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][ii])):
                imageS[i][y] = image[i][y][ii]

        glBindTexture(GL_TEXTURE_2D, IDs3[0]);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(image[0][ii]), len(image), 0, COLORS, MODE, imageS)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        self.glDraw();


    def loadImage(self, inputdir):
        global IDs, IDs2, IDs3, spacing, slice
        global lim1, lim2, lim3
        global image1, image2, image3, imagesGlobal,Lx,Ly,Lz
        COLORS = GL_LUMINANCE
        MODE = GL_UNSIGNED_BYTE
        k = 0
        image = []
        print (len(os.listdir(inputdir)))
        IDs = GL.glGenTextures(len(os.listdir(inputdir)))
        tmpplan = dicom.read_file(inputdir + os.listdir(inputdir)[0])
        spacing = tmpplan.PixelSpacing[0]
        slice = tmpplan.SpacingBetweenSlices
        for fichier in os.listdir(inputdir):
            plan = dicom.read_file(inputdir + fichier)
            image.append(plan.pixel_array)
            print (fichier)
            # print fichier
            ix = plan.Rows
            iy = plan.Columns
            max = np.amax(image)

            i = 0
            while i < len(image[k]):
                j = 0
                while j < len(image[k][i]):
                    image[k][i][j] = float(image[k][i][j]) / (max) * 255
                    j += 1
                i += 1

            glBindTexture(GL_TEXTURE_2D, IDs[k]);
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexImage2D(GL_TEXTURE_2D, 0, 3, ix, iy, 0, COLORS, MODE, image[k])
            glGetIntegerv(GL_TEXTURE_BINDING_2D)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
            k += 1
        lim1 = [0, 0, ix, iy]
        imagesGlobal = image
        image1 = image[9]

        imageK = []
        IDs2 = glGenTextures(2)
        ii = 127
        imageK.append(np.zeros([len(image), len(image[0][ii])]));
        imageK[0].fill(255)
        print (ii)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][127])):
                imageK[0][i][y] = image[i][ii][y]
        glBindTexture(GL_TEXTURE_2D, IDs2[0]);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(image[0][ii]), len(image), 0, COLORS, MODE, imageK[0])
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image2 = imageK[0]
        #lim2 = [W + w / slice * spacing / 2, 0, W + w / slice * spacing + (w - w / slice * spacing) / 2, iy]
        lim2 = [W, h / slice * spacing / 2, 2*W, h / slice * spacing + (h - h / slice * spacing) / 2]
        rect2 = lim2

        ii = 127
        IDs3 = glGenTextures(3)
        imageS = (np.zeros([len(image), len(image[0][ii])]));
        imageS.fill(255)
        step = int(256 / float(len(image))) + 1
        for i in range(len(image)):
            for y in range(len(image[i][ii])):
                imageS[i][y] = image[i][y][ii]

        glBindTexture(GL_TEXTURE_2D, IDs3[0]);
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexImage2D(GL_TEXTURE_2D, 0, 3, len(image[0][ii]), len(image), 0, COLORS, MODE, imageS)
        glGetIntegerv(GL_TEXTURE_BINDING_2D)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        image3 = imageS
        lim3 = [0, H + h / slice * spacing / 2, ix, H + h / slice * spacing + (h - h / slice * spacing) / 2]
        Lz = int(window.horizontalSlider1.value() * (w / slice * spacing) / len(imagesGlobal) + (
        w - w / slice * spacing) / 2)
        # Lz = window.horizontalSlider1.value()
        Lx = window.horizontalSlider2.value()

        Ly = window.horizontalSlider3.value()
    def __init__(self, parent=None):

        super(GLWidget, self).__init__(parent)
        #sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.setFixedSize(512, 512)
        self.setMouseTracking(True)


    def minimumSizeHint(self):
        return QtCore.QSize(512, 512)
    def maximumSizeHint(self):
        return QtCore.QSize(512, 512)
    def sizeHint(self):
        return QtCore.QSize(512,512)


    def initializeGL(self):
        #self.qglClearColor(self.trolltechPurple.dark())
        #self.object = self.makeObject()
        #GL.glShadeModel(GL.GL_FLAT)
        #GL.glEnable(GL.GL_DEPTH_TEST)
        #GL.glEnable(GL.GL_CULL_FACE)
        global WIDTH, HEIGHT
        global x, y, w, h, W, H
        plan = dicom.read_file("forlab7/brain_001.dcm")
        WIDTH = plan.Rows * 2
        HEIGHT = plan.Columns * 2
        H = plan.Rows
        W = plan.Columns
        x = H / 2
        y = W / 2
        h = H
        w = W
        glViewport(0, 0, WIDTH, HEIGHT)
        #GL.glClear()
        self.loadImage(inputdir)

    def paintGL(self):
        global X_AXIS, Y_AXIS, Z_AXIS
        global DIRECTION, IDs, IDs2, IDs3
        global spacing, slice
        global index1

        glEnable(GL_TEXTURE_2D)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glLoadIdentity()

        glOrtho(-W, W, -H, H, -W, W);

        glBindTexture(GL_TEXTURE_2D, IDs[index1])
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);
        glVertex2f(-w, h);
        glTexCoord2f(1.0, 0.0);
        glVertex2f(0, h);
        glTexCoord2f(1.0, 1.0);
        glVertex2f(0, 0);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(-w, 0);
        glEnd();

        glBindTexture(GL_TEXTURE_2D, IDs3[0])
        glBegin(GL_QUADS);

        glTexCoord2f(0.0, 0.0);
        glVertex2f(0, (h - h / slice * spacing) / 2);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(0, ((h - h / slice * spacing) / 2 + h / slice * spacing));

        glTexCoord2f(1.0, 1.0);
        glVertex2f(w, ((h - h / slice * spacing) / 2 + h / slice * spacing));


        glTexCoord2f(1.0, 0.0);
        glVertex2f(w, (h - h / slice * spacing) / 2);



        glEnd();

        glBindTexture(GL_TEXTURE_2D, IDs2[0])
        glBegin(GL_QUADS);

        glTexCoord2f(1.0, 1.0);
        glVertex2f(-w, -(h - h / slice * spacing) / 2);
        glTexCoord2f(0.0, 1.0);
        glVertex2f(0, -(h - h / slice * spacing) / 2);
        glTexCoord2f(0.0, 0.0);
        glVertex2f(0, -((h - h / slice * spacing) / 2 + h / slice * spacing));
        glTexCoord2f(1.0, 0.0);
        glVertex2f(-w, -((h - h / slice * spacing) / 2 + h / slice * spacing));

        glEnd();

        self.drawAreaSelected()
        self.drawLines()
        self.drawRects()
        glFlush()

    def drawAreaSelected(self):
        global W, H
        glDisable(GL_TEXTURE_2D)
        x0 = 0;
        y0 = 0;
        if self.x < W and self.y < H:
            x0=-W; y0=0;
        if self.x > W and self.y < H:
            x0 = 0;
            y0 = 0;
        if self.x < W and self.y > H:
            x0 = -W;
            y0 = -H;
        glLineWidth(2.0);

        glBegin(GL_LINES);
        glColor3f(1, 1, 1)
        glVertex2i(x0, y0);
        glVertex2i(x0+W, y0);
        glVertex2i(x0+W, y0);
        glVertex2i(x0+W, y0+H);
        glVertex2i(x0+W, y0+H);
        glVertex2i(x0, y0+H);
        glVertex2i(x0, y0+H);
        glVertex2i(x0, y0);
        glEnd();

    def drawLines(self):
        global Lx, Ly, Lz, W, H,w,h
        if Lz < (w - w / slice * spacing) / 2: Lz = int((w - w / slice * spacing) / 2);
        if Lz > (w - w / slice * spacing) / 2 + w / slice * spacing: Lz = int(
            (w - w / slice * spacing) / 2 + w / slice * spacing);
        glLineWidth(2.0);

        glBegin(GL_LINES);
        glColor3f(1, 0, 0)
        glVertex2i(-W, Ly);
        glVertex2i(0, Ly);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(1, 0, 0)
        #glVertex2i(W, Ly);
        #glVertex2i(0, Ly);
        glVertex2i(W-Ly, H);
        glVertex2i(W-Ly, 0);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 1, 0)
        glVertex2i(Lx - W, H);
        glVertex2i(Lx - W, 0);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 1, 0)
        glVertex2i(Lx - W, -H);
        glVertex2i(Lx - W, 0);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 0, 1)
        glVertex2i(W, Lz);
        glVertex2i(0, Lz);
        glEnd();

        glBegin(GL_LINES);
        glColor3f(0, 0, 1)
        glVertex2i(-W, -H+Lz);
        glVertex2i(0, -H+Lz);
        glEnd();

    def drawRects(self):
        glLineWidth(1.0);
        for ndx, member in enumerate(rects):
            rect2=rects[ndx]
            if rect2[0]<W and rect2[1]<H:
                if rect2[0] < lim1[0]: rect2[0] = lim1[0]
                if rect2[2] < lim1[0]: rect2[2] = lim1[0]
                if rect2[0] > lim1[2]: rect2[0] = lim1[2]
                if rect2[2] > lim1[2]: rect2[2] = lim1[2]

                if rect2[1] < lim1[1]: rect2[1] = lim1[1]
                if rect2[3] < lim1[1]: rect2[3] = lim1[1]
                if rect2[1] > lim1[3]: rect2[1] = lim1[3]
                if rect2[3] > lim1[3]: rect2[3] = lim1[3]
                n1 = float((rect2[2] - rect2[0]) / float(w / float(len(image1))) *
                           (rect2[3] - rect2[1]) / float(h / float(len(image1[0]))))
                s1 = float((rect2[2] - rect2[0]) / float(w / float(len(image1))) * spacing *
                           (rect2[3] - rect2[1]) / float(h / float(len(image1[0]))) * spacing)
            if rect2[0] > W and rect2[1] < H:
                if rect2[0] < lim2[0]: rect2[0] = lim2[0]
                if rect2[2] < lim2[0]: rect2[2] = lim2[0]
                if rect2[0] > lim2[2]: rect2[0] = lim2[2]
                if rect2[2] > lim2[2]: rect2[2] = lim2[2]

                if rect2[1] < lim2[1]: rect2[1] = lim2[1]
                if rect2[3] < lim2[1]: rect2[3] = lim2[1]
                if rect2[1] > lim2[3]: rect2[1] = lim2[3]
                if rect2[3] > lim2[3]: rect2[3] = lim2[3]
                n1 = float((rect2[2] - rect2[0]) / float(w / slice * spacing / float(len(image2[0]))) *
                           (rect2[3] - rect2[1]) / float(h / float(len(image2))))
                s1 = float((rect2[2] - rect2[0]) / float(w / slice * spacing / float(len(image2[0]))) * slice *
                           (rect2[3] - rect2[1]) / float(h / float(len(image2))) * spacing)

            if rect2[0] < W and rect2[1] > H:
                if rect2[0] < lim3[0]: rect2[0] = lim3[0]
                if rect2[2] < lim3[0]: rect2[2] = lim3[0]
                if rect2[0] > lim3[2]: rect2[0] = lim3[2]
                if rect2[2] > lim3[2]: rect2[2] = lim3[2]

                if rect2[1] < lim3[1]: rect2[1] = lim3[1]
                if rect2[3] < lim3[1]: rect2[3] = lim3[1]
                if rect2[1] > lim3[3]: rect2[1] = lim3[3]
                if rect2[3] > lim3[3]: rect2[3] = lim3[3]
                n1 = float((rect2[2] - rect2[0]) / float(w / float(len(image3[0]))) *
                           (rect2[3] - rect2[1]) / float(h / slice * spacing / float(len(image3))))
                s1 = float((rect2[2] - rect2[0]) / float(w / float(len(image3[0]))) * slice *
                           (rect2[3] - rect2[1]) / float(h / slice * spacing / float(len(image3))) * spacing)
            glColor3f(1, 1, 0)
            glBegin(GL_LINES)  # start drawing a rectangle
            glVertex2f(rect2[0] - W, H - rect2[1])  # bottom left point
            glVertex2f(rect2[2] - W, H - rect2[1])  # bottom right point
            glVertex2f(rect2[2] - W, H - rect2[1])  # bottom right point
            glVertex2f(rect2[2] - W, H - rect2[3])  # top right point
            glVertex2f(rect2[2] - W, H - rect2[3])  # top right point
            glVertex2f(rect2[2] - W, H - rect2[3])  # top right point
            glVertex2f(rect2[2] - W, H - rect2[3])  # top right point
            glVertex2f(rect2[0] - W, H - rect2[3])  # top left point
            glVertex2f(rect2[0] - W, H - rect2[3])  # top left point
            glVertex2f(rect2[0] - W, H - rect2[1])  # bottom left point
            glEnd()
            glUseProgram(0)
            self.renderText(rect2[2]+10-W, H-rect2[3]+10,0, 'N: ' + str("%.0f" % abs(n1)))
            self.renderText(rect2[2]+10-W, H-rect2[3]+20,0, 'S: ' + str("%.2f" % abs(s1)))
            glPointSize(5.0);
            glColor3f(1, 0, 0)
            glBegin(GL_POINTS);
            glVertex2f(rect2[0] - W, H - rect2[1]);
            glEnd()
            glColor3f(0, 0, 1)
            glBegin(GL_POINTS);
            glVertex2f(rect2[2] - W, H - rect2[3]);
            glEnd()



    def drawInstructions(self, painter):
        text = "Click and drag with the left mouse button to rotate the Qt " \
               "logo."
        metrics = QtGui.QFontMetrics(self.font())
        border = max(4, metrics.leading())

        rect = metrics.boundingRect(0, 0, self.width() - 2 * border,
                                    int(self.height() * 0.125),
                                    QtCore.Qt.AlignCenter | QtCore.Qt.TextWordWrap, text)
        painter.setRenderHint(QtGui.QPainter.TextAntialiasing)
        painter.fillRect(QtCore.QRect(0, 0, self.width(), rect.height() + 2 * border), QtGui.QColor(0, 0, 0, 127))
        painter.setPen(QtCore.Qt.white)
        painter.fillRect(QtCore.QRect(0, 0, self.width(), rect.height() + 2 * border), QtGui.QColor(0, 0, 0, 127))
        painter.drawText((self.width() - rect.width()) / 2, border, rect.width(),
                         rect.height(), QtCore.Qt.AlignCenter | QtCore.Qt.TextWordWrap,
                         text)
    def resizeGL(self, width, height):
        global x, y, w, h, W, H
        glOrtho(-W, W, -H, H, -W, W);

    def keyPressEvent(self, event):
        pass

    def mousePressEvent(self, event):
        x = event.pos().x()
        y = event.pos().y()
        if self.add==1:
            if not (x>W and y>H):
                rects.append([x,y,x,y])
            self.add=0
        for ndx, member in enumerate(rects):
            rect=rects[ndx]
            if abs(rect[0]-x)<20 and abs(rect[1]-y)<20:
                self.rectIndex=ndx
                self.pointIndex=0
                self.move = 1
            if abs(rect[2]-x)<20 and abs(rect[3]-y)<20:
                self.rectIndex=ndx
                self.pointIndex=1
                self.move = 1

    def mouseMoveEvent(self, event):
        self.x=event.pos().x()
        self.y=event.pos().y()
        if event.buttons() != QtCore.Qt.NoButton:
            if self.move==1:
                rects[self.rectIndex][self.pointIndex*2]=self.x
                rects[self.rectIndex][self.pointIndex*2+1]=self.y

        else:
            self.move = 0
        self.glDraw();

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Ui_Form()
    window.show()
    sys.exit(app.exec_())
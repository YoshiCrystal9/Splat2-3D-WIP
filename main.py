"""
Copyright (C) 2015-2016 Kinnay, MrRean, RoadrunnerWMC
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY Yannik Marchand ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Yannik Marchand BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation 
are those of the authors and should not be interpreted as representing
official policies, either expressed or implied, of Yannik Marchand.
"""
# make this 1 to enable a lot more info printed on the console
debugMode = 0

if debugMode == 1:
    print('Starting in debug mode...')

# taken from reggienext, for seeing if you have the right version
minimumVer = 3.4
import sys
currentRunningVersion = sys.version_info.major + (.1 * sys.version_info.minor)
if currentRunningVersion < minimumVer:
    errormsg = 'Please update your copy of Python to ' + str(minimumVer) + \
        ' or greater. Currently running on: ' + sys.version[:5] + ' . However, there is a(n) [outdated] python 2.7 version avaliable.'
    raise Exception(errormsg)

# PyQt5 import checker
try:
    from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui
    from PyQt5.QtOpenGL import *
except (ImportError, NameError):
    errormsg = 'PyQt5 is not installed for this Python installation. Go online and download it.'
    raise Exception(errormsg)

try:
    from OpenGL.GL import *
    from OpenGL.GLU import *
except (ImportError, NameError):
    errormsg = 'PyOpenGL 3.0.1 is not installed for this Python installation. Go online and download it. (or use pip install PyOpenGL)'
    raise Exception(errormsg)

import os

from names import levelName, objectName, SettingName
import byml, fmdl, sarc, yaz0

import datetime
now = datetime.datetime.now

color = 1

class CheckBox(QtWidgets.QCheckBox):
    def __init__(self,node):
        QtWidgets.QCheckBox.__init__(self)
        self.stateChanged.connect(self.changed)
        self.node = node

    def changed(self,state):
        self.node.changeValue(state==QtCore.Qt.Checked)

class LineEdit(QtWidgets.QLineEdit):
    def __init__(self,value,callback):
        QtWidgets.QLineEdit.__init__(self,str(value))
        self.callback = callback
        self.textChanged[str].connect(self.changed)

    def changed(self,text):
        if text:
            self.callback(self)

def FloatEdit(v,cb):
    edit = LineEdit(v,cb)
    edit.setValidator(QtGui.QDoubleValidator())
    return edit

def IntEdit(v,cb):
    edit = LineEdit(v,cb)
    edit.setValidator(QtGui.QIntValidator())
    return edit

class SettingsWidget(QtWidgets.QWidget):
    def __init__(self,parent):
        QtWidgets.QWidget.__init__(self,parent)
        layout = QtWidgets.QVBoxLayout(self)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        layout.addWidget(scroll)
       

        scrollContents = QtWidgets.QWidget()
        self.layout = QtWidgets.QVBoxLayout(scrollContents)
        self.layout.setAlignment(QtCore.Qt.AlignTop)
        scroll.setWidget(scrollContents)

    def reset(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

    def showSettings(self,obj):
        self.current = obj
        currentName = obj.data['UnitConfigName']
        self.config_lbl = QtWidgets.QLabel(objectName(currentName))
        self.config_lbl.setStyleSheet('font-size: 16px')
        self.config_lbl.setToolTip(obj.data['UnitConfigName'])
        self.layout.addWidget(self.config_lbl)

        confName = obj.data['UnitConfigName']
        if confName == 'RespawnPos':
            objdesc = 'The location where one team \nrespawns.'
        else:
            objdesc = 'There is no info on this \n object yet.'
        self.desc_lbl = QtWidgets.QLabel(objdesc)
        self.desc_lbl.setStyleSheet('font-size: 13px')
        self.layout.addWidget(self.desc_lbl)

        lbl = QtWidgets.QLabel('Translate:')
        lbl.setStyleSheet('font-size: 14px')
        self.layout.addWidget(lbl)
        self.transx = FloatEdit(obj.posx,self.changed)
        self.transy = FloatEdit(obj.posy,self.changed)
        self.transz = FloatEdit(obj.posz,self.changed)
        self.layout.addWidget(self.transx)
        self.layout.addWidget(self.transy)
        self.layout.addWidget(self.transz)

        lbl = QtWidgets.QLabel('Rotate:')
        lbl.setStyleSheet('font-size: 14px')
        self.layout.addWidget(lbl)
        self.rotx = FloatEdit(obj.rotx,self.changed)
        self.roty = FloatEdit(obj.roty,self.changed)
        self.rotz = FloatEdit(obj.rotz,self.changed)
        self.layout.addWidget(self.rotx)
        self.layout.addWidget(self.roty)
        self.layout.addWidget(self.rotz)

        lbl = QtWidgets.QLabel('Scale:')
        lbl.setStyleSheet('font-size: 14px')
        self.layout.addWidget(lbl)
        self.sclx = FloatEdit(obj.sclx,self.changed)
        self.scly = FloatEdit(obj.scly,self.changed)
        self.sclz = FloatEdit(obj.sclz,self.changed)
        self.layout.addWidget(self.sclx)
        self.layout.addWidget(self.scly)
        self.layout.addWidget(self.sclz)

        for key in obj.data:
            vnode = obj.data.getSubNode(key)
            if not key in ['Scale','Translate','Rotate','UnitConfig','Links','UnitConfigName',
                           'IsLinkDest','ModelSuffix','ModelName', 'Team', 'Text']:
                lbl = QtWidgets.QLabel(SettingName(key)+':')
                if isinstance(vnode,byml.FloatNode):
                    box = FloatEdit(obj.data[key],self.changed2)
                    box.node = vnode
                elif isinstance(vnode,byml.IntegerNode):
                    box = IntEdit(obj.data[key],self.changed2)
                    box.node = vnode
                elif isinstance(vnode,byml.BooleanNode):
                    box = CheckBox(vnode)
                    if obj.data[key]:
                        box.toggle()
                elif isinstance(vnode,byml.StringNode):
                    box = LineEdit(str(obj.data[key]),self.changed2)
                    box.node = vnode
                    box.setEnabled(False)
                else:
                    box = QtWidgets.QLineEdit(str(obj.data[key]))
                    box.setEnabled(False)
                self.layout.addWidget(lbl)
                self.layout.addWidget(box)
                
            elif key == 'UnitConfigName':
                lbl = QtWidgets.QLabel(key+':')
                #box = LineEdit(str(obj.data['UnitConfigName']),self.configNameChanged)
                #box.node = vnode
                box = QtWidgets.QLineEdit(str(obj.data[key]))
                box.setEnabled(False)
                self.layout.addWidget(lbl)
                self.layout.addWidget(box)
                
            elif key == 'ModelName':
                lbl = QtWidgets.QLabel(key+':')
                if isinstance(vnode,byml.StringNode):
                    box = LineEdit(str(obj.data['ModelName']),self.modelNameChanged)
                    box.node = vnode
                else:
                    box = QtWidgets.QLineEdit(str(obj.data['ModelName']))
                    box.setEnabled(False)
                self.layout.addWidget(lbl)
                self.layout.addWidget(box)
                
            elif key == 'Team':
                self.team_lbl = QtWidgets.QLabel(key+':')              
                if isinstance(vnode,byml.IntegerNode):
                    self.team_box = LineEdit((obj.data['Team']),self.changed2)
                    self.team_box.setToolTip('A value of 2 means neutral, for all game modes.')  
                    self.team_box.node = vnode
                else:
                    self.team_box = QtWidgets.QLineEdit(obj.data['Team'])
                    self.team_box.setToolTip('A value of 2 means neutral, for all game modes.')      
                    self.team_box.setEnabled(True)
                self.layout.addWidget(self.team_lbl)
                self.layout.addWidget(self.team_box)

            elif key == 'Text':
                lbl = QtWidgets.QLabel(key+':')
                box = QtWidgets.QLineEdit(str(obj.data['Text']))
                box.setEnabled(True)
                self.layout.addWidget(lbl)
                self.layout.addWidget(box)                

    def changed(self,box):
        if self.transx.text() and self.transy.text() and self.transz.text() and self.rotx.text() and self.roty.text() and self.rotz.text() and self.sclx.text() and self.scly.text() and self.sclz.text():
            self.current.posx = float(self.transx.text())
            self.current.posy = float(self.transy.text())
            self.current.posz = float(self.transz.text())
            self.current.rotx = float(self.rotx.text())
            self.current.roty = float(self.roty.text())
            self.current.rotz = float(self.rotz.text())
            self.current.sclx = float(self.sclx.text())
            self.current.scly = float(self.scly.text())
            self.current.sclz = float(self.sclz.text())
            self.current.saveValues()
            window.glWidget.updateGL()

    def changed2(self,box):
        if box.text():
            box.node.changeValue(box.text())

    #def configNameChanged(self,box):
    #    if box.text():
    #        box.node.changeValue(box.text())
    #        self.config_lbl.setText(box.text())
    #        self.current.updateModel()

    def modelNameChanged(self,box):
        if box.text():
            box.node.changeValue(box.text())
            self.current.updateModel()

class LevelObject:
    def __init__(self,obj,dlist):
        global color
        self.data = obj
        self.color = (color//100/10,((color//10)%10)/10,(color%10)/10)
        color+=1
        if debugMode == 1:
            print("Self.color output:" + str(self.color))
            print("Color output :" + str(color))
        self.list = dlist
        
        trans = obj['Translate']
        self.posx = trans['X']/100
        self.posy = trans['Y']/100
        self.posz = trans['Z']/100

        rot = obj['Rotate']
        self.rotx = rot['X']
        self.roty = rot['Y']
        self.rotz = rot['Z']

        scale = obj['Scale']
        self.sclx = scale['X']
        self.scly = scale['Y']
        self.sclz = scale['Z']

    def saveValues(self):
        obj = self.data
        trans = obj['Translate']
        if self.posx != trans['X']/100:
            trans.getSubNode('X').changeValue(self.posx*100)
        if self.posy != trans['Y']/100:
            trans.getSubNode('Y').changeValue(self.posy*100)
        if self.posz != trans['Z']/100:
            trans.getSubNode('Z').changeValue(self.posz*100)
            
        rot = obj['Rotate']
        if self.rotx != rot['X']:
            rot.getSubNode('X').changeValue(self.rotx)
        if self.roty != rot['Y']:
            rot.getSubNode('Y').changeValue(self.roty)
        if self.rotz != rot['Z']:
            rot.getSubNode('Z').changeValue(self.rotz)

        scale = obj['Scale']
        if self.sclx != scale['X']:
            scale.getSubNode('X').changeValue(self.sclx)
        if self.scly != scale['Y']:
            scale.getSubNode('Y').changeValue(self.scly)
        if self.sclz != scale['Z']:
            scale.getSubNode('Z').changeValue(self.sclz)

    def draw(self,pick):
        if pick:
            glColor3f(*self.color)
        glPushMatrix()
        glTranslatef(self.posx,self.posy,self.posz)
        glRotatef(self.rotx,1.0,0.0,0.0)
        glRotatef(self.roty,0.0,1.0,0.0)
        glRotatef(self.rotz,0.0,0.0,1.0)
        #glScalef(self.sclx,self.scly,self.sclz)
        glCallList(self.list)
        glPopMatrix()

    def updateModel(self):
        model = self.data['ModelName']
        if not self.data['ModelName']:
            model = self.data['UnitConfigName']
        if not model in window.glWidget.cache:
            window.glWidget.cache[model] = window.glWidget.loadModel(model)
        self.list = window.glWidget.cache[model]
        window.glWidget.updateGL()

class LevelWidget(QGLWidget):

    objects = []
    cache = {}
    rotx = roty = rotz = 0
    posx = posy = 0
    posz = -300
    picked = None
    
    def __init__(self,parent):
        QGLWidget.__init__(self,parent)

    def reset(self):
        self.objects = []
        self.rotx = self.roty = self.rotz = 0
        self.posx = self.posy =  0
        self.posz = -300

    def pickObjects(self,x,y):
        self.paintGL(1)
        array = (GLuint * 1)(0)
        pixel = glReadPixels(x,self.height()-y,1,1,GL_RGB,GL_UNSIGNED_BYTE,array)
        r,g,b = [round(((array[0]>>(i*8))&0xFF)/255.0,1) for i in range(3)]
        if debugMode == 1:
            print("R " + str(r))
            print("G " + str(g))
            print("B " + str(b))       
        self.picked = None
        window.settings.reset()
        for obj in self.objects:
            if obj.color == (r,g,b):
                self.picked = obj
                break
        if self.picked:
            if debugMode == 1:
                print('Picked State: ' + str(self.picked))
            window.settings.showSettings(self.picked)
        self.updateGL()

    def paintGL(self,pick=0):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(self.posx,self.posy,self.posz)
        glRotatef(self.rotx,1.0,0.0,0.0)
        glRotatef(self.roty,0.0,1.0,0.0)
        glRotatef(self.rotz,0.0,0.0,1.0)
        for obj in self.objects:
            if obj == self.picked:
                glColor3f(1.0,0.0,0.0)
            else:
                glColor3f(1.0,1.0,1.0)
            obj.draw(pick)

    def resizeGL(self,w,h):
        if h == 0:
            h = 1
            
        glViewport(0,0,w,h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0,float(w)/float(h),0.1,750.0)
        glMatrixMode(GL_MODELVIEW)

    def initializeGL(self):
        glClearColor(0.3,0.3,1.0,0.0)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        self.generateCubeList()

    def addObject(self,obj,modelName):
        if not modelName in self.cache:
            self.cache[modelName] = self.loadModel(modelName)
        lobj = LevelObject(obj,self.cache[modelName])
        self.objects.append(lobj)

    # chain for loading models, they're seperated in the game for some reason
    def loadModel(self,name):
        paths = ('/Model/',
               '/Pack/Obj/Model/',
               '/Pack/ObjSmall/Model/',
               '/Pack/Enemy/Model/')
        
        for objpath in paths:
            base = window.gamePath + str(objpath) + str(name)
            if os.path.isfile(str(base) + '.sarc'):
                ext = '.sarc'
            elif os.path.isfile(str(base) + '.szs'):
                ext = '.szs'
            else:
                kind = '(skipped)'
                continue

            if os.path.isfile(str(base) + str(ext)):
                with open(base + ext, 'rb') as f:
                    data = f.read()
                    print('Loading model ' + name + '!')
                    if data.startswith(b'Yaz0'):
                        print('Decompressing Yaz0...')
                        yaz0archive = yaz0.decompress(data)
                        if sarc.contains(yaz0archive, 'Output.bfres'):
                            bfres = sarc.extract(yaz0archive, 'Output.bfres')
                            model = fmdl.parse(bfres)
                            return self.generateList(model)
                    else:
                        print('Skipping yaz0 decompression')
                        sarchive = data
                        if sarc.contains(sarchive, 'Output.bfres'):
                            bfres = sarc.extract(sarchive, 'Output.bfres')
                            model = fmdl.parse(bfres)
                            return self.generateList(model)                                         
                    break              
        else:
            return self.cubeList         

    def generateList(self,model):
        displayList = glGenLists(1)
        glNewList(displayList,GL_COMPILE)

        for polygon in model.shapes:

            rotation = polygon.rotation
            triangles = polygon.indices
            vertices = polygon.vertices
            
            glPushMatrix()
            glRotatef(rotation[0],1.0,0.0,0.0)
            glRotatef(rotation[1],0.0,1.0,0.0)
            glRotatef(rotation[2],0.0,0.0,1.0)

            glBegin(GL_TRIANGLES)
            for vertex in triangles:
                glVertex3f(*[vertices[vertex][i]/100 for i in range(3)])
            glEnd()

            glPushAttrib(GL_CURRENT_BIT)
            glColor3f(0.0,0.0,0.0)
            for triangle in [triangles[i*3:i*3+3] for i in range(len(triangles)//3)]:
                glBegin(GL_LINES)
                for vertex in triangle:
                    glVertex3f(*[vertices[vertex][i]/100 for i in range(3)])
                glEnd()
            glPopAttrib()

            glPopMatrix()
        
        glEndList()
        return displayList

    def generateCubeList(self):
        displayList = glGenLists(1)
        glNewList(displayList,GL_COMPILE)

        glBegin(GL_QUADS)
        self.drawCube()
        glEnd()

        glBegin(GL_LINES)
        glColor3f(0.0,0.0,0.0)
        self.drawCube()
        glEnd()

        glEndList()

        self.cubeList = displayList

    def drawCube(self):
        glVertex3f( 0.3, 0.3,-0.3)
        glVertex3f(-0.3, 0.3,-0.3)
        glVertex3f(-0.3, 0.3, 0.3)
        glVertex3f( 0.3, 0.3, 0.3)

        glVertex3f( 0.3,-0.3, 0.3)
        glVertex3f(-0.3,-0.3, 0.3)
        glVertex3f(-0.3,-0.3,-0.3)
        glVertex3f( 0.3,-0.3,-0.3)
        
        glVertex3f( 0.3, 0.3, 0.3)
        glVertex3f(-0.3, 0.3, 0.3)
        glVertex3f(-0.3,-0.3, 0.3)
        glVertex3f( 0.3,-0.3, 0.3)

        glVertex3f( 0.3,-0.3,-0.3)
        glVertex3f(-0.3,-0.3,-0.3)
        glVertex3f(-0.3, 0.3,-0.3)
        glVertex3f( 0.3, 0.3,-0.3)
        
        glVertex3f(-0.3, 0.3, 0.3)
        glVertex3f(-0.3, 0.3,-0.3)
        glVertex3f(-0.3,-0.3,-0.3)
        glVertex3f(-0.3,-0.3, 0.3)
        
        glVertex3f( 0.3, 0.3,-0.3)
        glVertex3f( 0.3, 0.3, 0.3)
        glVertex3f( 0.3,-0.3, 0.3)
        glVertex3f( 0.3,-0.3,-0.3)
    
    mousex = mousey = 0
    def mousePressEvent(self,event):
        if event.button() == 1:
            self.pickObjects(event.x(),event.y())
            if debugMode == 1:
                print('Mouse click X: ' + str(event.x()))
                print('Mouse click Y: ' + str(event.y()))

        self.mousex = event.x()
        self.mousey = event.y()

    def mouseMoveEvent(self,event):
        deltax = (event.x()-self.mousex)/2
        deltay = (event.y()-self.mousey)/2
        buttons = event.buttons()
        if buttons & QtCore.Qt.LeftButton:
            self.posx += deltax
            self.posy -= deltay
        if buttons & QtCore.Qt.RightButton:
            self.roty += deltax
            self.rotx += deltay
        self.mousex = event.x()
        self.mousey = event.y()
        self.updateGL()

class ChooseLevelDialog(QtWidgets.QDialog):
    def __init__(self,levelList):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle('Choose Stage')
        self.currentLevel = None

        tree = QtWidgets.QTreeWidget()
        tree.setHeaderHidden(True)
        tree.currentItemChanged.connect(self.handleItemChange)
        tree.itemActivated.connect(self.handleItemActivated)
        
        nodes = []
        for level in levelList:
            levelNode = QtWidgets.QTreeWidgetItem()
            levelNode.setData(0,QtCore.Qt.UserRole,level['MapFileName'])
            darp = level['MapFileName']
            levelNode.setText(0,'Stage '+str(level['MapFileName']) + ' (' + levelName(darp) + ')')
            nodes.append(levelNode)
        tree.addTopLevelItems(nodes)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok|QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        btn = self.buttonBox.addButton("Other file...",QtWidgets.QDialogButtonBox.ActionRole)
        btn.clicked.connect(self.openFile)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(tree)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)

        self.setMinimumWidth(340)
        self.setMinimumHeight(384)

    def openFile(self):
        fn = QtWidgets.QFileDialog.getOpenFileName(self,'Open Level','Map','Level Archives (*.szs)')[0]
        self.currentLevel = os.path.basename(str(fn))[:-4]
        if self.currentLevel:
            self.accept()

    def handleItemChange(self,current,previous):
        self.currentLevel = str(current.data(0,QtCore.Qt.UserRole))
        if not self.currentLevel:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)
        else:
            self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(True)

    def handleItemActivated(self,item,column):
        self.currentLevel = str(item.data(0,QtCore.Qt.UserRole))
        if self.currentLevel:
            self.accept()

class MainWindow(QtWidgets.QMainWindow):

    keyPresses = {0x1000020: 0}
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Splat3D ALPHA v0.2")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setIconSize(QtCore.QSize(16, 16))        
        self.setGeometry(100,100,1080,720)

        #self.statusBar().showMessage('Ready')
        self.setupMenu()
        
        self.qsettings = QtCore.QSettings("Kinnay, MrRean","Splat3D, based off of 3DW Editor by Kinnay")
        self.gamePath = self.qsettings.value('gamePath')
        if not self.isValidGameFolder(self.gamePath):
            self.changeGamePath(True)

        self.loadStageList()
        
        self.settings = SettingsWidget(self)
        self.setupGLScene()
        self.resizeWidgets()

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateCamera)
        self.timer.start(30)

        self.show()

    def changeGamePath(self,disable=False):
        """
        Message box that appears when the user wants to change their set game path
        """        
        path = self.askGamePath()
        if path:
            self.qsettings.setValue('gamePath',path)
        else:
            if disable:
                self.openAction.setEnabled(False)
            QtWidgets.QMessageBox.warning(self,"Incomplete Folder","The folder you chose doesn't seem to contain the required files.")

    def askGamePath(self):
        """
        Message box that asks the user to choose a game path
        """        
        QtWidgets.QMessageBox.information(self,'Game Path',"You're now going to be asked to pick a folder. Choose the folder that contains at least the Pack and Model folders of Splatoon. You can change this later in the settings menu.")
        folder = QtWidgets.QFileDialog.getExistingDirectory(self,"Choose Game Path")
        if not self.isValidGameFolder(folder):
            return None
        return folder

    def isValidGameFolder(self,folder):
        """
        Returns a value depending on if the game folder the user chose is acceptable
        """        
        if not folder: return 0
        if not os.path.exists(folder+'/Pack'): return 0
        if not os.path.exists(folder+'/Model'): return 0
        if not os.path.exists(folder+'/Pack/Obj'): return 0
        if not os.path.exists(folder+'/Pack/ObjSmall'): return 0
        if not os.path.exists(folder+'/Pack/Enemy'): return 0
        if not os.path.exists(folder+'/Pack/Static'): return 0
        if not os.path.exists(folder+'/Pack/Static/Mush'): return 0
        if not os.path.exists(folder+'/Pack/Static/Map'): return 0         
        return 1

    # luckily Splatoon has a MapInfo.byaml to load stuff in....
    def loadStageList(self):
        """
        Loads MapInfo.byaml, to get the list of levels for the level choosing dialog
        """        
        with open(self.gamePath+'\Pack\Static\Mush\MapInfo.byaml','rb') as f:
            data = f.read()
            
        # no need to compress or anything, it's as-is
        self.levelList = byml.BYML(data).rootNode
        
    # Splatoon stores it's levels in /Pack/Map/____.szs/____.byaml so it's double layered
    # looks like we have to double the decompression and extraction
    # or we can just ask the user to kindly extract them??
    def showLevelDialog(self):
        """
        Loads the level choosing dialog, along with sending the level data to loadLevel()
        """        
        levelSelect = ChooseLevelDialog(self.levelList)
        levelSelect.exec_()
        print(self.gamePath + '/Pack/Static/Map/' + levelSelect.currentLevel + '.szs')
        if os.path.isfile(self.gamePath + '/Pack/Static/Map/' + levelSelect.currentLevel + '.szs'):
            with open(str(self.gamePath+'/Pack/Static/Map/'+levelSelect.currentLevel + '.szs'),'rb') as f:
                data = f.read()
            self.levelData = byml.BYML(sarc.extract(yaz0.decompress(data),levelSelect.currentLevel + '.byaml'))
            self.loadLevel(self.levelData.rootNode)
            self.setWindowTitle("Splat3D ALPHA v0.2 " + levelSelect.currentLevel + '.szs' + ' (' + levelName(levelSelect.currentLevel) + ')')
        else:
            return

    def loadLevel(self,levelData):
        """
        Loads a level, specified by 1 argument which is the data from the BYAML, usually called from showLevelDialog()
        """
        stime = now() # start the timer to count how long it takes to load a level
        self.glWidget.reset()
        self.settings.reset()
        amount = len(levelData['Objs']) # load the Objs subnode
        progress = QtWidgets.QProgressDialog(self)
        progress.setCancelButton(None)
        progress.setMinimumDuration(0)
        progress.setRange(0,amount)
        progress.setWindowModality(QtCore.Qt.WindowModal)
        progress.setWindowTitle('Loading...')
        i = 0
        for obj in levelData['Objs']: # load the objects
            progress.setLabelText('Loading object '+str(i+1)+'/'+str(amount)) # count, etc etc
            progress.setValue(i)
            self.loadObject(obj)
            self.glWidget.updateGL()
            i+=1
        progress.setValue(i)
        self.saveAction.setEnabled(True)
        doneBox = QtWidgets.QMessageBox()
        doneBox.setWindowTitle('Stage loaded')
        doneBox.setText("Stage is now loaded.")
        doneBox.exec_()
        print('Loading time: ' + str(now()-stime))

    def loadObject(self,obj):
        """
        Loads an object, with said object being the argument
        """        
        modelName = obj['ModelName'] if obj['ModelName'] else obj['UnitConfigName']
        regularName = str(obj['UnitConfigName'])
        print('Loaded object ' + objectName(regularName))     
        self.glWidget.addObject(obj,modelName)

    def openParamEditor(self):
        """
        Opens the param editor
        """        
        dlg = ParamWindow(self)
        dlg.exec_()

    # buttons n shortcuts
    def setupMenu(self):
        """
        Sets up the menu on the top part of the UI
        """        
        self.openAction = QtWidgets.QAction("Open",self)
        self.openAction.setShortcut("Ctrl+O")
        self.openAction.triggered.connect(self.showLevelDialog)

        self.saveAction = QtWidgets.QAction("Save",self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.saveLevel)
        self.saveAction.setEnabled(False)

        #self.openparamAction = QtWidgets.QAction("Param Editor",self)
        #self.openparamAction.setShortcut("Ctrl+P")
        #self.openparamAction.triggered.connect(self.openParamEditor)       

        pathAction = QtWidgets.QAction("Change Game Path",self)
        pathAction.setShortcut("Ctrl+G")
        pathAction.triggered.connect(self.changeGamePath)
        
        self.menubar = self.menuBar()
        fileMenu = self.menubar.addMenu("File")
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        #toolMenu = self.menubar.addMenu("Tools")
        #toolMenu.addAction(self.openparamAction)
        settingsMenu = self.menubar.addMenu("Settings")
        settingsMenu.addAction(pathAction)    

    def saveLevel(self):
        """
        Saves the level
        """        
        fn = QtWidgets.QFileDialog.getSaveFileName(self,'Save Level','Map','Unpacked Levels (*.byaml)')[0]
        with open(fn,'wb') as f:
            self.levelData.saveChanges()
            f.write(self.levelData.data)

    def setupGLScene(self):
        self.glWidget = LevelWidget(self)
        self.glWidget.show()

    def resizeWidgets(self):
        self.glWidget.setGeometry(220,21,self.width(),self.height()-21)
        self.settings.setGeometry(0,21,220,self.height()-21)

    def resizeEvent(self,event):
        self.resizeWidgets()

    def updateCamera(self):
        spd = self.keyPresses[0x1000020]*2+1
        updateScene = False
        for key in self.keyPresses:
            if self.keyPresses[key]:
                if key == ord('I'): self.glWidget.rotx+=spd
                elif key == ord('K'): self.glWidget.rotx-=spd
                elif key == ord('O'): self.glWidget.roty+=spd
                elif key == ord('L'): self.glWidget.roty-=spd
                elif key == ord('P'): self.glWidget.rotz+=spd
                elif key == ord(';'): self.glWidget.rotz-=spd
                elif key == ord('A'): self.glWidget.posx-=spd
                elif key == ord('D'): self.glWidget.posx+=spd
                elif key == ord('S'): self.glWidget.posy-=spd
                elif key == ord('W'): self.glWidget.posy+=spd
                elif key == ord('Q'): self.glWidget.posz-=spd
                elif key == ord('E'): self.glWidget.posz+=spd
                updateScene = True

        if updateScene:
            self.glWidget.updateGL()

    def keyReleaseEvent(self,event):
        self.keyPresses[event.key()] = 0

    def keyPressEvent(self,event):
        self.keyPresses[event.key()] = 1

    def wheelEvent(self,event):
        self.glWidget.posz += event.angleDelta().y() / 15
        self.glWidget.updateGL()

def main():
    global window
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

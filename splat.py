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
debugMode = 1

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
    from PyQt5.QtOpenGL import QGLWidget
except (ImportError, NameError):
    errormsg = 'PyQt5 is not installed for this Python installation.'
    raise Exception(errormsg)

try:
    from OpenGL import GL, GLU
except (ImportError, NameError):
    errormsg = 'PyOpenGL 3.0.1 is not installed for this Python installation.'
    raise Exception(errormsg)

from ctypes import util
try:
    from OpenGL.platform import win32
except (AttributeError):
    pass

import os, random
from names import description, levelName, objectName, SettingName, ReplaceModel
import byml, fmdl, inkling, preseteditor, sarc, yaz0

import datetime
now = datetime.datetime.now

color = 1

class MainWindow(QtWidgets.QMainWindow):

    keyPresses = {0x1000020: 0}
    
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowTitle("Splatoon 2 Level Editor ALPHA v0.1")
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setIconSize(QtCore.QSize(16, 16))        
        self.setGeometry(100,100,1080,720)

        self.setupMenu()
        
        self.qsettings = QtCore.QSettings("YoshiCrystal","Splatoon 2 Level Editor, based off of Splat3D by Kinnay and MrReam")
        self.gamePath = self.qsettings.value('gamePath')
        if not self.isValidGameFolder(self.gamePath):
            self.changeGamePath(True)

        self.loadStageList()
        
        self.settings = SettingsWidget(self)
        self.setupGLScene()
        self.resizeWidgets()
        
        self.setupBG()
        self.setupGender()

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
            # the lines here weren't quite needed, because it is discarded otherwise
            QtWidgets.QMessageBox.warning(self,"Incomplete Folder","The folder you chose doesn't seem to contain the required files.")

    def askGamePath(self):
        """
        Message box that asks the user to choose a game path
        """        
        QtWidgets.QMessageBox.information(self,'Game Path',"Select the romfs folder of Splatoon 2.")
        folder = QtWidgets.QFileDialog.getExistingDirectory(self,"Choose Game Path")
        if not self.isValidGameFolder(folder):
            return None
        else:
            QtWidgets.QMessageBox.information(self,'Success',"Game folder changed. You must restart the program for the changes to take effect.")
            return folder


    def isValidGameFolder(self,folder):
        """
        Returns a value depending on if the game folder the user chose is acceptable
        """        
        if not folder: return 0
        if not os.path.exists(folder+'/Mush'): return 0
        if not os.path.exists(folder+'/Model'): return 0
        if not os.path.exists(folder+'/Map'): return 0
        if not os.path.exists(folder+'/Param'): return 0
        return 1

    # luckily Splatoon has a MapInfo.byaml to load stuff in....
    def loadStageList(self):
        """
        Loads MapInfo.release.byaml, to get the list of levels for the level choosing dialog
        """        
        with open(self.gamePath+'/Mush/MapInfo.release.byml','rb') as f:
            data = f.read()
            
        # no need to compress or anything, it's as-is
        self.levelList = byml.Byml(data).parse()

        # byml.BYML(data).rootNode SEE WHAT TO DO WITH THIS LOL HELP
        
    # Splatoon stores it's levels in /Pack/Map/____.szs/____.byaml so it's double layered
    # looks like we have to double the decompression and extraction
    # or we can just ask the user to kindly extract them??
    def showLevelDialog(self):
        """
        Loads the level choosing dialog, along with sending the level data to loadLevel()
        """        
        levelSelect = ChooseLevelDialog(self.levelList)
        if levelSelect.exec_():
            if levelSelect.absolutePath:
                path = levelSelect.stageName
                name = levelSelect.stageNamePath
                print('Path: ' + path)
                print('Level name ' + name)
                custom = 1
            else:
                path = self.gamePath + '/Map' + levelSelect.stageName + '.szs'
                custom = 0

            if os.path.isfile(path):
                with open(path, 'rb') as f:
                    data = f.read()
                if custom == 0:
                    print(levelSelect.stageName + '.byaml')
                    self.levelData = byml.Byml((sarc.extract(path), self.gamePath + '/levelSelect.stageName' + levelSelect.stageName + '.byaml'))
                    self.loadLevel(self.levelData.rootNode)
                    self.setWindowTitle('Splatoon 2 Level Editor v0.1 ' + os.path.basename(path) + ' (' + levelName(levelSelect.stageName) + ')')                       
                if custom == 1:
                    self.levelData = byml.Byml((sarc.extract(path), self.gamePath + '/', levelSelect.stageName + levelSelect.stageName + '.byaml'))
                    self.loadLevel(self.levelData.rootNode)
                    self.setWindowTitle('Splatoon 2 Level Editor v0.1 ' + os.path.basename(path) + ' (' + levelName(levelSelect.stageName[:-4]) + ')')                 
                
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
        
##        amount2 = len(levelData['Rails']) # load the Objs subnode
##        progress2 = QtWidgets.QProgressDialog(self)
##        progress2.setCancelButton(None)
##        progress2.setMinimumDuration(0)
##        progress2.setRange(0,amount2)
##        progress2.setWindowModality(QtCore.Qt.WindowModal)
##        progress2.setWindowTitle('Loading...')            
##        i2 = 0
##        for rail in levelData['Rails']: # load the objects
##            progress.setLabelText('Loading rail '+str(i2+1)+'/'+str(amount2)) # count, etc etc
##            progress.setValue(i2)
##            self.loadRail(rail)
##            self.glWidget.updateGL()
##            i2+=1            
##        progress2.setValue(i2)
        
        self.saveAction.setEnabled(True)
        doneBox = QtWidgets.QMessageBox()
        doneBox.setWindowTitle('Stage loaded')
        doneBox.setText("Stage is now loaded.")
        doneBox.exec_()
        self.resetlevelAction.setEnabled(True)
        print('Loading time: ' + str(now()-stime))

    def loadObject(self,obj):
        """
        Loads an object, with said object being the argument
        """        
        modelName = obj['ModelName'] if obj['ModelName'] else obj['UnitConfigName']
        regularName = str(obj['UnitConfigName'])
        print('Loaded object ' + objectName(regularName))     
        self.glWidget.addObject(obj,modelName)

##    def loadRail(self,rail):
##        """
##        Loads a rail, with said rail being the argument
##        """
##        modelName = rail['ModelName'] if rail['ModelName'] else rail['UnitConfigName']
##        regularName = str(rail['UnitConfigName'])
##        print('Loaded rail ' + regularName)    
##        self.glWidget.addRail(rail, modelName)        

    def openParamEditor(self):
        """
        Opens the param editor
        """        
        dlg = ParamWindow(self)
        dlg.exec_()  

    def openInklingChooser(self):
        """
        Opens the inkling chooser
        """        
        dlg = inkling.ChooseInkling()
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return
        if dlg.maleButton.isChecked():
            self.glWidget.inkGender = 1
        if dlg.femaleButton.isChecked():
            self.glWidget.inkGender = 0
        self.qsettings.setValue('gender',self.glWidget.inkGender)

    def openPresetEditor(self):
        """
        Opens the preset editor
        """
        dlg = preseteditor.PresetEditor()
        if dlg.exec_() != QtWidgets.QDialog.Accepted:
            return

    def openBGChooser(self):
        """
        Opens the bg color chooser
        """        
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.white, self, 'asdf')
        if color is None: return
     
        self.glWidget.bgcolor = (color.red() / 255, color.green() / 255, color.blue() / 255, color.alpha() / 255)
     
        self.qsettings.setValue('bgcolor', self.glWidget.bgcolor)
        QtWidgets.QMessageBox.information(self, 'Background Changed!', 'Background color changed. You must restart the program for the changes to take effect.')
            
    # buttons n shortcuts
    def setupMenu(self):
        """
        Sets up the menu on the top part of the UI
        """        
        openAction = QtWidgets.QAction("Open",self)
        openAction.setShortcut("Ctrl+O")
        openAction.triggered.connect(self.showLevelDialog)

        self.saveAction = QtWidgets.QAction("Save",self)
        self.saveAction.setShortcut("Ctrl+S")
        self.saveAction.triggered.connect(self.saveLevel)
        self.saveAction.setEnabled(False)

        resetCamera = QtWidgets.QAction("Reset Camera",self)
        resetCamera.setShortcut("Ctrl+R")
        resetCamera.triggered.connect(self.resetCamera)
        self.resetlevelAction = QtWidgets.QAction("Reset Level",self)
        self.resetlevelAction.setShortcut("Ctrl+T")
        self.resetlevelAction.triggered.connect(self.resetLevel)
        self.resetlevelAction.setEnabled(False)

        pathAction = QtWidgets.QAction("Change Game Path",self)
        pathAction.setShortcut("Ctrl+G")
        pathAction.triggered.connect(self.changeGamePath)

        changeInkling = QtWidgets.QAction("Change Inkling",self)
        changeInkling.setShortcut("CTRL+I")
        changeInkling.triggered.connect(self.openInklingChooser)
        changeBGColor = QtWidgets.QAction("Change Background",self)
        changeBGColor.setShortcut("CTRL+B")
        changeBGColor.triggered.connect(self.openBGChooser)        
        changePreset = QtWidgets.QAction("Preset Editor",self)
        changePreset.setShortcut("CTRL+P")
        changePreset.triggered.connect(self.openPresetEditor)
        
        menubar = self.menuBar()
        fileMenu = menubar.addMenu("File").addActions([openAction, self.saveAction])
        toolMenu = menubar.addMenu("Tools").addActions([resetCamera, self.resetlevelAction])
        settingsMenu = menubar.addMenu("Settings").addAction(pathAction)
        otherMenu = menubar.addMenu("Other").addActions([changeInkling, changeBGColor, changePreset])

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

    def resetCamera(self):        
        self.glWidget.resetCamera()

    def resetLevel(self):
        self.glWidget.reset()

    def setupGender(self):
        self.glWidget.inkGender = self.qsettings.value('gender')

    def setupBG(self):
        self.glWidget.bgcolor = self.qsettings.value('bgcolor')     

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

        self.infolbl = QtWidgets.QLabel('Ready.')
        layout.addWidget(self.infolbl)

    def updateInfo(self, x, y):
        self.infolbl.setText('X: %d Y: %d' % (x, y))

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
        self.desc_lbl = QtWidgets.QLabel(description(confName))
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
            if not key in ['Scale','Translate','Rotate','UnitConfig','UnitConfigName',
                           'ModelName', 'Team', 'Text']:
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
                    self.team_box = ComboBoxEdit((obj.data['Team']),self.changed)
                    self.team_box.setToolTip('A value of 2 means neutral, for all game modes.')  
                    self.team_box.node = vnode
                else:
                    self.team_box = ComboBoxEdit(obj.data['Team'])
                    self.team_box.setToolTip('A value of 2 means neutral, for all game modes.')      
                    self.team_box.setEnabled(True)
                self.layout.addWidget(self.team_lbl)
                self.layout.addWidget(self.team_box)

            elif key == 'Text':
                lbl = QtWidgets.QLabel(key+':')
                box = QtWidgets.QLineEdit(str(obj.data['Text']))
                box.setEnabled(False)
                self.layout.addWidget(lbl)
                self.layout.addWidget(box)                

    def changed(self,box):
        if self.transx.text() and self.transy.text() and self.transz.text() and self.rotx.text() and self.roty.text() and self.rotz.text() and self.sclx.text() and self.scly.text() and self.sclz.text():
            try:
                self.current.posx = float(self.transx.text().replace(',', '.'))
                self.current.posy = float(self.transy.text().replace(',', '.'))
                self.current.posz = float(self.transz.text().replace(',', '.'))
                self.current.rotx = float(self.rotx.text().replace(',', '.'))
                self.current.roty = float(self.roty.text().replace(',', '.'))        
                self.current.rotz = float(self.rotz.text().replace(',', '.'))
                self.current.sclx = float(self.sclx.text().replace(',', '.'))
                self.current.scly = float(self.scly.text().replace(',', '.'))
                self.current.sclz = float(self.sclz.text().replace(',', '.'))
                self.current.saveValues()
                window.glWidget.updateGL()
            except:
                print("Please enter a valid float")

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
        if debugMode == 1:
            print(self.list)
        
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
            GL.glColor3f(*self.color)
        GL.glPushMatrix()
        GL.glTranslatef(self.posx,self.posy,self.posz)
        GL.glRotatef(self.rotx,1.0,0.0,0.0)
        GL.glRotatef(self.roty,0.0,1.0,0.0)
        GL.glRotatef(self.rotz,0.0,0.0,1.0)
        #glScalef(self.sclx,self.scly,self.sclz)
        GL.glCallList(self.list)
        GL.glPopMatrix()

    def updateModel(self):
        model = self.data['ModelName']
        if not self.data['ModelName']:
            model = self.data['UnitConfigName']
        if not model in window.glWidget.cache:
            window.glWidget.cache[model] = window.glWidget.loadModel(model)
        self.list = window.glWidget.cache[model]
        if debugMode == 1:
            print(self.list)
        window.glWidget.updateGL()

class LevelWidget(QGLWidget):

    objects = []
    cache = {}
    rotx = 45
    roty = -45
    rotz = 0
    posx = posy = 0
    posz = -10
    picked = None
    bgcolor = (0, 0, 0, 0)
    
    def __init__(self,parent):
        QGLWidget.__init__(self,parent)

    def getTeam(self, obj):
        teamobj = obj.data['Team']
        print(str(teamobj))

    def reset(self):
        self.objects = []
        self.rotx = 45
        self.roty = -45
        self.rotz = 0
        self.posx = self.posy = 0
        self.posz = -10

    def resetCamera(self):
        self.rotx = 45
        self.roty = -45
        self.rotz = 0
        self.posx = self.posy = 0
        self.posz = -10
        
    def pickObjects(self,x,y):
        self.paintGL(1)
        array = (GL.GLuint * 1)(0)
        pixel = GL.glReadPixels(x,self.height()-y,1,1,GL.GL_RGB,GL.GL_UNSIGNED_BYTE,array)
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
        GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
        GL.glLoadIdentity()         
        GL.glTranslatef(self.posx,self.posy,self.posz)
        GL.glRotatef(self.rotx,1.0,0.0,0.0)
        GL.glRotatef(self.roty,0.0,1.0,0.0)
        GL.glRotatef(self.rotz,0.0,0.0,1.0)
        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(0.0,0.0,0.0)
        GL.glColor3f(1, 0, 0)
        GL.glVertex3f(0, 0, 0)
        GL.glVertex3f(10000, 0, 0)
        GL.glColor3f(0, 1, 0)
        GL.glVertex3f(0, 0, 0)
        GL.glVertex3f(0, 10000, 0)
        GL.glColor3f(0, 0, 1)
        GL.glVertex3f(0, 0, 0)
        GL.glVertex3f(0, 0, 10000)
        GL.glEnd()
        for obj in self.objects:
            if obj == self.picked:
                GL.glColor3f(1.0,0.0,0.0)
            else:
                GL.glColor3f(1.0,1.0,1.0)
            obj.draw(pick)

    def resizeGL(self,w,h):
        if h == 0:
            h = 1
            
        GL.glViewport(0,0,w,h)
        GL.glMatrixMode(GL.GL_PROJECTION)
        GL.glLoadIdentity()
        GLU.gluPerspective(45.0,float(w)/float(h),0.1,750.0)
        GL.glMatrixMode(GL.GL_MODELVIEW)

    def initializeGL(self):
        if self.bgcolor is not None:
            GL.glClearColor(*self.bgcolor)
        else:
            GL.glClearColor(0.3, 0.3, 0.3, 0.0)
            QtWidgets.QMessageBox.information(self,'Default Background',"You have not chosen a background yet! If you want to use a custom background, go to Other > Change Background to change it. For now, we'll default you with one.")
        GL.glDepthFunc(GL.GL_LEQUAL)
        GL.glEnable(GL.GL_DEPTH_TEST)
        self.generateCubeList()  

    def addObject(self,obj,modelName):
        if modelName not in self.cache:
            self.cache[modelName] = self.loadModel(modelName)
        lobj = LevelObject(obj,self.cache[modelName])
        self.objects.append(lobj)

##    def addRail(self, rail, modelName):
##        if not modelName in self.cache:
##            self.cache[modelName] = self.loadModel(modelName)
##        lobj = LevelObject(rail,self.cache[modelName])
##        self.objects.append(lobj)        

    # chain for loading models, they're seperated in the game for some reason
    def loadModel(self,newname):
        
        if self.inkGender == 1:
            gen = 1
        else:
            gen = 0

        if newname == 'StartPos' and gen == 1:
            newname = 'Player01'
        if newname == 'StartPos' and gen == 0:
            newname = 'Player00'

        name = ReplaceModel(newname, gen)
        
        paths = ('/Model/',
               '/Pack/Obj/Model/',
               '/Pack/ObjSmall/Model/',
               '/Pack/Enemy/Model/',
               '/Pack/Player/Model/')
        
        for objpath in paths:
            base = window.gamePath + str(objpath) + str(name)
            if os.path.isfile(str(base) + '.sarc'):
                ext = '.sarc'
            elif os.path.isfile(str(base) + '.szs'):
                ext = '.szs'
            else:
                kind = '(skipped)'
                continue

            if base == window.gamePath + '/Pack/ObjSmall/Model/Obj_DemoPlayer':
                return self.cubeList
            
            if os.path.isfile(str(base) + str(ext)):
                with open(base + ext, 'rb') as f:
                    data = f.read()
                    print('Loading model ' + name + '!')   
                    if data.startswith(b'Yaz0'):
                        print('Decompressing Yaz0...')
                        yaz0archive = yaz0.decompress(data)
                        if b"Output.bfres" in yaz0archive:
                            bfres = sarc.extract(yaz0archive, 'Output.bfres')
                            model = fmdl.parse(bfres)
                            return self.generateList(model)
                        else:
                            return self.cubeList   
                    else:
                        print('Skipping yaz0 decompression')
                        sarchive = data
                        if b"Output.bfres" in sarchive:
                            bfres = sarc.extract(sarchive, 'Output.bfres')
                            model = fmdl.parse(bfres)
                            return self.generateList(model)
                        else:
                            return self.cubeList   
                    break              
        else:
            return self.cubeList         

    def generateList(self,model):
        displayList = GL.glGenLists(1)
        GL.glNewList(displayList,GL.GL_COMPILE)

        for polygon in model.shapes:

            rotation = polygon.rotation
            triangles = polygon.indices
            vertices = polygon.vertices
            
            GL.glPushMatrix()
            GL.glRotatef(rotation[0],1.0,0.0,0.0)
            GL.glRotatef(rotation[1],0.0,1.0,0.0)
            GL.glRotatef(rotation[2],0.0,0.0,1.0)

            GL.glBegin(GL.GL_TRIANGLES)
            for vertex in triangles:
                GL.glVertex3f(*[vertices[vertex][i]/100 for i in range(3)])
            GL.glEnd()

            GL.glPushAttrib(GL.GL_CURRENT_BIT)
            GL.glColor3f(0.0,0.0,0.0)
            for triangle in [triangles[i*3:i*3+3] for i in range(len(triangles)//3)]:
                GL.glBegin(GL.GL_LINES)
                for vertex in triangle:
                    GL.glVertex3f(*[vertices[vertex][i]/100 for i in range(3)])
                GL.glEnd()
            GL.glPopAttrib()

            GL.glPopMatrix()
        
        GL.glEndList()
        return displayList

    def generateCubeList(self):
        displayList = GL.glGenLists(1)
        GL.glNewList(displayList,GL.GL_COMPILE)

        GL.glBegin(GL.GL_QUADS)
        self.drawCube()
        GL.glEnd()

        GL.glBegin(GL.GL_LINES)
        GL.glColor3f(0.0,0.0,0.0)
        self.drawCube()
        GL.glEnd()

        GL.glEndList()

        self.cubeList = displayList     

    def drawCube(self):
        GL.glVertex3f( 0.1, 0.1,-0.1)
        GL.glVertex3f(-0.1, 0.1,-0.1)
        GL.glVertex3f(-0.1, 0.1, 0.1)
        GL.glVertex3f( 0.1, 0.1, 0.1)

        GL.glVertex3f( 0.1,-0.1, 0.1)
        GL.glVertex3f(-0.1,-0.1, 0.1)
        GL.glVertex3f(-0.1,-0.1,-0.1)
        GL.glVertex3f( 0.1,-0.1,-0.1)
        
        GL.glVertex3f( 0.1, 0.1, 0.1)
        GL.glVertex3f(-0.1, 0.1, 0.1)
        GL.glVertex3f(-0.1,-0.1, 0.1)
        GL.glVertex3f( 0.1,-0.1, 0.1)

        GL.glVertex3f( 0.1,-0.1,-0.1)
        GL.glVertex3f(-0.1,-0.1,-0.1)
        GL.glVertex3f(-0.1, 0.1,-0.1)
        GL.glVertex3f( 0.1, 0.1,-0.1)
        
        GL.glVertex3f(-0.1, 0.1, 0.1)
        GL.glVertex3f(-0.1, 0.1,-0.1)
        GL.glVertex3f(-0.1,-0.1,-0.1)
        GL.glVertex3f(-0.1,-0.1, 0.1)
        
        GL.glVertex3f( 0.1, 0.1,-0.1)
        GL.glVertex3f( 0.1, 0.1, 0.1)
        GL.glVertex3f( 0.1,-0.1, 0.1)
        GL.glVertex3f( 0.1,-0.1,-0.1)

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
        self.setMouseTracking(True)
        self.parent().settings.updateInfo(event.x(), event.y())
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
    stageName = ''
    absolutePath = False
    stageNamePath = ''

    def __init__(self, levelList):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle('Choose Stage')

        tree = QtWidgets.QTreeWidget()
        tree.setHeaderHidden(True)
        tree.currentItemChanged.connect(self.handleItemChange)
        tree.itemActivated.connect(self.handleItemActivated)
        
        nodes = []
        for level in levelList:
            levelNode = QtWidgets.QTreeWidgetItem()
            levelNode.setData(0, QtCore.Qt.UserRole, level['MapFileName'])
            oldName = level['MapFileName']
            levelNode.setText(0, levelName(oldName) + ' (' + level['MapFileName'] + ')')
            nodes.append(levelNode)
        tree.addTopLevelItems(nodes)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(False)

        btn = self.buttonBox.addButton('Other file...', QtWidgets.QDialogButtonBox.ActionRole)
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
        """
        The user chose to open a specific file
        """
        fn = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Level', 'Map', 'Level Archives (*.szs)')[0]
        self.stageName = fn
        self.stageNamePath = os.path.basename(str(fn))[:-4]
        print(self.stageName)
        if self.stageName:
            self.absolutePath = True
            self.accept()

    def handleItemChange(self, current, previous):
        """
        The user single-clicked on a level name
        """
        self.stageName = str(current.data(0, QtCore.Qt.UserRole))
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ok).setEnabled(bool(self.stageName))

    def handleItemActivated(self, item, column):
        """
        The user double-clicked on a level name
        """
        self.stageName = str(item.data(0, QtCore.Qt.UserRole))
        if self.stageName:
            self.accept()      

class CheckBox(QtWidgets.QCheckBox):
    """
    A checkbox widget for setting a value of 0 or 1 within a node.
    """
    def __init__(self,node):
        QtWidgets.QCheckBox.__init__(self)
        self.stateChanged.connect(self.changed)
        self.node = node

    def changed(self,state):
        self.node.changeValue(state==QtCore.Qt.Checked)

teams = [
        'Team Alpha',
        'Team Beta',
        'Neutral'
        ]

class ComboBoxEdit(QtWidgets.QComboBox):
    """
    A combobox widget for choosing a value rather than manually inputting it
    """
    def __init__(self, value, callback):
        super().__init__()
        self.clear()
        self.addItems(teams)
        self.setCurrentIndex(value % 3)
        self.callback = callback
        self.currentIndexChanged.connect(self.changedValue)

    def changedValue(self, value):
        self.callback(self)        

class FloatBoxEdit(QtWidgets.QDoubleSpinBox):
    """
    Class for a QDoubleSpinBox, for floating points and various values
    """
    def __init__(self, value, callback):
        super().__init__()
        self.setSingleStep(0.1)
        self.setRange(-99999999, 999999999)
        self.setValue(value)
        self.callback = callback
        self.valueChanged.connect(self.changedValue)

    def changedValue(self, value):
        self.callback(self)

class IntBoxEdit(QtWidgets.QSpinBox):
    """
    Class for a QSpinBox, for ints and various values
    """
    def __init__(self, value, callback):
        super().__init__()
        self.setSingleStep(1)
        self.setRange(-99999999, 999999999)
        self.setValue(value)
        self.callback = callback
        self.valueChanged.connect(self.changedValue)

    def changedValue(self, value):
        self.callback(self)

class LineEdit(QtWidgets.QLineEdit):
    """
    A simple QLineEdit widget for editing a value, such as a string.
    """
    def __init__(self,value,callback):
        QtWidgets.QLineEdit.__init__(self,str(value))
        self.callback = callback
        self.textChanged[str].connect(self.changed)

    def changed(self,text): 
        if text:
            self.callback(self)

def FloatEdit(v,cb):
    """
    Returns an edit for a float
    """
    edit = FloatBoxEdit(v,cb)
    return edit

def IntEdit(v,cb):
    """
    Returns an edit for an integer
    """
    edit = IntBoxEdit(v,cb)
    return edit

def main():
    global window   
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

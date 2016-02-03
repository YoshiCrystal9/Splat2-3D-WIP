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
import splat
import os
from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui

class PresetEditor(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle('Inkopolis Preset Editor') 
        self.setGeometry(100,100,500,500)
        ChooserWidget(self)

    def parseBIN(self):
        pass
    
class ChooserWidget(QtWidgets.QWidget): 
    def __init__(self,parent):
        QtWidgets.QWidget.__init__(self,parent)

        tree = QtWidgets.QTreeWidget()
        tree.setHeaderHidden(True)
        tree.currentItemChanged.connect(self.handleItemChange)
        tree.itemActivated.connect(self.handleItemActivated)
        
        files = []
        path = r"C:\Users\Joshua\WiiU\nus_content\0005000E10176900\160Broke\content\Pack\Static\Etc\PlayerInfo\\"
        for name in os.listdir(path):
            if os.path.isfile(os.path.join(path, name)):
                files.append(name)
                presetBin = QtWidgets.QTreeWidgetItem()
                presetBin.setData(0, QtCore.Qt.UserRole, path)
                presetBin.setText(0, name)
                files.append(presetBin)
        tree.addTopLevelItems(files)
        
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(tree)
        self.setLayout(layout)

    def handleItemChange(self):
        pass

    def handleItemActivated(self):
        pass


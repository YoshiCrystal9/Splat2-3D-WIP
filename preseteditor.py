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
import os, struct
from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui

class PresetEditor(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle('Inkopolis Preset Editor') 
        self.setGeometry(100,100,500,500)

        openAction = QtWidgets.QAction('Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open Bin')
        openAction.triggered.connect(self.openBin)

        menubar = QtWidgets.QMenuBar()
        fileMenu = menubar.addMenu('File')
        fileMenu.addAction(openAction)

        self.nameEdit = QtWidgets.QLineEdit()
        self.nameEdit.setMaxLength(21)
        self.nameEdit.setMaximumWidth(120)

        self.unk1Edit = QtWidgets.QSpinBox()
        self.unk1Edit.setSingleStep(1)
        self.unk1Edit.setRange(-99999999, 999999999)
        
        layout = QtWidgets.QFormLayout(self)
        layout.addWidget(menubar)
        layout.addRow('Inkling Name:', self.nameEdit)
        layout.addRow('Unknown 0x37:', self.unk1Edit)

    def parseBin(self, data):
        offset = 0x06
        binstruct = struct.Struct('>42s4xI')

        bindata = binstruct.unpack_from(data, offset)

        namereg, unk1 = bindata

        self.name = namereg.decode('utf-16be')

        self.nameEdit.setText(self.name)
        self.unk1Edit.setValue(unk1)

    def openBin(self):
        fn = QtWidgets.QFileDialog.getOpenFileName(self, 'Open Preset', 'derp', 'Binary files (*.bin)')[0]
        with open(fn, 'rb') as f:
            data = f.read()
            if data[:6] != b'\xFF\xFF\xFF\xFF\x01\xEF':
                invalidBinBox = QtWidgets.QMessageBox()
                invalidBinBox.setWindowTitle('Invalid File')
                invalidBinBox.setText("The BIN file you have tried to load is invalid.")
                invalidBinBox.exec_()
            else:
                self.parseBin(data)

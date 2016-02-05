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
from PyQt5 import QtWidgets, QtCore, QtWidgets, QtGui

class ChooseInkling(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        self.setWindowTitle('Choose Inkling Gender')
        #self.setWindowIcon(QtGui.QIcon('icon.png'))
        #self.setIconSize(QtCore.QSize(16, 16))        
        self.setGeometry(100,100,170,70)

        layout = QtWidgets.QVBoxLayout()
        self.label = QtWidgets.QLabel("Choose your Inkling gender!")       
        self.maleButton = QtWidgets.QRadioButton("Male", self)
        self.femaleButton = QtWidgets.QRadioButton("Female", self)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)        
        
        self.label.move(10,10)
        self.maleButton.move(10,10)
        self.femaleButton.move(80,10)
        self.maleButton.setChecked(False)
        self.femaleButton.setChecked(True)
        
        layout.addWidget(self.label)
        layout.addWidget(self.maleButton)
        layout.addWidget(self.femaleButton)
        layout.addWidget(self.buttonBox)
        
        self.genderButtons = QtWidgets.QButtonGroup()
        self.genderButtons.addButton(self.maleButton)
        self.genderButtons.addButton(self.femaleButton)

        self.setLayout(layout)

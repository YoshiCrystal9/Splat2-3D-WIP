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
def SettingName(oldName):
    if oldName == 'PaintDefault':
        return 'Painted Default?'
    if oldName == 'FloatParameter0':
        return 'Floating Parameter 0'
    if oldName == 'FloatParameter1':
        return 'Floating Parameter 1'
    if oldName == 'FloatParameter2':
        return 'Floating Parameter 2'
    if oldName == 'FloatParameter3':
        return 'Floating Parameter 3'
    if oldName == 'FloatParameter4':
        return 'Floating Parameter 4'
    if oldName == 'PaintRatePerBullet':
        return 'Painting Rate'
    if oldName == 'IsAbleToBeVsCulled':
        return 'Is Vs Culled'       
    return oldName

def objectName(oldobjectName):
    if oldobjectName == 'Brd_Sparrow00':
        return 'Sparrow'
    if oldobjectName == 'ScrambleBombFlower':
        return 'Rainmaker'
    
    return oldobjectName

def levelName(oldlevelName):
    if oldlevelName.startswith('Test'):
        return 'Test Level (UNUSED)'
    if oldlevelName == 'Fld_Crank00_Vss':
        return 'Urchin Underpass (VSS)'
    if oldlevelName == 'Fld_Warehouse00_Vss':
        return 'Walleye Warehouse (VSS)'
    if oldlevelName == 'Fld_SeaPlant00_Vss':
        return 'oh shit'
    if oldlevelName == 'Fld_UpDown00_Vss':
        return 'Saltspray Rig (VSS)'
    if oldlevelName == 'Fld_SkatePark00_vss':
        return 'Blackbelly Skatepark (VSS)'
    if oldlevelName == 'Fld_Athletic00_Vss':
        return 'Camp Triggerfish (VSS)'
    if oldlevelName == 'Fld_Amida00_Vss':
        return 'oh shit'
    if oldlevelName == 'Fld_Maze00_Vss':
        return 'Kelp Dome (VSS)'
    if oldlevelName == 'Fld_Tuzura00_Vss':
        return 'oh shit'
    if oldlevelName == 'Fld_Ruins00_Vss':
        return 'oh shit'

    return oldlevelName

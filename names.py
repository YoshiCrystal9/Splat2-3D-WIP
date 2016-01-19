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
def description(confName):
    descs = {
        'RespawnPos': 'The location where one team \nrespawns.',
        'Fld_Crank00': 'The Urchin Underpass map.',
        'GachihokoRouteArea': 'A line for tower control. \nConnects two points.',
        'GachihokoTargetPoint': 'A point for tower control. \nThis is where a line connects.',
        'Obj_Tree00': 'A tree. It can be painted on.',
        'Obj_VictoryPoint': 'A point where one team wins. \nThe winning point for \nRainmaker and Tower Control.',
        'Obj_VictoryLift': 'The Tower! Bring it to the \nenemy goal to win!',
        'Obj_Windsock': 'A decoration. It blows in the \nwind.',
        'Obj_Bunker01': 'A bunker for protection!',
        }
    return descs.get(confName, confName)
        
def SettingName(oldName):
    params = {
        }     
    return params.get(oldName, oldName)

def objectName(oldobjectName):
    objs = {
        'Brd_Sparrow00': 'Sparrow',
        'ScrambleBombFlower': 'Rainmaker',
        'RespawnPos': 'Respawn Position',
        'StartPos': 'Starting Position',
        'Obj_VictoryLift': 'Tower Control Tower',
        'PaintTargetArea': 'Splat Zone',
        'Obj_VictoryPoint': 'Victory Point',
        'Obj_Jerry00': 'Jellyfish',
        'GachihokoTargetPoint': 'Tower Control Point',
        'GachihokoRouteArea': 'Tower Control Line',
        'Obj_Tree00': 'Tree',
        'Obj_SeaGull': 'Seagull',
        'Obj_Windsock': 'Windsock',
        'Lft_HeavyCraneMachine': 'Saltspray Crane',
        'Obj_Flag': 'Flag',
        'Obj_AirDancer': 'Air Dancer',
        'Obj_Grass00': 'Grass',
        'Lft_Forklift': 'Forklift',
        'Obj_TreeBanana': 'Banana Tree',
        'ExplanationTextObj': 'Explanation Trigger',
        'SwitchAllDead': 'Extermination Switch',
        'Fld_Crank00': 'Urchin Underpass Map',
        }
    return objs.get(oldobjectName, oldobjectName)

def levelName(oldlevelName):
    if oldlevelName.startswith('Test'):
        return 'Test Level (UNUSED)'
    if oldlevelName == 'Fld_Crank00_Vss':
        return 'Urchin Underpass (VSS)'
    if oldlevelName == 'Fld_Warehouse00_Vss':
        return 'Walleye Warehouse (VSS)'
    if oldlevelName == 'Fld_SeaPlant00_Vss':
        return 'Saltspray Rig (VSS)'
    if oldlevelName == 'Fld_UpDown00_Vss':
        return 'Arowna Mall (VSS)'
    if oldlevelName == 'Fld_SkatePark00_Vss':
        return 'Blackbelly Skatepark (VSS)'
    if oldlevelName == 'Fld_Athletic00_Vss':
        return 'Camp Triggerfish (VSS)'
    if oldlevelName == 'Fld_Amida00_Vss':
        return 'Port Mackerel (VSS)'
    if oldlevelName == 'Fld_Maze00_Vss':
        return 'Kelp Dome (VSS)'
    if oldlevelName == 'Fld_Tuzura00_Vss':
        return 'Moray Towers (VSS)'
    if oldlevelName == 'Fld_Ruins00_Vss':
        return 'Bluefin Depot (VSS)'
    if oldlevelName == 'Fld_ShootingRange_Shr':
        return 'Shooting Range'
    if oldlevelName == 'Fld_Tutorial00_Ttr':
        return 'Tutorial Stage'
    if oldlevelName == 'Fld_World00_Wld':
        return 'Octovalley Map'
    if oldlevelName == 'Fld_Plaza00_Plz':
        return 'Inkopolis'

    return oldlevelName

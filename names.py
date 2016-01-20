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
		'Brd_Sparrow00': 'A little bird for decoration.',
		'ScrambleBombFlower': 'The Rainmaker spawn point.',
		'StartPos': 'The normal player \nspawn point.',
		'Obj_Grass00': 'A decoration.',
		'PaintTargetArea': 'A Splat Zone for multiplayer.',
		'Obj_TreeBanana': 'A Banana Tree. It can be \npainted on.',
		'Obj_SighterTarget': 'A shootable target \nused in the shooting range.',
		'Obj_BigNamazu': 'The Big Zapfish. Used \nas a decoration.',
		'Obj_PlazaTrain': 'A Train used on the \nplaza for decoration',
		'Obj_PlazaAmiibo': 'The amiibo case used \non the plaza.',
		'Npc_Jerry00': 'A NPC used for decoration.',
		'Fld_Hiagari00': 'The Map model for \nHiagari.',
		'GachihokoHikikomoriArea': 'The Rainmaker Free Zone \nused in multiplayer.',
		'Obj_JerryBeachBall': 'NPCs used for \ndecoration on hiagari.',
		'Obj_JerryBikini': 'A NPC used for \ndecoration on hiagari.',
		'Obj_JerryWeddingRelative': 'A Jellyfish relative used\n for the wedding on \n Hiagari.',
		'Obj_JerryWeddingBride': 'A Jellyfish bride used \nfor the wedding on \nHiagari.',
		'Obj_JerryFloat_Bikini00': 'A NPC used for \ndecoration on Hiagari.',
		'Obj_JerryFloat_Bikini01': 'A NPC used for \ndecoration on Hiagari.',
		'Obj_JerryFloat_Nude01': 'A NPC used for \ndecoration on Hiagari.',
		'Obj_JerryFloat_Mat00': 'A NPC used for \ndecoration on Hiagari.',
		'Obj_QuarryBeltHoko': 'The first set of \nTransport Belts used \non Quarry',
		'Obj_QuarryBeltYagura': 'The second set of \nTransport Belts used \non Quarry',
		'Fld_Quarry00': 'The moving Platforms in Pivot.',
		'Obj_QuarryBBQSet': 'A BBQ set used for\n decoration on Quarry.',
		'Obj_QuarryFlag': 'A flag used for decoration\n on Quarry.',
		'Obj_GachiSignBoad': 'A sign used to \ninform players of\n a Rainmaker Zone.',
		'Fld_Tutorial00': 'The Map model for \nthe Tutorial Map.',
		'Obj_AirBall': 'A Air Balloon that\n can be shot.',
		'Obj_AutoWarpPoint': 'A target/destination \npoint for planned \nink jumps.',
		'Obj_WaterTank': 'A Water Tank used \nfor decoration.',
		'Obj_IkaSetB': 'A Statue Set used \nfor decoration.',
		'Obj_IkaSetA': 'A Statue Set used \nfor decoration.',
		'Fld_Pivot00': 'The Map model for \nQuarry.',
		'Lft_PivotDoor00': 'The moving Platforms in Pivot.',
		'Lft_PivotDoor01': 'The moving Platforms in Pivot.',
		'Obj_JerryArt': 'A NPC used for \ndecoration on Pivot.',
		'Obj_Bunker02': 'A bunker for protection!',
		'Lft_PivotDoor03': 'The moving Platforms in Pivot.',
		'Fld_SkatePark00': 'The Map model for \nSkatePark.',
		'Fld_Crank01': 'The updated \nMap model for \nCrank.',
		'Fld_Athletic00': 'The Map model for \nAthletic',
		'Fld_Maze00': 'The Map model for \nMaze',
		'Fld_Kaisou00': 'The Map model for \nKaisou.',
		'Fld_Tuzura00': 'The Map model for \nTuzura.',
		'Obj_Athletic00': 'A box used on \nAthletic.',
		'Obj_BalloonLightMDL': 'A light used for \ndecoration.',
		'Obj_kaisouBox': 'A box used on \nKaisou',
		'Obj_Athletic01': 'A wall used on \nAthletic',
		'Obj_AirWallKaisouSteelFrame': 'The bridge steel frame \nused on Kaisou.',
		'Enm_RailKing': 'The DJ Octavio \nboss enemy.',
		'Obj_Compass': 'A target for \nthe arrow pointing \nthe player to a \nmission goal.',
		'Npc_CommanderBind': 'Cpt. Cuttlefish \nhow he appears in the \n final boss fight.',
		'ExplanationTextObjLastBoss': 'Explanation Trigger(Boss)',
		'Obj_Goal': 'Boss Goal',
		'Enm_CylinderKing': 'Octonozzle(Boss)',
		'Obj_Sphere': 'A orb adding 1 to \nthe players sp currency.',
		'Obj_AncientDocument': 'An ancient scroll that \ncan be found in missions.',
		'Obj_TreeOrange': 'A orange tree used for decoration.',
		'Fld_World00': 'The Map model for \nthe SP hub.',
		'Obj_Gateway': 'A level entry for \nsingleplayer maps.',
		'Obj_Geyser': 'A ink geyser used \nin singleplayer.',
		'Obj_InkRail': 'A Ink Rail spawner used \nin singleplayer.',
		'Obj_RailKingPilotHouse': 'The glass bowl DJ Octavio \ncan be seen in after beating \n the singleplayer.',
		'Obj_PlazaIdolSpeakerA': 'A speaker that can be \nseen on the plaza while \na splatfest is running.',
		'Obj_PlazaIdolSpeakerB': 'A speaker that can be \nseen on the plaza while \na splatfest is running.',
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
		'Fld_Crank00': 'Crank Map Field(old)',
		'Obj_SighterTarget': 'Shoothing Range Target',
		'Obj_BigNamazu': 'Big Zapfish',
		'Obj_PlazaTrain': 'Plaza Train',
		'Obj_PlazaAmiibo': 'Plaza Amiibo Case',
		'Npc_Jerry00': 'Jellyfish',
		'Fld_Hiagari00': 'Hiagari Map Field',
		'GachihokoHikikomoriArea': 'Rainmaker Free Zone',
		'Obj_JerryBeachBall': 'Beachball Jellyfish',
		'Obj_JerryBikini': 'Beach Jellyfish',
		'Obj_JerryWeddingRelative': 'Jellyfish Wedding Relative',
		'Obj_JerryWeddingBride': 'Jellyfish Wedding Bride',
		'Obj_JerryFloat_Bikini00': 'Pool Jellyfish 1',
		'Obj_JerryFloat_Bikini01': 'Pool Jellyfish 2',
		'Obj_JerryFloat_Nude01': 'Pool Jellyfish 3',
		'Obj_JerryFloat_Mat00': 'Pool Jellyfish 4',
		'Obj_QuarryBeltHoko': 'Quarry Transport Belt 1',
		'Obj_QuarryBeltYagura': 'Quarry Transport Belt 2',
		'Fld_Quarry00': 'Quarry Map Field',
		'Obj_QuarryBBQSet': 'BBQ Set',
		'Obj_QuarryFlag': 'Flag',
		'Obj_GachiSignBoad': 'Rainmaker Zone Sign',
		'Fld_Tutorial00': 'Tutorial Map Field',
		'Obj_AirBall': 'Air Balloon',
		'Obj_AutoWarpPoint': 'Warp Point',
		'Obj_WaterTank': 'Water Tank',
		'Obj_IkaSetB': 'Statue Set B',
		'Obj_IkaSetA': 'Statue Set A',
		'Fld_Pivot00': 'Pivot Map Field',
		'Lft_PivotDoor00': 'Pivot Moving PLatforms(small)',
		'Lft_PivotDoor01': 'Pivot Moving PLatforms(big)',
		'Obj_JerryArt': 'Art Jellyfish',
		'Obj_Bunker01': 'VS Bumper(small)',
		'Obj_Bunker02': 'VS Bumper(big)',
		'Lft_PivotDoor03': 'Pivot Moving PLatforms(mid)',
		'Fld_SkatePark00': 'Skatepark Map Field',
		'Fld_Crank01': 'Crank Map Field(new)',
		'Fld_Athletic00': 'Athletic Map Field(new)',
		'Fld_Maze00': 'Maze Map Field',
		'Fld_Kaisou00': 'Kaisou Map Field',
		'Fld_Tuzura00': 'Tuzura Map Field',
		'Obj_Athletic00': 'Athletic Map Box',
		'Obj_BalloonLightMDL': 'Balloon Light',
		'Obj_kaisouBox': 'Kaisou Box',
		'Obj_Athletic01': 'Athletic Map Wall',
		'Obj_AirWallKaisouSteelFrame': 'Kaisou Steel Frame',
		'Enm_RailKing': 'DJ Octavio(Boss)',
		'Obj_Compass': 'Mission Arrow Target',
		'Npc_CommanderBind': 'Cpt.Cuttlefish(Boss)',
		'ExplanationTextObjLastBoss': 'Explanation Trigger(Boss)',
		'Obj_Goal': 'Boss Goal',
		'Enm_CylinderKing': 'Octonozzle(Boss)',
		'Obj_Sphere': 'SP Currency',
		'Obj_AncientDocument': 'SP Scroll',
		'Obj_TreeOrange': 'Orange Tree',
		'Fld_World00': 'World Map Field',
		'Obj_Gateway': 'SP level entry',
		'Obj_Geyser': 'Ink Geyser',
		'Obj_InkRail': 'Ink Rail Spawner',
		'Obj_RailKingPilotHouse': 'Octavio glass bowl',
		'Obj_PlazaIdolSpeakerA': 'Splatfest Speaker A',
		'Obj_PlazaIdolSpeakerB': 'Splatfest Speaker B',
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

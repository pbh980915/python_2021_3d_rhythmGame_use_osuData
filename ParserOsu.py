import pygame
from time import time
from T3dData import *
from multiprocessing import Process
processes = []

class HitObject_data:
    def __init__(self, hitobject):
        self.data       = hitobject
        self.x          = hitobject[0]       
        self.y          = hitobject[1]       
        self.time       = hitobject[2]    
        self.type       = hitobject[3]    
        self.hitSound   = hitobject[4]
        
        self.hitSample          = -1                
        self.hitType            = -1            
        self.spinner_endTime    = -1    
        self.curve_type         = -1        
        self.curve_points       = -1      
        self.curve_repeat       = -1      
        self.curve_length       = -1      
        self.curve_edgeSounds   = -1  
        self.curve_edgeSets     = -1   
        self.bezier             = -1  
        try:
            if len(hitobject) == 6:   # if circle
                self.hitSample = hitobject[5]
                self.hitType = 'circle'
                
            elif len(hitobject) == 7: # if spinner
                self.spinner_endTime = hitobject[5]
                self.hitSample = hitobject[6]
                self.hitType = 'spinner'
            else:                     # if curve
                self.curve_type   = hitobject[5][0]    
                self.curve_points = hitobject[5][1:]    
                self.curve_repeat = hitobject[6]        
                self.curve_length = hitobject[7]    
                self.curve_edgeSounds = hitobject[8]    
                self.curve_edgeSets = hitobject[9]
                self.hitSample = hitobject[10]
                self.hitType = 'curve'
                self.curve_time   = None
        except: pass


class TimingPoint:
    def __init__(self,timingPoint):
        self.data = timingPoint
        self.time        = self.data[0] # start section
        self.length      = self.data[1] # if length sign(-) slider speed %
        self.beatMeter   = self.data[2] # beat count 4
        self.sampleSet   = self.data[3] # soundSet (0 default, 1 normal, 2 soft, 3 drum)
        self.sampleIndex = self.data[4] # soundSet inner sound 
        self.volume      = self.data[5] # volume
        self.uninherited = self.data[6] # 0
        self.effects     = self.data[7] # bright effect
        #
        #
class BeatmapData:
    def __init__(self):
        parseData = self.load_osu_file(py3d_data.songPath+py3d_data.songdif)

        #general
        self.audioFilename          = parseData[0][1][1]
        self.audioLeadIn            = parseData[0][2][1]
        self.previewTime            = parseData[0][3][1]
        self.countdown              = parseData[0][4][1]
        self.sampleSet              = parseData[0][5][1]
        self.stackLeniency          = parseData[0][6][1]
        self.mode                   = parseData[0][7][1]
        self.letterboxInBreaks      = parseData[0][8][1]
        self.widescreenStoryboard   = parseData[0][9][1]
        
        #editor not used
        
        #matadata
        self.title          = parseData[2][1][1]
        self.titleUnicode   = parseData[2][2][1]
        self.artist         = parseData[2][3][1]
        self.artistUnicode  = parseData[2][4][1]
        self.creator        = parseData[2][5][1]
        self.version        = parseData[2][6][1]
        self.source         = parseData[2][7][1]
        self.tags           = parseData[2][8][1]
        self.source         = parseData[2][9][1]
        self.beatmapID      = parseData[2][9][1]
        self.beatmapSetID   = parseData[2][10][1]
        
        #difficulty
        self.hpDrainRate        = parseData[3][1][1]
        self.circleSize         = parseData[3][2][1]
        self.overallDifficulty  = parseData[3][3][1]
        self.approachRate       = parseData[3][4][1]
        self.sliderMultiplier   = parseData[3][5][1]
        self.sliderTickRate     = parseData[3][6][1]
        
        self.events     = parseData[4] #events

        self.colours    = parseData[6] #colours
        
        #hitObjects, timingPoints
        self.hitObjects         = [ HitObject_data  (parseData[7][i]) for i in range(1,len(parseData[7])) ]
        self.timingPoints       = [ TimingPoint     (parseData[5][i]) for i in range(1,len(parseData[5])) ]
        self.tp_idx             = 0 #timing_point_index
        self.ho_idx             = 0 #hit_object_index
        self.time_beatmap_start = -1

        self.hitSounds          = [[[0 for idx in range(20)] for addition in range(4)] for normal in range(4)]
        try   : self.audio              = pygame.mixer.Sound(py3d_data.songPath+"audio.mp3")
        except: self.audio              = pygame.mixer.Sound(py3d_data.songPath+"audio.wav")
        self.volume_audio       = py3d_data.game_volumeAudio
        self.volume_hitSound    = py3d_data.game_volumeHit
        self.load_hitSounds()

        self.start_time = time()
        self.running = True
        #
        #
    def load_osu_file (self,filename):
        def read_file (filename):
            datas = []; data = []
            file = open(filename, 'r', encoding = 'UTF8'); lines = file.readlines(); file.close()
            for i in range(len(lines)):
                if     lines[i][0] == '[' : datas.append(data); data = []
                if not lines[i][0] == '\n': data.append(lines[i][:-1])
            datas.append(data)

            datas    = get_beatmapOptions  (datas)
            datas[6] = get_timing_points(datas[6])
            if len(datas) == 8: 
                datas.append(datas[7])
                datas[7] = []
            datas[8] = get_hit_objects  (datas[8])
            return datas[1:]

        def get_beatmapOptions (datas):
            for i in range(1,5): # general,editor,matadata,difficulty,                
                for j in range(len(datas[i])): datas[i][j] = datas[i][j].replace(' ','').split(':')
            #for i in range(1, len(datas[7])  ): # colour
            #    datas[7][i] = datas[7][i].replace(' ','').split(':')[1].split(',')
            #    for j in range(len(datas[7][i])): datas[7][i][j] = float(datas[7][i][j])
            return datas   

        def get_timing_points (timingpoints):
            for i in range(1, len(timingpoints)):
                timingpoints[i] = timingpoints[i].split(',')
                for j in range(len(timingpoints[i])): timingpoints[i][j] = float(timingpoints[i][j])
                timingpoints[i][3] = int(timingpoints[i][3])
            return timingpoints

        def get_hit_objects (hitobjects):
            def ifCircle (data):
                data[5] = (data[5] + '0').split(':')
                for j in range(len(data[5])):  data[5][j] = float(data[5][j])
                data[5][:2] = int(data[5][0]), int(data[5][1])
                return data
            def ifSpinner (data):
                data[5] = float(data[5])
                data[6] = (data[6] + '0').split(':')
                for j in range(len(data[6])):  data[6][j] = float(data[6][j])
                data[6][:2] = int(data[6][0]), int(data[6][1])
                return data
            def ifCurve (data):
                try:
                    data[5] = data[5].split('|') # curve type x,y
                    data[8] = data[8].split('|') # edge sound
                    data[9] = data[9].split('|') # edge sound sets # normal set # addition set
                    data[6:8] = float(data[6]),float(data[7][:6]) # repeat, length
                    data[10] = (data[10] + '0').split(':')
                    for j in range(1,len(data[5])): 
                        data[5][j] = hitobjects[i][5][j].split(':')                 
                        data[5][j][:2] = float(data[5][j][0]), float(data[5][j][1]) # curve x,y
                    for j in range(len(data[8])): data[8][j] = get_bitSet(data[8][j])
                    for j in range(len(data[9])):
                        data[9][j] = data[9][j].split(':')
                        data[9][j][:2] = int(data[9][j][0]),int(data[9][j][1])       
                    for j in range(len(hitobjects[i][10])): data[10][j] = float(data[10][j])
                except: pass
                return data

            for i in range(1,len(hitobjects)):   
                hitobjects[i] = hitobjects[i].split(',')
                for j in range(5): hitobjects[i][j] = float(hitobjects[i][j]) #x,y,time,type,hitsound
                hitobjects[i][4] = get_bitSet(hitobjects[i][4])
                if   len(hitobjects[i]) == 6 : hitobjects[i] = ifCircle (hitobjects[i])
                elif len(hitobjects[i]) == 7 : hitobjects[i] = ifSpinner(hitobjects[i])
                else                         : hitobjects[i] = ifCurve  (hitobjects[i])
            return hitobjects            
        def get_bitSet (inData):
            outData = []; inData = int(inData)
            for i in range(4): 
                if (inData>>i)%2 == 1:  outData.append(i)
            return outData
        return read_file(filename)


    def load_hitSounds (self):
        normalSet   = ['default', 'normal', 'soft', 'drum']
        additionSet = ['normal', 'whistle', 'finish', 'clap']
        for i,j in [[i,j] for i in range(0,4) for j in range(0,4)]:                     # skin 폴더에서 해당하는 데이터를 읽어옵니다
            fileName = normalSet[i] + '-hit' + additionSet[j] + '.wav'
            try:    self.hitSounds[i][j][1] = pygame.mixer.Sound( "skin/"+fileName )
            except: pass
            for idx in range(2,20):
                fileName = normalSet[i] + '-hit' + additionSet[j] + str(idx) + '.wav'
                try: self.hitSounds[i][j][idx] = pygame.mixer.Sound( "skin/"+fileName )
                except: pass

        for i,j in [[i,j] for i in range(0,4) for j in range(0,4)]:                     # 비트맵 자체적인 데이터를 읽어옵니다.
            fileName = normalSet[i] + '-hit' + additionSet[j] + '.wav'
            try:    self.hitSounds[i][j][1] = pygame.mixer.Sound( py3d_data.songPath+"/"+fileName )
            except: pass
            for idx in range(2,20):
                fileName = normalSet[i] + '-hit' + additionSet[j] + str(idx) + '.wav'
                try: self.hitSounds[i][j][idx] = pygame.mixer.Sound( py3d_data.songPath+"/"+fileName )
                except: pass


    def play_song (self): #음악을 시작합니다.
        self.audio.set_volume( py3d_data.game_volumeHit )
        self.audio.play()


    def play_hitSounds (self,hitObject,timingPoint):
        def play_hitSounds_circle (hitObject,timingPoint):
            tpSet       = timingPoint.sampleSet
            tpIndex     = timingPoint.sampleIndex
            tpvolume    = timingPoint.volume
            normalSet   = hitObject.hitSample[0]
            additionSet = hitObject.hitSample[1]
            
            soundIndex  = hitObject.hitSample[2]
            if tpSet == 0: tpSet = 1
            if tpIndex == 0: tpIndex = 1
            if normalSet == 0: normalSet = tpSet
            if soundIndex == 0: soundIndex = tpIndex

            hitSounds_curr = [hitObject.hitSound[i] for i in range(len(hitObject.hitSound))]
            if  len(hitObject.hitSound) == 0: hitSounds_curr = [0]  # 옵션이 없을 경우에는 기본음 normal 으로 세팅합니다.
            
            sounds = [  # 타이밍 포인트에서 지정한 샘플, 출력 음, 음의 번호
                self.hitSounds[int(normalSet)][int(hitSounds_curr[i])][int(soundIndex)]                  
                for i in range(len(hitSounds_curr)) ]
            if sounds[0] == 0: sounds = [self.hitSounds[1][0][1]]           
            for i in range(len(sounds)):        
                try: 
                    sounds[i].set_volume( py3d_data.game_volumeHit )
                    sounds[i].play()
                except: pass 

            pygame.mixer.set_num_channels(10)
            #
            #
        def play_hitSounds_curve  (hitObject,timingPoint):
            tpSet       = timingPoint.sampleSet
            tpIndex     = timingPoint.sampleIndex
            
            edgeSounds = [] 
            for i in range(1):#len(hitObject.curve_edgeSounds)):
                normalSet       =  hitObject.curve_edgeSets[i][0]
                additionSet     =  hitObject.curve_edgeSets[i][1]
                sounds          = [hitObject.curve_edgeSounds[i][j] for j in range(len(hitObject.curve_edgeSounds[i]))]
                if normalSet == 0: normalSet = tpSet
                edgeSound =[self.hitSounds[int(normalSet)][int(sounds[j])][int(tpIndex)] 
                    for j in range(len(hitObject.curve_edgeSounds[i]))]
                if len(edgeSound) == 0 : edgeSound = [self.hitSounds[1][0][1]]  
                edgeSounds.extend(edgeSound)

            for i in range(len(edgeSounds)):        
                try: 
                    edgeSounds[i].set_volume(self.volume_hitSound)
                    edgeSounds[i].play()
                except: pass

        if hitObject.hitType == 'circle': play_hitSounds_circle(hitObject,timingPoint)
        if hitObject.hitType == 'curve':  play_hitSounds_curve (hitObject,timingPoint)
        if hitObject.hitType == 'spinner': pass
           
py3d_data.set_BeatmapData(BeatmapData()) 


#https://osu.ppy.sh/wiki/sk/osu!_File_Formats/Osu_%28file_format%29
#C:\Users\USER\AppData\Local\osu!


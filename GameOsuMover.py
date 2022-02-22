from ParserOsu import *
from GameMover3d  import *

class OsuMover:
    def __init__(self, hitObject, timingPoint):
        self.available      = False
        self.OsuDataH = hitObject
        self.OsuDataT = timingPoint
         
        global mover_spd, game_length
        self.game_length    = py3d_data.game_length
        self.speed          = py3d_data.game_mover_spd
        self.hitbox_size    = 10
        self.mover          = Mover3d (location = Vec3d( (self.OsuDataH.x-350)/10,(self.OsuDataH.y-200)/10+10,75))
        self.mover_goal     = Vec3d((self.OsuDataH.x-350)/20,  (self.OsuDataH.y-200)/20+10,  -self.game_length )
        self.mover_start    = self.mover.copy()
        self.mover.velocity = self.mover.location.copy().sub(self.mover_goal).norm().mlt(-self.speed)
        self.color_dist    = 1
        self.comboBreak = pygame.mixer.Sound( "skin/comboBreak.wav" )
        
    def update (self): 
        if self.mover.available == True: 
            self.chk_goal_point_reach()
            self.update_color_dist()
            self.mover.update() 

            
    def update_color_dist (self):
        dist1 = self.mover.location.copy().sub(self.mover_goal).mag()
        dist2 = self.mover_start.location.copy().sub(self.mover_goal).mag()
        self.color_dist = dist1/dist2

    def chk_collide (self, obj):
        dist = self.mover.location.copy().sub(obj.location).mag()
        if dist < self.hitbox_size:
            self.mover.available = False 
            obj.available = False
            self.play_hitSound()
            py3d_data.bgColor = np.array([
                py3d_data.bgColor[0]+self.mover.cnstC[0]//10+25,
                py3d_data.bgColor[1]+self.mover.cnstC[1]//10+25,
                py3d_data.bgColor[2]+self.mover.cnstC[2]//10+25])
            py3d_data.bgColor[py3d_data.bgColor>255] = 250

            if self.color_dist >0.5:
                self.comboBreak.set_volume (1)
                self.comboBreak.play()

    def chk_goal_point_reach (self):  
        dist1 = self.mover_start.location.copy().sub(self.mover.location).mag()
        dist2 = self.mover_start.location.copy().sub(self.mover_goal).mag()
        if dist1 > dist2: 
            self.mover.available = False
            self.play_hitSound()
            py3d_data.bgColor = np.array([
                py3d_data.bgColor[0]+self.mover.cnstC[0]//10+25,
                py3d_data.bgColor[1]+self.mover.cnstC[1]//10+25,
                py3d_data.bgColor[2]+self.mover.cnstC[2]//10+25])
            py3d_data.bgColor[py3d_data.bgColor>255] = 250
        
            #self.comboBreak.set_volume (1)
            #self.comboBreak.play()
            
            

    def play_hitSound (self):  
        global beatmap
        py3d_data.beatmap.play_hitSounds(self.OsuDataH, self.OsuDataT)
        
    def get_model (self): 
        if self.mover.available == True:  return self.mover.get_model(1-self.color_dist)
        else:  return [],[]





class MoverCircle:
    def __init__(self, hitObject, timingPoint):
        self.osuMover = OsuMover(hitObject, timingPoint)
        self.time = hitObject.time
        self.osuMover.mover.cnstC = np.array([150,50,50],float)
        self.osuMover.mover.randC = np.array([100,0,0],float)
    def update (self): self.osuMover.update()
    def get_model (self): return  self.osuMover.get_model()


class MoverSwipe:
    def __init__(self, hitObject, timingPoint):
        self.osuMover = OsuMover(hitObject, timingPoint)
        self.time = hitObject.time
        self.direction = None
        self.osuMover.mover.cnstC = np.array([50,150,50],float)
        self.osuMover.mover.randC = np.array([0,100,0],float)
    def update (self): self.osuMover.update()
    def get_model (self): return self.osuMover.get_model()


class MoverCurve:
    def __init__(self, hitObject, timingPoint):
        self.osuMoverS = OsuMover(hitObject, timingPoint)
        self.osuMoverE = OsuMover(hitObject, timingPoint) 
        self.osuMoverM = [  OsuMover(hitObject, timingPoint) for i in range(10)  ]
        self.time = hitObject.time
        self.osuMoverS.mover.cnstC = np.array([50,50,150],float)
        self.osuMoverS.mover.randC = np.array([0,0,100],float)
    
    def available (self):
        self.osuMoverE.mover.available = True
        self.osuMoverS.mover.available = True
        for i in range(10): self.osuMoverM[i].mover.available = True
    def update (self): 
        self.osuMoverS.update()
        #self.osuMoverE.update()
        #for i in range(10): self.osuMoverM[i].update()
    def get_model (self): return  self.osuMoverS.get_model()




    




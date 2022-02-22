from GameMover3d import *
from threading import Thread
from T3dData import *
from T3dUpdate import *
import serial
import time

class HandController:
    def __init__(self):
        #object mover
        
        cam.set_angle([0,0,0])
        self.angle       = np.array([0,0,0],float)
        self.location_normal = Vec3d(3,-0.5,2)
        self.location_aim    = Vec3d(0,-2,0)
        self.location    = self.location_normal
        self.endLocation = Vec3d(0,0,0)
        self.moverVec    = Vec3d(0,0,0)
        self.length      = 20
        
        #inner mover
        self.hit_movers  = []
        for i in range(10):
            mover = Mover3d()
            mover.location = Vec3d(0,self.length/10*i,0)
            self.hit_movers.append(mover)
        
        #serial
        self.click      = 0
        self.raw_data  = None
        self.runThread = False
        self.ser       = None
        #while self.ser == None: self.ser = serial.Serial('COM8',115200)
        #print("device reset start 3sec ")
        #self.ser.write('r'.encode())
        #while time.time()-t < 3:
        #    try: self.raw_data=self.ser.readline().decode('utf-8')
        #    except: pass
        #reset

        t = time.time()
        self.angle = np.array([0,0,0])
        cam.angle = np.array([0,0,0])
        print("device reset complete")

        self.sensitive = 1
        
        #model
        self.raw_model = get_cylinder( 2,self.length,5 )
        self.model_colors = [[50,50,200],[50,50,50]] 

        #bullet mover
        self.bullets = []
        self.bullet_speed = 15
        self.bullet_cool_time = 0.1
        self.bullet_last_create = time.time()
        self.bullet_model_raw = get_sphere(3 )
        self.model_bullet_colors = [[200,200,200],[50,50,50]] 

        self.gunshot = pygame.mixer.Sound( "gunshot.wav" )
        self.woR = 0
        self.woH = 0
        
    def create_bullet (self):
        mover = Mover3d()
        mover.available = True
        mover.location = self.endLocation.copy()
        mover.velocity = self.moverVec.copy().mlt(self.bullet_speed)
        self.bullets.append(mover)
        if len(self.bullets) == 20: del(self.bullets[0])

    def update (self):
        angle       = self.angle - cam.angle
        location = self.location.copy().sub_list(cam.location)
        self.moverVec = Vec3d(0,0,1).rotate3f([ angle[1]+90,-angle[0]+90,angle[2]])
        self.endLocation = location.copy().add( self.moverVec.copy().mlt(1.5) )
        if self.click == 1: self.create_bullet()
        self.update_bullet()         

    def update_bullet (self):
        for i in range(len(self.bullets)): 
            if self.bullets[i].available == True:   self.bullets[i].update()

    def get_model (self):
        models, colors = [],[]
        model = np.array(self.raw_model.copy())
        model = udt_s(model, [0.5,0.5,0.5])
        model = udt_a(model, self.angle.copy() - cam.angle.copy())
        model = udt_l(model, self.endLocation.toList())
        models.extend(model.tolist())
        colors.extend(get_tmp_color(self.model_colors[1],self.model_colors[0],model))
        return models, colors
    def get_model_bullet (self):
        models, colors = [],[]
        for i in range(len(self.bullets)):
            if self.bullets[i].available == True: 
                model = np.array(self.bullet_model_raw.copy())
                model = udt_s(model, [0.5,0.5,0.5])
                model = udt_l(model, self.bullets[i].location.toList())
                models.extend(model.tolist())
                colors.extend(get_tmp_color(
                    self.model_bullet_colors[1],
                    self.model_bullet_colors[0],model))
        return models, colors
            
    def run_thread (self):
        self.runThread = True
        self.thread = Thread(target=HandController.readThread, args=(self,))
        self.thread.setDaemon(True)
        self.thread.start()
    def readThread (self):
        self.angle = np.array([0,0,0])
        while self.run_thread:
            try:
                self.raw_data=self.ser.readline().decode('utf-8')
                self.parse_datas()
            except:pass
    def parse_datas (self):
        raw_datas = self.raw_data.split(' ')
        for i in range(len(raw_datas)):
            wr,wh = 0,0
            #if 'roll'  in raw_datas[i]: self.angle[2] = self.sensitive*+float(raw_datas[i].replace("roll",""))
            #if 'yaw'   in raw_datas[i]: self.angle[1] = self.sensitive* float(raw_datas[i].replace("yaw",""))
            if 'pitchR' in raw_datas[i]: self.angle[0] = self.sensitive*+float(raw_datas[i].replace("pitchR",""))
            if 'dyR'   in raw_datas[i]: wr = self.sensitive* float(raw_datas[i].replace("dyR",""))
            if wr!=0: # integra ya\
                print(raw_datas)
                self.angle[1] += wr
                self.angle[1] *= 0.999
                self.angle[1] += (wr-self.woR);
                self.woR = wr
            
            if 'pitchH' in raw_datas[i]: cam.angle[0] = -self.sensitive*+float(raw_datas[i].replace("pitchH",""))
            if 'dyH'   in raw_datas[i]: wh = self.sensitive* float(raw_datas[i].replace("dyH",""))
            if wh!=0: # integra yaw
                cam.angle[1] -= wh
                cam.angle[1] *= 0.999
                cam.angle[1] -= (wh-self.woH);
                self.woH = wh

            if 'btn' in raw_datas[i]:  self.click = int(raw_datas[i].replace("btn",""))
            if 'vry' in raw_datas[i]: 
                vry = int(raw_datas[i].replace("vry",""))
                if   vry == -1: self.angle[1] = 0
                elif vry ==  1: self.location = self.location_aim.copy()
                else :          self.location = self.location_normal.copy()

from Vec3d import *
from random import random
from T3dUpdate import *
from T3dObj import *

def get_tmp_color (randC, cnstC, model):
    return [  
        [ randC[0]*random() + cnstC[0], 
          randC[1]*random() + cnstC[1], 
          randC[2]*random() + cnstC[2] ] for i in range(len(model)//4)]

class Mover3d:
    def __init__(self, location = Vec3d(0,0,0),velocity = Vec3d(0,0,0), acceleration = Vec3d(0,0,0)):
        self.available = False
        self.location = location
        self.velocity = velocity
        self.acceleration = acceleration

        self.model_raw = get_sphere(5)
        self.size =     [3,3,3]
        self.rotate =   [1,1,1]
        self.randC = np.array([0,0,0])
        self.cnstC = np.array([255,0,0])

    def copy(self): return Mover3d(self.location.copy(), self.velocity.copy(), self.acceleration.copy() )

    def update (self):
        #self.update_edge()
        self.velocity.add(self.acceleration)
        self.location.add(self.velocity.copy().mlt(1/py3d_data.fps*30))

        self.acceleration.mlt(0)

    def update_edge (self):
        if (self.location.x<=-100)|(self.location.x>=100):  self.velocity.x = -self.velocity.x; self.location.x += self.velocity.x*2
        if (self.location.y<= 0  )|(self.location.y>=100):  self.velocity.y = -self.velocity.y; self.location.y += self.velocity.y*2
        if (self.location.z<=-100)|(self.location.z>=100):  self.velocity.z = -self.velocity.z; self.location.z += self.velocity.z*2
    
    def set_model ( self, model ): self.model_raw = model.copy()
    def get_model (self, colorDist = 1):
        model = udt_a(np.array(self.model_raw.copy()), self.rotate)
        model = udt_s(model, self.size)
        model = udt_l(model, self.location.toList())
        return model.tolist(), get_tmp_color(self.randC, self.cnstC*colorDist, model)


        

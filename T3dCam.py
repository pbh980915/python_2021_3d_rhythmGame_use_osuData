from T3dData import *

def rot (p,a): return (p[0]*c(a)-p[1]*s(a), p[0]*s(a)+p[1]*c(a))
def rad (a):   return np.pi*a/180
def s(a): return np.sin(rad(a))
def c(a): return np.cos(rad(a))
       

class Cam:
    def __init__(self):
        self.location = [0,0,0]
        self.angle = [0,0,0]
        self.key_a_status = False
        self.key_d_status = False
        self.key_w_status = False
        self.key_s_status = False
        self.key_q_status = False
        self.key_e_status = False
        self.speed = None
        self.mouse_btn = False
        self.mouse_btn_chg = False
        
    def set_location (self,data):   self.location   = np.array(data,float)
    def set_angle (self, data):     self.angle      = np.array(data,float)
    def update_mouse (self):
        mouse_position = pygame.mouse.get_pos()
        pygame.mouse.set_pos(py3d_data.w/2,py3d_data.h/2)
        add_angle = (np.array(mouse_position)-[py3d_data.w/2,py3d_data.h/2])/10
        self.angle = self.angle + [-add_angle[1], add_angle[0], 0]
        
    def update (self):
        spd,l,a = self.speed, self.location, self.angle
        if spd == None: self.speed = 1
        if self.key_a_status == True: self.location += [+spd*c(a[1]), 0, -spd*s(a[1])]
        if self.key_d_status == True: self.location += [-spd*c(a[1]), 0, +spd*s(a[1])]
        if self.key_w_status == True: self.location += [-spd*s(a[1]), 0, -spd*c(a[1])]
        if self.key_s_status == True: self.location += [+spd*s(a[1]), 0, +spd*c(a[1])]
        if self.key_q_status == True: self.location[1] += spd
        if self.key_e_status == True: self.location[1] -= spd
        
    def update_keyBoard (self, key, event_type):
        if event_type == 1:
            if key == pygame.K_a: self.key_a_status = True
            if key == pygame.K_d: self.key_d_status = True
            if key == pygame.K_w: self.key_w_status = True
            if key == pygame.K_s: self.key_s_status = True
            if key == pygame.K_q: self.key_q_status = True
            if key == pygame.K_e: self.key_e_status = True
            if key == pygame.K_z: py3d_data.running = False
        if event_type == 0:
            if key == pygame.K_a: self.key_a_status = False
            if key == pygame.K_d: self.key_d_status = False
            if key == pygame.K_w: self.key_w_status = False
            if key == pygame.K_s: self.key_s_status = False
            if key == pygame.K_q: self.key_q_status = False
            if key == pygame.K_e: self.key_e_status = False


def update_event ():
    for events in pygame.event.get():
        UP,DOWN = 0,1
        if events.type == pygame.QUIT:          py3d_data.running = False
        if events.type == pygame.MOUSEMOTION:   cam.update_mouse()
        if events.type == pygame.KEYDOWN:       cam.update_keyBoard(events.key,DOWN)
        if events.type == pygame.KEYUP:         cam.update_keyBoard(events.key,UP)
        if events.type == pygame.MOUSEBUTTONDOWN:  cam.mouse_btn = True
        if events.type == pygame.MOUSEBUTTONUP:    cam.mouse_btn = False; 
    cam.update()
cam = Cam()

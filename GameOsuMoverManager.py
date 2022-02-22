from GameOsuMover import *



class OsuMoverManager:
    def __init__(self, beatMapData):
        self.beatMapData  = beatMapData
        self.OsuDataH = self.beatMapData.hitObjects
        self.OsuDataT = self.beatMapData.timingPoints

        self.moverCircles = []; self.idxC = 0
        self.moverSwipes  = []; self.idxS = 0
        self.moverCurves  = []; self.idxV = 0
        self.set_movers ()

        self.hand_r = None
        self.timeStart    = -1
    
    def set_movers(self):
        t, idxT, idxH = 0,0,0
        while True:
            t += 1
            if t > self.OsuDataT[idxT].time:  
                idxT += 1
                if idxT >= len(self.OsuDataT): break
            if t > self.OsuDataH[idxH].time:
                idxH += 1
                if idxH >= len(self.OsuDataH): break
                if self.OsuDataH[idxH].hitType == 'circle': self.moverCircles.append(MoverCircle(self.OsuDataH[idxH],self.OsuDataT[idxT]))
                if self.OsuDataH[idxH].hitType == 'curve':
                    if self.OsuDataH[idxH].curve_type == 'L': self.moverSwipes.append(MoverSwipe(self.OsuDataH[idxH],self.OsuDataT[idxT]))
                    if self.OsuDataH[idxH].curve_type == 'B': self.moverCurves.append(MoverCurve(self.OsuDataH[idxH],self.OsuDataT[idxT]))
                    if self.OsuDataH[idxH].curve_type == 'P': self.moverCurves.append(MoverCurve(self.OsuDataH[idxH],self.OsuDataT[idxT]))
            if t%10000 == 0: print("current:",t,"loading goal:",self.OsuDataT[-1].time)
    
    def play_song (self):
        if self.timeStart == -1: 
            self.beatMapData.play_song()
            self.timeStart = time.time()
        t = (time.time() - self.timeStart + py3d_data.game_sync )*1000
        try:
            if (self.idxC<len(self.moverCircles))&(t > self.moverCircles[self.idxC].time): 
                self.moverCircles[self.idxC].osuMover.mover.available = True; self.idxC += 1;
            if (self.idxS<len(self.moverSwipes ))&(t > self.moverSwipes [self.idxS].time): 
                self.moverSwipes [self.idxS].osuMover.mover.available = True; self.idxS += 1; 
            if (self.idxV<len(self.moverCurves ))&(t > self.moverCurves [self.idxV].time): 
                self.moverCurves [self.idxV].available(); self.idxV += 1; 
        except: pass

    def update (self):
        update_event()  
        self.play_song()
        self.hand_r.update()
        if cam.mouse_btn == True:
            if self.hand_r.bullet_cool_time + self.hand_r.bullet_last_create < time.time():
                self.hand_r.create_bullet()
                self.hand_r.bullet_last_create = time.time()
            

        for i in range(len(self.moverCircles)): self.moverCircles[i].update ()
        for i in range(len(self.moverSwipes)):  self.moverSwipes [i].update ()
        for i in range(len(self.moverCurves)):  self.moverCurves [i].update ()
        for j in range(len(self.hand_r.bullets)):
            if self.hand_r.bullets[j].available == True:
                for i in range(len(self.moverCircles)): 
                    if self.moverCircles[i].osuMover.mover.available == True:
                        self.moverCircles[i].osuMover.chk_collide (self.hand_r.bullets[j])
                for i in range(len(self.moverSwipes)):  
                    if self.moverSwipes[i].osuMover.mover.available == True:
                        self.moverSwipes [i].osuMover.chk_collide (self.hand_r.bullets[j])
                for i in range(len(self.moverCurves)):  
                    if self.moverCurves[i].osuMoverS.mover.available == True:
                        self.moverCurves [i].osuMoverS.chk_collide (self.hand_r.bullets[j])


    def get_model (self):
        models, colors = [],[]
        for i in range(len(self.moverCircles)):  model,color = self.moverCircles[i].get_model (); models.extend(model); colors.extend(color)
        for i in range(len(self.moverSwipes)):   model,color = self.moverSwipes[i].get_model (); models.extend(model); colors.extend(color)
        for i in range(len(self.moverCurves)):   model,color = self.moverCurves[i].get_model (); models.extend(model); colors.extend(color)
        return models, colors




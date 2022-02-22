import pygame
import numpy as np
from random import randrange

pygame.init()
pygame.mixer.init()
class Py3d_data:
    def __init__(self):
        self.running = True
        self.w = 640
        self.h = 480
        pygame.mixer.init()

        self.screen_size = np.array([640,480])
        self.perspective = 300
        self.color_screen = (255,255,255)
        self.screen=pygame.display.set_mode((self.w,self.h))
        self.bgColor   = np.array([0,0,0],float)

        self.songPath = "osuMap/"
        self.songdif  = "extra.osu"
        self.beatmap = None
        
        self.game_mover_spd     = 10
        self.game_length        = 100
        self.game_sync          = 0.4
        self.game_volumeAudio   = 0.4
        self.game_volumeHit     = 1.0
        self.fps = 1
        
        #old var
        self.width = self.w
        self.height = self.h
    
    def set_BeatmapData(self,beatmapData):
        self.beatmap = beatmapData

py3d_data = Py3d_data()



#from cuda_simple_3d_base_update import *
from T3dUpdate import *
from T3dObj import *
from GameOsuMoverManager import *
from GameHandController import *

def get_floor_models ():
    global floor
    models, colors = [],[]
    for i,j in [[i,j] for i in range(-10,10) for j in range(-10,10)]:
        d = udt_s(floor.copy(), [1,0,1])
        d = udt_l(d, [i*10, py3d_data.bgColor.mean()/3-py3d_data.bgColor.mean()/1*random()-10, j*10])
        models.extend(d.tolist())

        if j < -12: colors.append([200,200,200])
        elif j < -8: colors.append([170,170,170])
        else : colors.append([128,128,128])
    return models, colors

def set_models ():
    models, colors = [],[]
    model, color = get_floor_models(); models.extend(model); colors.extend(color)
    model, color = game.get_model(); models.extend(model); colors.extend(color)
    model, color = hand_r.get_model(); models.extend(model); colors.extend(color)
    model, color = hand_r.get_model_bullet(); models.extend(model); colors.extend(color)
    models, colors = np.array(models), np.array(colors)
    return models, colors

pygame.mouse.set_pos(py3d_data.w/2,py3d_data.h/2)
hand_r = HandController()
#hand_r.run_thread()


mlt = 2
py3d_data.game_mover_spd     = 10/mlt
py3d_data.game_length        = 120
py3d_data.game_sync          = 0.6*mlt
py3d_data.game_volumeAudio   = 0.3
py3d_data.game_volumeHit     = 1
game = OsuMoverManager(py3d_data.beatmap)
game.hand_r = hand_r

clock = pygame.time.Clock()
cam.set_location([5,-10,130])
cam.set_angle([0,0,0])
cam.speed = 3



bg = pygame.image.load(py3d_data.songPath+"bg.jpg").convert_alpha()
bg = pygame.transform.scale(bg, (py3d_data.w, py3d_data.h))
def main():
    global bgColor, fps
    welcome = pygame.mixer.Sound( "skin/welcome.wav" )
    welcome.set_volume (1)
    welcome.play()
    bg.set_alpha(40)
    while py3d_data.running:
        t = time.time()

        game.update()
        models, colors = set_models()
             
        models = udt_l(models,cam.location)
        models = udt_a(models,cam.angle)

        py3d_data.screen.fill(py3d_data.bgColor)
        py3d_data.screen.blit(bg,(0,0))
        process(models, colors)

        pygame.display.flip()
        clock.tick(60)

        py3d_data.fps = 1/(time.time()-t)
        py3d_data.bgColor *= 0.85
main()
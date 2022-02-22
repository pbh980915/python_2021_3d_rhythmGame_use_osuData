from T3dCam import *


def udt_a (pos,angle):
    pos = pos.copy()
    pos[:,0],pos[:,2] = rot([pos[:,0],pos[:,2]],angle[1])
    pos[:,1],pos[:,2] = rot([pos[:,1],pos[:,2]],angle[0])
    pos[:,0],pos[:,1] = rot([pos[:,0],pos[:,1]],angle[2])
    return pos
def udt_l (pos,location): return pos + location
def udt_s (pos,size):     return pos * size



import time

def process (pos, color):
    def get_depth (pos):
        return np.sqrt(pos[:,2]**2)

    def get_screenCoord (pos):
        z = py3d_data.perspective/pos[:,2]
        newCoord = np.zeros(np.shape(pos[:,:2]))
        newCoord[:,0] = z*pos[:,0]+py3d_data.width/2
        newCoord[:,1] = z*pos[:,1]+py3d_data.height/2
        return newCoord

    def get_rect_depth(pos):
        depth = np.array(get_depth(pos))
        return depth.reshape(int(depth.shape[0]/4),4).mean(1)

    def get_rect_coord(pos):
        coordPos = get_screenCoord(pos)
        return coordPos.reshape((int(coordPos.shape[0]/4),8))

    def delete_dump_data (rect_coord, rect_depth,color):
        rect_depth.sort()
        w,h,rc = py3d_data.w, py3d_data.h, rect_coord
        color = np.delete(color, np.where((rect_depth < 0))[0], axis=0)
        rc    =    np.delete(rc, np.where((rect_depth < 0))[0], axis=0)
        color = np.delete(color, np.where((rc[:,[0,2,4,6]]>=w+200)|(rc[:,[0,2,4,6]]<=-200))[0], axis=0) 
        rc    =    np.delete(rc, np.where((rc[:,[0,2,4,6]]>=w+200)|(rc[:,[0,2,4,6]]<=-200))[0], axis=0) 
        color = np.delete(color, np.where((rc[:,[1,3,5,7]]>=h+200)|(rc[:,[1,3,5,7]]<=-200))[0], axis=0)
        rc    =    np.delete(rc, np.where((rc[:,[1,3,5,7]]>=h+200)|(rc[:,[1,3,5,7]]<=-200))[0], axis=0)
        
        return rc,color
    
    def draw (rect_coord, color):
        for i in range(len(rect_coord)): #reshape -> x,y
            if np.isnan(rect_coord[i]).sum() == 0:
                pygame.draw.polygon(py3d_data.screen, color[i], rect_coord[i].reshape((4,2)))

    pos[:,1] = -pos[:,1]
    pos[pos[:,2]<0] = np.NaN
    rect_depth = get_rect_depth(pos)
    rect_coord = get_rect_coord(pos)
    rect_coord = rect_coord[rect_depth.argsort()[::-1]]
    color      = color     [rect_depth.argsort()[::-1]]
    rect_coord,color = delete_dump_data (rect_coord, rect_depth,color)
    draw (rect_coord, color)






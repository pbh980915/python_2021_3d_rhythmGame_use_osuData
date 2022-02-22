import numpy as np
from random import random
def load_obj (filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    
    vs,ts,fs = [],[],[]
    fvs, fts = [], []
    for line in lines:
        data = line.split(' ')
        if data[0] =='vt': ts.append(data)
        if data[0] =='v' : vs.append(data)
        if data[0] =='f' : fs.append(data)

    for i in range(len(vs)): vs[i] = [float(vs[i][1]),float(vs[i][2]),float(vs[i][3])]
    for i in range(len(ts)): ts[i] = [float(ts[i][1]),float(ts[i][2]),float(ts[i][3])]
    for i in range(len(fs)):
        fs[i] = [fs[i][1].split('/'),fs[i][2].split('/'),fs[i][3].split('/')]
        fvs.append([int(fs[i][0][0])-1,int(fs[i][1][0])-1, int(fs[i][2][0])-1,int(fs[i][2][0])-1])
        fts.append([int(fs[i][0][1])-1,int(fs[i][1][1])-1, int(fs[i][2][1])-1,int(fs[i][2][1])-1])
    print(len(vs),len(ts),len(fs))
    return vs,ts,fvs,fts



def get_cylinder (radius=10, length=10, size=10):
    models = []; colors = []
    for z,a in [[z,a] for z in range(1,size+2) for a in range(1,size+2)]:
        p1 = [c(360/size*(a-1)) * radius, s(360/size*(a-1)) * radius,  length/size*(z-1) ]
        p2 = [c(360/size*(a-0)) * radius, s(360/size*(a-0)) * radius, length/size*(z-1) ]
        p3 = [c(360/size*(a-1)) * radius, s(360/size*(a-1)) * radius, length/size*(z-0) ]
        p4 = [c(360/size*(a-0)) * radius, s(360/size*(a-0)) * radius, length/size*(z-0) ]
        models.extend([p1,p2,p3,p4])
    return models#, colors

def c(a): return np.cos(a*np.pi/180)
def s(a): return np.sin(a*np.pi/180)
def get_sphere (n=10):
    models,colors = [],[]
    d = int(360/n)
    for i,j in [[i,j] for i in range(n) for j in range(n)]:
        p1 = [c((i+0)*d), c((j+0)*d)*s((i+0)*d), s((j+0)*d)*s((i+0)*d)]
        p2 = [c((i+1)*d), c((j+0)*d)*s((i+1)*d), s((j+0)*d)*s((i+1)*d)]
        p3 = [c((i+1)*d), c((j+1)*d)*s((i+1)*d), s((j+1)*d)*s((i+1)*d)]
        p4 = [c((i+0)*d), c((j+1)*d)*s((i+0)*d), s((j+1)*d)*s((i+0)*d)]
        models.extend([p1,p2,p3,p4])
    return models#,colors
model_sphere = get_sphere(10)        

floor = np.array([[ 1, 1, 1], [ 1, 1,-1], [-1, 1,-1], [-1, 1, 1]],float)
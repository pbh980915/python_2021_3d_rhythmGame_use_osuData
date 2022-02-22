import numpy as np

def rad(a): return np.pi*a/180
class Vec3d:
    def __init__(self,x,y,z): self.x = x; self.y = y; self.z = z
    def set_list(self,l): self.x = l[0]; self.y = l[1]; self.z = l[2]
    def copy (self): return Vec3d(  self.x, self.y, self.z)
    def add (self, n): self.x += n.x; self.y += n.y; self.z += n.z; return self
    def sub (self, n): self.x -= n.x; self.y -= n.y; self.z -= n.z; return self
    def mlt (self, n): self.x *= n; self.y *= n; self.z *= n; return self
    def add_list (self, n): self.x += n[0]; self.y += n[1]; self.z += n[2]; return self
    def sub_list (self, n): self.x -= n[0]; self.y -= n[1]; self.z -= n[2]; return self
    def mag (self): return np.sqrt( self.x**2 + self.y**2 + self.z**2 )
    def norm(self): return self.mlt(1/self.mag())

    def rotate3f (self, a):
        self.y, self.z = (
            self.y*np.sin(rad(a[0])) - self.z*np.cos(rad(a[0])),  
            self.y*np.cos(rad(a[0])) + self.z*np.sin(rad(a[0])))
        self.x, self.z = (
            self.x*np.sin(rad(a[1])) - self.z*np.cos(rad(a[1])),  
            self.x*np.cos(rad(a[1])) + self.z*np.sin(rad(a[1])))
        self.x, self.y = (
            self.x*np.sin(rad(a[2])) - self.y*np.cos(rad(a[2])),  
            self.x*np.cos(rad(a[2])) + self.y*np.sin(rad(a[2])))
        return self

    def toList (self): return [self.x, self.y, self.z]
    def toArray (self): return np.array(self.toList())
import numpy as np
import math
import random

def randvector(length=1):
    #not used - gives a random normalised (or set length) vector in 3d
    x = random.uniform(-1,1)
    y = random.uniform(-1,1)
    z = random.uniform(-1,1)
    vector = np.array([x,y,z])
    mag = np.linalg.norm(vector)
    vector = vector/mag
    vector = vector*bond
    return vector

def randrotationMatrix():
    #gives a random 3d rotation
    #according to people on the internet this is not truly randomising
    yaw = random.uniform(0,360)
    pitch = random.uniform(0,360)
    roll = random.uniform(0,360)
    r = np.matmul(yrotation(pitch),zrotation(roll))
    r = np.matmul(xrotation(yaw),r)
    return r

def zrotation(angle):
    #gives a 3d rotation about the z axis - works with degrees
    angle = math.radians(angle)
    r = np.array([[math.cos(angle),-1*math.sin(angle),0],[math.sin(angle),math.cos(angle),0],[0,0,1]])
    return r

def yrotation(angle):
    #gives a 3d rotation about the y axis - works with degrees
    angle = math.radians(angle)
    r = np.array([[math.cos(angle),0,math.sin(angle)],[0,1,0],[-1*math.sin(angle),0,math.cos(angle)]])
    return r

def xrotation(angle):
    #gives a 3d rotation about the x axis - works with degrees
    angle = math.radians(angle)
    r = np.array([[1,0,0],[0,math.cos(angle),-1*math.sin(angle)],[0,math.sin(angle),math.cos(angle)]])
    return r

def tetrahedron(bondlength):
    #gives 4 vectors from the center of a tetrahedron to the vertices from a given "radius"
    v1 = np.array([[bondlength*math.cos(math.radians(19.5))],[0],[bondlength*math.sin(math.radians(19.5))]])
    v2 = np.matmul(zrotation(109.5),v1)
    v3 = np.matmul(zrotation(109.5),v2)
    v4 = np.matmul(yrotation(109.5),v1)
    return[v1,v2,v3,v4]

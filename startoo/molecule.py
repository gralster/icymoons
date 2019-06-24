import numpy as np
import threed
import random
from atom import Atom

class Molecule():
    def __init__(self,pos):
        self.pos = pos
        self.hydrogen = []
        self.bondlength = 1
        self.central = Atom(self.pos,"carbon")
        self.size = 1
        self.bonds = 0
        self.placehydrogen()

    def placehydrogen(self):
        self.bonds = threed.tetrahedron(self.bondlength)[0:self.size]
        for vector in self.bonds:
            self.hydrogen.append(Atom(self.pos+vector,"hydrogen"))

    def getpos(self):
        return self.pos

    def gethydrogen(self):
        positions = []
        for each in self.hydrogen:
            positions.append(each.pos)
        return positions

    def spin(self):
        rotation = threed.randrotationMatrix()
        for i in range(len(self.bonds)):
            self.bonds[i] = np.matmul(rotation,self.bonds[i])
            self.hydrogen[i].pos = self.pos+self.bonds[i]

    def getmass(self):
        total = 0
        for atom in self.hydrogen:
            total = total + atom.getmass()
        total = total + self.central.getmass()
        return total

class Water(Molecule):
    def __init__(self,pos):
        self.pos = pos
        self.hydrogen = []
        self.bondlength = 0.98
        self.size = 2
        self.central = Atom(self.pos,"oxygen")
        self.bonds = 0
        self.placehydrogen()

class Methane(Molecule):
    def __init__(self,pos):
        self.pos = pos
        self.hydrogen = []
        self.bondlength = 1.09
        self.size = 4
        self.central = Atom(self.pos,"carbon")
        self.bonds = 0
        self.placehydrogen()

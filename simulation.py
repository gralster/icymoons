
import numpy as np
import matplotlib.pyplot as plt
from box import Frame
from atom import Atom


class Simulation():

    def __init__(self):
      self.frames = []
      self.steps = 0
      self.natoms=0

    def readxyz(self,filename):
        file = open(filename + ".xyz", "r")
        contents = file.readlines()
        n = int(contents[0])
        self.natoms = n
        contents = [i.split() for i in contents if len(i) > 1]
        self.steps = int(len(contents)/(n+2))
        for j in range(self.steps):
            self.frames.append(Frame(10))
            for i in range(self.natoms):
                if len(contents[i])>1:
                    self.frames[j].atoms.append(Atom(np.array(contents[i+(j*self.natoms)][1:]).astype(float),str(contents[i][0])))
            #print (len(self.frames[j].atoms))

            '''
        for j in range(self.steps):
            self.frames.append(Frame(10))
            for i in range(self.natoms):
                if len(contents[i])>1:
                    #index = i%n
                    #print(index)
                    self.frames[j].atoms.append(Atom(np.array(contents[i][1:]).astype(float),str(contents[i][0])))
                    #atoms[index].append(contents[i][1:])
                    print(len(self.frames[index].atoms))
                else:
                    pass
                    '''

    def meansqrdisp(self):
        msds = []
        for i in range(self.steps):
            d=[]
            #print("!!!!!!!!!!!!!") ~~~~~~~~~~~HAY MUCHOS PROBLEMAS

            print(i)
            for j in range(self.natoms-2):
                #print(self.natoms)
                print(len(self.frames[i].atoms))
                d.append(np.linalg.norm(self.frames[i].atoms[j].pos - self.frames[0].atoms[j].pos))

                #print(j)
            sd = list(map(lambda x: x**2, d))
            sumsd = sum(sd)
            normedsum = sumsd/len(sd)
            msds.append(normedsum)
        times = [i for i in range(self.steps)]
        plt.plot(times,msds)
        plt.show()
        return msds

    def gofrmom(self):
        d=[]
        for i in range(len(self.natoms)):
            d.append(ruler(atoms[i][step],atoms[atom][step]))
        return d

    def gofrav(atom,atoms,steps):
    #not normalised
        ds = []
        for j in range(steps):
            d=[]
            for i in range(len(atoms)):
                d.append(ruler(atoms[atom][j],atoms[i][j]))
            d = np.array(d)
            ds.append(d)
        sumds = sum(ds)
        avsum = np.array(sumds)/steps
        return avsum

import numpy as np
import threed
import random

from atom import Atom
from molecule import Molecule, Methane, Water, TestHole

class Frame():
    def __init__(self, dimensions, atoms = []):
        self.molecules = []
        self.atoms = []
        self.positions = []
        self.dim = dimensions

    def fccposition(self):
        #face centered cubic
        p1 = np.array([[0],[0],[0]])
        p2 = np.array([[0.5*self.dim],[0.5*self.dim],[0]])
        p3 = np.array([[0.5*self.dim],[0],[0.5*self.dim]])
        p4 = np.array([[0],[0.5*self.dim],[0.5*self.dim]])
        self.positions = np.array([p1,p2,p3,p4])

    def bccposition(self):
        #body centered cubic
        p1 = np.array([[0],[0],[0]])
        p2 = np.array([[0.5*self.dim],[0.5*self.dim],[0.5*self.dim]])
        self.positions =  np.array([p1,p2])

    def randposition(self,n = 3):
        ps = []
        for i in range(n):
            x = random.uniform(0,self.dim)
            y = random.uniform(0,self.dim)
            z = random.uniform(0,self.dim)
            ps.append(np.array([[x],[y],[z]]))
        self.positions = np.array(ps)

    def fill(self,proportion=0.5,holes=0):
        np.random.shuffle(self.positions)
        nmethane = round(proportion*(len(self.positions)-holes))
        print ("Methane Molecules: "+ str(nmethane))
        for i in range(nmethane):
            self.molecules.append(Methane(self.positions[i]))
        print(len(self.positions)-nmethane-holes)
        for j in range(len(self.positions)-nmethane-holes):
            self.molecules.append(Water(self.positions[nmethane+j]))
        #for k in range(holes):
        #    self.molecules.append(TestHole(self.positions[len(self.positions)-holes +k]))

    def superpose(self,other):
        self.positions = self.positions + other.positions
        self.molecules = self.molecules + other.molecules

    def tesselate(self,length):
        xtranslations = []
        ytranslations = []
        ztranslations = []
        translations = []
        for i in range(length):
            xtranslations.append(np.array([[self.dim*i],[0],[0]]))
            ytranslations.append(np.array([[0],[self.dim*i],[0]]))
            ztranslations.append(np.array([[0],[0],[self.dim*i]]))
        for x in xtranslations:
            for y in ytranslations:
                for z in ztranslations:
                    t = np.array([[0],[0],[0]])
                    t = np.add(t,x)
                    t = np.add(t,y)
                    t = np.add(t,z)
                    translations.append(t)
        newpos = []
        for p in self.positions:
            for t in translations:
                newpos.append(np.add(p,t))
        self.positions = newpos
        self.dim = length*self.dim

    def shake(self):
        for molecule in self.molecules:
            molecule.spin()

    def getmolpos(self):
        centralpos = []
        hydrogenpos = []
        for molecule in self.molecules:
            centralpos.append(molecule.getpos())
            hydrogenpos.append(molecule.gethydrogen())
        return [centralpos,hydrogenpos]

    def ruler(self,index1,index2):
        diff = self.atoms[index1].pos-self.atoms[index2].pos
        return np.linalg.norm(diff)

    def gettotalmass(self):
        totalmass = 0
        for molecule in self.molecules:
            totalmass = totalmass + molecule.getmass()
        for atom in self.atoms:
            totalmass = totalmass + atom.getmass()
        return totalmass

    def getdim(self,density):
        mass = self.gettotalmass()
        len = np.cbrt(mass/density)/3
        return len

    def getdensity(self):
        totalmass = self.gettotalmass()
        volume = self.dim**3
        return totalmass/volume

    def writecellfile(self,name):
        filename = name
        file = open(filename + ".cell", "w")

        file.write("%BLOCK lattice_cart")
        file.write("\n")
        file.write(str(self.dim) + "   0   0")
        file.write("\n")
        file.write("0   " + str(self.dim) + "   0")
        file.write("\n")
        file.write("0   0   "+ str(self.dim))
        file.write("\n")
        file.write("%ENDBLOCK lattice_cart")
        file.write("\n\n")

        file.write("%BLOCK positions_frac")
        file.write("\n")
        for molecule in self.molecules:
            for hydrogen in molecule.hydrogen:
                file.write(hydrogen.name)
                file.write("   ")
                for dimension in hydrogen.pos:
                    file.write(str(dimension[0]/self.dim))
                    file.write("   ")
                file.write("\n")
            file.write(molecule.central.name)
            file.write("   ")
            for dimension in molecule.central.pos:
                file.write(str(dimension[0]/self.dim))
                file.write("   ")
            file.write("\n")
        file.write("%ENDBLOCK positions_frac")
        file.write("\n\n")
        file.close()

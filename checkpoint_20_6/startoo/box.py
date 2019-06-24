import numpy as np
import threed
import random

from molecule import Molecule, Methane, Water

class Box():
    def __init__(self, dimensions, molecules = []):
        self.molecules = molecules
        self.dim = dimensions

    def fccposition(self):
        #face centered cubic
        p1 = np.array([[0],[0],[0]])
        p2 = np.array([[0.5*self.dim],[0.5*self.dim],[0]])
        p3 = np.array([[0.5*self.dim],[0],[0.5*self.dim]])
        p4 = np.array([[0],[0.5*self.dim],[0.5*self.dim]])
        return np.array([p1,p2,p3,p4])

    def bccposition(self):
        #body centered cubic
        p1 = np.array([[0],[0],[0]])
        p2 = np.array([[0.5*self.dim],[0.5*self.dim],[0.5*self.dim]])
        return np.array([p1,p2])

    def randposition(self,n = 3):
        ps = []
        for i in range(n):
            x = random.uniform(0,self.dim)
            y = random.uniform(0,self.dim)
            z = random.uniform(0,self.dim)
            ps.append(np.array([[x],[y],[z]]))
        return np.array(ps)

    def fill(self,proportion=0.5,arrangement="4"):
        if arrangement == "FCC":
            places = self.fccposition()
        elif arrangement == "BCC":
            places = self.bccposition()
        else:
            n = int(arrangement)
            places = self.randposition(n)
        nmethane = round(proportion*len(places))
        for i in range(nmethane):
            self.molecules.append(Methane(places[i]))
        for j in range(len(places)-nmethane):
            self.molecules.append(Water(places[nmethane+j]))

    def superpose(self,other):
        self.molecules = self.molecules + other.molecules

    #def add(self,other,direction):
    #    distance = self.dim
    #    for i in range(len(other.molecules)):
    #    #for molecule in other.molecules:
    #        other.molecules[i].pos = threed.translation(other.molecules[i].pos,distance,direction)
    #        other.molecules[i].hydrogen = []
    #        other.molecules[i].placehydrogen()
    #    return Box(self.molecules + other.molecules)

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

    def getdensity(self):
        totalmass = 0
        for molecule in self.molecules:
            totalmass = totalmass + molecule.getmass()
        volume = self.dim**3
        return totalmass/volume

    def writecellfile(self):
        filename = "castep"
        file = open(filename + ".cell", "w")
        file.write("%BLOCK positions_frac")
        file.write("\n")
        for molecule in self.molecules:
            for hydrogen in molecule.hydrogen:
                file.write(hydrogen.name)
                file.write("   ")
                for dimension in hydrogen.pos:
                    file.write(str(dimension[0]))
                    file.write("   ")
                file.write("\n")
            file.write(molecule.central.name)
            file.write("   ")
            for dimension in molecule.central.pos:
                file.write(str(dimension[0]))
                file.write("   ")
            file.write("\n")
        file.write("%ENDBLOCK positions_frac")
        file.write("\n\n")
        file.close()

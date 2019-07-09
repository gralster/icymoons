import numpy as np
import random
import math
import sys

#################################################################################
#THIS WHOLE PROGRAM WORKS WITH DEGREES!!! NOT RADIANS
#################################################################################
#hardcoded parameters

#units of angstroms
chBondLength = 1.09
ohBondLength = 0.98
boxDim = 6
#boxDim = 100000 #"diameter" for FCC gives density = 1 kg/m^3
#units of kgs
u = 1.66054*(10**(-27))
cmass = 12.107*u
hmass = 1.00784*u
#kpoints = sys.argv[1]
#pressure = sys.argv[2]

###############################################################################
#positioning molecules in different ways

def fccposition(atomtype):
    #face centered cubic
    atomtype.append(np.array([[0],[0],[0]]))
    atomtype.append(np.array([[0.5*boxDim],[0.5*boxDim],[0]]))
    atomtype.append(np.array([[0.5*boxDim],[0],[0.5*boxDim]]))
    atomtype.append(np.array([[0],[0.5*boxDim],[0.5*boxDim]]))

def bccposition(atomtype):
    #body centered cubic
    atomtype.append(np.array([[0],[0],[0]]))
    atomtype.append(np.array([[0.5*boxDim],[0.5*boxDim],[0.5*boxDim]]))

def randposition(atomtype):
    #random positions
    #buffer = max(chBondLength,ohBondLength)
    x = random.uniform(0,boxDim)
    y = random.uniform(0,boxDim)
    z = random.uniform(0,boxDim)
    atomtype.append(np.array([[x],[y],[z]]))

################################################################################
#some 3d geometry stuff

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

#################################################################################
#addition of hydrogen around the central atom of the molecule

def placenHydrogen(holder,centralpos,n,bond,aligned):
    #returns a list of hydrogen positions for a tetragonal molecule given
    #position of central molecule, number of hydrogen wanted and bond length
    #can be randomly oriented
    vectors = tetrahedron(bond)
    if aligned == False:
        spin = randrotationMatrix()
        for i in range(len(vectors)):
            vectors[i] = np.matmul(spin,vectors[i])
    else:
        pass
    for i in range(n):
        pos = centralpos + vectors[i]
        holder.append(pos)

#################################################################################
#file writing
#oh my god this is embarrassing

def writeout(atoms,names):
    filename = "castep"
    file = open(filename + ".cell", "w")

    file.write("%BLOCK lattice_cart")
    file.write("\n")
    file.write(str(boxDim) + "   0   0")
    file.write("\n")
    file.write("0   " + str(boxDim) + "   0")
    file.write("\n")
    file.write("0   0   "+ str(boxDim))
    file.write("\n")
    file.write("%ENDBLOCK lattice_cart")
    file.write("\n\n")

    file.write("%BLOCK positions_frac")
    file.write("\n")
    for i in range(len(atoms)):
        for j in range(len(atoms[i])):
            for k in range(len(atoms[i][j])):
                file.write(names[i])
                file.write("   ")
                for u in range(len(atoms[i][j][k])):
                    for o in range(len(atoms[i][j][k][u])):
                        file.write(str(atoms[i][j][k][u][o]))
                        file.write("   ")
                file.write("\n")
    file.write("%ENDBLOCK positions_frac")
    file.write("\n\n")

    file.close()

def writesettings(ncentral):
    file = open("settings.txt","w")
    file.write("chBondLength = " + str(chBondLength))
    file.write("\n")
    file.write("ohBondLength = " + str(ohBondLength))
    file.write("\n")
    file.write("boxDim = " + str(boxDim))
    file.write("\n")
    #file.write("pressure = " + str(pressure))
    #file.write("\n")
    #file.write("kpoints = " + str(kpoints))
    #file.write("\n")
    file.write("number of molecules = " + str(ncentral))
    file.write("\n")
    file.close()

#################################################################################
#error and sense checking etc

def ruler(one,others):
    #prints distance between one atom and others
    for i in range(len(others)):
        bond = one-others[i]
        print(np.linalg.norm(bond))

def getdensity(ncarbon, nhydrogen):
    #BUT WITHOUT THE BUFFER THIS IS A BIT IFFY?? ESP for random placements
    #returns the density of the box
    mass = ncarbon*cmass + nhydrogen*hmass
    volume = (boxDim*(10**(-10))**3)
    return(mass/volume)

#################################################################################
def main():

    #these will be 2d lists of coordinates of each type of atom
    oxygen = []
    carbon = []
    hydrogen = []

    #user input for alignement
    #orientation = input("Would you like the molecules to be randomly oriented? (y/n)")
    #if orientation == "y":
    #    aligned = False
    #else:
    #    aligned = True

    #user input for presets
    aligned = False
    #runtype = input("Please type 'FCC' for face centered cubic, 'BCC' for body centered cubic, or and integer number of molecules for random placement:")
    runtype = "BCC"
    if runtype == "FCC":
        ncarbon = 4
        fccposition(carbon)
        for c in carbon:
            placenHydrogen(hydrogen,c,4,chBondLength,aligned)

    elif runtype == "BCC":
        ncarbon = 2
        bccposition(carbon)
        for c in carbon:
            placenHydrogen(hydrogen,c,4,chBondLength,aligned)
    else:
        ncarbon = int(runtype)
        for i in range(ncarbon):
            randposition(carbon)
        for c in carbon:
            placenHydrogen(hydrogen,c,4,chBondLength,aligned)

    #check bond length is correct
    #ruler(carbon[1],carbon[0:4])

    #scale to fractional positions
    carbon = (np.array(carbon))/boxDim
    hydrogen = (np.array(hydrogen))/boxDim
    ncarbon = len(carbon)
    nhydrogen = len(hydrogen)
    #writearray([[carbon],[hydrogen]])
    writeout([[carbon],[hydrogen]],["C","H"])
    #print(getdensity(len(carbon),len(hydrogen)))
    writesettings(ncarbon)
main()

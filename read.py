import numpy as np
import matplotlib.pyplot as plt
import subprocess

def readxyz(filename,datatype):
    file = open(filename + ".xyz", "r")
    contents = file.readlines()
    n = int(contents[0])
    print(n)
    contents = [i.split() for i in contents if len(i) > 1]
    atoms = []
    names = []
    for j in range(n):
        atoms.append([])
        names.append(contents[j+2][0])
    for i in range(len(contents)):
        if len(contents[i])>1:
            index = i%n
            atoms[index].append(contents[i][1:])
        else:
            pass
    atoms = np.array(atoms)
    atoms = atoms.astype(datatype)
    stepsn = len(atoms[0])
    return atoms,stepsn,n,names

def readtxt(filename,datatype):
    file = open(filename + ".txt","r")
    contents = file.readlines()
    file.close()
    for i in range(len(contents)):
        contents[i] = contents[i][:-1] # to remove the new line "\n" symbol
    return np.array(contents).astype(datatype)

def breakfields(lines, delimiter):
    contents = []
    for i in lines:
        contents.append(i.split(delimiter))
    return contents


def ruler(pos1,pos2):
    diff = np.array(pos1)-np.array(pos2)
    return np.linalg.norm(diff)

def meansqrdisp(atoms,steps,n):
    msds = []
    for i in range(steps):
        d = []
        for j in range(len(atoms)):
            #rint(np.array(atoms[j][i]))
            d.append(ruler(atoms[j][i],atoms[j][0]))
        sd = list(map(lambda x: x**2, d))
        sumsd = sum(sd)
        normedsum = sumsd/len(sd)
        msds.append(normedsum)
    return(msds)

def gofrmom(atom,atoms,step):
    d=[]
    for i in range(len(atoms)):
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

def findx(y,xs,ys):
    #uses scipys interpolation function to give x given y
    interpolation = interp1d(ys,xs)
    return interpolation(y)

def findy(x,xs,ys):
    #uses scipys interpolation function to give y given x
    interpolation = interp1d(xs,ys)
    return interpolation(x)

def plot(xs,ys):
    plt.plot(xs,ys)
    plt.xlabel(str((input("x label: "))))
    plt.ylabel(str((input("y label: "))))
    plt.show()

def plothist(xs):
    plt.hist(xs,bins=50)
    plt.xlabel(str((input("x label: "))))
    plt.show()

def main():
    atom = 3
    atoms,steps,n,names = readxyz("castep",float)
    
    msds = meansqrdisp(atoms,steps,n)
    times = [i for i in range(steps)]
    plt.plot(times,msds)
    plt.show()

    distribution = gofrav(6,atoms,steps)
    plt.hist(distribution,bins = 50)
    plt.show()


main()

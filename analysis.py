import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def readtxtfile(filename,datatype):
    file = open(filename + ".txt","r")
    contents = file.readlines()
    file.close()
    for i in range(len(contents)):
        contents[i] = contents[i][:-1] # to remove the new line "\n" symbol
    return np.array(contents).astype(datatype)

def readxyzfile(filename,datatype):
    file = open(filename + ".xyz", "r")
    contents = file.readlines()
    n = int(contents[0])
    contents = [i.split() for i in contents if len(i) > 1]
    atoms = []
    for j in range(n):
        atoms.append([])
    for i in range(len(contents)):
        if len(contents[i])>1:
            index = i%n
            atoms[index].append(contents[i][1:])
        else:
            pass
    atoms = np.array(atoms)
    atoms = atoms.astype(datatype)
    stepsn = len(atoms[0])
    return atoms,stepsn,n

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

def breakfields(lines, delimiter):
    contents = []
    for i in lines:
        contents.append(i.split(delimiter))
    return contents

def plot(xs,ys):
    plt.plot(xs,ys)
    plt.xlabel(str((input("x label: "))))
    plt.ylabel(str((input("y label: "))))
    plt.show()

def findx(y,xs,ys):
    #uses scipys interpolation function to give x given y
    interpolation = interp1d(ys,xs)
    return interpolation(y)

def findy(x,xs,ys):
    #uses scipys interpolation function to give y given x
    interpolation = interp1d(xs,ys)
    return interpolation(x)

def permolecule():
    pass

def normalise():
    pass

def main():
    filepath = str(input("data file path: "))

    yname = str(input("Name of data file: "))
    xname = str(input("Name of own data file: "))
    ydata = readtxtfile(filepath + yname,float)
    xdata = readtxtfile(filepath + xname,float)

    #times = readtxtfile(filepath + "time",float)
    #settings = readtxtfile(filepath + "settings","txt")
    #settings = breakfields(settings,"=")
    #nmolecules = int(settings[-1][1])
    nmolecules=15
    #permol = ydata/nmolecules
    #difference = permol-permol[-1]
    difference = ydata-ydata[-1]
    plot(xdata,difference)
    plot(xdata,ydata)
    #plot(xdata,times)
    y = str(input("desired proximity to converged value: "))
    print (findx(y,xdata,difference))
main()

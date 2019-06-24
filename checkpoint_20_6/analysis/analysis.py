import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

#only supports txt files so far.

def readfile(filename,extension):
    file = open(filename + "." + extension,"r")
    contents = file.readlines()
    file.close()
    if extension == "txt":
        for i in range(len(contents)):
            contents[i] = contents[i][:-1] # to remove the new line "\n" symbol
    return np.array(contents)

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

def main():
    filepath = str(input("data file path: "))
    yname = str(input("Name of castep stripped data file: "))
    xname = str(input("Name of own data file: "))

    ydata = readfile(filepath + yname,"txt").astype("float64")
    xdata = readfile(filepath + xname,"txt").astype("float64")
    times = readfile(filepath + "time","txt").astype("float64")
    settings = readfile(filepath + "settings","txt")
    settings = breakfields(settings,"=")
    nmolecules = int(settings[-1][1])
    permol = ydata/nmolecules
    difference = permol-permol[-1]
    plot(xdata,difference)
    plot(xdata,permol)
    plot(xdata,times)
    y = str(input("desired proximity to converged value (eV): "))
    print (findx(y,xdata,difference))
main()

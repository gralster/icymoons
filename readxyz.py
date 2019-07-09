import numpy as np
import matplotlib.pyplot as plt

boxdim = 12.5

def readxyz(filename,datatype):
    file = open(filename + ".xyz", "r")
    contents = file.readlines()
    n = int(contents[0])
    print(n)
    contents = [i.split() for i in contents if len(i) > 1]
    atoms = []
    names = []
    relevent = []
    for i in range(len(contents)):
        if len(contents[i])>1:
            relevent.append(contents[i])
        else:
            pass
    for j in range(n):
        atoms.append([])
        names.append(relevent[j][0])
    for i in range(len(relevent)):
            index = i%n
            atoms[index].append(relevent[i][1:])

    atoms = np.array(atoms)
    atoms = atoms.astype(datatype)
    stepsn = len(atoms[0])
    return atoms,stepsn,n,names

def readtxtfile(filename,datatype):
    file = open(filename + ".txt","r")
    contents = file.readlines()
    file.close()
    for i in range(len(contents)):
        contents[i] = contents[i][:-1] # to remove the new line "\n" symbol
    return np.array(contents).astype(datatype)

def ruler(pos1,pos2):
    boxdim=12.5
    diff = np.array(pos1)-np.array(pos2)
    adj = (diff+boxdim*0.5)%boxdim-boxdim*0.5
    return np.linalg.norm(adj)

def meansqrdisp(atoms,steps,n):
    boxdim=12.5 #find a way to read this in
    msds = []
    for i in range(steps):
        d = []
        for j in range(len(atoms)):
            d.append(ruler(atoms[j][i],atoms[j][0]))
        sd = list(map(lambda x: x**2, d))
        sumsd = sum(sd)
        normedsum = sumsd/len(atoms)
        msds.append(normedsum)
    return(msds)

def gofr(atoms,steps):
    bins = 5
    ds = []
    for k in range(steps):
        d = []
        for i in range(len(atoms)):
            for j in range(i+1,len(atoms)):
                d.append(ruler(atoms[i][k],atoms[j][k]))
        d = np.array(d)
        ds.append(d)
    sumds = sum(ds)
    avsum = np.array(sumds)/(steps)

    hist,edges = np.histogram(avsum,bins)
    dr = edges[1]-edges[0]
    numdens = len(atoms)/(boxdim**3)
    r = edges+(dr/2)
    normalising_factor = (4*numdens*np.pi*dr*r**2)
    ys = (hist/normalising_factor[:-1])
    return ys, r

def gofrav(atom,atoms,steps):
#not normalised
    numdens = len(atoms)/(boxdim**3)
    ds = []
    for j in range(steps):
        d=[]
        for i in range(len(atoms)):
            d.append(ruler(atoms[atom][j],atoms[i][j]))
        d = np.array(d)
        ds.append(d)
    sumds = sum(ds)
    avsum = np.array(sumds)/(steps*boxdim)
    return avsum

def selection(names,atoms,selection):
    newatoms = []
    for i in range(len(names)):
        if names[i] == selection:
            newatoms.append(atoms[i])
        else:
            pass
    return newatoms

def main():

    times = [i*0.5e-15 for i in range(steps)]

    atoms,steps,n,names = readxyz("/home/s1624534/Mine/icymoons/thomas/castep",float)
    msds = meansqrdisp(atoms,steps,n)
    plt.plot(times,msds)
    plt.xlabel("time")
    plt.ylabel("mean square displacement")
    plt.show()

    carbons=selection(names,atoms, "C")
    msds = meansqrdisp(carbons,steps,n)
    plt.plot(times,msds)
    plt.xlabel("time")
    plt.ylabel("mean square displacement")
    plt.show()

    oxygens=selection(names,atoms, "O")
    msds = meansqrdisp(oxygens,steps,n)
    plt.plot(times,msds)
    plt.xlabel("timestep")
    plt.ylabel("mean square displacement")
    plt.show()
    '''

    distribution,r = gofr(atoms,steps)
    print(distribution)
    print(r)
    plt.plot(r[:-1],distribution)
    plt.show()
    #plt.hist(distribution,bins = 50)
    #plt.xlabel("distance (angstroms)")
    #plt.show()
    '''

main()

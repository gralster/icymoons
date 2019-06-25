import numpy as np

# atoms[i].append(x.split()[1:])
def readin(filename):
    file = open(filename + ".xyz", "r")
    contents = file.readlines()

    n = int(contents[0])

    print(n)
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
    atoms = atoms.astype(float)
    stepsn = len(atoms[0])
    return atoms,stepsn,n

def ruler(pos1,pos2):
    diff = np.array(pos1)-np.array(pos2)
    return np.linalg.norm(diff)

def meansqrdisp(atoms,steps,n):
    msds = []
    for j in range(len(atoms)):
        d = []
        for i in range(steps):
            #rint(np.array(atoms[j][i]))
            d.append(ruler(atoms[j][i],atoms[j][0]))
        sd = list(map(lambda x: x**2, d))
        sumsd = sum(sd)
        normedsum = sumsd/len(sd)
        msds.append(normedsum)
    print(msds)


def main():
    atom = 3
    atoms,steps,n = readin("castep")
    squaredisplacement = meansqrdisp(atoms,steps,n)
main()

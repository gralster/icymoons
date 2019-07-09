from box import Frame
from simulation import Simulation
def main():

    densitywanted = 0.714361356132767
    percentagemethane = 0.5
    nholes = 12

    box1 = Frame(5)
    box1.fccposition()
    box1.tesselate(3)
    box1.fill(proportion=percentagemethane,holes=nholes)

    box2 = Frame(box1.getdim(densitywanted))
    box2.fccposition()
    box2.tesselate(3)
    box2.fill(proportion=percentagemethane,holes=nholes)
    box2.shake()
    box2.writecellfile("48-48-12")
    #print(str(box1.dim**3)+"A^3")

    #box1.fccposition()
    #box1.fill(proportion=2,arrangement="FCC")
    #box1.shake()
    #box1.writecellfile("moldyn_convergence_test")
main()

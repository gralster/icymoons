u = 1.66054*(10**(-27))

class Atom():
    def __init__(self,pos,type):
        if type == "carbon":
            self.name = "C"
            self.mass = 12.107*u
        elif type == "oxygen":
            self.name = "O"
            self.mass = 15.999*u
        else:
            self.name = "H"
            self.mass = 1.00784*u #assume hydrogen
        self.pos = pos

    def getpos(self):
        return self.pos

    def getmass(self):
        return self.mass

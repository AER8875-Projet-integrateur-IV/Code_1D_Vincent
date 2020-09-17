from math import *
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
import argparse
#importer fonctions maths. L'* est importante
#importer les tableaux
# collection of command style functions that make
# matplotlib work like MATLAB concerning plots.
# collection of command style functions that make
# matplotlib work like MATLAB concerning animations.
#The argparse module makes it easy to write user-friendly command-line interfaces.

# Creation de la classe onde
class Onde(object):

#__init__ is one of the reserved methods in Python.
# In object oriented programming, it is known as a constructor.
# The __init__ method can be called when an object is created from the class,
# and access is required to initialize the attributes of the class.
    def __init__(self, ni, l, deriv, cfl, c):
#    def __init__(self, ni, l, cfl, c):
        super(Onde,self).__init__()
# Return a proxy object that delegates method calls to a parent or sibling class
# of type. This is useful for accessing inherited methods that have been
# overridden in a class. The search order is same as that used by getattr()
# except that the type itself is skipped.


# Initialisation des objets de la classe
        self.ni = ni                        # nombre intervalles
        self.length = l                     # longueur
        self.x = np.linspace(0.0,100.0,ni+1)    # position des noeuds
        self.Xmid = np.zeros(self.ni)       # postiion au milieu des noeuds
        self.dx = l / float(ni)         # pas
        self.u = np.zeros(self.ni+2)        # Vecteur u
        self.uPre = np.copy(self.u)         # Vecteur u temporaire pour iteration
        self.cfl = cfl                      # Limite physique du modele
        self.c = c                          # Vitesse de onde
        self.deriv = deriv                  # methode de derivation

        for i in range(1,self.ni):                     # Boucle for
        # This is a versatile function to create lists containing arithmetic
        # progressions. It is most often used in for loops. The arguments must
        # be plain integers. If the step argument is omitted, it defaults to 1
            self.Xmid[i] = (self.x[i] + self.x[i+1]) * 0.5 # Calcul de Xmid

    def condInit(self):
        for i in range(1,self.ni+1):
            if (self.x[i] < 40.0):
                self.u[i] = 0.0
            elif (self.x[i-1] > 60.0):
                self.u[i] = 0.0
            else:
                self.u[i] = 100.0


    def periodBound(self):
        self.u[0] = self.u[self.ni]
        self.u[self.ni+1]=self.u[1]

    def stableDeltaT(self):
        # Equation 5 , CFLmax = 1.0
        return self.cfl * self.dx / self.c

#    def iteration(self, dt): # iteration
#        for i in range(1, self.ni+1):
#            self.u[i] = self.uPre[i] - self.c * dt / self.dx * (self.uPre[i] - self.uPre[i-1])

    def iteration(self, dt): # iteration
        if self.deriv == "b":
            for i in range(1, self.ni+1):
               self.u[i] = self.uPre[i] - self.c * dt / self.dx * (self.uPre[i] - self.uPre[i-1])
        elif self.deriv == "f":
            for i in range(1, self.ni+1):
                self.u[i] = self.uPre[i] - self.c * dt / self.dx * (self.uPre[i+1] - self.uPre[i])
        else:
            for i in range(1, self.ni+1):
                self.u[i] = self.uPre[i] - self.c * dt / (2.0 * self.dx) * (self.uPre[i-1] - self.uPre[i+1])

            #methode de calcul, cond initiales puis dt et plot
    def run(self):
     self.condInit()
     dt = self.stableDeltaT()
     fig = plt.figure()
     ims = []
     t = 0.0
     tf = 3
     #temps final
     for i in range(10000):
         #nombre itteration tres grand pour etre sur de sortir
         self.uPre = np.copy(self.u)
          #copie de u
         self.iteration(dt)
          #avance dans le temps
         self.periodBound()
         #fonrtiere periodique
         ims.append(plt.plot(self.Xmid, self.u[1:self.ni+1], color='black'))
         t += dt #incremantation
         if t >= tf:
             break
     ani = anim.ArtistAnimation(fig, ims, interval=50, blit=False)
     plt.show()



if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='Wave Equation')
    parser.add_argument("--ni", type=int)
    #argument 1 a taper --ni val_ni
    parser.add_argument("--length", type=float)
    parser.add_argument("--deriv", type=str)
    parser.add_argument("--cfl", type=float)
    parser.add_argument("--c", type=float)

    args = parser.parse_args()
    solution = Onde(args.ni,args.length,args.deriv,args.cfl,args.c) #Stockage objet dans var
    #solution = Onde(args.ni,args.length,args.deriv,args.cfl,args.c) #Stockage objet dans var
    solution.run() #Execution

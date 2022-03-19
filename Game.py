from GUI_demineur.guiDemineur_V2 import *
from random import randint

class Game(object):

    def __init__(self, long):
        self.gui = GUIdemineur(long, 32) #créer une instance de guiDemineur_V2
        
        self.gui.refresh(self.grille, )
        
    def start(self):
        """
        Boucle de jeu principale :
            - Reçoit les clics
            - 
        Elle permet de gérer chaque itération de la boucle, du début jusqu'à la fin (Game Over ou Win)
        """
        while True:
            x, y, clic = self.gui.waitClick() # renvoie les coordonnées de la case et du clic
            if clic == "D" : #si clic droit
                pass
            elif clic == "G": #si clic gauche
                pass

                

    def propagation(self, case):
        """
        Regarde si une case blanche est clické. Si oui, propage l'ouverture de case.
        """
        pass

class Grille(object):

    def __init__ (self, long):
        self.grid = [[-1 for x in range(long)] for y in range(long//2)]
        self.bombGrid = [[-1 for x in range(long)] for y in range(long//2)]

    def randomizeBomb(self, nbBomb):
        #1 = bombe, sinon 0
        for i in range(nbBomb):
            r1 = randint(0, len(self.bombGrid) - 1)
            r2 = randint(0, len(self.bombGrid[1]) - 1)
            self.bombGrid[r1][r2] = 1

if __name__ == '__main__' :
    m = Game(32)
    m.start()
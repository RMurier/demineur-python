from random import randint
import time

from GUI_demineur.guiDemineur_V2 import *
from Grille import Grille
from ScoreBoard import ScoreBoard

class Game(object):

    def __init__(self, long=40):
        """
        Permet l'initialisation du jeu.
        """
        # self.scoreboard = ScoreBoard()
        self.gui = GUIdemineur(long, 32) #créer une instance de guiDemineur_V2
        self.grid = Grille(long)
        self.flagputted = 0
        self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0)
        
    def start(self):
        """
        Boucle de jeu principale
        Elle permet de gérer chaque itération de la boucle, du début jusqu'à la fin (Game Over ou Win)
        """
        coosBefore = None
        self.gui.startTime()
        while True:
            x, y, clic = self.gui.waitClick() # renvoie les coordonnées de la case et du clic
            if clic == "D" : #si clic droit
                if self.grid.grid[y][x] == -1:
                    if self.flagputted != self.grid.nbBomb:
                        self.grid.grid[y][x] = -2
                        self.flagputted += 1
                elif self.grid.grid[y][x] == -2:
                    self.flagputted -= 1
                    self.grid.grid[y][x] = -3
                elif self.grid.grid[y][x] == -3:
                    self.grid.grid[y][x] = -1
                self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0)
            elif clic == "G": #si clic gauche
                coosBefore = (x, y)
                if self.grid.grid[y][x] == -1:
                    pass
                self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 3)
            elif clic == "R": #si clic relaché
                if coosBefore == (x, y):
                    if self.grid.grid[y][x] == -1:
                        if self.grid.bombGrid[y][x] == 1:
                            self.grid.grid[y][x] = -5
                            self.gui.gameOver()
                            time.sleep(1)
                        else:
                            self.grid.grid[y][x] = self.grid.numberNeighborBomb(x, y)
                            self.propagation((y, x))
                    self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0)

                

    def propagation(self, case):
        """
        Regarde si une case vide est cliqué. Si oui, propage l'ouverture des cases situés à coté qui sont aussi vides.
        """
        y, x = case
        print(y,x)
        self.grid.grid[y][x] = self.grid.numberNeighborBomb(x, y)
        if self.grid.grid[y][x] != 0:
            return
        if x > 0 and self.grid.grid[y][x-1] == -1: #gauche
            self.propagation((y, x-1))
        if x < len(self.grid.bombGrid[0]) - 1 and self.grid.grid[y][x+1] == -1: #droite
            self.propagation((y, x+1))
        if y > 0 and self.grid.grid[y-1][x] == -1: #haut
            self.propagation((y-1, x))
        if y < len(self.grid.bombGrid) - 1 and self.grid.grid[y+1][x] == -1: #bas
            self.propagation((y+1, x))


if __name__ == '__main__' :
    m = Game()
    m.start()
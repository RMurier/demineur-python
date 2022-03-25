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
        self.scoreboard = ScoreBoard()
        self.gui = GUIdemineur(long, 32) #créer une instance de guiDemineur_V2
        self.grid = Grille(long, 99)
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
                            self.gui.stopTime()
                            time.sleep(1)
                        else:
                            self.grid.grid[y][x] = self.grid.numberNeighborBomb(x, y)
                            self.grid.propagation((y, x))
                    self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0)

            


if __name__ == '__main__' :
    m = Game()
    m.start()
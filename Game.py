from random import randint
import time

from GUI_demineur.guiDemineur_V2 import *
from Grille import Grille

class Game(object):

    def __init__(self, long = 40):
        """
        Permet l'initialisation du jeu.
        """
        self.gui = GUIdemineur(long, 32) #créer une instance de guiDemineur_V2
        self.grid = Grille(long, 99) #créer une instance de Grille
        self.flagputted = 0 #nombre de drapeaux placés
        self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0) #refresh la grille
        
    def start(self):
        """
        Boucle de jeu principale
        Elle permet de gérer chaque itération de la boucle, du début jusqu'à la fin (Game Over ou Win)
        """
        coosBefore = None
        while True:
            x, y, clic = self.gui.waitClick() # renvoie les coordonnées de la case et le type de clic
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
                if not self.gui.chronoIsEnable():
                    self.gui.startTime()
                coosBefore = (x, y)
                if self.grid.grid[y][x] == -1:
                    pass
                self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 3)
            elif clic == "R": #si clic relaché
                if coosBefore == (x, y):
                    if self.grid.grid[y][x] == -1:
                        if self.grid.bombGrid[y][x] == 1: #si click sur une bombe
                            self.grid.grid[y][x] = -5
                            self.gui.gameOver()
                            self.gui.stopTime()
                            self.grid.updateGameOver()
                            self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0)
                            time.sleep(1)
                        else:
                            self.grid.grid[y][x] = self.grid.numberNeighborBomb(x, y)
                            self.grid.propagation((y, x))
                            if self.isWon(): #si fin de partie
                                self.gui.gagne()
                                self.gui.stopTime()
                                time.sleep(2)
                    self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0)

    def isWon(self):
        """
        Permet de savoir si le joueur a gagné ou non
        """
        for i in range(len(self.grid.grid)):
            for j in range(len(self.grid.grid[i])):
                if self.grid.grid[i][j] == -1:
                    return False
        return True
                

if __name__ == '__main__' :
    m = Game()
    m.start()
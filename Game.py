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
        self.grid = Grille(long, 10) #créer une instance de Grille
        self.flagputted = 0 #nombre de drapeaux placés
        self.firstclick = True
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
                            if self.firstclick: #si premier click, pas possible de tomber sur une bombe
                                self.grid.bombGrid[y][x] = 0
                                self.grid.addNewBomb(y, x)
                                self.firstclick = False
                                self.grid.grid[y][x] = self.grid.numberNeighborBomb(x, y)
                            else:
                                self.grid.grid[y][x] = -5
                                self.gui.gameOver()
                                self.gui.stopTime()
                                time.sleep(1)
                                for i in range(len(self.grid.grid)):
                                    self.grid.updateGameOver(i)
                                    self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0)
                                    time.sleep(0.5)
                                break #fin de partie, sort de la boucle
                        else:
                            if self.firstclick:
                                self.firstclick = False
                            self.grid.grid[y][x] = self.grid.numberNeighborBomb(x, y)
                            self.grid.propagation((y, x))
                            if self.isWon(): #si fin de partie
                                self.gui.stopTime()
                                self.gui.gagne()
                                time.sleep(3)
                                self.gui.addScore(self.gui.getTime())
                                break #fin de partie, sort de la boucle
                    self.gui.refresh(self.grid.grid, self.grid.nbBomb - self.flagputted, 0)

    def isWon(self):
        """
        Permet de savoir si le joueur a gagné ou non
        """
        for y in range(len(self.grid.grid)):
            for x in range(len(self.grid.grid[1])):
                if self.grid.grid[y][x] == -1 and self.grid.bombGrid[y][x] == 0:
                    return False
        return True

    def isRestart(self):
        """
        Permet de savoir si le joueur veut recommencer ou non
        """
        pass
                

if __name__ == '__main__' :
    m = Game()
    m.start()
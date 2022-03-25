import random

class Grille(object):
    """
    Initialisation de la grille, qui est utiliser pour générer une grille, ainsi qu'effectuer une modification sur cette dernière.
    Elle prends plusieurs paramètres:
    - La longueure n (définite sur 40 par défaut dans Game), qui définis le tableau t (t = n * n//2)
    - Le nombre de bombe (définite sur 15 par défaut).
        Dans le cas ou le bombre de bombes dépasse le nombre de cases disponible, le nombre de bombes sera égale a l'entier 
        inférieur au nombre de case divisé par 8 ((longueur*largeur)//2)
    """
    def __init__ (self, long, nbomb = 15):
        self.grid = [[-1 for x in range(long)] for y in range(long//2)]
        self.bombGrid = [[0 for x in range(long)] for y in range(long//2)]
        self.nbBomb = (long*long//2)//8 if nbomb > long*long//2 else nbomb
        self.randomizeBomb()

    def randomizeBomb(self):
        """
        Permet de mettre x bombes aléatoirement sur la grille lors du démarage de la partie.
        """
        for _ in range(self.nbBomb):
            while True:
                y = random.randint(0, len(self.bombGrid) - 1) #entre 0 et n-1 sur l'axe y (hauteur)
                x = random.randint(0, len(self.bombGrid[1]) - 1) #entre 0 et n-1 sur l'axe x (largeur)
                if self.bombGrid[y][x] == 1:
                    continue
                self.bombGrid[y][x] = 1
                break

    def numberNeighborBomb(self, x, y):
        nb = 0
        nb += 1 if x > 0 and self.bombGrid[y][x-1] == 1 else 0 #gauche
        nb += 1 if x < len(self.bombGrid[0]) -1 and self.bombGrid[y][x+1] == 1 else 0 #droite
        nb += 1 if y > 0 and self.bombGrid[y-1][x] == 1 else 0 #haut
        nb += 1 if y < len(self.bombGrid) -1 and self.bombGrid[y+1][x] == 1 else 0 #bas
        nb += 1 if (x > 0 and y > 0) and self.bombGrid[y-1][x-1] == 1 else 0 #haut gauche
        nb += 1 if (x < len(self.bombGrid[0]) -1 and y > 0) and self.bombGrid[y-1][x+1] == 1 else 0 #haut droit
        nb += 1 if (x > 0 and y < len(self.bombGrid) -1) and self.bombGrid[y+1][x-1] == 1 else 0 #bas gauche
        nb += 1 if (x < len(self.bombGrid[0]) -1 and y < len(self.bombGrid) -1) and self.bombGrid[y+1][x+1] == 1 else 0
        return nb

    def propagation(self, case):
        """
        Regarde si une case vide est cliqué. Si oui, propage l'ouverture des cases situés à coté qui sont aussi vides.
        """
        y, x = case
        print(y,x)
        self.grid[y][x] = self.grid.numberNeighborBomb(x, y)
        if self.grid[y][x] != 0:
            return

        if x > 0 and self.grid[y][x-1] == -1: #gauche
            self.propagation((y, x-1))

        if x < len(self.grid.bombGrid[0]) - 1 and self.grid[y][x+1] == -1: #droite
            self.propagation((y, x+1))

        if y > 0 and self.grid[y-1][x] == -1: #haut
            self.propagation((y-1, x))

        if y < len(self.grid.bombGrid) - 1 and self.grid[y+1][x] == -1: #bas
            self.propagation((y+1, x))

        if x > 0 and y > 0 and self.grid[y-1][x-1] == -1: #haut gauche:
            self.propagation((y-1, x-1))

        if x < len(self.grid.bombGrid[0]) - 1 and y > 0 and self.grid[y-1][x+1] == -1: #haut droit
            self.propagation((y-1, x+1))

        if x > 0 and y < len(self.grid.bombGrid) - 1 and self.grid[y+1][x-1] == -1: #bas gauche
            self.propagation((y+1, x-1))

        if x < len(self.grid.bombGrid[0]) - 1 and y < len(self.grid.bombGrid) - 1 and self.grid[y+1][x+1] == -1:
            self.propagation((y+1, x+1))

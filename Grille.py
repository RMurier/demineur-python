import random

class Grille(object):
    """
    Initialisation de la classe, qui est utilisée pour générer une grille, ainsi qu'effectuer une modification sur cette dernière.
    Elle prends plusieurs paramètres:
    - La longueur n (définie sur 40 par défaut dans Game), qui définis le tableau t (t = n * n//2)
    - Le nombre de bombes (définies sur 15 par défaut).
        Dans le cas ou le nombre de bombes dépasse le nombre de cases disponible, le nombre de bombes sera égale a l'entier 
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
                if self.bombGrid[y][x] == 1: #si la case est déjà occupée, on recommence
                    continue
                self.bombGrid[y][x] = 1
                break

    def numberNeighborBomb(self, x, y):
        """
        Donne le nombre de bombes dans les cases voisinses de la grille en coordonnées y / x
        """
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
        Permet de faire apparaitre les bombes ou les cases vides dans les cases voisines de la case en coordonnées y / x.
        """
        y, x = case
        self.grid[y][x] = self.numberNeighborBomb(x, y)
        if self.grid[y][x] != 0:
            return

        if x > 0 and self.grid[y][x-1] == -1: #gauche
            self.propagation((y, x-1))

        if x < len(self.bombGrid[0]) - 1 and self.grid[y][x+1] == -1: #droite
            self.propagation((y, x+1))

        if y > 0 and self.grid[y-1][x] == -1: #haut
            self.propagation((y-1, x))

        if y < len(self.bombGrid) - 1 and self.grid[y+1][x] == -1: #bas
            self.propagation((y+1, x))

        if x > 0 and y > 0 and self.grid[y-1][x-1] == -1: #haut gauche:
            self.propagation((y-1, x-1))

        if x < len(self.bombGrid[0]) - 1 and y > 0 and self.grid[y-1][x+1] == -1: #haut droit
            self.propagation((y-1, x+1))

        if x > 0 and y < len(self.bombGrid) - 1 and self.grid[y+1][x-1] == -1: #bas gauche
            self.propagation((y+1, x-1))

        if x < len(self.bombGrid[0]) - 1 and y < len(self.bombGrid) - 1 and self.grid[y+1][x+1] == -1: #bas droit
            self.propagation((y+1, x+1))

    def updateGameOver(self, y):
        """
        Met à jour la grille en fonction de la fin de la partie.
        """
        for x in range(len(self.grid[0])):
            if self.bombGrid[y][x] == 1:
                if self.grid[y][x] == -1 or self.grid[y][x] == -2:
                    self.grid[y][x] = -4
            else:
                if self.grid[y][x] == -2:
                    self.grid[y][x] = -6
                else:
                    self.grid[y][x] = 0

    def addNewBomb(self, yb, xb):
        """
        Permet d'ajouter une nouvelle bombe sur la grille.
        """
        while True:
            x = random.randint(0, len(self.bombGrid[0]) - 1)
            y = random.randint(0, len(self.bombGrid) - 1)
            if self.bombGrid[y][x] == 0 and (y, x) != (yb, xb):
                self.bombGrid[y][x] = 1
                break


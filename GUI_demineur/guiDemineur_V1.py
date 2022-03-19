# Grégory Coutable 2022
# Partage sous licence Creative Commons :
# https://creativecommons.org/licenses/by-sa/3.0/fr/
#
# Version 1 : pas de gestion du temps de partie

import pygame
from pygame.locals import *
#pour le rendre dispo de n'importe où
import os
pathname = os.path.dirname(__file__)

class GUIdemineur (object):
    
    def __init__(self, nb, w):
        """
        Initialise une grille du jeu démineur rectangulaire de nb * nb/2 cases.
        
        """
        
        #des constantes pour le dessin de la grille
        self.nbx = nb #la taille de la grille
        self.nby = nb // 2 #la taille de la grille
        self.w = w #largeur d'une case
        self.d = self.w // 10 #entre deux cases
        self.wPol = int(self.w / 1.5) #taille de base des polices
        self.wPol2 = (nb * w) // 10 
        #la liste des coordonnées de chaque case de la grille (coordonnées du coin en haut à gauche)
        self.xy0 = [self.d + (self.d + self.w) * x for x in range(self.nbx)]

        #initialisation de pygame
        pygame.init()
        #calcul de la taille totale de la fenètre
        self.wFen = self.nbx * self.w + (self.nbx + 1) * self.d
        #hauteur idem + un bandeau pour le score
        self.hBandeau = 100
        hFen = self.nby * self.w + (self.nby + 1) * self.d + self.hBandeau
        self.rectG = pygame.Rect(0, 0, self.wFen //3, self.hBandeau)
        self.rectC = pygame.Rect(self.wFen //3, 0, self.wFen //3, self.hBandeau)
        self.rectD = pygame.Rect(2*self.wFen //3, 0, self.wFen //3, self.hBandeau)
        #on définit la fenêtre de base de notre jeu
        self.fond = pygame.display.set_mode((self.wFen, hFen))
        #un titre sur cette fenêtre
        pygame.display.set_caption("Démineur")

        #une liste contenant les différentes cases possibles
        self.cases = [self._creerCase(i) for i in range(-6, 9)]
        
        self.refresh([[-1 for x in range(self.nbx)] for y in range(self.nby)], 0, 0)
    
    def _creerCase(self, n):
        """
        Créé les cases pour le jeu : il en existe 15 différentes selon la valeur de n :
        -6 : Bombe barrée -> case faussement attribuée a un bombe
        -5 : Bombe sur fond rouge -> Explosion, c'est perdu
        -4 : Bombe découverte
        -3 : ? sur case cachée -> vous avez un doute
        -2 : Drapeau rouge sur case cachée : vous pensez que c'est une bombe, le click devra être bloqué
        -1 : Case cachée
        0 : case découverte vierge
        1 à 8 : case découverte avec 1 à 8 bombe dans les cases adjacentes
        """
        clrCase = ['#EEE4DA', '#CDC1B3', '#FF0000']
        clrPolice = ['black', 'blue', 'green', 'red', 'black', 'white', 'violet', 'orange', 'yellow']

        case = pygame.Surface((self.w, self.w))
        taille = int (self.wPol * 2)
        police = pygame.font.SysFont("Arial Black.ttf",taille)
            
        if n == 0:
            case.fill(pygame.Color(clrCase[1]))
        
        elif 0 < n < 9:
            case.fill(pygame.Color(clrCase[1]))
            texte = police.render(str(n), True, clrPolice[n])
            #pour centrer le texte dans la case
            rectTexte = texte.get_rect()
            rectTexte.center = case.get_rect().center
            
            case.blit(texte, rectTexte)
            
        elif n == -1:
            case.fill(pygame.Color(clrCase[0]))
            
        elif -4 >= n >= -6:
            if n == -5:
                case.fill(pygame.Color(clrCase[2]))
            else:
                case.fill(pygame.Color(clrCase[1]))
            imgMine = pygame.transform.scale(pygame.image.load(os.path.join(pathname, "mine.png")).convert_alpha(), (self.w, self.w))
            case.blit(imgMine, (0, 0))
            if n == -6:
                pygame.draw.line(case, 'red', (0.1*self.w, 0.1*self.w), (0.9*self.w, 0.9*self.w), 3)
                pygame.draw.line(case, 'red', (0.1*self.w, 0.9*self.w), (0.9*self.w, 0.1*self.w), 3)
            
        elif n == -2:
            case.fill(pygame.Color(clrCase[0]))
            imgFlag = pygame.transform.scale(pygame.image.load(os.path.join(pathname, "flag.png")).convert_alpha(), (self.w, self.w))
            case.blit(imgFlag, (0, 0))
            
        elif n == -3:
            case.fill(pygame.Color(clrCase[0]))
            texte = police.render('?', True, clrPolice[0])
            #pour centrer le texte dans la case
            rectTexte = texte.get_rect()
            rectTexte.center = case.get_rect().center
            
            case.blit(texte, rectTexte)
            
        return case
    
    def refresh(self, g, mine, emo = 0):
        """
        Cette méthode rafraichie l'affichage du démineur conformément à la grille passée en argument.
        
        g est une liste de nb listes.
        Par exemple ;
        g[0][0] est la case en haut a gauche,
        g[0][3] est la case en haut a droite,
        g[3][3] est la case en bas à droite dans une grille de 4*4.
        
        Le contenu de la grille définit le dessin de la case :
            -6 : Bombe barrée -> case faussement attribuée a un bombe
            -5 : Bombe sur fond rouge -> Explosion, c'est perdu
            -4 : Bombe découverte
            -3 : ? sur case cachée -> vous avez un doute
            -2 : Drapeau rouge sur case cachée : vous pensez que c'est une bombe, le click devra être bloqué
            -1 : Case cachée
            0 : case découverte vierge
            1 à 8 : case découverte avec 1 à 8 bombe dans les cases adjacentes        
        
        mine correspond au nombre de mine à deviner a afficher à gauche du bandeau.
        
        emo correspond au numéro de l'émoji à afficher :
            0 : Souriant -> en général
            1 : Lunette de soleil -> victoire
            2 : en pleure -> pour la défaite
            3 : Anxieux -> pendant le click sur une case
        """

        self.fond.fill(pygame.Color("#BCAF9F"))
        for y in range(self.nby):
            for x in range(self.nbx):
                self.fond.blit(self.cases[g[y][x] + 6], (self.xy0[x], self.xy0[y] + self.hBandeau)) 
        #le score :
        police = pygame.font.Font(os.path.join(pathname, "led.ttf"), self.wPol2 // 2)        
        txtMines = police.render(str(mine), True, 'yellow')
        rectTxt2 = txtMines.get_rect()
        rectTxt2.center = self.rectG.center
        self.fond.blit(txtMines, rectTxt2)


        emoji = pygame.image.load(os.path.join(pathname, F"emoji_{emo}.png")).convert_alpha()
        self.rectEmo = emoji.get_rect()
        self.rectEmo.center = self.rectC.center
        self.fond.blit(emoji, self.rectEmo)
                
        #Rafraîchissement de l'écran
        pygame.display.update()

    def gagne(self):
        """
        Cette méthode permet d'afficher GAGNE plein écran sur fond rouge.
        """
        self.fond.fill("green")
        police = pygame.font.Font(os.path.join(pathname, "led.ttf"),int (self.wPol2))
        texte = police.render("GAGNE !!", True, pygame.Color("#FFFF00"))
        #pour centrer le texte
        rectTexte = texte.get_rect()
        rectTexte.center = self.fond.get_rect().center
        self.fond.blit(texte,rectTexte)
        #Rafraîchissement de l'écran
        pygame.display.update()

    def gameOver(self):
        """
        Cette méthode permet d'afficher GAME OVER plein écran sur fond rouge.
        """
        self.fond.fill("red")
        police = pygame.font.Font(os.path.join(pathname, "led.ttf"),int (self.wPol2))
        texte = police.render("GAME OVER", True, pygame.Color("#FFFF00"))
        #pour centrer le texte
        rectTexte = texte.get_rect()
        rectTexte.center = self.fond.get_rect().center
        self.fond.blit(texte,rectTexte)
        #Rafraîchissement de l'écran
        pygame.display.update()
        
    def waitClick(self):
        """
        Cette méthode attend l'action d'un joueur. Elle gère cinq types d'actions :
            - demande fermeture de la fenètre : fermeture propre de la fenètre pygame et fin du programme python.
            - click sur la fenetre : retourne un tuple contenant les numéros (x, y, bouton) de la case choisie.
                Bouton fait référence au click souris : 'D' pour droit, 'G' pour gauche.
            - click sur l'émoji : retourne 'E'
            - laché du bouton gauche de la souris : retourne 'G'
            - Quelques autres touches sont également gérées et retourne la lettre saisie.
        Une fois exécutée, on ne peut sortir de cette méthode que par l'une de ces actions.

        """        
        while True:
            #Limitation de vitesse de la boucle
            pygame.time.Clock().tick(30)
            
            for event in pygame.event.get():    #Attente des événements
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                    
                if event.type == MOUSEBUTTONDOWN:
                    if event.button == 1 or event.button == 3:   #Si clic gauche ou droit
                        if self.rectEmo.collidepoint(event.pos):
                            return 'E'
                        if event.pos[1] > self.hBandeau:
                            return (event.pos[0]//(self.w + self.d), (event.pos[1] - self.hBandeau)//(self.w + self.d), ('G', 'C', 'D')[event.button - 1])
                
                if event.type == MOUSEBUTTONUP and event.button == 1:
                    #detecte le relachement du click gauche
                        if event.pos[1] > self.hBandeau:
                            return (event.pos[0]//(self.w + self.d), (event.pos[1] - self.hBandeau)//(self.w + self.d), 'R')


                if event.type == KEYDOWN:
                    touches = {K_RIGHT : '_R', K_LEFT : '_L', K_UP : '_U', K_DOWN : '_D', K_RETURN : '_E', K_BACKSPACE : '_B', K_ESCAPE : '_S'}
                    touche = event.key
                    if touche in touches:
                        return touches[touche]
                    return event.unicode
                

if __name__ == "__main__":
    import time
    
    GUI = GUIdemineur(30, 32)
    #GUI = GUIdemineur(40, 24)
    #GUI = GUIdemineur(60, 20)
    #GUI = GUIdemineur(80, 16)
    time.sleep(2)
    
    GUI.gameOver()
    time.sleep(2)

    g = [[-1 for x in range(30)] for y in range(15)]
    
    for y in range(15):
        for x in range(30):
            g[y][x] = y - 6
        GUI.refresh(g, 99, 6)    
        time.sleep(0.2)
        
    GUI.refresh(g, 10, 1)
    time.sleep(1)
    GUI.refresh(g, 20, 9)
    time.sleep(1)
    GUI.refresh(g, 30, 3)
    time.sleep(1)
    GUI.refresh(g, 40, 0)
    while True:
        event = GUI.waitClick()
        print(event)
        
        if len(event) == 3 and event[2] == 'G':
            GUI.refresh(g, 99, 8)
        elif len(event) == 3 and event[2] == 'R':
            GUI.refresh(g, 99, 0)
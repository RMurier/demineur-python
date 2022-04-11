from socketserver import DatagramRequestHandler
import pygame
from pygame.locals import *
import os
from win32api import GetSystemMetrics
import re
import time

from Data.database_handler import DataBaseHandler
database_handler = DataBaseHandler("madb.db")

username_re = re.compile(r"[^a-zA-Z]")

def convert_time(a:int):
    d = 0
    h = 0
    m = 0
    while a > 59:
        if a >= 86400:
            d += 1
            a -= 86400
        elif a >= 3600:
            h += 1
            a -= 3600
        elif a >= 60:
            m += 1
            a -= 60
    msg = ""
    if d != 0:
        msg += f"{d}j "
    if h != 0:
        msg += f"{h}h "
    if m != 0:
        msg += f"{m}m "
    if a != 0:
        msg += f"{a}s"
    return msg

class ScoreBoard(object):
    
    def __init__(self):
        """
        Initialise les informations de la classe Scoreboard, comme par exemple
        - Un écran de jeu, pour se connecter avec son nom d'utilisateur
        """
        self.username = ""
        self.userid = None
        self.usernameError = False

        pygame.init()
        self.screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), RESIZABLE) #création de la fênêtre
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "input.ttf"), 32) #police / taille du texte
        
        #input:
        self.rectinput = pygame.Rect((GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.5, 500, 50))
        self.color = pygame.Color(0,0,0) #couleur de texte
        self.colorinput = pygame.Color(166, 62, 197) #couleur de l'input
        self.txt_surface = self.font.render("Entrez votre pseudo !", True, self.color)

        self.txt_rect = self.txt_surface.get_rect()
        self.cursor = pygame.Rect(self.txt_rect.topright, (3, self.txt_rect.height + 2))

        #bouton play
        pygame.Rect((GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.5, 500, 50))
        self.imgplay = self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\play.png")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.3))

        #bouton classement
        pygame.Rect((GetSystemMetrics(0)//2-250, GetSystemMetrics(1), 500, 50))
        self.imgclassment = self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\classement.png")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.17))
        self.rect1 = self.rect2 = self.rect3 = self.rect4 = self.rect5 = None
        #bouton dans le menu classement
        self.returnhome = None

        self.update()
        self.draw()
        pygame.display.update()
        self.waitClick()

    def waitClick(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.imgplay.collidepoint(event.pos):
                        self.username = self.username.lower()
                        if len(self.username) == 0:
                            self.draw()
                            rect = pygame.Rect(GetSystemMetrics(0)//2, 0, 100, 50)
                            text = self.font.render(f"Le pseudonyme est vide !", True, pygame.Color(255, 0, 0), pygame.Color(0, 0, 0))
                            rect.centerx = GetSystemMetrics(0) // 2 - text.get_width()//2 + 50
                            self.screen.blit(text, rect)
                            pygame.display.update()
                            continue
                        return
                    elif self.imgclassment.collidepoint(event.pos):
                        self.showScoreBoard()
                        self.draw()
                        pygame.display.update()
                elif event.type == pygame.KEYDOWN:
                    if len(self.username) < 15 :
                        if event.key == pygame.K_BACKSPACE:
                            self.username = self.username[:-1]
                                      
                        else:
                            self.username += username_re.sub("", event.unicode)
                            
                        self.txt_surface = self.font.render(self.username, True, self.color)
                        self.update()

                        pygame.draw.rect(self.screen, self.color, self.rectinput, 1)
                        pygame.display.update()
    
    def update(self):
        self.rectinput.w = max(500, self.txt_surface.get_width()+10)
        self.rectinput.left = GetSystemMetrics(0)//2-self.rectinput.width//2
        if self.rectinput.w == 500:
            self.draw()

    def draw(self):
        self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\welcome.png")) ,(GetSystemMetrics(0), GetSystemMetrics(1))), [0, 0])
        self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\play.png")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.35))
        self.imgclassment = self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\classement.png")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.17))
        pygame.draw.rect(self.screen, self.colorinput, self.rectinput, 0, 12)
        self.screen.blit(self.txt_surface, (self.rectinput.x+5, self.rectinput.y+5))

    def showScoreBoard(self):
        self.screen.blit(pygame.transform.scale( pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\welcome.png")) ,(GetSystemMetrics(0), GetSystemMetrics(1))), [0, 0])
        self.returnhome = self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\retour.png")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.17))
        scoreboard = self.scoreboard()
        for i in range(len(scoreboard)):
            rect = pygame.Rect(GetSystemMetrics(0)//4, GetSystemMetrics(1)//2+i*50, 100, 50)
            text = self.font.render(f"{scoreboard[i][0]} a terminé le démineur en {convert_time(scoreboard[i][1])}", True, pygame.Color(255, 255, 255))
            self.screen.blit(text, rect)
        self.waitClickScoreBoard()

    def waitClickScoreBoard(self):
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.returnhome.collidepoint(event.pos):
                        return

    def scoreboard(self):
        """
        Retourne le top 10 des meilleurs score sous forme de liste
        """
        return database_handler.scoreboard()

    def fetchUser(self):
        """
        Récupère le joueur, ou l'ajoute en base de donnée si il n'existe pas
        """
        if database_handler.userExist(self.username):
            self.userid, self.username = database_handler.getUser(self.username)
            return print(self.username, self.userid)
        self.userid = database_handler.createUser(self.username)

    def addScore(self, score):
        """
        Ajoute une entrée en base de donnée contenant le score lié à l'ID de l'utilisateur qui joue.
        """

if __name__ == "__main__":
    s = ScoreBoard()

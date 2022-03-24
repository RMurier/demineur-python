import pygame
from pygame.locals import *
import os
from win32api import GetSystemMetrics

from Data.database_handler import DataBaseHandler
database_handler = DataBaseHandler("madb.db")

class ScoreBoard(object):
    
    def __init__(self):
        """
        Initialise les informations de la classe Scoreboard, comme par exemple
        - Un écran de jeu, pour se connecter avec son nom d'utilisateur
        """
        self.username = ""
        self.userid = None

        pygame.init()
        self.screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), RESIZABLE) #création de la fênêtre
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "GUI_demineur\\led.ttf"), 32) #police / taille du texte
        
        #input:
        self.rectinput = pygame.Rect((GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.5, 500, 50))
        self.color = pygame.Color('dodgerblue2') #couleur de texte
        pygame.draw.rect(self.screen, pygame.Color(255,255,255), self.rectinput)
        self.txt_surface = self.font.render("Entrez votre pseudo !", True, self.color)
        
        #bouton play
        pygame.Rect((GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.5, 500, 50))
        self.imgplay = self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\play.webp")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.3))

        #bouton classement
        pygame.Rect((GetSystemMetrics(0)//2-250, GetSystemMetrics(1), 500, 50))
        self.imgclassment = self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\classement.webp")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.17))

        self.draw()
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
                        return
                    elif self.imgclassment.collidepoint(event.pos):
                        self.showScoreBoard()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode if event.unicode != " " else ""
                    print(self.username)
                    self.txt_surface = self.font.render(self.username, True, self.color)
                    self.update()
                    self.draw()
            pygame.display.update()
    
    def update(self):
        self.rectinput.w = max(500, self.txt_surface.get_width()+10)
        self.rectinput.left = GetSystemMetrics(0)//2-self.rectinput.width//2

    def draw(self):
        self.screen.blit(pygame.transform.scale( pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\presentation.webp")) ,(GetSystemMetrics(0), GetSystemMetrics(1))), [0, 0])
        self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\play.webp")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.35))
        self.screen.blit(self.txt_surface, (self.rectinput.x+5, self.rectinput.y+5))
        self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\classement.webp")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.17))
        pygame.draw.rect(self.screen, self.color, self.rectinput, 2)

    def showScoreBoard(self):
        self.waitClickScoreBoard()
        self.screen.blit(pygame.transform.scale( pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\presentation.webp")) ,(GetSystemMetrics(0), GetSystemMetrics(1))), [0, 0])
        self.screen.blit(pygame.transform.scale(pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\classement.webp")), (500, 100)), (GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.17))

    def waitClickScoreBoard(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.imgplay.collidepoint(event.pos):
                        self.username = self.username.lower()
                        return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    else:
                        self.username += event.unicode if event.unicode != " " else ""
                    print(self.username)
                    self.txt_surface = self.font.render(self.username, True, self.color)
                    self.update()
                    self.draw()
            pygame.display.update()

    def scoreboard(self):
        """
        Retourne le top 10 des meilleurs score sous forme de liste
        """
        print(database_handler.scoreboard())

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

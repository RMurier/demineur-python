import pygame
from pygame.locals import *
import os
from win32api import GetSystemMetrics

from Data.database_handler import DataBaseHandler

class ScoreBoard(object):
    
    def __init__(self):
        """
        Initialise les informations de la classe Scoreboard, comme par exemple
        - Un écran de jeu, pour se connecter avec son nom d'utilisateur
        """
        self.username = ""

        pygame.init()
        self.screen = pygame.display.set_mode((GetSystemMetrics(0), GetSystemMetrics(1)), RESIZABLE)
        self.screen.blit(pygame.transform.scale( pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\presentation.webp")) ,(GetSystemMetrics(0), GetSystemMetrics(1))), [0, 0]) #met l'image d'arrière plan, et la met automatiquement a la taille de l'écran
        self.rectinput = pygame.Rect((GetSystemMetrics(0)//2-250, GetSystemMetrics(1)//1.5, 500, 50))
        self.color = pygame.Color('dodgerblue2') #couleur de texte
        self.font = pygame.font.Font(os.path.join(os.path.dirname(__file__), "GUI_demineur\\led.ttf"), 32) #police / taille du texte
        self.text_input = self.font.render("Entrez votre nom !", True, self.color)
        self.screen.blit(self.text_input, (self.rectinput.x+5, self.rectinput.y+5))
        pygame.draw.rect(self.screen, pygame.Color(255,255,255), self.rectinput)
        
        self.waitClick()


    def waitClick(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                # if event.type == pygame.MOUSEBUTTONDOWN:
                #     if self.text_input.collidepoint(event.pos):
                #         print("click input box")
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
        self.screen.blit(pygame.transform.scale( pygame.image.load(os.path.join(os.path.dirname(__file__), "src\\images\\presentation.webp")) ,(GetSystemMetrics(0), GetSystemMetrics(1))), [0, 0]) #met l'image d'arrière plan, et la met automatiquement a la taille de l'écran
        self.screen.blit(self.txt_surface, (self.rectinput.x+5, self.rectinput.y+5))
        pygame.draw.rect(self.screen, self.color, self.rectinput, 2)


    def scoreboard(self):
        """
        Retourne le top 10 des meilleurs score sous forme de liste
        """
        pass

    def fetch(self, username):
        """
        Récupère le joueur passé en argument, ou l'ajoute en base de donnée si il n'existe pas
        """
        # self.username = "monusername"
        # self.userid = "monuserid"
        pass

    def addScore(self, username, score):
        """
        Ajoute une entrée en base de donnée
        """

s = ScoreBoard()
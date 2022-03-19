from Data.database_handler import DataBaseHandler

class DataBase(object):
    
    def __init__(self):
        self.username = self.userid = None

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
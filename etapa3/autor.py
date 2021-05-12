class Autor(object):
    def __init__(self,nome):
        self.nome = nome
        self.media_rating = None
        self.lidos = None
        self.abandonos = None
# GETTERS
    def get_nome(self):
        return self.nome  
    def get_media(self):
        return self.media_rating 
    def get_lidos(self):
        return self.lidos
    def get_abandonos(self):
        return self.abandonos   
# SETTERS
    def set_nome(self,nome):
        self.nome = nome
    def set_media(self,media):
        self.media_rating = media
    def set_lidos(self,lidos):
        self.lidos = lidos
    def set_abandonos(self,abandonos):
        self.abandonos = abandonos
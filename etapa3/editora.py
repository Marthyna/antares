class Editora(object):
    def __init__(self,nome):
        self.nome = nome
        self.media_rating = None
# GETTERS
    def get_nome(self):
        return self.nome    
    def get_media(self):
        return self.media_rating    
# SETTERS
    def set_nome(self,nome):
        self.nome = nome
    def set_media(self,media):
        self.media_rating = media
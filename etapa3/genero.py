class Genero(object):
    def __init__(self,nome):
        self.nome = nome
# GETTERS
    def get_nome(self):
        return self.nome    
# SETTERS
    def set_nome(self,nome):
        self.nome = nome
    
    def to_dict(self):
        return {
            'nome':(self.nome).title()
        }

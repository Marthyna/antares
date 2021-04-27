import csv
import pickle

class livro:    
    def __init__(self,v0,v1,v2,v3,v4,v5,v6,v7,v8,v9,v10,v11,v12,v13,v14,v15):
        self.id_livro = v0
        self.titulo = v1
        self.isbn10 = v2
        self.idioma = v3
        self.paginas = v4
        self.ano = v5
        self.avaliacao = v6
        self.qt_avaliacoes = v7
        self.avandonos = v8
        self.relendo = v9
        self.querem_ler = v10
        self.lendo = v11
        self.leram = v12
        self.qt_mulheres = v13
        self.qt_homens = v14
        self.id_editora = v15

class editora:
    def __init__(self,v0,v1):
        self.id_editora = v0
        self.nome_editora = v1

class autor:
    def __init__(self,v0,v1):
        self.id_autor = v0
        self.nome_autor = v1

class livro_autor:
    def __init__(self,v0,v1,v2):
        self.id_livro_autor = v0
        self.id_livro = v1
        self.id_autor = v2

class genero:
    def __init__(self,v0,v1):
        self.id_genero = v0
        self.nome_genero = v1

class livro_genero:
    def __init__(self,v0,v1,v2):
        self.id_livro_genero = v0
        self.id_livro = v1
        self.id_genero = v2

fo = open("editoras.csv",'wb+')

# preencher arquivo binário das editoras
with open('livros.csv','r') as file:
    reader = csv.reader(file)
    i=0
    for row in reader:
        ed = editora(i,row[7])
        i += 1
        



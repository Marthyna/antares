from editora import Editora
from autor import Autor

class Livro(object):    
    def __init__(self,titulo,isbn10,idioma,paginas, \
                ano,avaliacao,qt_avaliacoes,abandonos,relendo, \
                queremler,lendo,leram,qt_mulheres,qt_homens,editora,autor,generos):
        self.titulo = titulo
        self.isbn10 = isbn10
        self.idioma = idioma
        self.paginas = paginas
        self.ano = ano
        self.avaliacao = avaliacao
        self.qt_avaliacoes = qt_avaliacoes
        self.abandonos = abandonos
        self.relendo = relendo
        self.querem_ler = queremler
        self.lendo = lendo
        self.leram = leram
        self.qt_mulheres = qt_mulheres
        self.qt_homens = qt_homens
        self.editora = editora
        self.autor = autor
        self.generos = generos
# GETTERS
    def get_titulo(self):
        return self.titulo
    def get_isbn10(self):
        return self.isbn10
    def get_idioma(self):
        return self.isbn10
    def get_paginas(self):
        return self.paginas
    def get_ano(self):
        return self.ano
    def get_avaliacao(self):
        return self.avaliacao
    def get_qtavaliacoes(self):
        return self.qt_avaliacoes
    def get_abandonos(self):
        return self.abandonos
    def get_relendo(self):
        return self.relendo
    def get_queremler(self):
        return self.querem_ler
    def get_lendo(self):
        return self.lendo
    def get_leram(self):
        return self.leram
    def get_qtmulheres(self):
        return self.qt_mulheres
    def get_qthomens(self):
        return self.qt_homens
    def get_editora(self):
        return self.editora
    def get_autor(self):
        return self.autor
    def get_generos(self):
        return self.generos
# SETTERS
    def set_titulo(self, titulo):
        self.titulo = titulo
    def set_isbn10(self, isbn10):
        self.isbn10 = isbn10
    def set_idioma(self, idioma):
        self.idioma = idioma
    def set_paginas(self, paginas):
        self.paginas = paginas
    def set_ano(self, ano):
        self.ano = ano
    def set_avaliacao(self, avaliacao):
        self.avaliacao = avaliacao
    def set_qtavaliacoes(self, qt_avaliacoes):
        self.qt_avaliacoes = qt_avaliacoes
    def set_abandonos(self, abandonos):
        self.abandonos = abandonos
    def set_relendo(self, relendo):
        self.relendo = relendo
    def set_queremler(self, querem_ler):
        self.querem_ler = querem_ler
    def set_lendo(self, lendo):
        self.lendo = lendo
    def set_leram(self, leram):
        self.leram = leram
    def set_qtmulheres(self, qt_mulheres):
        self.qt_mulheres = qt_mulheres
    def set_qthomens(self, qt_homens):
        self.qt_homens = qt_homens
    def set_editora(self, editora):
        self.editora = editora
    def set_autor(self, autor):
        self.autor = autor
    def set_generos(self, generos):
        self.generos = generos

    def to_dict(self):
        return {
            'Título':(self.titulo).title(),
            'Autor':(self.autor.get_nome()).title(),
            'Editora':(self.editora.get_nome()).title(),           
            'Gênero':self.generos[0],
            'Páginas':self.paginas,
            'Ano':self.ano,
            'Avaliação':self.avaliacao
        }
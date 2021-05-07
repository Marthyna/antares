class Livro(object):    
    def __init__(self,id,titulo,isbn10,idioma,paginas, \
                ano,avaliacao,qt_avaliacoes,abandonos,relendo, \
                queremler,lendo,leram,qt_mulheres,qt_homens,editora,autor,generos):
        self.id = id
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
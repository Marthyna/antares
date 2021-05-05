# bibliotecas
import csv
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle
import re

# classes da aplicação
class Livro(object):    
    def __init__(self,id,titulo,isbn10,idioma,paginas, \
                ano,avaliacao,qt_avaliacoes,abandonos,relendo, \
                queremler,lendo,leram,qt_mulheres,qt_homens,editora,autor):
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

class Editora(object):
    def __init__(self,id,nome):
        self.id = id
        self.nome = nome

class Autor(object):
    def __init__(self,id,nome):
        self.id = id
        self.nome = nome

#class Livro_autor(object):
#    def __init__(self,v0,v1,v2):
#        self.id_livro_autor = v0
#        self.id_livro = v1
#        self.id_autor = v2

class Genero(object):
    def __init__(self,id,nome):
        self.id = id
        self.nome = nome

class Livro_genero(object):
    def __init__(self,id,livro,genero):
        self.id = id
        self.livro = livro
        self.genero = genero

# limpar dados brutos
with open("books.csv",'r') as f:
    reader = csv.reader(f)
    with open("livros_limpo.csv",'w') as f1:
        writer = csv.writer(f1, delimiter=',')
        next(f) # pula o cabeçalho
        escreve = False
        for row in reader:
            # se ISBN10 != 'nan' e sem espaço em branco
            # se ano tem exat. 4 digitos
            # se paginas não tem mais que 5 dígitos e != 0
            # se avaliacao é numero
            # se qt_avaliacoes é um int
            # se abandonos é um int
            # se genero é != 'nan'
            # qt_homens é um int
            # qt_mulheres é um int
            # campos não são vazios
            for i in range(0,20):
                row[i] = row[i].lower()
                row[i] = row[i].strip()
                
            if (" " not in row[3]) \
                and (len(row[17]) >= 5) \
                and (len(row[4]) == 4) and (len(row[5]) <= 5) \
                and ("." in row[8]) \
                and (row[9].isdigit()) \
                and (row[18].isdigit()) \
                and (row[19].isdigit()):
                for i in range(0,20):
                    escrevei = False
                    if (row[i] != '') and (row[i] != ' ') and (row[i] != 'nan') \
                    and (row[i].isascii()):
                        escrevei = True
                if escrevei:
                    escreve = True
  
            if escreve:
                writer.writerow(row)

# excluir duplicados
with open("livros_limpo.csv",'r') as inp, open("livros_unicos.csv",'w') as outp:
    reader = csv.reader(inp)
    lista = []
    writer = csv.writer(outp)
    for row in reader:
        row[0] = row[0].strip()
        if row[0] not in lista: # repetição de título
            lista.append(row[0])
            writer.writerow(row)
        else:
            lista.clear()
            row[3] = row[3].strip()
            if row[3] not in lista: # repetição de isbn10
                lista.append(row[3])
                writer.writerow(row)
    lista.clear()

# preencher arquivos binários
# autores
with open('livros_unicos.csv','r') as file:
    reader = csv.reader(file)
    i = 0
    with open('autores.pkl','wb') as pkfile:
        lista = []
        for row in reader:
            autor = Autor(i,row[1])
            nome = autor.nome.strip()
            if nome not in lista:
                lista.append(nome)
                pickle.dump(autor, pkfile)
                i += 1
        lista.clear()

# generos
with open('livros_unicos.csv','r') as file:
    reader = csv.reader(file)
    i = 0
    with open('generos.pkl','wb') as pkfile:
        lista = []
        for row in reader:
            # pegar o campo de genero de um livro e separar numa lista (separar pelo '/')
            generos = row[17].split('/') 
            for genero in generos:
                # remove chars hexadecimais e espaços em branco na frente/atrás
                genero = genero.replace('\x92','')
                genero = genero.replace('\x93','')
                genero = genero.replace('\x94','')
                genero = genero.replace('\x96','')
                genero = genero.replace('\x97','')
                genero = genero.replace('\x85','')
                genero = genero.replace('\xa0','')
                genero = genero.replace('\u2800','')
                genero = genero.strip()
                # para cada item da lista de generos de um livro:
                # verificar se esse item esta na lista de todos os generos
                if (genero not in lista) and (len(genero) >= 5):
                    # se nao está, inserir na lista e escrever no arquivo binário de generos
                    lista.append(genero)
                    genero_obj = Genero(i,genero)
                    pickle.dump(genero_obj,pkfile)
                    i += 1
        lista.clear()

# editoras
with open('livros_unicos.csv','r') as file:
    reader = csv.reader(file)
    i = 0
    with open('editoras.pkl','wb') as pkfile:
        lista = []
        for row in reader:
            editora = Editora(i,row[7])
            nome = editora.nome.strip()
            if nome not in lista:
                lista.append(nome)
                pickle.dump(editora, pkfile)
                i += 1
        lista.clear()

# livros
with open('livros_unicos.csv','r') as file:
    reader = csv.reader(file)
    i = 0
    with open('livros.pkl','wb') as pkfile:
        lista = []
        for row in reader:
            #procura editora no pkfile de editoras
            livro_editora = Editora(0,'')
            with open('editoras.pkl','rb') as pkeditoras:
                while True:
                    try:
                        ed = pickle.load(pkeditoras)
                        if ed.nome == row[7]:
                            livro_editora = ed
                            break
                    except EOFError:
                        print("id editora não encontrado")
                        break
            #procura id autor no pkfile de editoras
            livro_autor = Autor(0,'')
            with open('autores.pkl','rb') as pkautores:
                while True:
                    try:
                        at = pickle.load(pkautores)
                        if at.nome == row[1]:
                            livro_autor = at
                            break
                    except EOFError:
                        print("id autor não encontrado")
                        break

            # apaga espaços em branco atrás/na frente de cada atributo
            row[0] = row[0].strip()
            row[3] = row[3].strip()
            row[6] = row[6].strip()
            row[5] = row[5].strip()
            row[4] = row[4].strip()
            row[8] = row[8].strip()
            row[9] = row[9].strip()
            row[11] = row[11].strip()
            row[12] = row[12].strip()
            row[13] = row[13].strip()
            row[14] = row[14].strip()
            row[15] = row[15].strip()
            row[19] = row[19].strip()
            row[18] = row[18].strip()

            livro = Livro(i, row[0], row[3], row[6],  \
                row[5], row[4], row[8], row[9], row[11], \
                row[12], row[13], row[14], row[15], row[19], \
                row[18],livro_editora,livro_autor)
            nome = livro.titulo

            if nome not in lista:
                lista.append(nome)
                pickle.dump(livro, pkfile)
                i += 1
        lista.clear()

# livros_generos
    
ids = nomes = []
with open('livros.pkl','rb') as pkfile:
    while True:
        try:
            lv = pickle.load(pkfile)
            print(lv.titulo,' - ',lv.autor.nome)
        except EOFError:
            break
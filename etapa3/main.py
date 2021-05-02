# bibliotecas
import csv
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle
import re

# classes da aplicação
class Livro(object):    
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

class Editora(object):
    def __init__(self,v0,v1):
        self.id_editora = v0
        self.nome_editora = v1

class Autor(object):
    def __init__(self,v0,v1):
        self.id_autor = v0
        self.nome_autor = v1

class Livro_autor(object):
    def __init__(self,v0,v1,v2):
        self.id_livro_autor = v0
        self.id_livro = v1
        self.id_autor = v2

class Genero(object):
    def __init__(self,v0,v1):
        self.id_genero = v0
        self.nome_genero = v1

class Livro_genero(object):
    def __init__(self,v0,v1,v2):
        self.id_livro_genero = v0
        self.id_livro = v1
        self.id_genero = v2

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
        
# ajeitar genero (formato:'genero/genero/genero/.../genero')
#def split_genero(texto):
#    genero = texto.split('/',1)
    # se o genero era um só um, retorna ele, senão retorna a lista
#    if len(genero) < 2:
#        return genero
#    else:
#        return (genero[1]) 

#with open("livros_unicos.csv",'r') as inp, open("livros_trim.csv",'w') as outp:
#    reader = csv.reader(inp)
#    writer = csv.writer(outp)
#    for row in reader:
#        gen = row[17]
#        if len(gen) > 100:
#            gen = split_genero(gen) # se string muito grande, trunca no segundo genero da lista
        # se split_genero retornou -1, pula esse registro
#        if gen != -1:
#            if len(gen) > 3:
#                row[17] = gen
#                writer.writerow(row)

# preencher arquivos binários
# autores
with open('livros_unicos.csv','r') as file:
    reader = csv.reader(file)
    i = 0
    with open('autores.pkl','wb') as pkfile:
        lista = []
        for row in reader:
            autor = Autor(i,row[1])
            nome = autor.nome_autor.strip()
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
                genero = genero.replace('\x94','')
                genero = genero.replace('\x96','')
                genero = genero.strip()
                genero = genero.replace('\xa0','')
                genero = genero.replace('\x93','')
                genero = genero.replace('\x97','')
                genero = genero.replace('\x92','')
                genero = genero.replace('\x85','')
                genero = genero.replace('\u2800','')
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
            nome = editora.nome_editora.strip()
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
            #procura id editora no pkfile de editoras
            id_editora = 0
            with open('editoras.pkl','rb') as pkeditoras:
                while True:
                    try:
                        ed = pickle.load(pkeditoras)
                        if ed.nome_editora == row[7]:
                            id_editora = ed.id_editora
                            break
                    except EOFError:
                        print("id não encontrado")
                        break
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
                row[18],id_editora)
            nome = livro.titulo

            if nome not in lista:
                lista.append(nome)
                pickle.dump(livro, pkfile)
                i += 1
        lista.clear()

# livros_autores
# livros_generos
    
ids = nomes = []
with open('generos.pkl','rb') as pkfile:
    while True:
        try:
            gn = pickle.load(pkfile)
            print(gn.id_genero,' - ',repr(gn.nome_genero))
        except EOFError:
            break
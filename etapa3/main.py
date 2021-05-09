# bibliotecas
import os
import csv
try:
    import cPickle as pickle
except ModuleNotFoundError:
    import pickle
from livro import Livro
from genero import Genero
from editora import Editora
from autor import Autor
from trie_livro import nodoTrie_livro
from trie_livro import TrieLivro

# -------- LIMPEZA DE DADOS BRUTOS --------
# limpar registros do arquivo csv original que estejam com campos em formato incorreto
if not os.path.exists('trim1.csv'):
    with open('books.csv','r') as f:
        reader = csv.reader(f)
        with open("trim1.csv",'w') as f1:
            writer = csv.writer(f1, delimiter=',')
            next(f) # pula o cabeçalho
            escreve = False
            for row in reader:
                # ISBN10 != 'nan' e sem espaço em branco, ano tem exat. 4 digitos
                # paginas não tem mais que 5 dígitos e != 0, avaliacao é numero
                # qt_avaliacoes é um int, abandonos é um int, genero é != 'nan'
                # qt_homens é um int, qt_mulheres é um int, campos não são vazios
                for i in range(0,20):
                    row[i] = row[i].lower()
                    row[i] = row[i].strip()
                    
                if " " not in row[3] and len(row[17]) >= 5 and len(row[4]) == 4 and len(row[5]) <= 5 \
                    and "." in row[8] and row[9].isdigit() and row[18].isdigit() and row[19].isdigit():
                    for i in range(0,20):
                        escrevei = False
                        if row[i] != '' and row[i] != ' ' and row[i] != 'nan' and row[i].isascii():
                            escrevei = True
                    if escrevei:
                        escreve = True
                if escreve:
                    writer.writerow(row)

# limpar registros duplicados
if not os.path.exists('trim2.csv'):
    with open("trim1.csv",'r') as inp:
        with open("trim2.csv",'w') as outp:
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

# --------- PREENCHIMENTO DE ARQUIVOS BINÁRIOS -----------
# autores
if not os.path.exists('autores.pkl'):
    with open('trim2.csv','r') as file:
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
        
# editoras
if not os.path.exists('editoras.pkl'):
    with open('trim2.csv','r') as file:
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

# generos e livros
if not os.path.exists('generos.pkl') and not os.path.exists('livros.pkl'):
    with open('trim2.csv','r') as file:
        reader = csv.reader(file)
        lista = lista_generos = []
        i = j = 0
        with open('generos.pkl','wb') as pkgenero:
            with open('livros.pkl','wb') as pklivros:
                lista_generos_livro = []
                for row in reader:
                    # pegar o campo de genero de um livro e separar numa lista (separar pelo '/')
                    generos = row[17].split('/') 
                    for genero in generos:
                        # remove chars hexadecimais e espaços em branco na frente/atrás
                        genero = (((genero.replace('\x92','')).replace('\x93','')).replace('\x94','')).replace('\x96','')
                        genero = (((genero.replace('\x97','')).replace('\x85','')).replace('\xa0','')).replace('\u2800','')
                        genero = genero.strip()
                        # se genero tem tamanho adequado
                        if len(genero) >= 5:
                            # e não está na lista geral de gêneros, inserir e escrever no arquivo binário
                            if genero not in lista_generos:
                                lista_generos.append(genero)
                                genero_obj = Genero(i,genero)
                                pickle.dump(genero_obj,pkgenero)
                                i += 1
                            # se não está na lista de gêneros do livro atual, inserir
                            if genero not in lista_generos_livro:
                                lista_generos_livro.append(genero)

                    if lista_generos_livro != []:
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
                        for k in range(19):
                            row[k] = row[k].strip()
                        # cria objeto Livro
                        livro = Livro(j, row[0], row[3], row[6], row[5], row[4], row[8], row[9], row[11], \
                            row[12], row[13], row[14], row[15], row[19], row[18],livro_editora,livro_autor,lista_generos_livro)
                        nome = livro.titulo
                        # insere no arquivo pickle
                        if nome not in lista:
                            lista.append(nome)
                            pickle.dump(livro, pklivros)
                            j += 1
                    lista_generos_livro.clear()
        lista.clear()
        lista_generos.clear()

 
# ---------- DEFINIÇÃO DE FUNÇÕES ----------- 
# Dado um objeto, carrega o arquivo binário dele numa Trie
def carregaTrie(objeto):
    if isinstance(objeto,Livro):
        t = TrieLivro()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    livro = pickle.load(pklivros)
                    t.insere(str(livro.id),livro)
                except EOFError:
                    break
    #elif isinstance(objeto,Autor):
     
    #elif isinstance(objeto,Editora):
     
    #elif isinstance(objeto,Genero):

livro = Livro(0,'','','',0,0,0,0,0,0,0,0,0,0,0,None,None,None)
carregaTrie(livro)
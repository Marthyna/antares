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
from trie import nodoTrie
from trie import Trie

# alfabeto usada na indexação da Trie
alfabeto = ['a','á','ã','â','à','ä','b','c','d','e','ë','é','ê','f','g','h','i',\
            'í','î','ï','j','k','l','m','n','o','ö','ó','õ','ô','p','q','r','s',\
            't','u','ú','ü','v','w','x','y','z','0','1','2','3','4','5','6','7','8',\
            '9','(',')','-','.',',',' ','!','?','@','#','%','&','*','+',\
            "'",'/','"','|',':',';','[',']','ª','º','°','²','ø']

# -------- LIMPEZA DE DADOS BRUTOS --------
# limpar registros do arquivo csv original que estejam com campos em formato incorreto
if not os.path.exists('trim1.csv'): # se já existe o arquivo
    with open('books.csv','r') as f: # abre o csv bruto
        reader = csv.reader(f) 
        with open("trim1.csv",'w') as f1: # cria o arquivo para a limpeza
            writer = csv.writer(f1, delimiter=',') # usa , como delimitador
            next(f) # pula o cabeçalho
            escreve = False 
            for row in reader: # para cada linha no arquivo bruto
                # percorre cada coluna
                for i in range(0,20):
                    row[i] = row[i].lower() # formata pra minúsculo
                    row[i] = row[i].strip() # apaga espaços em branco na frente e atrás
                    
                # se ISBN10 não tem espaços em branco, gênero tem 5 letras ou mais,
                # ano tem 4 dígitos, páginas tem até 5 digitos, rating é um float,
                # e avaliações, abandonos, quero ler, leram, lendo, qt_homens e qt_mulheres são dígitos
                if " " not in row[3] and len(row[17]) >= 5 and len(row[4]) == 4 and len(row[5]) <= 5 \
                    and "." in row[8] and row[9].isdigit() and row[18].isdigit() and row[19].isdigit() \
                    and row[11].isdigit() and row[12].isdigit() and row[13].isdigit() and row[14].isdigit() \
                    and row[15].isdigit():
                    # para cada coluna
                    for i in range(0,20):
                        escrevei = False
                        # Se não é uma string só com espaços, nem vazia, nem 'nan', nem contém chars não ascii
                        if row[i].isspace()==False and row[i] != '' and row[i] != 'nan' and row[i].isascii():
                            escrevei = True # flag de escrita é true
                    # se todas as colunas da linha estão bem formatadas, escreve a linha no arquivo de limpeza
                    if escrevei:
                        escreve = True
                if escreve:
                    writer.writerow(row)

# limpar registros duplicados
if not os.path.exists('trim2.csv'): # checa se arquivo já existe
    with open("trim1.csv",'r') as inp:
        with open("trim2.csv",'w') as outp:
            reader = csv.reader(inp)
            lista = []
            writer = csv.writer(outp)
            # para cada linha do arquivo da primeira limpeza
            for row in reader:
                row[0] = row[0].strip() # remove espaços em branco no fim/começo
                if row[0] not in lista: # checa se há repetição de título
                    lista.append(row[0]) # se não, adiciona título na lista de títulos
                    writer.writerow(row) # escreve linha
                else:
                    lista.clear() # reinicializa lista
                    row[3] = row[3].strip()
                    if row[3] not in lista: # checa se há repetição de isbn10
                        lista.append(row[3]) 
                        writer.writerow(row)
            lista.clear()

# --------- PREENCHIMENTO DE ARQUIVOS BINÁRIOS -----------
# Autores
if not os.path.exists('autores.pkl'): # checa se arquivo já existe
    with open('trim2.csv','r') as file:
        reader = csv.reader(file)
        with open('autores.pkl','wb') as pkfile:
            lista = []
            # para cada linha no arquivo csv limpo
            for row in reader:
                autor = Autor(row[1]) # cria objeto autor
                nome = autor.get_nome().strip() # limpa espaços em branco na frente/atrás
                # se nome não foi adicionado ainda e não é uma string vazia
                if nome not in lista and len(nome)>0:
                    lista.append(nome) # adiciona na lista
                    pickle.dump(autor, pkfile) # e no arquivo pickle de autores
            lista.clear()
        
# Editoras
if not os.path.exists('editoras.pkl'):
    with open('trim2.csv','r') as file:
        reader = csv.reader(file)
        with open('editoras.pkl','wb') as pkfile:
            lista = []
            for row in reader:
                editora = Editora(row[7])
                nome = editora.get_nome().strip()
                if nome not in lista:
                    lista.append(nome)
                    pickle.dump(editora, pkfile)
            lista.clear()

# Gêneros e livros
# checa por existência dos arquivos
if not os.path.exists('generos.pkl') or not os.path.exists('livros.pkl'):
    with open('trim2.csv','r') as file:
        reader = csv.reader(file)
        lista = lista_generos = []
        with open('generos.pkl','wb') as pkgenero:
            with open('livros.pkl','wb') as pklivros:
                lista_generos_livro = []
                # para cada linha no arquivo csv limpo
                for row in reader:
                    # pegar o campo de genero de um livro e separar numa lista pelo '/'
                    generos = row[17].split('/') 
                    # para cada item na lista de gêneros
                    for genero in generos:
                        # remover chars hexadecimais e espaços em branco na frente/atrás
                        genero = (((genero.replace('\x92','')).replace('\x93','')).replace('\x94','')).replace('\x96','')
                        genero = (((genero.replace('\x97','')).replace('\x85','')).replace('\xa0','')).replace('\u2800','')
                        genero = genero.strip()
                        # se genero tem tamanho adequado
                        if len(genero) >= 5:
                            # e não está na lista geral de gêneros, inserir e escrever no arquivo binário
                            if genero not in lista_generos:
                                lista_generos.append(genero)
                                genero_obj = Genero(genero)
                                pickle.dump(genero_obj,pkgenero)
                            # se não está na lista de gêneros do livro atual, inserir
                            if genero not in lista_generos_livro:
                                lista_generos_livro.append(genero)

                    if lista_generos_livro != []: # se a lista de generos do livro não é vazia
                        # procura editora no pkfile de editoras
                        livro_editora = None
                        with open('editoras.pkl','rb') as pkeditoras:
                            while True:
                                try:
                                    ed = pickle.load(pkeditoras)
                                    nome = ed.get_nome()
                                    if nome == row[7]:
                                        livro_editora = ed
                                        break
                                except EOFError:
                                    print("Editora não encontrada")
                                    break
                        # procura autor no pkfile de autores
                        livro_autor = None
                        with open('autores.pkl','rb') as pkautores:
                            while True:
                                try:
                                    at = pickle.load(pkautores)
                                    nome = at.get_nome()
                                    if nome == row[1]:
                                        livro_autor = at
                                        break
                                except EOFError:
                                    print("autor não encontrado")
                                    break
                        # apaga espaços em branco atrás/na frente de cada atributo
                        for k in range(19):
                            row[k] = row[k].strip()
                        # cria objeto Livro
                        livro = Livro(row[0], row[3], row[6], row[5], row[4], row[8], row[9], row[11], \
                            row[12], row[13], row[14], row[15], row[19], row[18],livro_editora,livro_autor,lista_generos_livro)
                        nome = livro.get_titulo()
                        # insere no arquivo pickle
                        if nome not in lista:
                            lista.append(nome)
                            pickle.dump(livro, pklivros)
                    lista_generos_livro.clear()
        lista.clear()
        lista_generos.clear()

 
# ---------- DEFINIÇÃO DE FUNÇÕES BUSCA/ATUALIZAÇÃO/DELEÇÃO/INSERÇÃO ----------- 
# Dada uma classe, carrega o arquivo binário dessa classe numa Trie, e a retorna
def carregaTrie(classe):
    t = Trie() # Cria nova Trie
    if classe == 0: #Livro
        # Abre arquivo binário de livros e insere todos os livros na Trie
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    livro = pickle.load(pklivros)
                    t.insere(livro)
                except EOFError:
                    break
        return t
    elif classe == 1: #Autor
        with open('autores.pkl','rb') as pkautores:
            while True:
                try:
                    autor = pickle.load(pkautores)
                    t.insere(autor)
                except EOFError:
                    break
        return t
    elif classe == 2: #Editora
        with open('editoras.pkl','rb') as pkeditoras:
            while True:
                try:
                    editora = pickle.load(pkeditoras)
                    t.insere(editora)
                except EOFError:
                    break
        return t
    elif classe == 3: #Genero
        with open('generos.pkl','rb') as pkgeneros:
            while True:
                try:
                    genero = pickle.load(pkgeneros)
                    t.insere(genero)
                except EOFError:
                    break
        return t

# Função recursiva auxiliar que, dada a raiz de uma Trie, retorna lista com os elementos dela
def listar(raiz):
    l = []
    if raiz.fimPalavra: # se raiz é folha
        l.append(raiz.objeto) # adiciona seu objeto na lista
    else:
        for nodo in raiz.filhos: # se raiz tem filhos
            if nodo != None: # para cada filho não nulo, aplicar listar() recursivamente
                l = l + listar(nodo)
    return l

# Busca de registros em arquivo: dada uma chave e uma classe, 
# busca essa chave na Trie dessa classe
def buscar(chave, classe):
    t = carregaTrie(classe) # carrega a Trie dessa classe
    chave = chave.lower() # formata para só minúsculas
    if classe == 0: # Livro
        livro = t.busca(chave) # busca o livro na Trie
        return livro
    if classe == 1: # Autor
        autor = t.busca(chave)
        return autor
    if classe == 2: # Editora
        editora = t.busca(chave)
        return editora
    if classe == 3: # Genero
        genero = t.busca(chave)
        return genero

# Inserção de novo registro em um arquivo pickle
# Retorna true se for bem sucedida e false caso contrário
def inserir(objeto,classe):
    t = carregaTrie(classe)
    if classe == 0: # Livro
        chave = objeto.get_titulo()
        # se a busca por esse livro na Trie retorna None, insere no arquivo
        if t.busca(chave) == None:
            with open('livros.pkl','ab') as pklivros:
                pickle.dump(objeto, pklivros)
            return True
        else:
            return False
    elif classe == 1: # Autor
        chave = objeto.get_nome()
        if t.busca(chave) == None:
            with open('autores.pkl','ab') as pkautores:
                pickle.dump(objeto, pkautores)
            return True
        else:
            return False
    elif classe == 2: # Editora
        chave = objeto.get_nome()
        if t.busca(chave) == None:
            with open('editoras.pkl','ab') as pkeditoras:
                pickle.dump(objeto, pkeditoras)
            return True
        else:
            return False
    elif classe == 3: # Gênero
        chave = objeto.get_nome()
        if t.busca(chave) == None:
            with open('generos.pkl','ab') as pkgeneros:
                pickle.dump(objeto, pkgeneros)
            return True
        else:
            return False
    
# função auxiliar para atualizar o arquivo pickle dada uma lista de registros
def atualizaPickle(objeto,lista):
    if isinstance(objeto,Livro):
        open("livros.pkl", "w").close() # esvazia arquivo
        with open('livros.pkl','ab') as pklivros:
            for i in lista: # para cada elemento na lista
                pickle.dump(i, pklivros) # escreve elemento no arquivo
    if isinstance(objeto,Autor):
        open("autores.pkl", "w").close()
        with open('autores.pkl','ab') as pkautores:
            for i in lista:
                pickle.dump(i, pkautores)
    if isinstance(objeto,Editora):
        open("editoras.pkl", "w").close()
        with open('editoras.pkl','ab') as pkeditoras:
            for i in lista:
                pickle.dump(i, pkeditoras)
    if isinstance(objeto,Genero):
        open("generos.pkl", "w").close()
        with open('generos.pkl','ab') as pkgeneros:
            for i in lista:
                pickle.dump(i, pkgeneros)

# Atualização de registro em arquivo
# Retorna true se for bem sucedida e false caso contrário
def atualizar(chave_velho,objeto_novo,classe):
    chave_velho = chave_velho.lower() # formata chave velha pra minúsculo
    t = carregaTrie(classe) # carrega trie da classe
    if classe == 0: # se for Livro
        velho = t.busca(chave_velho) # busca o registro desatualizado 
        if velho != None: # se achar
            sucesso = t.atualiza(velho,objeto_novo) # atualiza trie com livro atualizado
            if sucesso:
                lista = listar(t.raiz) # lista elementos da trie atualizada
                atualizaPickle(objeto_novo,lista) # atualiza pickle file
                return True
            else:
                return False
        else:
            return False
    else: # Autor/Editora/Gênero
        velho = t.busca(chave_velho) 
        if velho != None:
            sucesso = t.atualiza(velho,objeto_novo)
            if sucesso:
                lista = listar(t.raiz)
                atualizaPickle(velho,lista)
                return True
            else:
                return False
        else:
            return False

# Deleção de um registro em arquivo
# Retorna true se for bem sucedida e false caso contrário
def deletar(objeto,classe):
    t = carregaTrie(classe)
    # se a deleção retorna True, deu certo, atualiza o arquivo Pickle
    if t.deleta(objeto):
        lista = listar(t.raiz)
        atualizaPickle(objeto,lista)
        return True
    else:
        return False

# ---------- DEFINIÇÃO DE FUNÇÕES DE ORDENAÇÃO E CLASSIFICAÇÃO ----------- 
# Dados uma classe, um atributo e uma ordem, 
# ordena os objetos dessa classe de acordo com o atributo e a ordem
def sort(classe,atributo,ordem):
    # livros
        # Por ano
            anos = []
            t_ano = Trie()
            # carregar trie usando ano
            # para cada livro, inserir ele na lista do nodo de ano correspondente
            with open('livros.pkl','rb') as pklivros:
                lv = pklivros.load(pklivros)
                # se ano ainda não foi inserido, insere
                if lv.ano not in anos:
                    anos.append(lv.ano)
                    t_ano.insere_ano(lv.ano,lv)
                # se já foi, acha o nodo desse ano na Trie e insere o livro na lista desse nodo
                else:
                    t_ano.atualiza_ano(lv.ano,lv.ano,lv)
            # Crescente
            # percorrer Trie da esquerda pra direita, listando todos os livros em cada nodo


            # Decrescente
            # percorrer Trie da direita pra esquerda

        # Por nota de avaliação
            # Crescente

            # Decrescente

        # Qt Leitores
            # Crescente

            # Decrescente

        # Qt páginas
            # Crescente

            # Decrescente

        # Qt mulheres
            # Crescente

            # Decrescente

        # Qt homens
            # Crescente

            # Decrescente

        # abandonos
            # Crescente

            # Decrescente

        # releituras
            # Crescente

            # Decrescente
    # autores
        # por média das avaliações dos seus livros
            # crescente

            # Decrescente
        # qt livros lidos
            # crescente

            # Decrescente
        # qt abandonados
            # crescente

            # Decrescente
    # editoras
        # por média das avaliações dos seus livros
            # crescente

            # Decrescente
        # qt livros lidos
            # crescente

            # Decrescente
        # qt abandonados
            # crescente

            # Decrescente

# Dados um autor, um atributo e uma ordem, listar as obras desse autor
# de acordo com o atributo e na dada ordem
#def listarAutor(autor,atributo,ordem):
    # por ano
        # crescente

        # decrescente

    # avaliação
        # crescente

        # decrescente

    # leitores
        # crescente

        # decrescente

    # páginas
        # crescente

        # decrescente

    # mulheres
        # crescente

        # decrescente

    # homens
        # crescente

        # decrescente

    # abandonos
        # crescente

        # decrescente

    # releituras
        # crescente

        # decrescente
        

# Dados uma editora, um atributo e uma ordem, listar as obras dessa editora
# de acordo com o atributo e na dada ordem
#def listarEditora(editora,atributo,ordem):
    # por ano
        # crescente

        # decrescente

    # avaliação
        # crescente

        # decrescente

    # leitores
        # crescente

        # decrescente

    # páginas
        # crescente

        # decrescente

    # mulheres
        # crescente

        # decrescente

    # homens
        # crescente

        # decrescente

    # abandonos
        # crescente

        # decrescente

    # releituras
        # crescente

        # decrescente


# Dados um gênero, um atributo e uma ordem, listar as obras desse gênero
# de acordo com o atributo e na dada ordem
#def listarGenero(genero,atributo,ordem):
    # mais lidos

    # melhor avaliados

    # mais abandonos

    # mais relidos

    # maior numero de paginas

    # mais leitoras

    # mais 

# Listar elementos em dada ordem
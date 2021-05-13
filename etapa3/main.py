# bibliotecas
import os
import csv
import pickle
import pandas as pd
from livro import Livro
from genero import Genero
from editora import Editora
from autor import Autor
from trie import Trie

# alfabeto usada na indexação da Trie
alfabeto = ['a','á','ã','â','à','ä','b','c','d','e','ë','é','ê','f','g','h','i',\
            'í','î','ï','j','k','l','m','n','o','ö','ó','õ','ô','p','q','r','s',\
            't','u','ú','ü','v','w','x','y','z','0','1','2','3','4','5','6','7','8',\
            '9','(',')','-','.',',',' ','!','?','@','#','%','&','*','+',\
            "'",'/','"','|',':',';','[',']','ª','º','°','²','ø']

# -------- LIMPEZA DE DADOS BRUTOS --------
# limpar registros do arquivo csv original que estejam com campos em formato incorreto
def carregar_dados():
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
    if classe == 'livro': 
        # Abre arquivo binário de livros e insere todos os livros na Trie
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    livro = pickle.load(pklivros)
                    t.insere(livro)
                except EOFError:
                    break
        return t
    elif classe == 'autor': 
        with open('autores.pkl','rb') as pkautores:
            while True:
                try:
                    autor = pickle.load(pkautores)
                    t.insere(autor)
                except EOFError:
                    break
        return t
    elif classe == 'editora': 
        with open('editoras.pkl','rb') as pkeditoras:
            while True:
                try:
                    editora = pickle.load(pkeditoras)
                    t.insere(editora)
                except EOFError:
                    break
        return t
    elif classe == 'genero':
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
    if raiz.get_fimPalavra(): # se raiz é folha
        # se objeto for uma lista, une com a lista atual
        if isinstance(raiz.get_objeto(), list):
            l = l + raiz.get_objeto()
        # se objeto for livro/autor/editora/gênero, adiciona na lista atual
        else:
            l.append(raiz.get_objeto()) # adiciona seu objeto na lista
    else:
        for nodo in raiz.get_filhos(): # se raiz tem filhos
            if nodo != None: # para cada filho não nulo, aplicar listar() recursivamente
                l = l + listar(nodo)
    return l

# Busca de registros em arquivo: dada uma chave e uma classe, 
# busca essa chave na Trie dessa classe
def buscar(chave, classe):
    t = carregaTrie(classe) # carrega a Trie dessa classe
    chave = chave.lower() # formata para só minúsculas
    if classe == 'livro': 
        livro = t.busca(chave) # busca o livro na Trie
        return livro
    if classe == 'autor':
        autor = t.busca(chave)
        return autor
    if classe == 'editora':
        editora = t.busca(chave)
        return editora
    if classe == 'genero':
        genero = t.busca(chave)
        return genero

# Inserção de novo registro em um arquivo pickle
# Retorna true se for bem sucedida e false caso contrário
def inserir(objeto,classe):
    t = carregaTrie(classe)
    if classe == 'livro': 
        chave = objeto.get_titulo()
        # se a busca por esse livro na Trie retorna None, insere no arquivo
        if t.busca(chave) == None:
            with open('livros.pkl','ab') as pklivros:
                pickle.dump(objeto, pklivros)
            return True
        else:
            return False
    elif classe == 'autor':
        chave = objeto.get_nome()
        if t.busca(chave) == None:
            with open('autores.pkl','ab') as pkautores:
                pickle.dump(objeto, pkautores)
            return True
        else:
            return False
    elif classe == 'editora':
        chave = objeto.get_nome()
        if t.busca(chave) == None:
            with open('editoras.pkl','ab') as pkeditoras:
                pickle.dump(objeto, pkeditoras)
            return True
        else:
            return False
    elif classe == 'genero':
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
    if classe == 'livro':
        velho = t.busca(chave_velho) # busca o registro desatualizado 
        if velho != None: # se achar
            sucesso = t.atualiza(velho,objeto_novo) # atualiza trie com livro atualizado
            if sucesso:
                lista = listar(t.get_raiz()) # lista elementos da trie atualizada
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
                lista = listar(t.get_raiz())
                atualizaPickle(velho,lista)
                return True
            else:
                return False
        else:
            return False

# Deleção de um registro em arquivo
# Retorna true se for bem sucedida e false caso contrário
def deletar(objeto,classe):
    if classe == 'autor':
        livros = [] # inicializa lista de livros desse autor
        nome = objeto.get_nome() 
        with open('livros.pkl','rb') as pklivros: # abre arquivo de livros
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == nome: # se o livro lido é desse autor
                        livros.append(lv) # insere ele na lista
                except EOFError:
                    break
        for i in livros: # para cada livro na lista
            deletar(i,'livro') # deleta do arquivo
    elif classe == 'editora':
        livros = []
        nome = objeto.get_nome()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == nome:
                        livros.append(lv)
                except EOFError:
                    break
        for i in livros:
            deletar(i,'livro')
    elif classe == 'genero':
        livros = []
        nome = objeto.get_nome()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if nome in lv.get_generos():
                        livros.append(lv)
                except EOFError:
                    break
        for i in livros:
            deletar(i,'livro')
    # as etapas acima só são efetuadas caso o objeto não seja um livro, se for, só deleta ele
    t = carregaTrie(classe)
    # se a deleção retorna True, deu certo, atualiza o arquivo Pickle
    if t.deleta(objeto):
        lista = listar(t.get_raiz())
        atualizaPickle(objeto,lista)
        return True
    else:
        return False


# ---------- DEFINIÇÃO DE FUNÇÕES DE ORDENAÇÃO E CLASSIFICAÇÃO ----------- 
# Dados uma classe, um atributo e uma ordem, 
# ordena os objetos dessa classe de acordo com o atributo e a ordem
def sort(classe,atributo,ordem):
    # livros
    if classe == 'livro':
        # Por ano
        if atributo == 'ano':
            anos = []
            t_ano = Trie()
            # carregar trie usando ano
            # para cada livro, inserir ele na lista do nodo de ano correspondente
            with open('livros.pkl','rb') as pklivros:
                while True:
                    try:
                        lv = pickle.load(pklivros)
                        # se ano ainda não foi inserido, insere
                        if lv.get_ano() not in anos:
                            anos.append(lv.ano)
                            t_ano.insere_sort(lv.get_ano(),lv)
                        # se já foi, acha o nodo desse ano na Trie e insere o livro na lista desse nodo
                        else:
                            t_ano.atualiza_sort(lv.get_ano(),lv)
                    except EOFError:
                        break
            # percorrer Trie e listar todos os livros em cada nodo        
            lista = listar(t_ano.get_raiz())                
            # se for Decrescente, retornar lista reversa, senão retornar a normal
            if ordem == 'd':
                lista.reverse()
            return lista

        # Por nota de avaliação
        if atributo == 'rating':
            ratings = []
            t_rate = Trie()
            # carregar trie usando rating
            # para cada livro, inserir ele na lista do nodo de rating correspondente
            with open('livros.pkl','rb') as pklivros:
                while True:
                    try:
                        lv = pickle.load(pklivros)
                        # se rating ainda não foi inserido, insere
                        if lv.get_avaliacao() not in ratings:
                            ratings.append(lv.get_avaliacao())
                            t_rate.insere_sort(lv.get_avaliacao(),lv)
                        # se já foi, acha o nodo desse rating na Trie e insere o livro na lista desse nodo
                        else:
                            t_rate.atualiza_sort(lv.get_avaliacao(),lv)
                    except EOFError:
                        break
            # percorrer Trie e listar todos os livros em cada nodo        
            lista = listar(t_rate.get_raiz())                
            # se for Decrescente, retornar lista reversa, senão retornar a normal
            if ordem == 'd':
                lista.reverse()
            return lista

        # Quantidade de pessoas lendo
        if atributo == 'lendo':
            # carrega lista a partir da Trie de livros
            t = carregaTrie('livro')
            l = listar(t.get_raiz())
            # ordena essa lista de acordo com o atributo
            newlist = sorted(l, key=lambda x: int(x.lendo), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.lendo), reverse=True)
            return newlist
        # Qt páginas
        if atributo == 'paginas':
            t = carregaTrie('livro')
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.paginas), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.paginas), reverse=True)
            return newlist
        # Qt mulheres
        if atributo == 'mulheres':
            t = carregaTrie('livro')
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.qt_mulheres), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.qt_mulheres), reverse=True)
            return newlist
        # Qt homens
        if atributo == 'homens':
            t = carregaTrie('livro')
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.qt_homens), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.qt_homens), reverse=True)
            return newlist
        # abandonos
        if atributo == 'abandonos':
            t = carregaTrie('livro')
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.abandonos), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.abandonos), reverse=True)
            return newlist
        # releituras
        if atributo == 'relendo':
            t = carregaTrie('livro')
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.relendo), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.relendo), reverse=True)
            return newlist
    # autores
    if classe == 'autor': 
        # por média das avaliações dos seus livros
        if atributo == 'media_ratings': 
            t = Trie()
            # para cada autor no arquivo de autores
            with open('autores.pkl','rb') as pkautores:
                while True:
                    try:
                        at = pickle.load(pkautores)
                        soma_ratings = qt_livros = media = 0
                        # lista os livros desse autor, e vai somando a avaliação de cada um em 'soma'
                        with open('livros.pkl','rb') as pklivros:
                            while True:
                                try:
                                    lv = pickle.load(pklivros)
                                    if lv.get_autor().get_nome() == at.get_nome():
                                        soma_ratings += float(lv.get_avaliacao())
                                        qt_livros += 1
                                except EOFError:
                                    break
                        # se foi achado ao menos um livro desse autor, calcula a média das avaliações
                        if qt_livros != 0:
                            media = soma_ratings / qt_livros
                        at.set_media(media)
                        t.insere(at)
                    except EOFError:
                        break
            # lista todos os autores e ordena pelo atributo
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.get_media()), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.get_media()), reverse=True)
            return newlist
  
        # qt livros lidos
        if atributo == 'lidos':
            t = Trie()
            with open('autores.pkl','rb') as pkautores:
                while True:
                    try:
                        at = pickle.load(pkautores)
                        lidos = 0
                        with open('livros.pkl','rb') as pklivros:
                            while True:
                                try:
                                    lv = pickle.load(pklivros)
                                    if lv.get_autor().get_nome() == at.get_nome():
                                        lidos += int(lv.get_leram())
                                except EOFError:
                                    break
                        at.set_lidos(lidos)
                        t.insere(at)
                    except EOFError:
                        break
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.get_lidos()), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.get_lidos()), reverse=True)
            return newlist
            
        # qt abandonados
        if atributo == 'abandonos': 
            t = Trie()
            with open('autores.pkl','rb') as pkautores:
                while True:
                    try:
                        at = pickle.load(pkautores)
                        abandonos = 0
                        with open('livros.pkl','rb') as pklivros:
                            while True:
                                try:
                                    lv = pickle.load(pklivros)
                                    if lv.get_autor().get_nome() == at.get_nome():
                                        abandonos += int(lv.get_abandonos())
                                except EOFError:
                                    break
                        at.set_abandonos(abandonos)
                        t.insere(at)
                    except EOFError:
                        break
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.get_abandonos()), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.get_abandonos()), reverse=True)
            return newlist

    # editoras
    elif classe == 'editora': 
        # por média das avaliações dos seus livros
        if atributo == 'media_ratings': 
            t = Trie()
            with open('editoras.pkl','rb') as pkeditoras:
                while True:
                    try:
                        ed = pickle.load(pkeditoras)
                        soma_ratings = qt_livros = media = 0
                        with open('livros.pkl','rb') as pklivros:
                            while True:
                                try:
                                    lv = pickle.load(pklivros)
                                    if lv.get_editora().get_nome() == ed.get_nome():
                                        soma_ratings += float(lv.get_avaliacao())
                                        qt_livros += 1
                                except EOFError:
                                    break
                        if qt_livros != 0:
                            media = soma_ratings / qt_livros
                        ed.set_media(media)
                        t.insere(ed)
                    except EOFError:
                        break
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.get_media()), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.get_media()), reverse=True)
            return newlist
  
        # qt livros lidos
        if atributo == 'lidos': 
            t = Trie()
            with open('editoras.pkl','rb') as pkeditoras:
                while True:
                    try:
                        ed = pickle.load(pkeditoras)
                        lidos = 0
                        with open('livros.pkl','rb') as pklivros:
                            while True:
                                try:
                                    lv = pickle.load(pklivros)
                                    if lv.get_editora().get_nome() == ed.get_nome():
                                        lidos += int(lv.get_leram())
                                except EOFError:
                                    break
                        ed.set_lidos(lidos)
                        t.insere(ed)
                    except EOFError:
                        break
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.get_lidos()), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.get_lidos()), reverse=True)
            return newlist
            
        # qt abandonados
        if atributo == 'abandonos':
            t = Trie()
            with open('editoras.pkl','rb') as pkeditoras:
                while True:
                    try:
                        ed = pickle.load(pkeditoras)
                        abandonos = 0
                        with open('livros.pkl','rb') as pklivros:
                            while True:
                                try:
                                    lv = pickle.load(pklivros)
                                    if lv.get_editora().get_nome() == ed.get_nome():
                                        abandonos += int(lv.get_abandonos())
                                except EOFError:
                                    break
                        ed.set_abandonos(abandonos)
                        t.insere(ed)
                    except EOFError:
                        break
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.get_abandonos()), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.get_abandonos()), reverse=True)
            return newlist

# Dados um autor, um atributo e uma ordem, listar as obras desse autor
# de acordo com o atributo e na dada ordem
def listarPorAutor(autor,atributo,ordem):
    # por ano
    if atributo == 'ano':
        anos = []
        t = Trie()
        # carregar trie usando ano
        # para cada livro, inserir ele na lista do nodo de ano correspondente
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
                        # se ano ainda não foi inserido, insere
                        if lv.get_ano() not in anos:
                            anos.append(lv.ano)
                            t.insere_sort(lv.get_ano(),lv)
                        # se já foi, acha o nodo desse ano na Trie e insere o livro na lista desse nodo
                        else:
                            t.atualiza_sort(lv.get_ano(),lv)
                except EOFError:
                    break
        # percorrer Trie e listar todos os livros em cada nodo        
        lista = listar(t.get_raiz())                
        # se for Decrescente, retornar lista reversa, senão retornar a normal
        if ordem == 'd':
            lista.reverse()
        return lista

    # avaliação
    if atributo == 'rating':
        t = Trie()
        ratings = []
        # insere cada livro desse autor numa trie cuja chave é a avaliação
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
                        if lv.get_avaliacao() not in ratings:
                            ratings.append(lv.get_avaliacao())
                            t.insere_sort(lv.get_avaliacao(),lv)
                        else:
                            t.atualiza_sort(lv.get_avaliacao(), lv)
                except EOFError:
                    break   
        lista = listar(t.get_raiz())                
        if ordem == 'd':
            lista.reverse()
        return lista

    # leitores
    if atributo == 'lidos':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.leram), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.leram), reverse=True)
        return newlist

    # páginas
    if atributo == 'paginas':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.paginas), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.paginas), reverse=True)
        return newlist

    # mulheres
    if atributo == 'mulheres':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.qt_mulheres), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.qt_mulheres), reverse=True)
        return newlist

    # homens
    if atributo == 'homens':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.qt_homens), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.qt_homens), reverse=True)
        return newlist

    # abandonos
    if atributo == 'abandonos':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.abandonos), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.abandonos), reverse=True)
        return newlist

    # releituras
    if atributo == 'relendo':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.relendo), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.relendo), reverse=True)
        return newlist
        
# Dados uma editora, um atributo e uma ordem, listar as obras dessa editora
# de acordo com o atributo e na dada ordem
def listarPorEditora(editora,atributo,ordem):
    # por ano
    if atributo == 'ano':
        anos = []
        t = Trie()
        # carregar trie usando ano
        # para cada livro, inserir ele na lista do nodo de ano correspondente
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == editora:
                        # se ano ainda não foi inserido, insere
                        if lv.get_ano() not in anos:
                            anos.append(lv.ano)
                            t.insere_sort(lv.get_ano(),lv)
                        # se já foi, acha o nodo desse ano na Trie e insere o livro na lista desse nodo
                        else:
                            t.atualiza_sort(lv.get_ano(),lv)
                except EOFError:
                    break
        # percorrer Trie e listar todos os livros em cada nodo        
        lista = listar(t.get_raiz())                
        # se for Decrescente, retornar lista reversa, senão retornar a normal
        if ordem == 'd':
            lista.reverse()
        return lista

    # avaliação
    if atributo == 'rating':
        t_rate = Trie()
        ratings = []
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == editora:
                        if lv.get_avaliacao() not in ratings:
                            ratings.append(lv.get_avaliacao())
                            t_rate.insere_sort(lv.get_avaliacao(),lv)
                        else:
                            t_rate.atualiza_sort(lv.get_avaliacao(), lv)
                except EOFError:
                    break       
        lista = listar(t_rate.get_raiz())                
        if ordem == 'd':
            lista.reverse()
        return lista

    # leitores
    if atributo == 'lidos':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == editora:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.leram), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.leram), reverse=True)
        return newlist

    # páginas
    if atributo == 'paginas':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == editora:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.paginas), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.paginas), reverse=True)
        return newlist

    # mulheres
    if atributo == 'mulheres':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == editora:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.qt_mulheres), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.qt_mulheres), reverse=True)
        return newlist

    # homens
    if atributo == 'homens':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == editora:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.qt_homens), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.qt_homens), reverse=True)
        return newlist

    # abandonos
    if atributo == 'abandonos':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == editora:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.abandonos), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.abandonos), reverse=True)
        return newlist

    # releituras
    if atributo == 'relendo':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_editora().get_nome() == editora:
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.relendo), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.relendo), reverse=True)
        return newlist

# Dados um gênero, um atributo e uma ordem, listar as obras desse gênero
# de acordo com o atributo e na dada ordem
def listarPorGenero(genero,atributo,ordem):
    # mais lidos
    if atributo == 'lidos':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if genero in lv.get_generos():
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.leram), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.leram), reverse=True)
        return newlist

    # melhor avaliados
    if atributo == 'rating':
        t_rate = Trie()
        ratings = []
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if genero in lv.get_generos():
                        if lv.get_avaliacao() not in ratings:
                            ratings.append(lv.get_avaliacao())
                            t_rate.insere_sort(lv.get_avaliacao(),lv)
                        else:
                            t_rate.atualiza_sort(lv.get_avaliacao(), lv)
                except EOFError:
                    break       
        lista = listar(t_rate.get_raiz())                
        if ordem == 'd':
            lista.reverse()
        return lista

    # mais abandonos
    if atributo == 'abandonos':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if genero in lv.get_generos():
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.abandonos), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.abandonos), reverse=True)
        return newlist

    # mais relidos
    if atributo == 'relendo':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if genero in lv.get_generos():
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.relendo), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.relendo), reverse=True)
        return newlist

    # maior numero de paginas
    if atributo == 'paginas':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if genero in lv.get_generos():
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.paginas), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.paginas), reverse=True)
        return newlist

    # mais leitoras
    if atributo == 'mulheres':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if genero in lv.get_generos():
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.qt_mulheres), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.qt_mulheres), reverse=True)
        return newlist

    # mais leitores
    if atributo == 'homens':
        t = Trie()
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if genero in lv.get_generos():
                        t.insere(lv)
                except EOFError:
                    break   
        l = listar(t.get_raiz())
        newlist = sorted(l, key=lambda x: int(x.qt_homens), reverse=False)
        if ordem == 'd':
            newlist = sorted(l, key=lambda x: int(x.qt_homens), reverse=True)
        return newlist

# Dada uma classe, lista seus objetos por ordem alfabética da chave
# Livros por título
# Autores/Gêneros/Editoras por nome
def listarObjetos(classe,ordem):
    t = carregaTrie(classe)
    lista = listar(t.get_raiz())
    if ordem == 'd':
        lista.reverse()
    if classe == 'livro':
        return lista
    else:
        return lista

# Função para imprimir o menu inicial e capturar a opção escolhida
def print_menu(): 
    print(66*'-')
    print(10*' ','BEM VINDO AO CATÁLOGO DE LIVROS ANTARES!')
    print(66*'-')
    print(30 * "-" , "MENU" , 30 * "-")
    print('[1] - Listar Registros')
    print('[2] - Adicionar Livro')
    print('[3] - Atualizar Livro')
    print('[4] - Excluir Registro')
    print('[5] - Buscar Registro')
    print('[6] - Sair')
    print(67 * "-")
    return input('Escolha uma opção: ')

# Função para imprimir o menu de escolha de classe e capturar a opção escolhida
def print_listar():
    print('\n',20*'-','Escolha um registro:',20*'-')
    print('[1] - Livros')
    print('[2] - Autores')
    print('[3] - Editoras')
    print('[4] - Sair')
    print(47 * "-")

    return input('Qual registro você deseja? ')

# Função para imprimir o menu de escolha de classe para deleção e capturar a opção escolhida
def print_listaDeletar():
    print('\n',20*'-','Escolha um registro para deletar:',20*'-')
    print('[1] - Livro')
    print('[2] - Autor (deleta seus livros também)')
    print('[3] - Editora (deleta seus livros também)')
    print('[4] - Gênero (deleta seus livros também)')
    print('[5] - Sair')
    print(47 * "-")

    return input('Qual registro você deseja deletar? ')

# Função para imprimir o menu de escolha de atributo pra listagem e capturar a opção escolhida
def print_listar_livros():
    print('\n',20*'-','Listar livros por:',20*'-')
    print('[1] - Título')
    print('[2] - Ano')
    print('[3] - Avaliação')
    print('[4] - Número de leitores')
    print('[5] - Número de páginas')
    print('[6] - Número de mulheres que leram')
    print('[7] - Número de homens que leram')
    print('[8] - Número de abandonos')
    print('[9] - Número de pessoas relendo')
    print('[10] - Voltar')
    print(67 * "-")

    return input('Por qual opção você deseja listar os livros? ')

# Função para imprimir o menu de escolha de atributo pra listagem e capturar a opção escolhida
def print_listar_outros():
    print('\n',20*'-','Listar registros por:',20*'-')
    print('[1] - Nome')
    print('[2] - Média de avaliações dos livros')
    print('[3] - Número de abandonos dos livros')
    print('[4] - Número de leitores dos livros')
    print('[5] - Voltar')
    print(67 * "-")

    return input('Por qual opção você deseja listar os registros? ')

# Função para imprimir o menu de cadastro de livro e retornar o objeto livro
def print_addLivro():
    print('\n',20*'-','Cadastrar novo livro:',20*'-')
    titulo = input('Título: ')
    autor = input('Autor: ')
    at = buscar(autor,'autor')
    if at:
        editora = input('Editora: ')
        ed = buscar(editora,'editora')
        if ed:
            isbn10 = input('ISBN10: ')
            idioma = input('Idioma: ')
            paginas = input('Páginas: ')
            ano = input('Ano: ')
            genero = input('Gênero: ')

            livro = Livro(titulo,isbn10,idioma,paginas,ano,0,0,0,0,0,0,0,0,0,ed,at,genero)
            return livro
        else:
            return -2
    else:
        return -1

# Função para imprimir o menu de atualização de livro e retornar o objeto livro
def print_updLivro():
    print('\n',20*'-','Atualizar livro:',20*'-')
    titulo = input('Título do livro a ser atualizado: ')
    lv = buscar(titulo,'livro')
    if lv:
        chave_velho = titulo

        print('[1] - Título')
        print('[2] - ISBN10')
        print('[3] - Idioma')
        print('[4] - Páginas')
        print('[5] - Ano')
        print('[6] - Avaliação')
        print('[7] - Autor')
        print('[8] - Editora')
        print('[9] - Gênero')
        print('[10] - Sair')
        
        atributo = input('Qual atributo você deseja atualizar?\n')

        if atributo != '10':
            if atributo == '1':
                titulo = input('Novo título: ')
                lv_novo = Livro(titulo,lv.isbn10,lv.idioma,lv.paginas,lv.ano,lv.avaliacao,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram,lv.qt_mulheres,lv.qt_homens,\
                            lv.editora,lv.autor,lv.generos)
                return [lv_novo,chave_velho]

            elif atributo == '2':
                isbn10 = input('Novo ISBN10: ')
                lv_novo = Livro(lv.titulo,isbn10,lv.idioma,lv.paginas,lv.ano,lv.avaliacao,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram,lv.qt_mulheres,lv.qt_homens,\
                            lv.editora,lv.autor,lv.generos)
                return [lv_novo,chave_velho]
            elif atributo == '3':
                idioma = input('Novo idioma: ')
                lv_novo = Livro(lv.titulo,lv.isbn10,idioma,lv.paginas,lv.ano,lv.avaliacao,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram,lv.qt_mulheres,lv.qt_homens,\
                            lv.editora,lv.autor,lv.generos)
                return [lv_novo,chave_velho]
            elif atributo == '4':
                paginas = input('Nova quantia de páginas: ')
                lv_novo = Livro(lv.titulo,lv.isbn10,lv.idioma,paginas,lv.ano,lv.avaliacao,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram,lv.qt_mulheres,lv.qt_homens,\
                            lv.editora,lv.autor,lv.generos)
                return [lv_novo,chave_velho]
            elif atributo == '5':
                ano = input('Novo ano: ')
                lv_novo = Livro(lv.titulo,lv.isbn10,lv.idioma,lv.paginas,ano,lv.avaliacao,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram,lv.qt_mulheres,lv.qt_homens,\
                            lv.editora,lv.autor,lv.generos)
                return [lv_novo,chave_velho]
            elif atributo == '6':
                rating = input('Nova avaliação: ')
                lv_novo = Livro(lv.titulo,lv.isbn10,lv.idioma,lv.paginas,lv.ano,rating,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram,lv.qt_mulheres,lv.qt_homens,\
                            lv.editora,lv.autor,lv.generos)
                return [lv_novo,chave_velho]
            elif atributo == '7':
                autor = input('Novo autor: ')
                at = buscar(autor,'autor')
                if at:
                    lv_novo = Livro(lv.titulo,lv.isbn10,lv.idioma,lv.paginas,lv.ano,lv.avaliacao,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram,lv.qt_mulheres,lv.qt_homens,\
                            lv.editora,at,lv.generos)
                    return [lv_novo,chave_velho]
                else:
                    return -2
                
            elif atributo == '8':
                editora = input('Nova editora: ')
                ed = buscar(editora,'editora')
                if ed:
                    lv_novo = Livro(lv.titulo,lv.isbn10,lv.idioma,lv.paginas,lv.ano,lv.avaliacao,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram,lv.qt_mulheres,lv.qt_homens,\
                            ed,lv.autor,lv.generos)
                    return [lv_novo,chave_velho]
                else:
                    return -3
            elif atributo == '9':
                genero = input('Novo gênero: ')
                lv_novo = Livro(lv.titulo,lv.isbn10,lv.idioma,lv.paginas,lv.ano,lv.avaliacao,lv.qt_avaliacoes,\
                            lv.abandonos,lv.relendo,lv.querem_ler,lv.lendo,lv.leram3,lv.qt_mulheres,lv.qt_homens,\
                            lv.editora,lv.autor,genero)
                return [lv_novo,chave_velho]
        else:
            return -1
    else:
        return 0

# Função para imprimir o menu de escolha de classe pra busca e capturar a opção escolhida
def print_srcReg():
    print('\n',20*'-','Escolha um registro para buscar:',20*'-')
    print('[1] - Livro')
    print('[2] - Autor')
    print('[3] - Editora')
    print('[4] - Gênero')
    print('[5] - Sair')
    print(47 * "-")

    return input('Qual registro você deseja buscar? ')

# Função para imprimir o menu de escolha de atributo pra listagem e capturar a opção escolhida
def print_listarPor():
    print('\n',20*'-','Listar livros por:',20*'-')
    print('[1] - Ano')
    print('[2] - Avaliação')
    print('[3] - Número de leitores')
    print('[4] - Número de páginas')
    print('[5] - Número de mulheres que leram')
    print('[6] - Número de homens que leram')
    print('[7] - Número de abandonos')
    print('[8] - Número de pessoas relendo')
    print('[9] - Voltar')
    print(67 * "-")

    return input('Por qual opção você deseja listar os livros? ')

# programa principal
def main():
    carregar_dados() # carrega dados do arquivo csv para os pickles
    pd.set_option('display.max_rows', 5000) # configurações da tabela pandas

    # valores do menu inicial
    listReg = '1'
    addLivro = '2'
    updLivro = '3'
    delReg = '4'
    srchReg = '5'

    opc = print_menu()
    if opc != '6':
        while(opc != '6'):
            if opc == listReg:
                classe = print_listar()
                if classe != '4':
                    if classe == '1':
                        opcao = print_listar_livros()
                        if opcao != '10':
                            atributo = ''
                            if opcao == '2':
                                atributo = 'ano'
                            elif opcao == '3':
                                atributo = 'rating'
                            elif opcao == '4':
                                atributo = 'lendo'
                            elif opcao == '5':
                                atributo = 'paginas'
                            elif opcao == '6':
                                atributo = 'mulheres'
                            elif opcao == '7':
                                atributo = 'homens'
                            elif opcao == '8':
                                atributo = 'abandonos'
                            elif opcao == '9':
                                atributo = 'relendo'

                            ordem = input('\nListar livros em ordem:\n[c] - crescente\n[d] - decrescente\n')
                            lista = []
                            if atributo == '':
                                lista = listarObjetos('livro',ordem)
                            else:
                                lista = sort('livro',atributo,ordem)
                            df = pd.DataFrame([livro.to_dict() for livro in lista])
                            print(df)

                    elif classe == '2':
                        opcao = print_listar_outros()
                        if opcao != '5':
                            atributo = ''
                            if opcao == '2':
                                atributo = 'media_ratings'
                            elif opcao == '3':
                                atributo = 'abandonos'
                            elif opcao == '4':
                                atributo = 'lidos'
                            
                            ordem = input('\nListar autores em ordem:\n[c] - crescente\n[d] - decrescente\n')
                            lista = []
                            if atributo == '':
                                lista = listarObjetos('autor',ordem)
                            else:
                                lista = sort('autor',atributo,ordem)
                            df = pd.DataFrame([autor.to_dict() for autor in lista])
                            print(df)

                    elif classe == '3':
                        opcao = print_listar_outros()
                        if opcao != '5':
                            atributo = ''
                            if opcao == '2':
                                atributo = 'media_ratings'
                            elif opcao == '3':
                                atributo = 'abandonos'
                            elif opcao == '4':
                                atributo = 'lidos'
                            
                            ordem = input('\nListar editoras em ordem:\n[c] - crescente\n[d] - decrescente\n')
                            lista = []
                            if atributo == '':
                                lista = listarObjetos('editora',ordem)
                            else:
                                lista = sort('editora',atributo,ordem)
                            df = pd.DataFrame([editora.to_dict() for editora in lista])
                            print(df)   
            elif opc == addLivro:
                livro = print_addLivro()
                if livro != -1 and livro != -2:
                    certo = inserir(livro,'livro')
                    if certo:
                        print('Livro adicionado com sucesso!')
                    else:
                        print('Ocorreu um erro ao adicionar o livro...')
                else:
                    if livro == -1:
                        print('Autor não encontrado.')
                    else:
                        print('Editora não encontrada.')
            elif opc == updLivro:
                livro = print_updLivro()
                if not isinstance(livro,int):
                    certo = atualizar(livro[1],livro[0],'livro')
                    if certo:
                        print('Livro atualizado com sucesso!')
                    else:
                        print('Ocorreu um erro ao atualizar o livro...')
                else:
                    if livro == -2:
                        print('Autor não encontrado.')
                    elif livro == -3:
                        print('Editora não encontrada.')
                    elif livro == 0:
                        print('Livro não encontrado.')
            elif opc == delReg:
                classe = print_listaDeletar()
                if classe != '5':
                    if classe == '1':
                        titulo = input('Deletar livro de título: ')
                        lv = buscar(titulo,'livro')
                        if lv:
                            certo = deletar(lv,'livro')
                            if certo:
                                print('Deleção efetuada com sucesso!')
                            else:
                                print('Ocorreu um erro durante a deleção...')
                        else:
                            print('Livro não encontrado.')
                    elif classe == '2':
                        nome = input('ATENÇÃO! ISSO IRÁ DELETAR TODOS OS LIVROS DESTE AUTOR\nDeletar autor de nome: ')
                        at = buscar(nome,'autor')
                        if at:
                            certo = deletar(at,'autor')
                            if certo:
                                print('Deleção efetuada com sucesso!')
                            else:
                                print('Ocorreu um erro durante a deleção...')
                        else:
                            print('Autor não encontrado.')
                    elif classe == '3':
                        nome = input('ATENÇÃO! ISSO IRÁ DELETAR TODOS OS LIVROS DESTA EDITORA\nDeletar editora de nome: ')
                        ed = buscar(nome,'editora')
                        if ed:
                            certo = deletar(ed,'editora')
                            if certo:
                                print('Deleção efetuada com sucesso!')
                            else:
                                print('Ocorreu um erro durante a deleção...')
                        else:
                            print('Editora não encontrada.')
                    elif classe == '4':
                        nome = input('ATENÇÃO! ISSO IRÁ DELETAR TODOS OS LIVROS DESTE GÊNERO\nDeletar gênero de nome: ')
                        gn = buscar(nome,'genero')
                        if gn:
                            certo = deletar(gn,'genero')
                            if certo:
                                print('Deleção efetuada com sucesso!')
                            else:
                                print('Ocorreu um erro durante a deleção...')
                        else:
                            print('Gênero não encontrado.')
            elif opc == srchReg:
                classe = print_srcReg()
                if classe != '5':
                    if classe == '1':
                        titulo = input('Buscar livro de título: ')
                        lv = buscar(titulo,'livro')
                        if lv:
                            dicio = lv.to_dict()
                            for k,v in dicio.items():
                                print(f'{k}: {v}')
                        else:
                            print('Livro não encontrado')
                    elif classe == '2':
                        nome = input('Buscar autor de nome: ')
                        at = buscar(nome,'autor')
                        if at:
                            listarPor = print_listarPor()
                            if listarPor != '9':
                                ordem = input('\nListar livros em ordem:\n[c] - crescente\n[d] - decrescente\n')
                                lista = []
                                if listarPor == '1':
                                    lista = listarPorAutor(at.get_nome(),'ano',ordem)
                                elif listarPor == '2':
                                    lista = listarPorAutor(at.get_nome(),'rating',ordem)
                                elif listarPor == '3':
                                    lista = listarPorAutor(at.get_nome(),'lidos',ordem)
                                elif listarPor == '4':
                                    lista = listarPorAutor(at.get_nome(),'paginas',ordem)
                                elif listarPor == '5':
                                    lista = listarPorAutor(at.get_nome(),'mulheres',ordem)
                                elif listarPor == '6':
                                    lista = listarPorAutor(at.get_nome(),'homens',ordem)
                                elif listarPor == '7':
                                    lista = listarPorAutor(at.get_nome(),'abandonos',ordem)
                                elif listarPor == '8':
                                    lista = listarPorAutor(at.get_nome(),'relendo',ordem)
                                
                                df = pd.DataFrame([livro.to_dict() for livro in lista])
                                print(df)
                                
                        else:
                            print('Autor não encontrado')
                    elif classe == '3':
                        nome = input('Buscar editora de nome: ')
                        ed = buscar(nome,'editora')
                        if ed:
                            listarPor = print_listarPor()
                            if listarPor != '9':
                                ordem = input('\nListar livros em ordem:\n[c] - crescente\n[d] - decrescente\n')
                                lista = []
                                if listarPor == '1':
                                    lista = listarPorEditora(ed.get_nome(),'ano',ordem)
                                elif listarPor == '2':
                                    lista = listarPorEditora(ed.get_nome(),'rating',ordem)
                                elif listarPor == '3':
                                    lista = listarPorEditora(ed.get_nome(),'lidos',ordem)
                                elif listarPor == '4':
                                    lista = listarPorEditora(ed.get_nome(),'paginas',ordem)
                                elif listarPor == '5':
                                    lista = listarPorEditora(ed.get_nome(),'mulheres',ordem)
                                elif listarPor == '6':
                                    lista = listarPorEditora(ed.get_nome(),'homens',ordem)
                                elif listarPor == '7':
                                    lista = listarPorEditora(ed.get_nome(),'abandonos',ordem)
                                elif listarPor == '8':
                                    lista = listarPorEditora(ed.get_nome(),'relendo',ordem)
                                
                                df = pd.DataFrame([livro.to_dict() for livro in lista])
                                print(df)
                        else:
                            print('Editora não encontrada')
                    elif classe == '4':
                        nome = input('Buscar gênero de nome: ')
                        gn = buscar(nome,'genero')
                        if gn:
                            listarPor = print_listarPor()
                            if listarPor != '9':
                                ordem = input('\nListar livros em ordem:\n[c] - crescente\n[d] - decrescente\n')
                                lista = []
                                if listarPor == '1':
                                    lista = listarPorGenero(gn.get_nome(),'ano',ordem)
                                elif listarPor == '2':
                                    lista = listarPorGenero(gn.get_nome(),'rating',ordem)
                                elif listarPor == '3':
                                    lista = listarPorGenero(gn.get_nome(),'lidos',ordem)
                                elif listarPor == '4':
                                    lista = listarPorGenero(gn.get_nome(),'paginas',ordem)
                                elif listarPor == '5':
                                    lista = listarPorGenero(gn.get_nome(),'mulheres',ordem)
                                elif listarPor == '6':
                                    lista = listarPorGenero(gn.get_nome(),'homens',ordem)
                                elif listarPor == '7':
                                    lista = listarPorGenero(gn.get_nome(),'abandonos',ordem)
                                elif listarPor == '8':
                                    lista = listarPorGenero(gn.get_nome(),'relendo',ordem)
                                
                                df = pd.DataFrame([livro.to_dict() for livro in lista])
                                print(df)
                        else:
                            print('Gênero não encontrado')

            opc = print_menu()

if __name__ == '__main__':
    main()

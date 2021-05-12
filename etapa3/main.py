# bibliotecas
import os
import csv
import pickle
from livro import Livro
from genero import Genero
from editora import Editora
from autor import Autor
from trie import nodoTrie, Trie

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
            t = carregaTrie('livro')
            l = listar(t.get_raiz())
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
        if atributo == 'media_ratings': # funcional mas MUITO lento
            t = Trie()
            with open('autores.pkl','rb') as pkautores:
                while True:
                    try:
                        at = pickle.load(pkautores)
                        soma_ratings = qt_livros = media = 0
                        with open('livros.pkl','rb') as pklivros:
                            while True:
                                try:
                                    lv = pickle.load(pklivros)
                                    if lv.get_autor().get_nome() == at.get_nome():
                                        soma_ratings += float(lv.get_avaliacao())
                                        qt_livros += 1
                                except EOFError:
                                    break
                        if qt_livros != 0:
                            media = soma_ratings / qt_livros
                        at.set_media(media)
                        t.insere(at)
                    except EOFError:
                        break
            l = listar(t.get_raiz())
            newlist = sorted(l, key=lambda x: int(x.get_media()), reverse=False)
            if ordem == 'd':
                newlist = sorted(l, key=lambda x: int(x.get_media()), reverse=True)
            return newlist
  
        # qt livros lidos
        if atributo == 'lidos': # funcional mas MUITO lento
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
        if atributo == 'abandonos': # funcional mas MUITO lento
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
        if atributo == 'abandonos': # funcional mas MUITO lento
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
        # crescente

        # decrescente

    # avaliação
    if atributo == 'rating':
        t_rate = Trie()
        ratings = []
        with open('livros.pkl','rb') as pklivros:
            while True:
                try:
                    lv = pickle.load(pklivros)
                    if lv.get_autor().get_nome() == autor:
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
def listarPorEditora(editora,atributo,ordem):
    # por ano
        # crescente

        # decrescente

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
def listarPorGenero(genero,atributo,ordem):
    # mais lidos

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

    # mais relidos

    # maior numero de paginas

    # mais leitoras

    # mais leitores

# Dada uma classe, lista seus objetos por ordem alfabética da chave
# Livros por título
# Autores/Gêneros/Editoras por nome
def listarObjetos(classe,ordem):
    t = carregaTrie(classe)
    lista = listar(t.get_raiz())
    if ordem == 'd':
        lista.reverse()
    if classe == 'livro':
        for i in lista:
            print(i.get_titulo())
    else:
        for i in lista:
            print(i.get_nome())

# ------------------------------------------------------------------------


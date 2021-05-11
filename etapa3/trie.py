from livro import Livro
from genero import Genero
from editora import Editora
from autor import Autor

alfabeto = ['a','á','ã','â','à','ä','b','c','d','e','ë','é','ê','f','g','h','i',\
            'í','î','ï','j','k','l','m','n','o','ö','ó','õ','ô','p','q','r','s',\
            't','u','ú','ü','v','w','x','y','z','0','1','2','3','4','5','6','7','8',\
            '9','(',')','-','.',',',' ','!','?','@','#','%','&','*','+',\
            "'",'/','"','|',':',';','[',']','ª','º','°','²','ø']

class nodoTrie():
    def __init__(self):
        self.filhos = [None]*len(alfabeto) # letras e dígitos
        self.objeto = []
        # fimPalavra é True se o nodo representa o fim de uma palavra
        self.fimPalavra = False
    
    def get_filhos(self):
        return self.filhos
    def get_objeto(self):
        return self.objeto
    def get_fimPalavra(self):
        return self.fimPalavra

    def set_filhos(self,val,indice):
        self.filhos[indice] = val
    def set_objeto(self,objeto):
        self.objeto = objeto
    def set_fimPalavra(self,fimPalavra):
        self.fimPalavra = fimPalavra

class Trie:
    def __init__(self):
        self.raiz = self.getNode()
    
    def get_raiz(self):
        return self.raiz

    def set_raiz(self,raiz):
        self.raiz = raiz
  
    def getNode(self):      
        # Retorna novo nodo trie (inicializado para NULL)
        return nodoTrie()
  
    def charToIndex(self,ch):    
        # Converte o char-chave atual no seu índice da lista alfabeto
        indice = -1
        for i in range(len(alfabeto)):
            if ch == alfabeto[i]:
                indice = i                  
        return indice
  
    def insere(self,objeto):
        chave = ''
        # se objeto for Livro, usa o titulo como chave          
        if isinstance(objeto,Livro):
            chave = (str(objeto.titulo)).lower()
            # formata todos os campos pra minúsculo
            objeto.set_titulo(objeto.get_titulo().lower())
            objeto.set_isbn10(objeto.get_isbn10().lower())
            objeto.set_idioma(objeto.get_idioma().lower())
        # se for outra Autor/Editora/Gênero, usa o nome
        elif isinstance(objeto,Autor) or isinstance(objeto,Editora) or isinstance(objeto,Genero):
            chave = (str(objeto.nome)).lower()
            objeto.set_nome(objeto.get_nome().lower())

        atual = self.get_raiz() # começa percorrendo pela raiz
        n = len(chave) 
        for nivel in range(n):  # para cada letra da chave, vai descendo na Trie
            ch = chave[nivel]
            indice = self.charToIndex(ch)
  
            # se o nodo da letra atual não tem nada, inicializa ele
            if not atual.get_filhos()[indice]:
                atual.set_filhos(self.getNode(),indice) 
            atual = atual.get_filhos()[indice] # continua descende por essa sub-árvore
  
        # marca último nodo da palavra como folha e preenche seu atributo
        atual.set_fimPalavra(True)
        atual.set_objeto(objeto)
  
    def busca(self, chave):          
        # Busca chave na trie
        # Retorna o objeto se a chave está presente, senão retorna None
        atual = self.get_raiz() # começa pela raiz
        n = len(chave)
        for nivel in range(n): # para cada letra da chave, vai descendo na Trie
            indice = self.charToIndex(chave[nivel]) 

            if not atual.get_filhos()[indice]: # se nodo é folha mas não terminou a chave
                return None # não achou a palavra
            atual = atual.get_filhos()[indice] # senão continua descendo na sub-árvore
  
        # se nodo atual não vazio e é folha
        if atual != None and atual.get_fimPalavra():
            return atual.get_objeto() # retorna seu objeto
        else:
            return None

    # retorna True se deleção deu certo e False caso contrário
    def deleta(self, objeto):
        raiz = self.get_raiz()
        # se objeto é Livro, chave é o título
        if isinstance(objeto,Livro):
            chave = str(objeto.get_titulo())
        # se for Autor/Editora/Gênero, chave é o nome
        else:
            chave = str(objeto.get_nome())
        n = len(chave)

        # vai descendo um nível na Trie para cada letra da chave
        for i in range(n):
            index = self.charToIndex(chave[i])
            
            # se raiz nula, retorna false
            if not raiz:
                return False
            raiz = raiz.get_filhos()[index] # senão, raiz é o filho correspondente ao char atual

        # se nodo atual for nulo
        if not raiz:
            return False # não achou a palavra
        else:
            # senão, indica que aquele nodo não é mais final de palavra e retorna true
            raiz.set_fimPalavra(False)
            return True

    # retorna true se atualização deu certo e false caso contrário
    def atualiza(self, obj_antigo, novo_obj):
        val = self.deleta(obj_antigo)
        # se deleção deu certo, insere o objeto atualizado e retorna true
        if val:
            self.insere(novo_obj)
            return True
        else:
            return False

    # insere como chave o atributo do sort, para fazer a pesquisa de livros por atributo
    # o atributo 'objeto' do nodo é uma lista de livros
    def insere_sort(self,atrb,livro):
        chave = str(atrb) # a chave é o atributo
        atual = self.get_raiz() # começa pela raiz
        n = len(chave) 
        # vai descendo um nível na Trie por dígito na chave
        for nivel in range(n):
            indice = self.charToIndex(chave[nivel])
  
            # se dígito atual não está presente, insere
            if not atual.get_filhos()[indice]:
                atual.set_filhos(self.getNode(),indice)
            atual = atual.get_filhos()[indice] # continua descendo
  
        # marca último nodo como folha e inicializa sua lista de livros
        atual.set_fimPalavra(True)
        l = atual.get_objeto()
        l.append(livro)
        atual.set_objeto(l)
        
    # atualiza atributo do sort inserindo livro em sua lista de livros
    def atualiza_sort(self,atrb,livro):
        atual = self.get_raiz() # começa pela raiz
        chave = str(atrb)
        n = len(chave)
        for nivel in range(n): # para cada dígito da chave, vai descendo na Trie
            indice = self.charToIndex(chave[nivel]) 

            if not atual.get_filhos()[indice]: # se nodo é folha mas não terminou a chave
                return False # não achou o atributo
            atual = atual.get_filhos()[indice] # senão continua descendo na sub-árvore
  
        # se nodo atual não vazio e é folha, insere livro em sua lista e retorna true
        if atual != None and atual.get_fimPalavra():
            l = atual.get_objeto()
            l.append(livro)
            atual.set_objeto(l)
            return True
        else:
            return False

            
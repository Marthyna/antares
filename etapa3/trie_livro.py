class nodoTrie_livro():
    def __init__(self):
        self.filhos = [None]*10
        self.livro = ''
        # fimPalavra é True se o nodo representa o fim de uma palavra
        self.fimPalavra = False

class TrieLivro:
    def __init__(self):
        self.raiz = self.getNode()
  
    def getNode(self):      
        # Retorna novo nodo trie (inicializado para NULL)
        return nodoTrie_livro()
  
    def charToIndex(self,ch):    
        # Converte o char-chave atual em índice
        # só usa 'a'-'z' em minúsculo          
        return ord(ch)-ord('0')  
  
    def insere(self,chave,livro):          
        # Se chave não está na árvore, inserte
        # Se chave é prefixo de um nodo trie, marca como folha
        atual = self.raiz
        n = len(chave)
        for nivel in range(n):
            indice = self.charToIndex(chave[nivel])
  
            # se char atual não está presente
            if not atual.filhos[indice]:
                atual.filhos[indice] = self.getNode()
            atual = atual.filhos[indice]
  
        # marca último nodo como folha e preenche seu atributo livro
        atual.fimPalavra = True
        atual.livro = livro
  
    def busca(self, chave):          
        # Busca chave na trie
        # Retorna true se a chave está presente, senão false
        atual = self.raiz
        n = len(chave)
        for nivel in range(n):
            indice = self.charToIndex(chave[nivel])
            if not atual.filhos[indice]:
                return False
            atual = atual.filhos[indice]
  
        if atual != None and atual.fimPalavra:
            return atual.livro
        else:
            return None
  
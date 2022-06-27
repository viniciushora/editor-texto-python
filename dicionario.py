from hashing import TabelaHash
from spellchecker import SpellChecker #Biblioteca que sugere as palavras

class Dicionario:
    def __init__(self):
        self.palavras = TabelaHash() #Tabela hash das palavras do dicionário
        self.inicializar() #Função de carregar o dicionário # inicializa o corretor da biblioteca

    def inicializar(self): #Carrega o dicionário do arquivo para a variável
        f = open("dicionario.txt", "r", encoding="utf-16")
        linha = " "
        while (linha != ""): #Loop para percorrer as linhas do arquivo texto do dicionário
            linha = f.readline().strip("\n") # Pega a linha e retira o espaço
            self.palavras.armazenar(linha) # Armazena a palavra da linha na tabela hash (palavras)
        f.close() # Fecha o arquivo

    def palavras_parecidas(self, s):
        palavras = []
        pt = SpellChecker(language='pt') # inicializa o corretor da biblioteca
        candidatas = pt.candidates(s) # Pega sugestões da biblioteca
        for candidata in candidatas: # Loop na lista de sugestões
            hash2 = self.palavras.hash(candidata) # Verifica se a sugestão está armazenada na tabela hash do dicionário
            if self.palavras.tabela[hash2] != None and self.palavras.tabela[hash2] == candidata: # Se estiver e for igual ao elemento correspondido
                palavras.append(candidata) # Sugestão adicionada à lista de sugestões
        return palavras[:10] # Retorna só as 10 primeiras

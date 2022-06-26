from hashing import TabelaHash
from pyspellchecker.spellchecker import SpellChecker

class Dicionario:
    def __init__(self):
        self.palavras = TabelaHash()
        self.inicializar()

    def inicializar(self):
        f = open("dicionario.txt", "r", encoding="utf-16")
        linha = " "
        while (linha != ""):
            linha = f.readline().strip("\n")
            self.palavras.armazenar(linha)
        f.close()

    def palavras_parecidas(self, s):
        pt = SpellChecker(language='pt')
        palavras = []
        candidatas = pt.candidates(s)
        for candidata in candidatas:
            hash2 = self.palavras.hash(candidata)
            if self.palavras.tabela[hash2] != None and self.palavras.tabela[hash2] == candidata:
                palavras.append(candidata)
        return palavras[:10]

class TabelaHash:
    def __init__(self):
        self.tamanho = 10000009
        self.tabela = [None] * self.tamanho

    def hash(self,s):
        p = 31
        valor = 0
        p_pow = 1
        for c in s:
            valor = (valor + (ord(c) - ord('a') + 1) * p_pow) % self.tamanho
            p_pow = (p_pow * p) % self.tamanho
        return int(valor)

    def armazenar(self,s):
        chave = self.hash(s)
        if (self.tabela[chave] == None):
            self.tabela[chave] = s
        else:
            ("Colisão: msm valor ou não?")
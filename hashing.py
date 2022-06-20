class TabelaHash:
    def __init__(self):
        self.tabela = []
        self.tamanho = 1e9 + 9

    def iniciar():
        for i in range(self.tamanho):
            self.tabela.append(None)

    def hash(self,s):
        p = 31
        m = 1e9 + 9
        valor = 0
        p_pow = 1
        for c in s:
            valor = (valor + (c - 'a' + 1) * p_pow) % m
            p_pow = (p_pow * p) % m
        return valor

    def armazenar(self,s):
        chave = self.hash(s)
        if (self.tabela[chave] == None):
            self.tabela[chave] = s
        else:
            ("Colisão: msm valor ou não?")
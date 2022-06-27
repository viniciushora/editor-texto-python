class TabelaHash: # Classe tabela hash
    def __init__(self): # Construtor
        self.tamanho = 10000009 # Tamanho da tabela
        self.tabela = [None] * self.tamanho # Inicialização da tabela

    def hash(self,s): # Função de calcular a chave
        p = 31
        valor = 0
        p_pow = 1
        for c in s:
            valor = (valor + (ord(c) - ord('a') + 1) * p_pow) % self.tamanho
            p_pow = (p_pow * p) % self.tamanho
        return int(valor)

    def armazenar(self,s): # Função de armazenar na tabela
        chave = self.hash(s) # Calcula a chave
        if (self.tabela[chave] == None): # Se tiver vazia 
            self.tabela[chave] = s # Armazena na tabela
        else:
            ("Colisão: msm valor ou não?") 
import tkinter as tk #importando o Tkinter
import re #Importando o re
from tkinter.filedialog import askopenfilename, asksaveasfilename # Algumas bibioltecas auxiliares

class Editor: # Classe editor de texto
    def __init__(self, dicionario): # Construtor
        self.palavras = [] # Lista de palavras escritas no editor
        self.erros = [] # Lista com erros das palavras do editor (true ou false)
        self.tags = [] # Tags das palavras, para pintá-las
        self.marcacoes = [] # Lista das posições das palavras
        self.corret= [] # Lista das palavras das sugestões
        self.texto = "" # Texto do editor em estado bruto
        self.dicionario = dicionario # Dicionario na tabela hash
        self.window = None # Janela
        self.txt_edit = None # Text box
        self.fr_buttons = None 
        self.btn_open = None
        self.btn_save = None
        self.m = None # Menu
    
    def telaPrincipal(self):
        self.window = tk.Tk() #Criação da janela
        self.window.title("Editor de Texto") # Título
        self.window.rowconfigure(0, minsize=800, weight=1) # Linhas
        self.window.columnconfigure(1, minsize=800, weight=1) #Colunas
        self.m = tk.Menu(self.window, tearoff = 0) #Menu do clique com botão direito
        self.m.add_command(label ="Cut", command=self.cut) # Comando de cortar
        self.m.add_command(label ="Copy", command=self.copy) #Comando de copiar
        self.m.add_command(label ="Paste", command=self.paste) # Comando de colar
        self.m.add_separator() # Separador de comandos (linha entre eles)
        self.txt_edit = tk.Text(self.window) # Campo de de texto
        self.txt_edit.grid(row=0, column=1, sticky="nsew") # Criação do espaço do campo de texto
        self.txt_edit.tag_config("errado",foreground="red") 
        self.txt_edit.tag_config("certo",foreground="black")
        self.txt_edit.bind_all('<Key>', self.callback) # Evento de atualizar o vetor de palavras quando digitada qualquer tecla
        self.txt_edit.bind("<Button-3>", self.do_popup) # Evento de abrir o menu quando clicado com botão direito
        self.window.mainloop() # Loop para manter a janela aberta

    def do_popup(self,event): # Função pra abrir o menu
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def copy(self): # Função pra copiar
        self.txt_edit.event_generate("<<Copy>>")

    def cut(self): # Função pra cortar
        self.txt_edit.event_generate("<<Cut>>")

    def paste(self): # Função pra colar
        self.txt_edit.event_generate("<<Paste>>")

    def callback(self, *args): # Função pra verificar as palavras do texto
        self.texto = self.txt_edit.get("1.0",'end-1c') # Pega o conteúdo do text box
        self.tags = [] # Lista das tags zerada
        self.marcacoes = [] # Lista das marcações zerada
        self.texto = self.texto.replace("\n", " | ") # Substituindo o enter por | para calcular as linhas do editor
        self.texto = re.sub('\s+',' ', self.texto) # Comprimindo os espaços múltiplos
        self.palavras = self.texto.split(" ") # Splitando o texto pelo espaços para conseguir as palavras
        self.erros = [False] * len(self.palavras) # Preenchendo a lista de erros, false no momento (significa que ainda não tem erro)
        linha_atual = 1.0 # Linha inicial
        for i in range(len(self.palavras)): # Loop para percorrer a lista de palavras do textbox
            if (self.palavras[i] != "|"): # Se a palavra não for igual |, então realmente é uma palavra
                offset = '+%dc' % len(self.palavras[i]) # Tamanho da palavra no plano do textbox
                if (not self.posicao_inicial(self.palavras[i], self.marcacoes)): # Se palavra não está na lista de palavras
                    pos = self.ultima_posicao(self.marcacoes) # Verifica se tem algo escrito na linha
                    if pos == -1: # Se não tem nada escrito
                        pos = linha_atual # Recebe a posição inicial da linha
                    pos_start = self.txt_edit.search(self.palavras[i], pos, 'end-1c') # Posição inicial = posicao inicial da linha ou posicao da ultima palavra encontrada até o fim do documento
                else:
                    pos_start = self.posicao_inicial(self.palavras[i], self.marcacoes) + '+1c' # Posição do ultimo elemento igual a palavra
                pos_end = pos_start + offset # Posição finalé a posição inicial da palavra + seu tamanho
                posicao = (self.palavras[i], pos_start, pos_end) # Posição definida
                self.marcacoes.append(posicao) # Posição adicionada na lista de posições
                if (self.palavras[i] != "" ): # Se a palavra do elemento i da lista for diferente de vazio
                    if (not self.check_dicionario(self.palavras[i])): #Se palavra não está no dicionario
                        self.erros[i] = True # Palavra recebe erro true
                        tag = (str(i),1) # Tag recebe uma tupla com código da tag e o tipo da tag (1= errado, 2=correto)
                        self.tags.append(tag) # Lista de tags recebe a tag
                        self.txt_edit.tag_config(str(i),foreground="red") # Configurada a tag com código i e cor de marcação vermelha
                        self.txt_edit.tag_add(str(i), pos_start, pos_end) # Marca a tag da posição inicial até a posição final da palavra
                    else:
                        tag = (str(i),0) # Tag recebe uma tupla com código da tag e o tipo da tag (1= errado, 2=correto)
                        self.tags.append(tag) # Lista de tags recebe a tag
                        self.txt_edit.tag_config(str(i), foreground="green") # Configurada a tag com código i e cor de marcação verde
                        self.txt_edit.tag_add(str(i), pos_start, pos_end) # Marca a tag da posição inicial até a posição final da palavra
            else:
                linha_atual = linha_atual + 1.0 # Pula para a próxima linha
            for tag,tipo in self.tags: # Código da tag e tipo da tag na lista de tags
                self.txt_edit.tag_bind(tag, "<Button-3>", self.corretor(tag, tipo)) # Evento de clicar com o botão direito na palavra, irá abrir o menu

    def corretor(self, tag, tipo): #Função de correção das palavras
        if tipo == 1: # Se o tipo da palavra for errado
            tag = int(tag) # Converte a tag em inteiro
            palavras_parecidas = self.dicionario.palavras_parecidas(self.palavras[tag]) # Pega as palavras parecidas
            try:
                self.m.delete("Adicionar palavra ao dicionário") # Apaga os labels acumulados das outras palavras
                self.m.delete("Palavras sugeridas:")
                for palavra in self.corret:
                    self.m.delete(palavra)
                self.corret = [] # Reseta a lista de sugestões
                self.m.add_command(label= "Adicionar palavra ao dicionário", command= lambda:self.adicionar_palavra(self.palavras[tag])) #Cria o campo de adicionar palavra ao dicionario no menu da palavra
                self.m.add_command(label= "Palavras sugeridas:") #Cria um divisor e demarcador de palavras sugeridas
                for palavra in palavras_parecidas: # Percorre a lista de palavras parecidas
                    self.m.add_command(label= palavra, command= lambda palavra=palavra : self.alterar_palavra(palavra)) # Adiciona um campo com a palavra da sugestão
                    self.corret.append(palavra) # Adiciona a palavra na lista de sugestões
            except:
                self.corret = [] # Reseta a lista de sugestões
                self.m.add_command(label= "Adicionar palavra ao dicionário", command= lambda:self.adicionar_palavra(self.palavras[tag])) #Cria o campo de adicionar palavra ao dicionario no menu da palavra
                self.m.add_command(label= "Palavras sugeridas:") #Cria um divisor e demarcador de palavras sugeridas
                for palavra in palavras_parecidas:  # Percorre a lista de palavras parecidas
                    self.m.add_command(label= palavra, command= lambda palavra=palavra : self.alterar_palavra(palavra)) # Adiciona um campo com a palavra da sugestão
                    self.corret.append(palavra) # Adiciona a palavra na lista de sugestões
        else:
            try:
                self.m.delete("Adicionar palavra ao dicionário") # Apaga os labels acumulados das outras palavras
                self.m.delete("Palavras sugeridas:")
                for palavra in self.corret:
                    self.m.delete(palavra)
            except:
                return False

    def adicionar_palavra(self, palavra): # Função de adicionar nova palavra ao dicionário
        self.dicionario.palavras.armazenar(palavra) # Armazena a nova palavra na tabela hash
        self.callback() # Atualiza o visual da janela

    def alterar_palavra(self, n_palavra): # Função de alterar a palavra errada
        texto = ""
        for i in range(len(self.palavras)): # Loop para percorrer a lista de palavras
            if self.palavras[i] == self.palavras[-1]: # Se o elemento i for igual ao último
                self.palavras[i] = n_palavra # O elemento i agora é a nova palavra
        for palavra in self.palavras: # Loop para percorrer a lista de palavras
            if palavra != "|": # Se palavra igual !
                texto+= palavra + " " # Palavra recebe espaço
            else:
                texto= texto[:-1] # Texto perde o último elemento
                texto+="\n" # Texto recebe enter
        self.txt_edit.delete(1.0,"end") # Apaga todo o texto antigo
        self.txt_edit.insert(1.0,texto) # Coloca o novo texto na tela
        self.callback() # Atualiza o visual com as marcações

    def posicao_inicial(self,s, lista): # Função para retornar a posição inicial da palavra
        for palavra, pos_start, pos_end in reversed(lista): # Percorre a lista de palavras de trás pra frente
            if (s == palavra): # Se s é igual palavra
                return pos_end # Retorna a sua posição final
                break
        return False

    def ultima_posicao(self, lista): # Função para retornar a última posição do elemento
        if (len(lista) > 0): # Se tiverem palavras
            return lista[-1][2] # Posição é a posição final da última palavra
        else:
            return -1 # Senão a posição é o começo da linha
  
    def check_dicionario(self,s): # Função para checar se uma palavra está no dicionário
        hash = self.dicionario.palavras.hash(s) # Calcula o hash
        if (s != self.dicionario.palavras.tabela[hash]): # Se a palavra for diferente do elemento naquela chave
            return False
        else:
            return True
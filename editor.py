import tkinter as tk
import re
from tkinter.filedialog import askopenfilename, asksaveasfilename

class Editor:
    def __init__(self, dicionario):
        self.palavras = []
        self.erros = []
        self.tags = []
        self.marcacoes = []
        self.corret= []
        self.texto = ""
        self.dicionario = dicionario
        self.window = None
        self.txt_edit = None
        self.fr_buttons = None
        self.btn_open = None
        self.btn_save = None
        self.m = None
    
    def telaPrincipal(self):
        self.window = tk.Tk()
        self.window.title("Editor de Texto")
        self.window.rowconfigure(0, minsize=800, weight=1)
        self.window.columnconfigure(1, minsize=800, weight=1)
        self.m = tk.Menu(self.window, tearoff = 0)
        self.m.add_command(label ="Cut", command=self.cut)
        self.m.add_command(label ="Copy", command=self.copy)
        self.m.add_command(label ="Paste", command=self.paste)
        self.m.add_separator()
        self.txt_edit = tk.Text(self.window)
        self.txt_edit.grid(row=0, column=1, sticky="nsew")
        self.txt_edit.tag_config("errado",foreground="red")
        self.txt_edit.tag_config("certo",foreground="black")
        self.txt_edit.bind_all('<Key>', self.callback)
        self.txt_edit.bind("<Button-3>", self.do_popup)
        self.window.mainloop()

    def do_popup(self,event):
        try:
            self.m.tk_popup(event.x_root, event.y_root)
        finally:
            self.m.grab_release()

    def copy(self):
        self.txt_edit.event_generate("<<Copy>>")

    def cut(self):
        self.txt_edit.event_generate("<<Cut>>")

    def paste(self):
        self.txt_edit.event_generate("<<Paste>>")

    def callback(self, *args):
        self.texto = self.txt_edit.get("1.0",'end-1c')
        self.tags = []
        self.marcacoes = []
        self.texto = self.texto.replace("\n", " | ")
        self.texto = re.sub('\s+',' ', self.texto)
        self.palavras = self.texto.split(" ")
        self.erros = [False] * len(self.palavras)
        linha_atual = 1.0
        for i in range(len(self.palavras)):
            if (self.palavras[i] != "|"):
                offset = '+%dc' % len(self.palavras[i])
                if (not self.posicao_inicial(self.palavras[i], self.marcacoes)):
                    pos = self.ultima_posicao(self.marcacoes)
                    if pos == -1:
                        pos = linha_atual
                    pos_start = self.txt_edit.search(self.palavras[i], pos, 'end-1c')
                else:
                    pos_start = self.posicao_inicial(self.palavras[i], self.marcacoes) + '+1c'
                pos_end = pos_start + offset
                posicao = (self.palavras[i], pos_start, pos_end)
                self.marcacoes.append(posicao)
                if (self.palavras[i] != "" ):
                    if (not self.check_dicionario(self.palavras[i])):
                        self.erros[i] = True
                        tag = (str(i),1)
                        self.tags.append(tag)
                        self.txt_edit.tag_config(str(i),foreground="red")
                        self.txt_edit.tag_add(str(i), pos_start, pos_end)
                    else:
                        tag = (str(i),0)
                        self.tags.append(tag)
                        self.txt_edit.tag_config(str(i), foreground="green")
                        self.txt_edit.tag_add(str(i), pos_start, pos_end)
            else:
                linha_atual = linha_atual + 1.0
            for tag,tipo in self.tags:
                self.txt_edit.tag_bind(tag, "<Button-3>", self.corretor(tag, tipo))

    def corretor(self, tag, tipo):
        if tipo == 1:
            tag = int(tag)
            palavras_parecidas = self.dicionario.palavras_parecidas(self.palavras[tag])
            try:
                self.m.delete("Adicionar palavra ao dicionário")
                self.m.delete("Palavras sugeridas:")
                for palavra in self.corret:
                    self.m.delete(palavra)
                self.corret = []
                self.m.add_command(label= "Adicionar palavra ao dicionário", command= lambda:self.adicionar_palavra(self.palavras[tag]))
                self.m.add_command(label= "Palavras sugeridas:")
                for palavra in palavras_parecidas:
                    self.m.add_command(label= palavra, command= lambda palavra=palavra : self.alterar_palavra(palavra), value=tag)
                    self.corret.append(palavra)
            except:
                self.corret = []
                self.m.add_command(label= "Adicionar palavra ao dicionário", command= lambda:self.adicionar_palavra(self.palavras[tag]))
                self.m.add_command(label= "Palavras sugeridas:")
                for palavra in palavras_parecidas:
                    self.m.add_command(label= palavra, command= lambda palavra=palavra : self.alterar_palavra(palavra))
                    self.corret.append(palavra)
        else:
            try:
                self.m.delete("Adicionar palavra ao dicionário")
                self.m.delete("Palavras sugeridas:")
                for palavra in self.corret:
                    self.m.delete(palavra)
            except:
                return False

    def adicionar_palavra(self, palavra):
        self.dicionario.palavras.armazenar(palavra)
        self.callback()

    def alterar_palavra(self, n_palavra):
        texto = ""
        for i in range(len(self.palavras)):
            if self.palavras[i] == self.palavras[-1]:
                self.palavras[i] = n_palavra
        for palavra in self.palavras:
            if palavra != "|":
                texto+= palavra + " "
            else:
                texto= texto[:-1]
                texto+="\n"
        self.txt_edit.delete(1.0,"end")
        self.txt_edit.insert(1.0,texto)
        self.callback()

    def posicao_inicial(self,s, lista):
        for palavra, pos_start, pos_end in reversed(lista):
            if (s == palavra):
                return pos_end
                break
        return False

    def ultima_posicao(self, lista):
        if (len(lista) > 0):
            return lista[-1][2]
        else:
            return -1
  
    def check_dicionario(self,s):
        hash = self.dicionario.palavras.hash(s)
        if (s != self.dicionario.palavras.tabela[hash]):
            return False
        else:
            return True
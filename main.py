from editor import Editor
from hashing import *

def main():
    hash = TabelaHash()
    f = open("dicionario.txt", "r")
    linha = " "
    while (linha != ""):
        linha = f.readline()
        hash.armazenar(linha)
    f.close()
    Editor.telaPrincipal()

if __name__ == "__main__":
    main()
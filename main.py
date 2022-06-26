from editor import Editor
from dicionario import Dicionario

def main():
    dic = Dicionario()
    editor = Editor(dic)
    editor.telaPrincipal()

if __name__ == "__main__":
    main()
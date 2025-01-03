import os
import random
from tkinter import messagebox

def verificar_usuario():
    usuario = os.getlogin().lower()  
    parte_do_nome = "Vinicius".lower()

    if parte_do_nome in usuario:
        resultado = random.randint(1, 20) 
        if resultado > 1:
            print(resultado)
        else:
            messagebox.showerror("Resultado", f"ERRO: {resultado} - O script falhou, tente novamente.")
            exit()  
    else:
        print(usuario)


import os
from PIL import Image
import customtkinter as ctk
import tkinter as tk
import time
import pyautogui
from tkinter import messagebox, simpledialog
import imagens.rotulos as rotulos
from utils import RepetidorTeclas, wait_and_click, falar, verifica_caps_lock, desativar_caps_lock
# from verificacao import verificar_usuario

repetidor = RepetidorTeclas()
tempo = 0.2

#FUNÇÃO OST BEMISA
def ost_vamtec(placa, ticket, peso, emissao):
    # Confirmação inicial
    confirmacao = messagebox.askquestion(
        "Confirmação", 
        f"Pelo amor de Deus\nConfira as informações digitadas no programa \nConfirma o preenchimento?", 
        icon='question'
    )

    if confirmacao == 'yes':
        # Pergunta qual opção o usuário deseja
        escolha = simpledialog.askstring(
            "Escolha", 
            "Escolha uma opção:\n1. Vamtec Alegre\n2. Vamtec limoeiro"
        )

        if escolha == "1":
            pagador_cnpj = '22034458000366'
            remetente_cnpj = '22034458000102'
            destinatario_cnpj = '22034458000366'
            material = '712'
            escolha_texto = "Vamtec Alegre"
            falar('Manifestando Vamtec Alegre')
        elif escolha == "2":
            pagador_cnpj = '22034458000366'
            remetente_cnpj = '22034458000366'
            destinatario_cnpj = '22034458000102'
            material = '475'
            escolha_texto =  "Vamtec limoeiro"
            falar('Manifestando Vamtec limoeiro')

        else:
            messagebox.showerror("Erro", "Opção inválida! Tarefa cancelada.")
        
        # Verificar e ajustar Caps Lock
        if verifica_caps_lock():
            desativar_caps_lock()
            print("Caps Lock estava ativado e foi desativado.")
        else:
            print("Caps Lock não está ativado.")
        
        wait_and_click(rotulos.imagens_faturamento, deslocamento_x=0)
        time.sleep(0.5)
        repetidor.pressionar_tecla('down',2)
        pyautogui.press('right')
        repetidor.pressionar_tecla('enter', 1, 2.5)
        wait_and_click(rotulos.imagens_incluir,deslocamento_x=0)
        time.sleep(2)
        repetidor.pressionar_tecla('tab',7,0.2)
        wait_and_click(rotulos.imagens_placa, deslocamento_x=70)
        time.sleep(tempo)
        pyautogui.write(placa)
        pyautogui.press('tab')
        time.sleep(tempo)
    # Verifica se o aviso está presente na tela
        repetidor.pressionar_tecla('enter', 4, 0.3)

        wait_and_click(rotulos.imagens_pagador,deslocamento_x=60)
        time.sleep(tempo)
        pyautogui.write(pagador_cnpj)
        repetidor.pressionar_tecla('tab', 1, 0.3)
        wait_and_click(rotulos.imagens_remetente,deslocamento_x=60)
        time.sleep(tempo)
        pyautogui.write(remetente_cnpj)
        repetidor.pressionar_tecla('tab', 1, 0.3)
        wait_and_click(rotulos.imagens_destinatario,deslocamento_x=60)
        time.sleep(tempo)
        pyautogui.write(destinatario_cnpj)

        time.sleep(0.3)
        wait_and_click(rotulos.imagens_compcarga,deslocamento_x=0)
        time.sleep(0.5)
        wait_and_click(rotulos.imagens_insere,deslocamento_x=0)
        time.sleep(tempo)
        repetidor.pressionar_tecla('enter',1, 0.3)
        #numero de série da nota
        wait_and_click(rotulos.imagens_serienf,deslocamento_x=50)
        time.sleep(tempo)
        pyautogui.write('99')
        time.sleep(tempo)
        #numero da nota
        repetidor.pressionar_tecla('tab', 1, 0.3)
        pyautogui.write(ticket)
        time.sleep(tempo)
        #data e hora de emissão da nota
        repetidor.pressionar_tecla('tab', 1, 0.3)
        pyautogui.write(emissao)
        time.sleep(tempo)
        #chave de acesso
        repetidor.pressionar_tecla('tab', 2, 0.3)
        pyautogui.write(material)
        time.sleep(tempo)
        repetidor.pressionar_tecla('tab', 2, 0.3)
        pyautogui.write("5905")
        time.sleep(tempo)
        repetidor.pressionar_tecla('tab', 2, 0.3)
        pyautogui.write(peso)
        time.sleep(tempo)
        repetidor.pressionar_tecla('tab', 1, 0.3)
        pyautogui.write(peso)
        repetidor.pressionar_tecla('tab', 1, 0.3)
        repetidor.pressionar_tecla('enter', 1, 0.3)
        wait_and_click(rotulos.imagens_valor_mercadoria_ost_tcb,deslocamento_x=50)
        time.sleep(1)
        pyautogui.write('0,01')
        time.sleep(tempo)
        repetidor.pressionar_tecla('tab', 1, 0.3)
        
        messagebox.showinfo("Info","Finalizado! \n dados fornecidos foram preenchidos, por favor continue manualmente.")
        return escolha_texto
    else:
        messagebox.showinfo("Info","Tarefa cancelada pelo usuário")
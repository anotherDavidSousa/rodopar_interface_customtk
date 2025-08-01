import os
from PIL import Image
import customtkinter as ctk
import tkinter as tk
import time
import pyautogui
from tkinter import messagebox, simpledialog
import imagens.rotulos as rotulos
from utils import RepetidorTeclas, wait_and_click, falar, verifica_caps_lock, desativar_caps_lock

repetidor = RepetidorTeclas()
tempo = 0.2

#FUNÇÃO OST BEMISA
def ost_bemisa_geral(placa):
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
            "Escolha uma opção:\n1. TCB - Timoteo\n2. TBJC - Terminal João Correio - Santana do Paraíso\n3. TCS - Terminal de Cargas Sarzedo"
        )

        if escolha == "1":
            # Dados para TCB Bemisa - Timoteo
            pagador_cnpj = '08720614000664'
            remetente_cnpj = '08720614000664'
            destinatario_cnpj = '15643555000390'
            falar('Manifestando para Timoteo TCB')
            escolha_texto = "TCB"
        elif escolha == "2":
            # Dados para Terminal João Correio - Santana do Paraíso
            pagador_cnpj = '08720614000664'
            remetente_cnpj = '08720614000664'
            destinatario_cnpj = '15643555000471'
            falar('Manifestando para Terminal João Correia')
            escolha_texto =  "TBJC"
        
        elif escolha == "3":
            # Dados para Terminal João Correio - Santana do Paraíso
            pagador_cnpj = '08720614000664'
            remetente_cnpj = '08720614000664'
            destinatario_cnpj = '08720614000664'
            terminal_entrega = '07695967000184'
            falar('Manifestando para Terminal de cargas SARZEDO')
            escolha_texto =  "TCS"
            
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
        repetidor.pressionar_tecla('tab', 1, 0.3)
        if escolha == '3':
            repetidor.pressionar_tecla('tab',6)
            time.sleep(tempo)
            pyautogui.write(terminal_entrega)
            time.sleep(tempo)

        messagebox.showinfo("Info","Finalizado! \n dados fornecidos foram preenchidos, por favor continue manualmente.")
        return escolha_texto
    else:
        messagebox.showinfo("Info","Tarefa cancelada pelo usuário")
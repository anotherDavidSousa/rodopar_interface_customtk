from tkinter import messagebox
import time
import pyautogui
import imagens.rotulos as rotulos
from utils import RepetidorTeclas, wait_and_click, verifica_caps_lock, desativar_caps_lock
from xml_process.XML import DadosXML, solicitar_caminho_xml
import json

repetidor = RepetidorTeclas()

with open('configs/produtos.json', 'r') as arquivo:
    produtos = json.load(arquivo)

class ProcessadorXML3:
    @staticmethod
    def processar_arquivo_3(placa, dt, tempo):
        try:
            # Solicitar o arquivo XML
            caminho_arquivo = solicitar_caminho_xml()
            print(f"Caminho do arquivo selecionado: {caminho_arquivo}")
            if not caminho_arquivo:
                messagebox.showwarning("Aviso", "Nenhum arquivo selecionado!")
                return None

            # Criar uma instância de DadosXML e processar o arquivo
            dados = DadosXML()
            dados.extrair_informacao(caminho_arquivo)



        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
            # return None

        # Solicitar confirmação do usuário
        confirmacao = messagebox.askquestion(
            "Confirmação",
            f"Continuar o preenchimento do CTE com a nota de número:\n{dados.nNF} e placa: {placa}\n"
            f"Por favor, confira o número da nota.\nConfirma o preenchimento?",
            icon='question'
        )

        if confirmacao == 'yes':
            # Continuar com o preenchimento
            if verifica_caps_lock():
                desativar_caps_lock()
                print("Caps Lock estava ativado e foi desativado.")
            else:
                print("Caps Lock não está ativado.")

            if dados.cnpj_emit == '08720614000664' and dados.cnpj_dest == '08720614000907' or dados.cnpj_emit == '33390170001312' and dados.cnpj_dest =='08720614000664' or dados.cnpj_emit =='22034458000366' and dados.cnpj_dest =='33390170001312':
                time.sleep(2)
                wait_and_click(rotulos.imagens_faturamento, deslocamento_x=0)
                time.sleep(0.5)
                repetidor.pressionar_tecla('down',2)
                pyautogui.press('right')
                repetidor.pressionar_tecla('enter', 1, 2.5)
            else:
                time.sleep(2)
                wait_and_click(rotulos.imagens_faturamento, deslocamento_x=0)
                time.sleep(0.5)
                repetidor.pressionar_tecla('down',2)
                pyautogui.press('right')
                repetidor.pressionar_tecla('down', 1, 0.2)
                repetidor.pressionar_tecla('enter', 1, 2.5)
            wait_and_click(rotulos.imagens_incluir,deslocamento_x=0)
            time.sleep(0.3)
            repetidor.pressionar_tecla('tab',7,0.2)
            wait_and_click(rotulos.imagens_placa, deslocamento_x=70)
            time.sleep(tempo)
            pyautogui.write(placa)
            time.sleep(tempo)
            pyautogui.press('tab')
            time.sleep(tempo)
                # Verifica se o aviso está presente na tela
            repetidor.pressionar_tecla('enter', 4, 0.3)
            if dados.tomador_frete == '1':
                wait_and_click(rotulos.imagens_pagador,deslocamento_x=60)
                time.sleep(tempo)
                pyautogui.write(dados.cnpj_dest)
                repetidor.pressionar_tecla('tab', 1, 0.3)
                wait_and_click(rotulos.imagens_remetente,deslocamento_x=60)
                time.sleep(tempo)
                pyautogui.write(dados.cnpj_emit)
                repetidor.pressionar_tecla('tab', 1, 0.3)
                wait_and_click(rotulos.imagens_destinatario,deslocamento_x=60)
                time.sleep(tempo)
                pyautogui.write(dados.cnpj_dest)
            else:
                wait_and_click(rotulos.imagens_pagador,deslocamento_x=60)
                time.sleep(tempo)
                pyautogui.write(dados.cnpj_emit)
                repetidor.pressionar_tecla('tab', 1, 0.3)
                wait_and_click(rotulos.imagens_remetente,deslocamento_x=60)
                time.sleep(tempo)
                pyautogui.write(dados.cnpj_emit)
                repetidor.pressionar_tecla('tab', 1, 0.3)
                wait_and_click(rotulos.imagens_destinatario,deslocamento_x=60)
                time.sleep(tempo)
                pyautogui.write(dados.cnpj_dest)
            
            time.sleep(0.5)
            if dados.cnpj_emit == '08720614000664' and dados.cnpj_dest == '08720614000907':
                repetidor.pressionar_tecla('tab',6)
                time.sleep(tempo)
                pyautogui.write(dados.cnpj_dest)
                time.sleep(tempo)
            elif dados.cnpj_emit == '08720614000664' and dados.cnpj_dest == '60894730002582' or dados.cnpj_emit == '25462356000259' and dados.cnpj_dest == '60894730002582' or dados.cnpj_emit =='17227422000105' and dados.cnpj_dest == '60894730002582' or dados.cnpj_emit == '08175256000141' and dados.cnpj_dest == '60894730002582':
                wait_and_click(rotulos.imagens_adicionais,deslocamento_x=0)
                time.sleep(tempo)
                #wait_and_click(rotulos.imagens_adicionais,deslocamento_x=100, deslocamento_y=40)
                wait_and_click(rotulos.imagens_nossaref)
                time.sleep(tempo)
                pyautogui.write(dt)
                #mineração guanhaes para joão correia
            elif dados.cnpj_emit == '17903693000125' and dados.cnpj_dest == '08720614000664':
                repetidor.pressionar_tecla('tab',6)
                time.sleep(tempo)
                pyautogui.write(dados.cnpj_entrega)
                time.sleep(tempo)
            elif dados.cnpj_emit == '31732059000106' and dados.cnpj_dest == '31096483000284':
                repetidor.pressionar_tecla('tab',6)
                time.sleep(tempo)
                pyautogui.write('15643555000471')
                time.sleep(tempo)
            time.sleep(0.5)
            repetidor.pressionar_tecla('tab', 1, 0.3)
            messagebox.showinfo("Info","Finalizado! \n dados fornecidos foram preenchidos, por favor continue manualmente.")
        else:
            messagebox.showinfo("Info","Tarefa cancelada pelo usuário")


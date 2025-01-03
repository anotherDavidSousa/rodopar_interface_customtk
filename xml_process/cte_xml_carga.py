from tkinter import messagebox
import time
import pyautogui
import imagens.rotulos as rotulos
from funcoes import RepetidorTeclas, wait_and_click, verifica_caps_lock, desativar_caps_lock
from xml_process.XML import DadosXML, solicitar_caminho_xml
import json

repetidor = RepetidorTeclas()
tempo = 0.2

with open('produtos.json', 'r') as arquivo:
    produtos = json.load(arquivo)

class ProcessadorXML2:
    @staticmethod
    def processar_arquivo_2():
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
            f"Continuar o preenchimento do CTE com a nota de número:\n{dados.nNF}\n"
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

            time.sleep(2)
            wait_and_click(rotulos.imagens_insere,deslocamento_x=0)
            time.sleep(tempo)
            repetidor.pressionar_tecla('enter',1, 0.3)
            #numero de série da nota
            wait_and_click(rotulos.imagens_serienf,deslocamento_x=50)
            time.sleep(tempo)
            pyautogui.write(dados.serie_nf)
            time.sleep(tempo)
            #numero da nota
            repetidor.pressionar_tecla('tab', 1, 0.3)
            pyautogui.write(dados.nNF)
            time.sleep(tempo)
            #data e hora de emissão da nota
            repetidor.pressionar_tecla('tab', 1, 0.3)
            pyautogui.write(dados.dhRecbto)
            time.sleep(tempo)
            #chave de acesso
            repetidor.pressionar_tecla('tab', 1, 0.3)
            pyautogui.write(dados.chNFe)
            time.sleep(tempo)
            repetidor.pressionar_tecla('tab', 1, 0.3)
            #produtos aqui
            if dados.produto in produtos:
                pyautogui.write(produtos[dados.produto])
                time.sleep(tempo)
            else:
                print("Produto não encontrado")
            time.sleep(tempo)
            repetidor.pressionar_tecla('tab', 2, 0.3)
            pyautogui.write(dados.cfop_text)
            time.sleep(tempo)
            repetidor.pressionar_tecla('tab', 2, 0.3)
            if dados.cnpj_emit == '17903693000125' and dados.cnpj_dest == '08720614000907' or dados.cnpj_emit == '35452938000208' and dados.cnpj_dest == '14427957000123' or dados.cnpj_emit == '17903693000125' and dados.cnpj_dest == '08720614000664' or dados.cnpj_emit == '31732059000106' and dados.cnpj_dest == '31096483000284' or dados.cnpj_emit =='22034458000366' and dados.cnpj_dest =='33390170001312':
                #repetidor.pressionar_tecla('tab', 1, 0.3)
                time.sleep(1)
                pyautogui.write(dados.pesoqCom)
                time.sleep(1)
                repetidor.pressionar_tecla('tab', 1, 0.3)
                time.sleep(1)
                pyautogui.write(dados.pesoqCom)
                time.sleep(1)
            elif dados.cnpj_emit == '27748484000108' and dados.cnpj_dest =='31096483000284':
                #repetidor.pressionar_tecla('tab', 1, 0.3)
                time.sleep(1)
                pyautogui.write(dados.atlas_prod)
                time.sleep(1)
                repetidor.pressionar_tecla('tab', 1, 0.3)
                time.sleep(1)
                pyautogui.write(dados.atlas_prod)
                time.sleep(1)
            else:
                time.sleep(1)
                pyautogui.write(dados.pesoL)
                time.sleep(1)
                time.sleep(tempo)
                repetidor.pressionar_tecla('tab', 1, 0.3)
                time.sleep(1)
                pyautogui.write(dados.pesoL)
                time.sleep(1)
            repetidor.pressionar_tecla('tab', 1, 0.3)
            repetidor.pressionar_tecla('enter', 1, 0.3)
            wait_and_click(rotulos.imagens_valor,deslocamento_x=50)
            time.sleep(tempo)
            if dados.cnpj_emit == '08720614000664' and dados.cnpj_dest == '08720614000907' or dados.cnpj_emit == '33390170001312' and dados.cnpj_dest =='08720614000664' or dados.cnpj_emit =='22034458000366' and dados.cnpj_dest =='33390170001312' or dados.cnpj_emit =='31096483000284' and dados.cnpj_dest == '15643555000471':
                wait_and_click(rotulos.imagens_valor_mercadoria_ost_tcb,deslocamento_x=50)
                time.sleep(tempo)
                pyautogui.write(dados.vProd)
                
            else:
                wait_and_click(rotulos.imagens_valor,deslocamento_x=50)
                time.sleep(tempo)
                pyautogui.write(dados.vLiq)

            repetidor.pressionar_tecla('tab', 1, 0.3)
            messagebox.showinfo("Info","Finalizado! \n dados fornecidos foram preenchidos, por favor continue manualmente.")
        else:
            messagebox.showinfo("Info","Tarefa cancelada pelo usuário")


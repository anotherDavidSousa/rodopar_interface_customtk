import os
from tkinter import messagebox
import time
import pyautogui
import imagens.rotulos as rotulos
from utils import RepetidorTeclas, wait_and_click, verifica_caps_lock, desativar_caps_lock, falar
from xml_process.XML import DadosXML, solicitar_caminho_xml
import json

repetidor = RepetidorTeclas()

class ProcessadorXML2:
    @staticmethod
    def processar_arquivo_2(tempo):
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
            caminho_json = r"config/mensagem_rotas.json"
            
            with open(caminho_json, 'r', encoding='utf-8') as arquivo_json:
                dicionario_cnpjs = json.load(arquivo_json)
            dataemissao = dados.dhRecbto
            data_formatada = f"{dataemissao[:2]}/{dataemissao[2:4]}"
            chave_cnpjs = f"{dados.cnpj_emit}-{dados.cnpj_dest}"

            mensagem_resultado = dicionario_cnpjs.get(chave_cnpjs, "Chave não encontrada no dicionário.")
            mensagem_final = f"{mensagem_resultado} - Data: {data_formatada} - NF: {dados.nNF}"

        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {str(e)}")
            return None

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

            time.sleep(3)
            wait_and_click(rotulos.imagens_insere,deslocamento_x=0)
            time.sleep(tempo)
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
            caminho_json_produtos = os.path.join('config', 'produtos.json')

            try:
                with open(caminho_json_produtos, 'r', encoding='utf-8') as arquivo:
                    produtos = json.load(arquivo)
                
                produto = getattr(dados, 'produto', None)
                
                if produto and produto in produtos:
                    pyautogui.write(produtos[produto])
                    time.sleep(tempo)
                else:
                    falar(f"Produto '{produto}' não localizado" if produto else "Campo 'produto' vazio")
            except FileNotFoundError:
                falar("Arquivo de produtos não encontrado")
            except json.JSONDecodeError:
                falar("Erro no formato do JSON de produtos")

            time.sleep(tempo)
            repetidor.pressionar_tecla('tab', 2, 0.3)
            pyautogui.write(dados.cfop_text)
            time.sleep(tempo)
            repetidor.pressionar_tecla('tab', 2, 0.3)

            caminho_json_peso = os.path.join('config', 'peso_nota.json') 

            with open(caminho_json_peso, 'r', encoding='utf-8') as f:
                peso_nota = json.load(f)

            campo_peso = None

            for regra in peso_nota['regras']:
                if dados.cnpj_emit == regra['cnpj_emit'] and dados.cnpj_dest == regra['cnpj_dest']:
                    campo_peso = regra['campo_peso']
                    break

            if not campo_peso:
                campo_peso = peso_nota['padrao']['campo_peso']

            time.sleep(tempo)
            pyautogui.write(getattr(dados, campo_peso))
            time.sleep(tempo)
            repetidor.pressionar_tecla('tab', 1, 0.3)
            time.sleep(tempo)
            pyautogui.write(getattr(dados, campo_peso))
            time.sleep(tempo)
            repetidor.pressionar_tecla('tab', 1, 0.3)
            repetidor.pressionar_tecla('enter', 1, 0.3)
            
            # --- INÍCIO DA LÓGICA ATUALIZADA ---
            
            # Carrega o JSON de valor da nota
            caminho_json_valor = os.path.join('config', 'valor_nota.json')
            with open(caminho_json_valor, 'r', encoding='utf-8') as g:
                valor_nota = json.load(g)

            # Determina qual campo de valor usar (vNF ou vProd)
            campo_valor = None
            for regra in valor_nota['regras']:
                if dados.cnpj_emit == regra['cnpj_emit'] and dados.cnpj_dest == regra['cnpj_dest']:
                    campo_valor = regra['campo_valor']
                    break
            if not campo_valor:
                campo_valor = valor_nota['padrao']['campo_valor']

            # --- LÓGICA REAPROVEITÁVEL ---
            # Lendo o JSON de faturamento novamente para determinar o tipo de serviço.
            # Esta seção agora é autossuficiente.
            path_json_faturamento_local = os.path.join('config', 'tipo_faturamento.json')
            servico_local = "conhecimento_de_transporte" # Define um padrão
            try:
                with open(path_json_faturamento_local, 'r', encoding='utf-8') as arquivo_faturamento:
                    faturamento_local = json.load(arquivo_faturamento)
                
                # Procura a combinação de CNPJs na lista de "ordem_de_servico"
                for caso in faturamento_local.get("ordem_de_servico", []):
                    if dados.cnpj_emit == caso.get("cnpj_emit") and dados.cnpj_dest == caso.get("cnpj_dest"):
                        servico_local = "ordem_de_servico"
                        break # Encontrou a regra, pode parar de procurar
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Erro ao ler o JSON de faturamento local: {e}")
                # O código continuará com o padrão "conhecimento_de_transporte" se houver erro

            # Clica na imagem correta com base no tipo de serviço verificado localmente
            if servico_local == "conhecimento_de_transporte":
                print("Clicando em 'Valor' para Conhecimento de Transporte.")
                wait_and_click(rotulos.imagens_valor, deslocamento_x=50)
            else: # Se for "ordem_de_servico"
                print("Clicando em 'Valor Mercadoria' para Ordem de Serviço.")
                wait_and_click(rotulos.imagens_valor_mercadoria_ost_tcb, deslocamento_x=50)
            
            # Preenche o valor
            time.sleep(tempo)
            pyautogui.write(getattr(dados, campo_valor))
            
            # --- FIM DA LÓGICA ATUALIZADA ---
                
            repetidor.pressionar_tecla('tab', 1, 0.3)
            messagebox.showinfo("Info","Finalizado! \n dados fornecidos foram preenchidos, por favor continue manualmente.")
        else:
            messagebox.showinfo("Info","Tarefa cancelada pelo usuário")
        return mensagem_final

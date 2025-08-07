import os
import xml.etree.ElementTree as ET
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox
import winsound
from utils import falar
beep_wav = "media/audio/beep.wav"
def tocar_alarme_wav(beep_wav):
    """Toca um alarme sonoro usando um arquivo .wav."""
    try:
        winsound.PlaySound(beep_wav, winsound.SND_FILENAME | winsound.SND_ASYNC)
    except RuntimeError as e:
        print(f"Erro ao reproduzir som: {e}")


def mostrar_avisos(msg):
    """Exibe um aviso para o usuário que requer confirmação."""
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    messagebox.showwarning("Aviso de Dados Incorretos", msg)


def extrair_valor_elemento(root, caminho_xpath):
    elemento = root.find(caminho_xpath)
    return elemento.text if elemento is not None else None


def formatar_valor(valor):
    try:
        return float(valor.replace('.', ',')) if valor else None
    except ValueError:
        return None


def formatar_data(data_str):
    try:
        return datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S") if data_str else None
    except ValueError:
        return None


def solicitar_caminho_xml():
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo XML",
        filetypes=[("Arquivos XML", "*.xml")]
    )
    return caminho_arquivo


class DadosXML:
    def __init__(self):
        self.chNFe = None
        self.dhRecbto = None
        self.natOp = None
        self.pesoL = None
        self.vLiq = None
        self.vProd = None
        self.atlas_prod = None
        self.fertran = None
        self.nNF = None
        self.serie_nf = None
        self.cnpj_emit = None
        self.cnpj_dest = None
        self.nome_dest = None
        self.nome_emit = None
        self.nome_entrega = None
        self.cnpj_entrega = None
        self.doc_transp = None
        self.cfop_text = None
        self.produto = None
        self.tomador_frete = None
        self.pesoqCom = None
        self.pesoB = None

    def validar_dhRecbto(self):
        if self.dhRecbto and (len(self.dhRecbto) != 12 or not self.dhRecbto.isdigit()):
            mensagem = "A data/hora no XML está incorreta ou possui caracteres inválidos!"
            print("AVISO:", mensagem)
            tocar_alarme_wav(beep_wav)  # Alarme mais longo
            mostrar_avisos(mensagem)

    def validar_peso(self, peso, nome_campo):
        if peso and len(peso) < 5:
            mensagem = (f"O campo '{nome_campo}' está fora do normal e pode conter erro de digitação! \n"
                        f"O valor apresentado é: {self.pesoL} \n"
                        "VERIFICAR SE PREENCHERA O VALOR DO PESO CORRETAMENTE NO RODOPAR")
            print("AVISO:", mensagem)
            tocar_alarme_wav(beep_wav)  # Toca um arquivo de alerta específico
            mostrar_avisos(mensagem)

    def validar_natureza_operacao(self, natOp, produto):
        if natOp =='REMESSA P/ FORMACAO DE LOTE FERROVIARIO' or natOp =='REM. FORM. LOTE FERROV. (DIF)' or produto == 'MINERIO DE FERRO SINTER FEED M05' or produto == 'MINERIO DE FERRO SINTER FEED M05':
            mensagem = (f"ESSA NOTA PARECE SER UMA NOTA DE TROCA \n E NÃO DEVE SER MANIFESTADA \n POR FAVOR CONFIRA A NOTA")
            print("AVISO:", mensagem)
            tocar_alarme_wav(beep_wav)  # Toca um arquivo de alerta específico
            falar('NOTA DE TROCA,\n VERIFIQUE O RODAPÉ DA NOTA FISCAL PARA LOCALIZAR O NUMERO DA NOTA CORRETA')
            mostrar_avisos(mensagem)
            



    def extrair_informacao(self, caminho_arquivo):
        tree = ET.parse(caminho_arquivo)
        root = tree.getroot()

        self.chNFe = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}chNFe')

        dhRecbto_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}dhRecbto')
        dhRecbto = dhRecbto_element.text if dhRecbto_element is not None else None
        if dhRecbto:
            data_part = dhRecbto[:10].replace('-', '')
            data_part = dhRecbto[8:10] + dhRecbto[5:7] + dhRecbto[0:4]
            hora_part = dhRecbto[11:16].replace(':', '')
            self.dhRecbto = f"{data_part}{hora_part}"

        self.validar_dhRecbto()

        pesoL_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}vol/{http://www.portalfiscal.inf.br/nfe}pesoL')
        self.pesoL = pesoL_element.text.split('.')[0] if pesoL_element is not None else None
        if self.pesoL:
            self.pesoL = self.pesoL[:5].replace(',', '').replace('.', '')
        self.validar_peso(self.pesoL, "pesoL")

        pesoqCom_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}qCom')
        self.pesoqCom = None
        if pesoqCom_element is not None:
            pesoqCom = pesoqCom_element.text.replace('.', '').replace(',', '')
            if len(pesoqCom) > 5:
                pesoqCom = pesoqCom[:5]
            self.pesoqCom = pesoqCom
        self.validar_peso(self.pesoqCom, "qCom")

        vLiq_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}cobr/{http://www.portalfiscal.inf.br/nfe}fat/{http://www.portalfiscal.inf.br/nfe}vLiq')
        self.vLiq = vLiq_element.text if vLiq_element is not None else None
        if self.vLiq:
            self.vLiq = self.vLiq.replace('.', ',')  # Substitui ponto por vírgula
        
        vProd_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}vProd')
        self.vProd = vProd_element.text if vProd_element is not None else None
        if self.vProd:
            self.vProd = self.vProd.replace('.', ',')

        atlas_prod_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}qCom')
        self.atlas_prod = atlas_prod_element.text if atlas_prod_element is not None else None
        if self.atlas_prod:
            self.atlas_prod = self.atlas_prod.replace(',', '')
        # pesoB criado para o XML da MGOXIDO x JOÃO MONLEVADE
        pesoB_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}transp/{http://www.portalfiscal.inf.br/nfe}vol/{http://www.portalfiscal.inf.br/nfe}pesoB')
        self.pesoB = pesoB_element.text if pesoB_element is not None else None
        if self.pesoB:
            self.pesoB = self.pesoB.replace('.', '')

        self.fertran = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}transporta/{http://www.portalfiscal.inf.br/nfe}xNome')
        self.nNF = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}nNF')
        self.natOp = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}natOp')
        self.serie_nf = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}serie')
        self.cnpj_emit = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}CNPJ')
        if not self.cnpj_emit:
            self.cnpj_emit = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}CPF')
        self.cnpj_dest = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}CNPJ')
        if not self.cnpj_dest:
            self.cnpj_dest = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}CPF')
        self.nome_dest = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}xNome')
        self.nome_emit = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}xNome')
        self.nome_entrega = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}entrega/{http://www.portalfiscal.inf.br/nfe}xNome')
        self.cnpj_entrega = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}entrega/{http://www.portalfiscal.inf.br/nfe}CNPJ')
        self.doc_transp = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}obsCont/{http://www.portalfiscal.inf.br/nfe}xTexto')
        self.cfop_text = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}CFOP')
        self.produto = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}xProd')
        self.tomador_frete = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}transp/{http://www.portalfiscal.inf.br/nfe}modFrete')
        
        self.validar_natureza_operacao(self.natOp, self.produto)
        

        print("Chave",self.chNFe)
        print("data",self.dhRecbto)
        print("peso pesoL",self.pesoL)
        print("valor vliq",self.vLiq)
        print("valor Vprod",self.vProd)
        print("produto atlas",self.atlas_prod)
        print("transportadora",self.fertran)
        print("numero da nota",self.nNF)
        print("serie",self.serie_nf)
        print("cnpj emissor",self.cnpj_emit)
        print("cnpj destinatario",self.cnpj_dest)
        print("nome emitente",self.nome_emit)
        print("nome destinario",self.nome_dest)
        print("nome local de entrega se tiver",self.nome_entrega)
        print("cnpj local de entrega se tiver",self.cnpj_entrega)
        print("documento de transporte se tiver",self.doc_transp)
        print("cfop",self.cfop_text)
        print("nome do produto",self.produto)
        print("pagador do frete",self.tomador_frete)
        print("peso qCom",self.pesoqCom)
        print("natureza", self.natOp)
        print("pesoB", self.pesoB)

import os
import xml.etree.ElementTree as ET
from datetime import datetime
import tkinter as tk
from tkinter import filedialog


# Função para extrair o valor de um elemento XML
def extrair_valor_elemento(root, caminho_xpath):
    elemento = root.find(caminho_xpath)
    return elemento.text if elemento is not None else None  # Retorna o texto do elemento ou None

# Função para tratar e formatar o valor monetário
def formatar_valor(valor):
    try:
        return float(valor.replace(',', '.')) if valor else None
    except ValueError:
        return None

# Função para tratar e formatar a data
def formatar_data(data_str):
    try:
        return datetime.strptime(data_str, "%Y-%m-%dT%H:%M:%S") if data_str else None
    except ValueError:
        return None

# Função para solicitar o caminho do arquivo XML com filedialog
def solicitar_caminho_xml():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal
    caminho_arquivo = filedialog.askopenfilename(
        title="Selecione o arquivo XML",
        filetypes=[("Arquivos XML", "*.xml")]
    )
    return caminho_arquivo

# Classe para organizar os dados extraídos do XML
class DadosXML:
    def __init__(self):
        # Inicializa as variáveis com None
        self.chNFe = None
        self.dhRecbto = None
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

    # Função para extrair e processar as informações do XML
    def extrair_informacao(self, caminho_arquivo):
        tree = ET.parse(caminho_arquivo)  # Carrega o XML
        root = tree.getroot()  # Obtém o nó raiz do XML

        # Extrair o valor de chNFe
        self.chNFe = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}chNFe')

        # Processamento da data e hora (dhRecbto)
        dhRecbto_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}dhRecbto')
        dhRecbto = dhRecbto_element.text if dhRecbto_element is not None else None
        if dhRecbto:
            # Extrai a data no formato ddmmyyyy
            data_part = dhRecbto[:10].replace('-', '')
            data_part = dhRecbto[8:10] + dhRecbto[5:7] + dhRecbto[0:4]
            hora_part = dhRecbto[11:16].replace(':', '')
            # Formata a data e hora no formato desejado
            self.dhRecbto = f"{data_part}{hora_part}"

        # Processamento do pesoL
        pesoL_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}vol/{http://www.portalfiscal.inf.br/nfe}pesoL')
        self.pesoL = pesoL_element.text.split('.')[0] if pesoL_element is not None else None
        
        # Peso da nota mig mineração guanhães
        pesoqCom_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}qCom')
        if pesoqCom_element is not None:
            pesoqCom = pesoqCom_element.text.replace('.', '').replace(',', '')
            if len(pesoqCom) > 5:
                pesoqCom = pesoqCom[:5]  # Trunca para os primeiros 5 caracteres
            self.pesoqCom = pesoqCom
        else:
            self.pesoqCom = None

        # Processamento dos valores monetários vLiq e vProd
        vLiq_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}cobr/{http://www.portalfiscal.inf.br/nfe}fat/{http://www.portalfiscal.inf.br/nfe}vLiq')
        self.vLiq = vLiq_element.text if vLiq_element is not None else None
        if self.vLiq:
            self.vLiq = self.vLiq.replace('.', ',')  # Substitui ponto por vírgula

        vProd_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}vProd')
        self.vProd = vProd_element.text if vProd_element is not None else None
        if self.vProd:
            self.vProd = self.vProd.replace('.', ',')  # Substitui ponto por vírgula

        # Atlas_prod (quantidade de produtos)
        atlas_prod_element = root.find('.//{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}qCom')
        self.atlas_prod = atlas_prod_element.text if atlas_prod_element is not None else None
        if self.atlas_prod:
            self.atlas_prod = self.atlas_prod.replace(',', '')  # Remove vírgulas

        # Extração de outros dados
        self.fertran = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}transporta/{http://www.portalfiscal.inf.br/nfe}xNome')
        self.nNF = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}nNF')
        self.serie_nf = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}ide/{http://www.portalfiscal.inf.br/nfe}serie')
        self.cnpj_emit = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}CNPJ')
        self.cnpj_dest = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}CNPJ')
        self.nome_dest = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}dest/{http://www.portalfiscal.inf.br/nfe}xNome')
        self.nome_emit = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}emit/{http://www.portalfiscal.inf.br/nfe}xNome')
        self.nome_entrega = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}entrega/{http://www.portalfiscal.inf.br/nfe}xNome')
        self.cnpj_entrega = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}entrega/{http://www.portalfiscal.inf.br/nfe}CNPJ')
        self.doc_transp = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}obsCont/{http://www.portalfiscal.inf.br/nfe}xTexto')
        self.cfop_text = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}CFOP')
        self.produto = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}det/{http://www.portalfiscal.inf.br/nfe}prod/{http://www.portalfiscal.inf.br/nfe}xProd')
        self.tomador_frete = extrair_valor_elemento(root, './/{http://www.portalfiscal.inf.br/nfe}transp/{http://www.portalfiscal.inf.br/nfe}modFrete')
        
# Exemplo de uso
# dados_xml = DadosXML()
# caminho = solicitar_caminho_xml()  # Solicita o caminho do arquivo
# dados_xml.extrair_informacao(caminho)  # Extrai os dados


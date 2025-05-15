import os
import pyautogui
import time
import pyttsx3
import ctypes
import json



#DELETAR ARQUIVOS PDF E XML DA PASTA DE DOWNLOAD
def deletar_xml_na_pasta():
    user_profile = os.getenv('USERPROFILE')
    if user_profile and "claudio" in user_profile.lower():
        pasta_especifica = r"D:\Downloads"
    else:
        downloads_path = os.path.join(user_profile, 'Downloads')
        pasta_especifica = downloads_path

    for arquivo in os.listdir(pasta_especifica):
        if arquivo.endswith(".xml") or (arquivo.endswith(".pdf") and "CONTRATO" in arquivo.upper()) or (arquivo.endswith(".pdf") and "CTE" in arquivo.upper()) or (arquivo.endswith(".pdf") and "OST" in arquivo.upper()):
            caminho_arquivo = os.path.join(pasta_especifica, arquivo)
            os.remove(caminho_arquivo)
            print(f"Arquivo {arquivo} removido com sucesso.")

def verifica_caps_lock():
    return ctypes.windll.user32.GetKeyState(0x14) & 1

def desativar_caps_lock():
    ctypes.windll.user32.keybd_event(0x14, 0x45, 0x0001 | 0, 0)
    time.sleep(0.1)
    ctypes.windll.user32.keybd_event(0x14, 0x45, 0x0001 | 0x0002, 0)

def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

class RepetidorTeclas:
    def pressionar_tecla(self, tecla, vezes,tempo=0):
        for _ in range(vezes):
            pyautogui.press(tecla)
            time.sleep(tempo)

#FUNÇÃO LOCATEONSCREEN, O CORAÇÃO DO CÓDIGO
def wait_and_click(rotulos, deslocamento_x=40, deslocamento_y=0, confidence=0.7,max_attempts=3):
    attempts = 0
    while attempts < max_attempts:
        for rotulo in rotulos:
            try:
                posicao_rotulo = pyautogui.locateCenterOnScreen(rotulo, confidence=confidence)
                if posicao_rotulo:
                    click_position = (posicao_rotulo[0] + deslocamento_x, posicao_rotulo[1] + deslocamento_y)
                    pyautogui.click(click_position)
                    return
            except pyautogui.ImageNotFoundException:
                pass
        print(f"Texto '{rotulos}' não encontrado. Tentativa {attempts+1}/{max_attempts}. Aguardando...")
        attempts += 1
        time.sleep(1)
    print(f"Texto '{rotulos}' não encontrado. Aguardando...")
  
class MensagemExibida:
    @staticmethod
    def carregar_mensagem_rotas(caminho_arquivo="mensagem_rotas.json"):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                return json.load(arquivo)
        except FileNotFoundError:
            print("Arquivo mensagem_rotas.json não encontrado.")
            return {}

    @staticmethod
    def formatar_mensagem(cnpj_emit, cnpj_dest, nome_dest, dhRecbto, nNF):
        mensagem_rotas = MensagemExibida.carregar_mensagem_rotas()
        chave_cnpjs = f"{cnpj_emit}-{cnpj_dest}"

        nome_dest_formatado = mensagem_rotas.get(
            chave_cnpjs,
            nome_dest.replace("MUNICIPIO DE ", "")  # Valor padrão
        )

        try:
            data_formatada_nf = f"{dhRecbto[:2]}/{dhRecbto[2:4]}"  # Dia e mês no formato DD/MM
        except Exception:
            data_formatada_nf = "Data inválida"

        return (
            f" {nome_dest_formatado} Data: {data_formatada_nf} NF: {nNF}."
        )
    
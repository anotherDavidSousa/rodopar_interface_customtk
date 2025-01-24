import os
import time
import re
from PyPDF2 import PdfReader
import hashlib

# Configurações
USER_PROFILE = os.getenv("USERPROFILE")  # Diretório base do perfil do usuário
USER_NAME = os.getenv("USERNAME")  # Nome do usuário atual
MONITOR_DIR = (
    r"D:\Downloads" if USER_NAME.lower() == "david" else os.path.join(USER_PROFILE, "Downloads")
)
SEARCH_PATTERN = r"NºCONTRATO:\s*(\d{2})/(?:\w+|\d{2})/(\d+[\.,]?\d*)"
NEW_NAME_PREFIX = "CONTRATO_"  # Prefixo para o novo nome do arquivo
CHECK_INTERVAL = 5  # Intervalo entre varreduras em segundos

# Conjunto de hashes de arquivos já processados
processed_hashes = set()

def wait_for_file(file_path):
    """Aguarda até que o arquivo não esteja mais em uso."""
    while True:
        try:
            with open(file_path, 'rb'):
                break
        except (FileNotFoundError, PermissionError):
            time.sleep(0.5)

def gerar_hash_arquivo(file_path):
    """Gera um hash único com base no conteúdo do arquivo."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()

def renomear_com_sufixo(base_path, new_name):
    """Adiciona um sufixo incremental caso o nome do arquivo já exista."""
    base, ext = os.path.splitext(new_name)
    contador = 1
    new_path = os.path.join(base_path, new_name)
    while os.path.exists(new_path):
        new_path = os.path.join(base_path, f"{base}_{contador}{ext}")
        contador += 1
    return new_path

def process_pdf(file_path):
    """Processa o arquivo PDF e o renomeia, se necessário."""
    try:
        # Gera hash do arquivo para evitar reprocessamento
        file_hash = gerar_hash_arquivo(file_path)
        if file_hash in processed_hashes:
            # print(f"Arquivo já processado: {file_path}")
            return
        processed_hashes.add(file_hash)

        # Lê o conteúdo do PDF
        reader = PdfReader(file_path)
        content = "".join(page.extract_text() for page in reader.pages)

        # Procura pelo padrão do contrato no conteúdo
        match = re.search(SEARCH_PATTERN, content)
        if match:
            contrato_numero = match.group(2).replace(".", "")  # Extrai o número após a última barra e remove o ponto
            new_name = f"{NEW_NAME_PREFIX}{contrato_numero}.pdf"
            new_path = renomear_com_sufixo(MONITOR_DIR, new_name)
            os.rename(file_path, new_path)
            print(f"Arquivo renomeado para: {new_path}")
        else:
            print(f"NºCONTRATO: não encontrado em {file_path}")
    except Exception as e:
        print(f"Erro ao processar o arquivo {file_path}: {e}")

def monitor_directory(stop_event):
    """Verifica continuamente a pasta monitorada por novos arquivos."""
    print(f"Monitorando a pasta: {MONITOR_DIR}")
    while not stop_event.is_set():
        try:
            files = [f for f in os.listdir(MONITOR_DIR) if f.lower().endswith('.pdf')]
            for file_name in files:
                file_path = os.path.join(MONITOR_DIR, file_name)

                wait_for_file(file_path)
                process_pdf(file_path)

            time.sleep(CHECK_INTERVAL)
        except Exception as e:
            print(f"Erro no monitoramento: {e}")

def start_monitoring(stop_event):
    """Inicia o monitoramento em uma thread."""
    monitor_directory(stop_event)

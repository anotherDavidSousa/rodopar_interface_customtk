import requests
import os
import sys
import customtkinter as ctk
from packaging import version
import threading  # Para verificação periódica

class VersionChecker:
    def __init__(self, current_version, repo_api_url, download_url, token=None):
        self.current_version = current_version
        self.repo_api_url = repo_api_url
        self.download_url = download_url
        self.token = token  # Para autenticação opcional, se necessário

    def fetch_latest_version(self):
        """
        Busca a última versão publicada no repositório do GitHub.
        """
        headers = {}
        if self.token:
            headers["Authorization"] = f"token {self.token}"
        
        try:
            response = requests.get(self.repo_api_url, headers=headers)
            response.raise_for_status()
            data = response.json()

            # Captura a tag da última versão
            latest_version = data.get("tag_name")
            
            # Captura o primeiro asset de download, se existir
            if data.get("assets"):
                self.download_url = data["assets"][0]["browser_download_url"]

            return latest_version
        except Exception as e:
            print(f"Erro ao verificar a versão: {e}")
            return None

    def compare_versions(self):
        """
        Compara a versão atual com a mais recente e retorna a mais nova, se disponível.
        """
        latest_version = self.fetch_latest_version()
        if latest_version:
            # Usa a biblioteca `packaging` para comparar versões semanticamente
            if version.parse(latest_version) > version.parse(self.current_version):
                return latest_version
        return None

    def force_update(self):
        """
        Exibe uma interface gráfica obrigando o usuário a atualizar.
        """
        app = ctk.CTk()
        app.title("Atualização Obrigatória")
        app.geometry("400x200")
        
        label = ctk.CTkLabel(app, text="Uma nova versão está disponível.\nVocê deve atualizar para continuar!", font=("Arial", 14))
        label.pack(pady=20)
        
        def open_download():
            os.system(f'start {self.download_url}')  # Abre a URL do download
            sys.exit()
        
        download_button = ctk.CTkButton(app, text="Baixar Atualização", command=open_download)
        download_button.pack(pady=10)

        app.mainloop()

    def run(self):
        """
        Verifica a versão e força atualização, se necessário.
        """
        latest_version = self.compare_versions()
        if latest_version:
            print(f"Nova versão disponível: {latest_version}. Forçando atualização...")
            self.force_update()
        else:
            print("Você está usando a versão mais recente.")

    def start_periodic_check(self, interval=3600):
        """
        Inicia uma verificação periódica da versão.
        :param interval: Intervalo em segundos entre as verificações (padrão: 1 hora).
        """
        def periodic_check():
            print("Verificando versão periodicamente...")
            self.run()
            # Agenda a próxima verificação
            threading.Timer(interval, periodic_check).start()

        # Inicia a primeira verificação
        periodic_check()

# Configurações de versão e URLs
current_version = "v0.1.0-alpha"
repo_api_url = "https://api.github.com/repos/anotherDavidSousa/rodopar_interface_customtk/releases/latest"
download_url = "https://github.com/anotherDavidSousa/rodopar_interface_customtk/releases/latest"

# Instancia o verificador de versões
checker = VersionChecker(current_version, repo_api_url, download_url)

# Verificação inicial
checker.run()

# Inicia a verificação periódica (a cada 1 hora)
checker.start_periodic_check(interval=3600)  # 3600 segundos = 1 hora
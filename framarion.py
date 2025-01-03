from tkinter import Tk
from tkinter.filedialog import askopenfilename
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# Abrir janela de diálogo para selecionar o arquivo de texto
Tk().withdraw()  # Esconder a janela principal do tkinter
file_path = askopenfilename(title="Selecione o arquivo de Texto", filetypes=[("Arquivos de Texto", "*.txt")])

# Carregar o arquivo de texto em um DataFrame
with open(file_path, 'r') as file:
    documentos = [line.strip() for line in file]

df = pd.DataFrame(documentos, columns=["documentos"])

# Configuração do Selenium
chrome_options = Options()
chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
chrome_driver_path = r"D:\#Aquivos de Programas\chromedriver_win32\chromedriver.exe"
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)

# Acessar o site
driver.get("https://portal.e-fornecedores.ind.br/Default.aspx?cmp=Noticias.ascx")

# Realizar login
driver.find_element(By.ID, "ctlLoadedControl_txtLogin").send_keys("08925365")
driver.find_element(By.ID, "ctlLoadedControl_txtSenha").send_keys("fertra61")
driver.execute_script('document.getElementById("ctlLoadedControl_btnOK").click();')

time.sleep(1)

# Lista de valores possíveis no menu suspenso
fornecedor_opcoes = [
    "383929:0000052220:N",
    "383929:0000053687:N"
]

# Loop para processar cada item da lista (documentos)
for index, row in df.iterrows():
    documento = row['documentos']
    print(f"Processando documento: {documento}")
    
    resultado_encontrado = False

    # Tentar cada opção no menu suspenso até encontrar resultado ou esgotar opções
    for opcao in fornecedor_opcoes:
        try:
            # Selecionar a opção no menu suspenso
            select_element = driver.find_element(By.ID, "mnuPrincipal_lstFornecedor")
            select = Select(select_element)
            select.select_by_value(opcao)
            print(f"Selecionando opção: {opcao}")
            
            # Realizar a pesquisa com o documento
            input_element = driver.find_element(By.ID, "id_do_campo_documento")  # Substitua pelo ID correto
            input_element.clear()
            input_element.send_keys(documento)
            driver.find_element(By.ID, "id_do_botao_envio").click()  # Substitua pelo ID correto
            
            # Aguarde o carregamento do resultado
            time.sleep(2)
            
            # Verificar se o resultado foi encontrado
            try:
                # Tente encontrar um elemento indicando resultado positivo (substitua pelo seletor correto)
                driver.find_element(By.ID, "id_do_resultado_positivo")  # Substitua pelo ID correto
                print(f"Resultado encontrado para {documento} com a opção {opcao}")
                resultado_encontrado = True
                break  # Sai do loop de opções, pois encontramos um resultado
            except NoSuchElementException:
                print(f"Nenhum resultado encontrado para {documento} com a opção {opcao}")
        
        except Exception as e:
            print(f"Erro ao processar documento {documento} com a opção {opcao}: {e}")
    
    # Se nenhuma opção gerou resultados, trate aqui como desejar
    if not resultado_encontrado:
        print(f"Não foi possível encontrar resultados para o documento {documento} com nenhuma opção.")

# Finalizar o navegador
driver.quit()

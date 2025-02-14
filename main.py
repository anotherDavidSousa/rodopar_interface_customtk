import os
import threading
from PIL import Image
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import pdf_monitor
from utils import deletar_xml_na_pasta, falar
from ost_dadosfixos.ost_bemisa import ost_bemisa
from ost_dadosfixos.ost_bemisa_geral import ost_bemisa_geral
from ost_dadosfixos.ost_bemisa_carga import ost_bemisa_carga
from ost_dadosfixos.ost_vamtec import ost_vamtec
from ost_dadosfixos.ost_vamtec_geral import ost_vamtec_geral
from ost_dadosfixos.ost_vamtec_carga import ost_vamtec_carga
from xml_process.cte_xml import ProcessadorXML
from xml_process.cte_xml_carga import ProcessadorXML2
from xml_process.cte_xml_geral import ProcessadorXML3
from version_checker import VersionChecker

current_version = "v0.2.0-alpha"
repo_url = "https://api.github.com/repos/anotherDavidSousa/rodopar_interface_customtk/releases/latest"
download_url = "https://github.com/anotherDavidSousa/rodopar_interface_customtk/releases/latest"

# Verificação de versão
checker = VersionChecker(current_version, repo_url, download_url)
checker.run()  # Verifica a versão antes de iniciar a interface
checker.start_periodic_check(interval=3600)  # 3600 segundos = 1 hora

#EVENTOS DE MONITORAMENTE DE .PDF
monitor_thread = None
stop_event = threading.Event()  # Evento compartilhado para parar o monitoramento

def start_monitoring():
    global monitor_thread
    if monitor_thread and monitor_thread.is_alive():
        return  # Se o monitor já estiver ativo, não cria outro
    monitor_thread = threading.Thread(target=pdf_monitor.monitor_directory, args=(stop_event,), daemon=True)
    monitor_thread.start()
start_monitoring()
# Função para parar o monitoramento quando a interface for fechada
def on_close():
    stop_event.set()  # Notifica o monitoramento para parar
    if monitor_thread and monitor_thread.is_alive():
        monitor_thread.join()  # Aguarda o término da thread
    app.quit()  # Fecha a aplicação


#CTE E XML EM GERAL
def Manifestar_by_xml():
    placa = placa_cte_text.get()
    dt = dt_text.get()
    tempo_selecionado = tempo.get()

    # Chama o método e captura a mensagem final
    mensagem_final = ProcessadorXML.processar_arquivo(placa, dt,tempo_selecionado)

    if mensagem_final:
        # Atualiza o campo de texto somente leitura com a mensagem final
        nfe_info_var.set(mensagem_final)
    else:
        messagebox.showwarning("Aviso", "Nenhuma mensagem gerada ou ocorreu um erro.")
        nfe_info_var.set("")  # Limpa o campo caso necessário

def Manifestar_by_xml_parte_2():
    tempo_selecionado = tempo.get()
    # ProcessadorXML2.processar_arquivo_2(tempo_selecionado)
    mensagem_final = ProcessadorXML2.processar_arquivo_2(tempo_selecionado)

    if mensagem_final:
        # Atualiza o campo de texto somente leitura com a mensagem final
        nfe_info_var.set(mensagem_final)
    else:
        messagebox.showwarning("Aviso", "Nenhuma mensagem gerada ou ocorreu um erro.")
        nfe_info_var.set("")  # Limpa o campo caso necessário

def Manifestar_by_xml_parte_3():
    placa = placa_cte_text.get()
    dt = dt_text.get()
    tempo_selecionado = tempo.get()
    # ProcessadorXML3.processar_arquivo_3(placa, dt,tempo_selecionado)
    mensagem_final = ProcessadorXML3.processar_arquivo_3(placa, dt, tempo_selecionado)

    if mensagem_final:
        # Atualiza o campo de texto somente leitura com a mensagem final
        nfe_info_var.set(mensagem_final)
    else:
        messagebox.showwarning("Aviso", "Nenhuma mensagem gerada ou ocorreu um erro.")
        nfe_info_var.set("")  # Limpa o campo caso necessário


#OST
def validar_ticket(ticket, origem="BEMISA"):
    if origem == "BEMISA":
        # Regras para BEMISA
        if not (len(ticket) == 6 and ticket.isdigit()):
            messagebox.showerror("Erro de Validação", "O ticket deve conter exatamente 6 números.")
            return False

        if ticket.startswith("0"):
            messagebox.showerror("Erro de Validação", "O ticket não pode começar com 0.")
            return False

        valor_maximo = 180000
        if int(ticket) > valor_maximo:
            messagebox.showerror("Erro de Validação", f"O ticket não pode ser maior que {valor_maximo}.")
            return False
    elif origem == "VAMTEC":
        # Regras para VAMTEC (sem restrições de tamanho ou valor)
        if not ticket.isdigit():
            messagebox.showerror("Erro de Validação", "O ticket deve conter apenas números.")
            return False
    else:
        messagebox.showerror("Erro de Validação", "Origem do ticket inválida.")
        return False

    return True  # Ticket válido

def validar_peso(peso):
    if not (len(peso) == 5 and peso.isdigit()):
        messagebox.showerror("Erro de Validação", "O peso deve conter exatamente 5 números.")
        return False
    
    if int(peso) > 39000:
        messagebox.showerror("Erro de Validação", "O peso não pode ser maior que 39000.")
        return False

    return True  # Peso válido

#OST BEMISA E VALIDAÇÕES
def executar_ost_bemisa():
    # Obtendo os valores dos campos
    placa = placa_bemisa_text.get().strip()
    ticket = ticket_bemisa_text.get().strip()
    peso = peso_bemisa_text.get().strip()
    emissao = data_bemisa_text.get().strip()
    data_limpa = emissao.replace("/", "").replace(" ", "").replace(":", "")
    
    # Validações
    if not validar_ticket(ticket, origem="BEMISA"):
        return

    if not validar_peso(peso):
        return 

    try:
        data_formatada = emissao.split("/")[0] + "/" + emissao.split("/")[1]
    except IndexError:
        data_formatada = "Data inválida"

    # Chamada da função ost_bemisa com os dados validados
    escolha = ost_bemisa(placa, ticket, peso, data_limpa)

    if escolha:
        # Atualiza o campo de informação com a escolha, data e ticket
        mensagemostbemisa.set(f"{escolha} - Data: {data_formatada} - TICKET: {ticket}")

def ost_bemisa_parte_1():
    placa = placa_bemisa_text.get().strip()
    ost_bemisa_geral(placa)

def ost_bemisa_parte_2():
    # Obtendo os valores dos campos
    ticket = ticket_bemisa_text.get().strip()
    peso = peso_bemisa_text.get().strip()
    emissao = data_bemisa_text.get().strip()
    data_limpa = emissao.replace("/", "").replace(" ", "").replace(":", "")
    
    # Validações
    if not validar_ticket(ticket, origem="BEMISA"):
        return

    if not validar_peso(peso):
        return 

    try:
        data_formatada = emissao.split("/")[0] + "/" + emissao.split("/")[1]
    except IndexError:
        data_formatada = "Data inválida"

    # Chamada da função ost_bemisa_carga com os dados validados
    escolha = ost_bemisa_carga(ticket, peso, data_limpa)

    if escolha:
        # Atualiza o campo de informação com a escolha, data e ticket
        mensagemostbemisa.set(f"{escolha} - Data: {data_formatada} - TICKET: {ticket}")

def executar_ost_vamtec():
    # Obtendo os valores dos campos
    placa = placa_vamtec_text.get().strip()
    ticket = ticket_vamtec_text.get().strip()
    peso = peso_vamtec_text.get().strip()
    emissao = data_vamtec_text.get().strip()
    data_limpa = emissao.replace("/", "").replace(" ", "").replace(":", "")
    
    # Validações
    if not validar_ticket(ticket, origem="VAMTEC"):
        return

    if not validar_peso(peso):
        return 

    try:
        data_formatada = emissao.split("/")[0] + "/" + emissao.split("/")[1]
    except IndexError:
        data_formatada = "Data inválida"

    # Chamada da função ost_bemisa com os dados validados
    escolha = ost_vamtec(placa, ticket, peso, data_limpa)

    if escolha:
        # Atualiza o campo de informação com a escolha, data e ticket
        mensagemostvamtec.set(f"{escolha} - Data: {data_formatada} - TICKET: {ticket}")

def ost_vamtec_parte_1():
    placa = placa_vamtec_text.get().strip()
    ost_vamtec_geral(placa)

def ost_vamtec_parte_2():
    # Obtendo os valores dos campos
    ticket = ticket_vamtec_text.get().strip()
    peso = peso_vamtec_text.get().strip()
    emissao = data_vamtec_text.get().strip()
    data_limpa = emissao.replace("/", "").replace(" ", "").replace(":", "")
    
    # Validações
    if not validar_ticket(ticket, origem="VAMTEC"):
        return

    if not validar_peso(peso):
        return 

    try:
        data_formatada = emissao.split("/")[0] + "/" + emissao.split("/")[1]
    except IndexError:
        data_formatada = "Data inválida"

    # Chamada da função ost_bemisa_carga com os dados validados
    escolha = ost_vamtec_carga(ticket, peso, data_limpa)

    if escolha:
        # Atualiza o campo de informação com a escolha, data e ticket
        mensagemostvamtec.set(f"{escolha} - Data: {data_formatada} - TICKET: {ticket}")

#INICIALIZAÇÃO E CONFIGURAÇÕES DO CUSTOMTK
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Auto preenchimento")

stop_event = threading.Event()
app.protocol("WM_DELETE_WINDOW", on_close)

app.wm_attributes("-topmost", 1)
screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()

x_percent = 0.75  # 85% da largura da tela
y_percent = 0.55  # 65% da altura da tela

x = int(screen_width * x_percent)
y = int(screen_height * y_percent)
app.geometry(f"300x340+{x}+{y}")  # Tamanho ajustado

# Impedindo redimensionamento da janela
#app.resizable(False, False)

# Função para abrir uma nova janela de configurações
def abrir_janela_configuracoes():
    nova_janela = ctk.CTkToplevel(app)
    nova_janela.title("Configurações")
    nova_janela.geometry("250x250")  # Tamanho compacto para a nova janela
    
    # Configuração para a posição da nova janela
    screen_width_nova = nova_janela.winfo_screenwidth()
    screen_height_nova = nova_janela.winfo_screenheight()

    x_nova = int(screen_width_nova *  x_percent)  # Centralizando horizontalmente
    y_nova = int(screen_height_nova * y_percent) - 400  # Posicionando um pouco acima do centro vertical
    nova_janela.geometry(f"400x250+{x_nova}+{y_nova}")
    
    # Adicionando widgets na janela de configurações
    label_config = ctk.CTkLabel(nova_janela, text="Configurações", font=("Helvetica", 16))
    label_config.pack(pady=20)

    # Menu para mudar o modo de aparência
    label_modo = ctk.CTkLabel(nova_janela, text="Selecionar Modo:")
    label_modo.pack(pady=5)

    modo_menu = ctk.CTkOptionMenu(nova_janela, values=["light", "dark", "system"],
                                  command=lambda escolha: ctk.set_appearance_mode(escolha))
    modo_menu.set("dark")  # Modo padrão inicial
    modo_menu.pack(pady=10)

# Criando a barra de menus
menu_bar = tk.Menu(app)

# Criando o menu "Arquivo"
menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_arquivo.add_command(label="Configurações", command=abrir_janela_configuracoes)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=app.quit)

# Adicionando o menu "Arquivo" à barra de menus
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)

# Configurando a barra de menus na aplicação
app.config(menu=menu_bar)

# Criando o sistema de abas
tabview = ctk.CTkTabview(app)
tabview.pack(expand=True, fill="both", padx=10, pady=10)

tempo = ctk.DoubleVar(value=0.3)  # Valor inicial do slider (meio segundo)

# Adicionando abas
tab1 = tabview.add("Nota Fiscal")
tab2 = tabview.add("OST Bemisa")
tab3 = tabview.add("OST Vamtec")

#FORMATAR PLACAS DIGITADAS
def verificar_entrada(event):
    def processar_placa(entrada, entry_widget):
        entrada = entrada.upper()


        if entrada.startswith("OQE1I85") and (entrada == "OQE1I85" or entrada.endswith("MG") or entrada.endswith("SP")):
            formatada = "OQE 1I85"
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, formatada)
            return

        if entrada.endswith("MG") or entrada.endswith("SP"):
            entrada_sem_uf = entrada[:-2] 
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, entrada_sem_uf)
        else:
            entry_widget.delete(0, ctk.END)
            entry_widget.insert(0, entrada)

    processar_placa(placa_cte_text.get(), placa_cte_text)
    processar_placa(placa_bemisa_text.get(), placa_bemisa_text)
    processar_placa(placa_vamtec_text.get(), placa_vamtec_text)
    
#FORMATAÇÃO VISUAL DA DATA DE EMISSÃO DO TICKET
data_bemisa_bruto = ""  

def formatar_data(event):
    global data_bemisa_bruto

    # Obtém o valor do campo de entrada e remove qualquer caractere não numérico
    entrada = data_bemisa_text.get()
    entrada_limpa = "".join(filter(str.isdigit, entrada))

    # Atualiza a variável global para armazenar a versão sem formatação
    data_bemisa_bruto = entrada_limpa

    # Formata visualmente a entrada se tiver ao menos 12 caracteres (DDMMYYYYHHmm)
    if len(entrada_limpa) >= 12:
        data_formatada = f"{entrada_limpa[:2]}/{entrada_limpa[2:4]}/{entrada_limpa[4:8]} {entrada_limpa[8:10]}:{entrada_limpa[10:12]}"
    else:
        # Mostra parcialmente enquanto o usuário digita
        data_formatada = entrada_limpa

    # Atualiza o campo de entrada com o valor formatado
    data_bemisa_text.delete(0, ctk.END)
    data_bemisa_text.insert(0, data_formatada)

# Função para obter o valor bruto
def obter_data_bemisa_bruto():
    return data_bemisa_bruto

# Variável global para controle de confirmação do ano
ano_confirmado = False

# Função para formatar a data
def formatar_data(event, text_field):
    current_text = text_field.get().replace("/", "").replace(":", "").replace(" ", "")  # Remove formatação existente
    if len(current_text) >= 2 and len(current_text) <= 12:
        formatted_text = (
            f"{current_text[:2]}/{current_text[2:4]}/{current_text[4:8]} "
            f"{current_text[8:10]}:{current_text[10:]}"
        )
        text_field.delete(0, tk.END)
        text_field.insert(0, formatted_text)

# Função para verificar o ano
def verificar_ano(event, text_field):
    global ano_confirmado  # Acessa a variável global

    entrada = text_field.get()
    entrada_limpa = "".join(filter(str.isdigit, entrada))  # Remove caracteres não numéricos

    # Verifica se o ano foi digitado completamente
    if len(entrada_limpa) >= 8:
        ano = entrada_limpa[4:8]  # Extrai o ano (4ª a 8ª posições)

        if ano != "2025" and not ano_confirmado:
            # Reproduz o som de alerta
            falar(f"O ano informado é {ano}, o ano atual é 2025. Deseja continuar assim mesmo?")

            # Solicita confirmação ao usuário
            resposta = messagebox.askyesno(
                "Confirmação",
                f"O ano informado é {ano}, o ano atual é 2025. Deseja continuar assim mesmo?"
            )

            if resposta:
                ano_confirmado = True
                app.after(30000, limpar_ano_confirmado)  # Reseta a confirmação após 30 segundos
            else:
                text_field.delete(0, tk.END)  # Limpa o campo se o usuário cancelar
                messagebox.showinfo("Operação cancelada", "Por favor, insira um ano válido.")

# Função para resetar a confirmação do ano
def limpar_ano_confirmado():
    global ano_confirmado
    ano_confirmado = False

# Função para limpar um campo específico
def limpar_campo_especifico(*campos):
    for campo in campos:
        campo.delete(0, tk.END)
        nfe_info_var.set("")
        mensagemostbemisa.set("")
        mensagemostvamtec.set("")
        deletar_xml_na_pasta()

#WIDGETS DA TAB1
placa_cte_text = ctk.CTkEntry(tab1, placeholder_text="Placa do cavalo", font=('Arial', 14))
placa_cte_text.grid(column=0, row=0, sticky="NWES", pady=7, padx=5)
placa_cte_text.bind("<KeyRelease>", verificar_entrada)

dt_text = ctk.CTkEntry(tab1, placeholder_text="Dt usiminas", font=('Arial', 14))
dt_text.grid(column=0, row=1, sticky="NWES", pady=7, padx=5)

button_tab1 = ctk.CTkButton(tab1, text="CT-E Completo",font=('Arial', 14), command=Manifestar_by_xml)
button_tab1.grid(column=0, row=2, columnspan=2, sticky="NWES", pady=0, padx=5)

button_tab1_2 = ctk.CTkButton(tab1, text="Geral",font=('Arial', 14), command=Manifestar_by_xml_parte_3)
button_tab1_2.grid(column=0, row=3, sticky="NWES", pady=10, padx=5)

button_tab1_3 = ctk.CTkButton(tab1, text="Comp. Carga",font=('Arial', 14), command=Manifestar_by_xml_parte_2)
button_tab1_3.grid(column=1, row=3, sticky="NWES", pady=10, padx=5)

nfe_info_var = tk.StringVar(value="")
nfe_info = ctk.CTkEntry(tab1, textvariable=nfe_info_var, state="readonly", font=('Arial', 11))
nfe_info.grid(column=0, row=4, columnspan=2, sticky="NWES", pady=0, padx=5)

# Controle de Velocidade (tab1)
label_tempo = ctk.CTkLabel(tab1, text="Controle de Velocidade (segundos):")
label_tempo.grid(column=0, row=5, columnspan=2, sticky="NWES", pady=0, padx=5)

# Função para atualizar o campo de valor
def atualizar_valor_slider(valor):
    campo_valor.configure(state="normal")
    campo_valor.delete(0, "end")
    campo_valor.insert(0, f"{float(valor):.1f}")
    campo_valor.configure(state="readonly")

# Slider
slider_tempo = ctk.CTkSlider(
    tab1, 
    from_=0.3, 
    to=7, 
    variable=tempo,
    command=atualizar_valor_slider
)
slider_tempo.grid(column=0, row=6, columnspan=2, sticky="NWES", pady=10, padx=5)

# Campo de valor
campo_valor = ctk.CTkEntry(tab1, width=35, state="readonly")
campo_valor.grid(column=1, row=1, sticky="NE", pady=5, padx=0)
campo_valor.insert(0, f"{tempo.get():.1f}")  # Valor inicial

image = ctk.CTkImage(Image.open("media/image/clean_icon.png"), size=(20, 20))
clean_button = ctk.CTkButton(tab1,text="",width=0,image=image, command=lambda: limpar_campo_especifico(placa_cte_text,dt_text))
clean_button.grid(column=1, row=0,sticky="NE", pady=5, padx=0)

tab1.columnconfigure(0, weight=1)
tab1.columnconfigure(1, weight=1)


#WIDGET DA TAB2
placa_bemisa_text = ctk.CTkEntry(tab2, placeholder_text="Placa do cavalo", font=('Arial', 14))
placa_bemisa_text.grid(column=0, row=0, sticky="NW", pady=7, padx=5)
placa_bemisa_text.bind("<KeyRelease>", verificar_entrada)

ticket_bemisa_text = ctk.CTkEntry(tab2, placeholder_text="Nº do Ticket", font=('Arial', 14))
ticket_bemisa_text.grid(column=0, row=1, sticky="NW", pady=7, padx=5)

peso_bemisa_text = ctk.CTkEntry(tab2, placeholder_text="Peso da nota", font=('Arial', 14))
peso_bemisa_text.grid(column=1, row=1, sticky="NW", pady=7, padx=5)

data_bemisa_text = ctk.CTkEntry(tab2, placeholder_text="Data emissão ", font=('Arial', 13))
data_bemisa_text.grid(column=0, row=3, sticky="NW", pady=7, padx=5)
data_bemisa_text.bind("<KeyRelease>", lambda event: formatar_data(event, data_bemisa_text))
data_bemisa_text.bind("<FocusOut>", lambda event: verificar_ano(event, data_bemisa_text))

button_tab2 = ctk.CTkButton(tab2, text="OST Completo",font=('Arial', 14), command=executar_ost_bemisa)
button_tab2.grid(column=1, row=3, sticky="NW", pady=7, padx=5)

button_tab2_2 = ctk.CTkButton(tab2, text="Geral",font=('Arial', 14), command=ost_bemisa_parte_1)
button_tab2_2.grid(column=0, row=4, sticky="NWES", pady=10, padx=5)

button_tab2_3 = ctk.CTkButton(tab2, text="Comp. Carga",font=('Arial', 14), command=ost_bemisa_parte_2)
button_tab2_3.grid(column=1, row=4, sticky="NWES", pady=10, padx=5)

mensagemostbemisa = tk.StringVar(value="")
mensagemostbemisa_info = ctk.CTkEntry(tab2, textvariable=mensagemostbemisa, state="readonly", font=('Arial', 14))
mensagemostbemisa_info.grid(column=0, row=5,columnspan=2, sticky="NWES", pady=0, padx=5)

image = ctk.CTkImage(Image.open("media/image/clean_icon.png"), size=(20, 20))
clean_button = ctk.CTkButton(tab2,text="",width=0,image=image, command=lambda: limpar_campo_especifico(placa_bemisa_text,ticket_bemisa_text,peso_bemisa_text,data_bemisa_text))
clean_button.grid(column=1, row=0,sticky="NE", pady=5, padx=0)

tab2.columnconfigure(0, weight=1)
tab2.columnconfigure(1, weight=1)


placa_vamtec_text = ctk.CTkEntry(tab3, placeholder_text="Placa do cavalo", font=('Arial', 14))
placa_vamtec_text.grid(column=0, row=0, sticky="NW", pady=7, padx=5)
placa_vamtec_text.bind("<KeyRelease>", verificar_entrada)

ticket_vamtec_text = ctk.CTkEntry(tab3, placeholder_text="Nº do Ticket", font=('Arial', 14))
ticket_vamtec_text.grid(column=0, row=1, sticky="NW", pady=7, padx=5)

peso_vamtec_text = ctk.CTkEntry(tab3, placeholder_text="Peso da nota", font=('Arial', 14))
peso_vamtec_text.grid(column=1, row=1, sticky="NW", pady=7, padx=5)

data_vamtec_text = ctk.CTkEntry(tab3, placeholder_text="Data emissão ", font=('Arial', 13))
data_vamtec_text.grid(column=0, row=3, sticky="NW", pady=7, padx=5)
data_vamtec_text.bind("<KeyRelease>", lambda event: formatar_data(event, data_vamtec_text))
data_vamtec_text.bind("<FocusOut>", lambda event: verificar_ano(event, data_vamtec_text))

button_tab3 = ctk.CTkButton(tab3, text="OST Completo",font=('Arial', 14), command=executar_ost_vamtec)
button_tab3.grid(column=1, row=3, sticky="NW", pady=7, padx=5)

button_tab3_2 = ctk.CTkButton(tab3, text="Geral",font=('Arial', 14), command=ost_vamtec_parte_1)
button_tab3_2.grid(column=0, row=4, sticky="NWES", pady=10, padx=5)

button_tab3_3 = ctk.CTkButton(tab3, text="Comp. Carga",font=('Arial', 14), command=ost_vamtec_parte_2)
button_tab3_3.grid(column=1, row=4, sticky="NWES", pady=10, padx=5)

mensagemostvamtec = tk.StringVar(value="")
mensagemostvamtec_info = ctk.CTkEntry(tab3, textvariable=mensagemostvamtec, state="readonly", font=('Arial', 14))
mensagemostvamtec_info.grid(column=0, row=5,columnspan=2, sticky="NWES", pady=0, padx=5)

image = ctk.CTkImage(Image.open("media/image/clean_icon.png"), size=(20, 20))
clean_button = ctk.CTkButton(tab3,text="",width=0,image=image, command=lambda: limpar_campo_especifico(placa_vamtec_text,ticket_vamtec_text,peso_vamtec_text,data_vamtec_text))
clean_button.grid(column=1, row=0,sticky="NE", pady=5, padx=0)

tab3.columnconfigure(0, weight=1)
tab3.columnconfigure(1, weight=1)
# Iniciando o loop da aplicação
app.mainloop()

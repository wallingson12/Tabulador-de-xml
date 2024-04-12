import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import threading
import os
from PIL import Image, ImageTk
from main import process_xml_files

def selecionar_pasta():
    diretorio = filedialog.askdirectory(title="Selecione o diretório com os arquivos XML")
    if diretorio:
        messagebox.showinfo("Pasta Selecionada", f"A pasta selecionada é: {diretorio}")

def processar_arquivos():
    try:
        t = threading.Thread(target=process_xml_files, args=(diretorio,))
        t.start()
        messagebox.showinfo("Processamento Iniciado", "O processamento dos arquivos XML foi iniciado.")
    except Exception as e:
        messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

# Criar janela principal
janela = tk.Tk()
janela.title("Processamento de Arquivos XML")

# Definir tamanho e cor da janela
largura_display = 300
altura_display = 100

largura_tela = janela.winfo_screenwidth()
altura_tela = janela.winfo_screenheight()

posicao_x = (largura_tela - largura_display) // 2
posicao_y = (altura_tela - altura_display) // 2

janela.geometry(f"{largura_display}x{altura_display}+{posicao_x}+{posicao_y}")
janela.configure(bg="blue")

# Centralizar o botão
frame_central = tk.Frame(janela, bg="blue")
frame_central.pack(expand=True)

# Botão para selecionar a pasta
botao_selecionar = tk.Button(frame_central, text="Selecionar Pasta", command=selecionar_pasta, padx=10, pady=10)
botao_selecionar.pack(side=tk.LEFT, padx=10, pady=(altura_display//2 - 20))

# Botão para processar os arquivos
botao_processar = tk.Button(frame_central, text="Processar Arquivos XML", command=processar_arquivos, padx=10, pady=10)
botao_processar.pack(side=tk.LEFT, pady=(altura_display//2 - 20))

# Rodar a aplicação
janela.mainloop()

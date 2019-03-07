# import tkinter as tk
from tkinter import IntVar, Frame, Label, Button, TOP, BOTTOM, LEFT, RIGHT, Radiobutton, Toplevel, Text, END, Entry
# from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
#======================================
from functools import partial
from reader import ler_csv, ler_excel, validar_pontos
#======================================
from j_grafico import TelaGrafico

#==================================================================
#=Tela utilizada para a inserção de pontos.
#=Nela existem 3 alternativas:
#==Inserção manual, onde o usuário digita todos os pontos e erros
#==Inserção através de um arquivo .csv
#==Inserção através de um copy-paste a partir de um arquivo excel.
#==================================================================
class TelaPontos():

    #==================================================================
    #= Métodos que envolvem a criação e posicionamento de widgets
    #= na janela
    #==================================================================
    def __init__(self, janela, jAnterior):
        self.janela = janela
        self.jAnterior = jAnterior

        # Essas são as listas onde ficarão todos os pontos que serão
        # passados para a classe de ajuste de curvas.
        self.px = []
        self.py = []
        self.sx = []
        self.sy = []

        self.opt = IntVar()

        # Criação de widgets
        self.texto = Label(self.janela, text = "Selecione o modo de entrada dos pontos.", bg = "azure2")

        self.btn_fit = Button(self.janela, text="Ok", command= self.radio_choice, bg = "LightSkyBlue4", width = 5)
        self.btn_cancel = Button(self.janela, text="Voltar", command = self.voltar, bg = "LightSkyBlue4")

        self.radio_escolha_arquivo = Radiobutton(self.janela, variable=self.opt, value=1, text="Arquivo",  bg = "azure2", width = 20, anchor="w")
        self.radio_escolha_texto = Radiobutton(self.janela, variable=self.opt, value=2, text="Texto copiado do excel",  bg = "azure2", width = 20, anchor="w")
        self.radio_inserir_pontos = Radiobutton(self.janela, variable=self.opt, value=3, text="Inserir pontos um a um",  bg = "azure2", width = 20, anchor="w")
        self.radio_inserir_pontos.select()

        #== Posicionamento de widgets
        self.redesenhar()
        
        '''
        self.frm_upper.pack()
        self.frm_down.pack(side=BOTTOM)
        self.frm_radio.pack(side=RIGHT)
        self.radio_inserir_pontos.grid(row=0, column=3)
        self.radio_escolha_arquivo.grid(row=1, column=3)
        self.radio_escolha_texto.grid(row=2, column=3)
        self.btn_fit.grid(row=4, column=4)
        self.btn_cancel.grid(row=4, column=0)
        '''
    #==================================================================
    #=Função para limpar a janela atual e chamar a janela dos gráficos.
    #=Os pontos lidos são passados para o construtor
    def proxJanelaGrafico(self):
        self.limparJanela()
        TelaGrafico(self.janela, self, self.px, self.sx, self.py, self.sy)
    
    #==================================================================
    def voltar(self):
        self.limparJanela()
        self.jAnterior.redesenhar()

    #==================================================================
    def redesenhar(self):
        # Posicionamento de widgets
        self.janela.geometry("300x300+400+200")
        self.texto.place(x=13, y=4)

        self.radio_inserir_pontos.place(x=53, y=30)
        self.radio_escolha_arquivo.place(x=53, y=52)
        self.radio_escolha_texto.place(x=53, y=74)

        self.btn_fit.place(x=150, y=260)
        self.btn_cancel.place(x=80, y=260)

    #==================================================================
    def limparJanela(self):
        # Limpando os widgets
        self.texto.place_forget()
        self.btn_fit.place_forget()
        self.btn_cancel.place_forget()
        self.texto.place_forget()
        self.radio_escolha_arquivo.place_forget()
        self.radio_escolha_texto.place_forget()
        self.radio_inserir_pontos.place_forget()

    #==================================================================
    #==================================================================
    #==================================================================
    #=Janela da caixa de texto. Nela, existe uma caixa de texto para onde
    #=os pontos devem ser copiados no formato x - erro x - y - erro y
    def get_by_text(self):
        top_txt = Toplevel()
        top_txt.resizable(False, False)
        top_txt.title("Pontos")
        top_txt.configure(background="azure2")

        #= Criação de widgets
        txt_entry = Text(top_txt)
        frm_btn = Frame(top_txt)
        btn_cancel = Button(frm_btn, text="Cancelar", command=top_txt.destroy, bg = "LightSkyBlue4")
        
        #= Posicionamento de widgets
        txt_entry.pack()
        frm_btn.pack(side=BOTTOM)
        btn_cancel.pack(side=LEFT)

    
        #================================================================
        #= Função que valida o conteúdo da Text Entry e recebe os pontos
        #= (chamada ao clicar no botão)
        def get_pontos():
            self.txt_pontos = txt_entry.get("1.0", END)
            top_txt.destroy()
            try:
                self.px, self.py, self.sx, self.sy = ler_excel(self.txt_pontos) #método ler_excel do módulo reader
                self.proxJanelaGrafico()
            except ValueError:
                messagebox.showwarning("Erro!", "Valores inseridos incorretamente")
        #==============================

        #= Criação & posicionamento
        Button(frm_btn, text="OK", command=get_pontos, bg = "LightSkyBlue4").pack(side=RIGHT)

    #==================================================================
    # Função para criar um novo conjunto de entradas para os pontos e erros
    def append_labels(self, janela):

        self.labels.append(Label(janela, text="X", background="azure2"))
        self.labels[-1].grid(row=self.tam, column =0) 
        self.labels.append(Label(janela, text="Y", background="azure2"))
        self.labels[-1].grid(row=self.tam, column =2)
        self.labels.append(Label(janela, text="Erro X", background="azure2"))
        self.labels[-1].grid(row=self.tam, column =4) 
        self.labels.append(Label(janela, text="Erro Y", background="azure2"))
        self.labels[-1].grid(row=self.tam, column =6)
        #==================================================
        self.inserts.append(Entry(janela, width=10))
        self.inserts[-1].grid(row=self.tam, column =1)
        self.inserts.append(Entry(janela, width=10))
        self.inserts[-1].grid(row=self.tam, column =3)
        self.inserts.append(Entry(janela, width=10))
        self.inserts[-1].grid(row=self.tam, column =5)
        self.inserts.append(Entry(janela, width=10))
        self.inserts[-1].grid(row=self.tam, column =7)

        self.tam += 1

    #======================================================
    #= Função que itera pelas caixas de texto recebidas
    #= e passa todos os pontos e erros para as listas
    #= de pontos e erros
    def salvar_pontos(self):

        try:
            self.px, self.py, self.sx, self.sy = validar_pontos(self.inserts)
            self.proxJanelaGrafico()
        except ValueError:
            messagebox.showwarning("Erro!", "Valores inseridos incorretamente")
            
        self.top_pontos.destroy()

    #======================================================
    #= Janela onde os pontos serão inseridos manualmente
    def janela_Inserir_Pontos(self):
        self.top_pontos = Toplevel()
        self.top_pontos.resizable(False, False)
        self.top_pontos.title("Pontos")
        self.top_pontos.configure(background="azure2")
        
        self.tam=0
        self.labels = []
        self.inserts = []

        #= Criação de widgets
        frame_pontos = Frame(self.top_pontos, height=300, width=500, bd=10, background="azure2")

        btn_add = Button(self.top_pontos, text="Adicionar ponto", bg = "LightSkyBlue4")
        btn_cancel = Button(self.top_pontos, text="Cancelar", command=self.top_pontos.destroy, bg = "LightSkyBlue4", width=5)
        btn_add["command"] = partial(self.append_labels, frame_pontos)        
        btn_ok = Button(self.top_pontos, text="Ok", command=self.salvar_pontos, bg = "LightSkyBlue4", width=5)

        #= Posicionamento de widgets
        frame_pontos.pack(side=TOP)

        btn_add.pack(side = RIGHT)
        btn_ok.pack(side=LEFT)
        btn_cancel.pack(side=LEFT)

        #= Cria o primeiro conjunto de entradas
        self.append_labels(frame_pontos)

    #==================================================================
    #= Função que define qual método de inserção será chamado, depenendo
    #= do radio button selecionado
    def radio_choice(self):
        if(self.opt.get()==1):
            self.get_File()
        elif(self.opt.get()==2):
            self.get_by_text()
        elif(self.opt.get()==3):
            self.janela_Inserir_Pontos()

    #==================================================================
    #= Função para o método através do arquivo csv. Abre uma caixa que 
    #= solicita um arquivo e passa seu caminho para a função ler_csv
    #= do módulo reader.
    def get_File(self):
        filename = filedialog.askopenfilename(filetypes = [("arquivo csv","*.csv")])
        if filename:
            self.px, self.py, self.sx, self.sy = ler_csv(filename)
            self.proxJanelaGrafico() 
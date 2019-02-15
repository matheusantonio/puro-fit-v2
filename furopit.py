import tkinter as tk 
from tkinter import ttk
from tkinter import filedialog
#======================================
from functools import partial
from reader import ler_csv, ler_excel
from fit import *
#======================================
import matplotlib
matplotlib.use('TkAgg')
import numpy as np
from matplotlib.pyplot import savefig, gcf
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
#======================================


#==================================================================
#=Tela inicial do programa, onde é selecionada a opção de
#=criar um novo ajuste ou de verificar os ajustes salvos.
#==================================================================
class TelaInicial():

    #==================================================================
    def __init__(self, janela):
        janela.title("Furo Pit")
        self.janela = janela

        #=Criação e posicionamento de elementos da tela
        self.frm_upper = tk.Frame(janela)
        self.frm_down = tk.Frame(janela)

        self.lb_title = tk.Label(self.frm_upper, text="Furo Pit")
        self.btn_anteriores = tk.Button(self.frm_down, text="Últimos ajustes")
        self.btn_plotar = tk.Button(self.frm_down, text="Novo ajuste", command=self.proxJanelaNovo)
        self.btn_sair = tk.Button(self.frm_down, text="Sair", command=self.janela.destroy)

        self.frm_upper.grid()
        self.frm_down.grid()

        self.lb_title.grid()
        self.btn_anteriores.pack(side=tk.TOP)
        self.btn_plotar.pack(side=tk.TOP)
        self.btn_sair.pack(side=tk.BOTTOM)

    #==================================================================
    #=Passa para a próxima janela, limpando a anterior antes
    def proxJanelaNovo(self):
        self.limparJanela()
        TelaPontos(self.janela, self)

    #==================================================================
    #= Caso seja necessário retornar a essa janela, os objetos devem ser
    #= redesenhados.
    def redesenhar(self):
        self.frm_upper.grid()
        self.frm_down.grid()

        self.lb_title.grid()
        self.btn_anteriores.pack(side=tk.TOP)
        self.btn_plotar.pack(side=tk.TOP)
        self.btn_sair.pack(side=tk.BOTTOM)

    #==================================================================
    #= Caso seja necessário sair dessa janela, os objetos devem ser apagados.
    def limparJanela(self):

        self.lb_title.grid_forget()
        self.btn_anteriores.pack_forget()
        self.btn_plotar.pack_forget()
        self.btn_sair.pack_forget()

        self.frm_upper.grid_forget()
        self.frm_down.grid_forget()

#==================================================================
#=Tela utilizada para a inserção de pontos.
#=Nela existem 3 alternativas:
#==Inserção manual, onde o usuário digita todos os pontos e erros
#==Inserção através de um arquivo .csv
#==Inserção através de um copy-paste a partir de um arquivo excel.
#==================================================================
class TelaPontos():

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

        # Objetos da tela
        self.frm_upper = tk.Frame(janela)
        self.frm_down = tk.Frame(janela)

        self.frm_radio = tk.Frame(self.frm_upper)

        self.btn_fit = tk.Button(self.frm_down, text="Ok", command= self.radio_choice)
        self.btn_cancel = tk.Button(self.frm_down, text="Voltar", command = self.voltar)
        self.lb_pontos = tk.Label(self.frm_upper, text="Pontos")
        self.lb_filename = tk.Label(self.frm_upper, text="None")

        self.opt = tk.IntVar()

        self.radio_escolha_arquivo = tk.Radiobutton(self.frm_radio, variable=self.opt, value=1, text="Arquivo")
        
        self.radio_escolha_texto = tk.Radiobutton(self.frm_radio, variable=self.opt, value=2, text="Texto")
        self.radio_inserir_pontos = tk.Radiobutton(self.frm_radio, variable=self.opt, value=3, text="Inserir Pontos")
        self.radio_inserir_pontos.select()

        self.frm_upper.pack()
        self.frm_down.pack(side=tk.BOTTOM)

        self.frm_radio.pack(side=tk.RIGHT)


        self.lb_pontos.pack(side=tk.LEFT)
        self.lb_filename.pack(side=tk.RIGHT)

        self.radio_inserir_pontos.grid(row=0, column=3)
        self.radio_escolha_arquivo.grid(row=1, column=3)
        self.radio_escolha_texto.grid(row=2, column=3)

        self.btn_fit.grid(row=4, column=4)
        self.btn_cancel.grid(row=4, column=0)
    
    #==================================================================
    def voltar(self):
        self.limparJanela()
        self.jAnterior.redesenhar()

    #==================================================================
    def limparJanela(self):

        self.btn_fit.grid_forget()
        self.btn_cancel.grid_forget()

        self.radio_escolha_arquivo.grid_forget()
        self.radio_escolha_texto.grid_forget()
        self.radio_inserir_pontos.grid_forget()

        self.lb_pontos.pack_forget()
        self.lb_filename.pack_forget()

        self.frm_radio.pack_forget()

        self.frm_upper.pack_forget()
        self.frm_down.pack_forget()

    #==================================================================
    def redesenhar(self):
        self.frm_upper.pack()
        self.frm_down.pack(side=tk.BOTTOM)

        self.frm_radio.pack(side=tk.RIGHT)


        self.lb_pontos.pack(side=tk.LEFT)
        self.lb_filename.pack(side=tk.RIGHT)

        self.radio_inserir_pontos.grid(row=0, column=3)
        self.radio_escolha_arquivo.grid(row=1, column=3)
        self.radio_escolha_texto.grid(row=2, column=3)

        self.btn_fit.grid(row=4, column=4)
        self.btn_cancel.grid(row=4, column=0)

    #==================================================================
    #=Função para limpar a janela atual e chamar a janela dos gráficos.
    #=Os pontos lidos são passados para o construtor
    def proxJanelaGrafico(self):
        self.limparJanela()
        TelaGrafico(self.janela, self, self.px, self.sx, self.py, self.sy)

    #==================================================================
    #=Janela da caixa de texto. Nela, existe uma caixa de texto para onde
    #=os pontos devem ser copiados no formato x - erro x - y - erro y
    def get_by_text(self):
        top_txt = tk.Toplevel()
        top_txt.title = "Pontos"

        txt_entry = tk.Text(top_txt)
        txt_entry.pack()
            
        frm_btn = tk.Frame(top_txt)
        frm_btn.pack(side=tk.BOTTOM)
            
        btn_cancel = tk.Button(frm_btn, text="Cancelar", command=top_txt.destroy)
        btn_cancel.pack(side=tk.LEFT)

        def get_pontos():
            self.txt_pontos = txt_entry.get("1.0", tk.END)
            top_txt.destroy()
            self.px, self.py, self.sx, self.sy = ler_excel(self.txt_pontos) #método ler_excel do módulo reader
            self.proxJanelaGrafico()

        tk.Button(frm_btn, text="OK", command=get_pontos).pack(side=tk.RIGHT)
    
    #==================================================================
    # Função para criar um novo conjunto de entradas para os pontos e erros
    def append_labels(self, janela):

        self.labels.append(tk.Label(janela, text="X"))
        self.labels[-1].grid(row=self.tam, column =0) 
        self.labels.append(tk.Label(janela, text="Y"))
        self.labels[-1].grid(row=self.tam, column =2)
        self.labels.append(tk.Label(janela, text="Erro X"))
        self.labels[-1].grid(row=self.tam, column =4) 
        self.labels.append(tk.Label(janela, text="Erro Y"))
        self.labels[-1].grid(row=self.tam, column =6)


        self.inserts.append(tk.Entry(janela, width=10))
        self.inserts[-1].grid(row=self.tam, column =1)
        self.inserts.append(tk.Entry(janela, width=10))
        self.inserts[-1].grid(row=self.tam, column =3)
        self.inserts.append(tk.Entry(janela, width=10))
        self.inserts[-1].grid(row=self.tam, column =5)
        self.inserts.append(tk.Entry(janela, width=10))
        self.inserts[-1].grid(row=self.tam, column =7)

        
        self.tam += 1

    #======================================================
    #= Função que itera pelas caixas de texto recebidas
    #= e passa todos os pontos e erros para as listas
    #= de pontos e erros
    def salvar_pontos(self):

        self.px = []
        self.py = []
        self.sx = []
        self.sy = [] 

        for i in range(0, len(self.inserts), 4):
            self.px.append(float(self.inserts[i].get()))
            self.py.append(float(self.inserts[i+1].get()))
            self.sx.append(float(self.inserts[i+2].get()))
            self.sy.append(float(self.inserts[i+3].get()))

        self.top_pontos.destroy()

        self.proxJanelaGrafico()


    #======================================================
    #= Janela onde os pontos serão inseridos manualmente
    def janela_Inserir_Pontos(self):
        self.top_pontos = tk.Toplevel()
        self.top_pontos.title = "Pontos"
        self.tam=0
        self.labels = []
        self.inserts = []

        frame_pontos = tk.Frame(self.top_pontos, height=300, width=500, bd=10)

        btn_add = tk.Button(self.top_pontos, text="Adicionar ponto")
        btn_add["command"] = partial(self.append_labels, frame_pontos)        

        btn_ok = tk.Button(self.top_pontos, text="Ok", command=self.salvar_pontos)

        frame_pontos.pack(side=tk.TOP)
        btn_add.pack(side = tk.RIGHT)
        btn_ok.pack(side=tk.LEFT)

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
        filename = filedialog.askopenfilename()
        if(filename!=""):
            self.px = []
            self.py = []
            self.sx = []
            self.sy = []
            self.px, self.py, self.sx, self.sy = ler_csv(filename)

        self.proxJanelaGrafico()    


#==================================================================
#=
#==================================================================
class TelaGrafico():
    #==================================================================
    def __init__(self, janela, jAnterior, px, err_x, py, err_y):
        self.jAnterior = jAnterior
        self.janela = janela

        #=Frame feito para conter a imagem do plot========================
        self.frm_graphic = tk.Frame(janela, bd=10, height=300, width=500)
        self.frm_buttons = tk.Frame(janela, bd=10)

        self.btn_return = tk.Button(self.frm_buttons, text="Voltar", command=self.voltar)
        self.btn_plot = tk.Button(self.frm_buttons, text="Salvar", command = self.salvar_imagem)

        #=====Botoes de ajuste=====
        #=Ainda não estão funcionais
        self.btn_linear = tk.Button(self.frm_buttons, text="Linear")
        self.btn_linear["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_linear)
        self.btn_expo = tk.Button(self.frm_buttons, text="Exponencial")
        self.btn_expo["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_exponencial)
        self.btn_quadra = tk.Button(self.frm_buttons, text="Quadrática")
        self.btn_quadra["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_linear)
        self.btn_cube = tk.Button(self.frm_buttons, text="Cúbica")
        self.btn_cube["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_linear)
        self.btn_racio = tk.Button(self.frm_buttons, text="Racional")
        self.btn_racio["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_linear)
        #==========================

        #======================================================
        #=Código para desenhar o gráfico no frame da janela
        #
        #=Primeira linha cria a figura onde o plot será feito
        self.fig = Figure(figsize=(5,3))
        #=Não sei bem o que o add_subplot faz ainda, mas parece que é algum tipo
        #=de "preparação" pro plot ser feito em uma variável
        self.a = self.fig.add_subplot(111)
        #=função simples para plotar as duas variáveis. "bo" é o tipo de "linha"
        self.a.plot(px, py, "bo")

        

        #=Um "canvas" (tela de pintura) precisa ser feito no tkinter para desenhar o gráfico.
        #=aparentemente, esse método FigureCanvastkAgg cria essa "tela" e assoscia ela ao
        #=tkinter. Ela passa com parâmetro a figura que será desenhada e em qual janela,
        #=frame, etc ela será desenhada.
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frm_graphic)
        #=aparentemente é o que posiciona a imagem no frame, assim como fazemos
        #=com os widgets na janela.

        self.canvas.get_tk_widget().pack()
        #=faz o desenho do plot (seria interessante testar o código sem isso e ver se
        # simplesmente não vai aparecer o plot)
        self.canvas.draw()

        self.frm_graphic.pack(side=tk.TOP)
        self.frm_buttons.pack(side=tk.BOTTOM)

        self.btn_linear.grid(row=3,column=0)
        self.btn_expo.grid(row=3,column=1)
        self.btn_quadra.grid(row=3,column=2)
        self.btn_cube.grid(row=3,column=3)
        self.btn_racio.grid(row=3,column=4)
        self.btn_return.grid(row=4, column=0)
        self.btn_plot.grid(row=4, column=4)

    #==================================================================
    def limparJanela(self):
        self.btn_return.grid_forget()
        self.btn_plot.grid_forget()
        self.btn_linear.grid_forget()
        self.btn_expo.grid_forget()
        self.btn_quadra.grid_forget()
        self.btn_cube.grid_forget()
        self.btn_racio.grid_forget()

        self.frm_buttons.pack_forget()
        self.frm_graphic.pack_forget()

    #==================================================================
    def voltar(self):
        self.limparJanela()
        self.jAnterior.redesenhar()

    #==================================================================
    def limpar_grafico(self):
        self.canvas.get_tk_widget().pack_forget()

    #==================================================================

    def curve_plot(self, px, err_x, py, err_y, Funcao):

        funct = Funcao( np.array(px), np.array(py), np.array(err_x), np.array(err_y))
        popt, pcov = funct.gerar_qui_quadrado()

        x_teste = range(int(px[0]),int(px[len(px)-1])+1)
        self.limpar_grafico()

        self.fig = Figure(figsize=(5,3))
        self.a = self.fig.add_subplot(111)
        self.a.plot(px, py, "bo")

        def gerar_legenda():
            legenda = ""
            for coef, letra in zip(popt, ['A','B','C','D']):
                legenda += letra + f" = {coef}\n"
            #legenda += f"Q² = {pcov}"
            return legenda

        self.a.plot(x_teste, funct.funcao(popt, x_teste), "k", 
                    label = gerar_legenda())
        self.a.legend()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frm_graphic)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    def salvar_imagem(self):
        filename = filedialog.asksaveasfilename()
        self.fig.savefig(filename)


janela = tk.Tk()
TelaInicial(janela)
janela.mainloop()
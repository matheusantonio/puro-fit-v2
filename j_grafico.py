import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
#======================================
from functools import partial
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
        self.btn_linear = tk.Button(self.frm_buttons, text="Linear")
        self.btn_linear["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_linear)
        self.btn_expo = tk.Button(self.frm_buttons, text="Exponencial")
        self.btn_expo["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_exponencial)
        self.btn_quadra = tk.Button(self.frm_buttons, text="Quadrática")
        self.btn_quadra["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_quadrada)
        self.btn_cube = tk.Button(self.frm_buttons, text="Cúbica")
        self.btn_cube["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_cubica)
        self.btn_racio = tk.Button(self.frm_buttons, text="Racional")
        self.btn_racio["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_racional)
        #==========================

        self.frm_graphic.pack(side=tk.TOP)
        self.frm_buttons.pack(side=tk.BOTTOM)

        self.btn_linear.grid(row=3,column=0)
        self.btn_expo.grid(row=3,column=1)
        self.btn_quadra.grid(row=3,column=2)
        self.btn_cube.grid(row=3,column=3)
        self.btn_racio.grid(row=3,column=4)
        self.btn_return.grid(row=4, column=0)
        self.btn_plot.grid(row=4, column=4)

        #======================================================
        #=Código para desenhar o gráfico no frame da janela
        #
        #=Primeira linha cria a figura onde o plot será feito
        self.fig = Figure(figsize=(7,5))
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
        funct = Funcao( px, py, err_x, err_y)        
        popt, pcov, qui_quadrado = funct.gerar_qui_quadrado()

        x_teste = range(int(px.min()),int(px.max())+1)
        
        self.limpar_grafico()

        def gerar_legenda():
            legenda = ""
            for coef, err_coef, letra in zip(popt, pcov, ['A','B','C','D']):
                legenda += letra + f" = {coef} +/- {err_coef}\n"
            legenda += f"Q² = {qui_quadrado}"
            return legenda

        self.fig = Figure(figsize=(7,5))
        self.grafico = self.fig.add_subplot(111)
        self.grafico.plot(x_teste, funct.funcao(popt, x_teste), "k", 
                    label = gerar_legenda())
        self.grafico.errorbar(px, py, yerr=2*np.array(err_y), fmt='o' )
        self.grafico.legend(fontsize='x-small')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frm_graphic)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

    #==========================================================================
    def salvar_imagem(self):
        filename = filedialog.asksaveasfilename()
        self.fig.savefig(filename)
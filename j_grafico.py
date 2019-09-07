# import tkinter as tk
from tkinter import Frame, Button, TOP, BOTTOM, Toplevel, Entry, Label, BOTH
# from tkinter import ttk
from tkinter import filedialog
#======================================
from functools import partial
from fit import Fit_linear, Fit_exponencial, Fit_quadrada, Fit_cubica, Fit_racional
#======================================
from matplotlib import use
use('TkAgg')
from numpy import array
from matplotlib.pyplot import savefig, gcf, style, xlabel, ylabel, rc
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from math import floor, ceil
#rc('text', usetex=True)
#======================================

#==================================================================
class TelaGrafico():
    #==================================================================
    def __init__(self, janela, jAnterior, px, err_x, py, err_y):
        
        style.use("bmh")
        
        self.jAnterior = jAnterior
        self.janela = janela.geometry("500x620+200+0")

        tam=8
        #=Frame feito para conter a imagem do plot========================
        self.frm_graphic = Frame(janela, bd=10, height=300, width=500, bg = "azure2")
        self.frm_buttons = Frame(janela, bd=10, bg = "azure2")

        self.btn_return = Button(self.frm_buttons, text="Voltar", command=self.voltar, bg = "LightSkyBlue4",  width=tam)
        self.btn_plot = Button(self.frm_buttons, text="Salvar", command = self.salvar_imagem, bg = "LightSkyBlue4",  width=tam)

        #=====Botoes de ajuste=====
        self.btn_linear = Button(self.frm_buttons, text="Linear", bg = "LightSkyBlue4",  width=tam)
        self.btn_linear["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_linear, "Linear")
        self.btn_expo = Button(self.frm_buttons, text="Exponencial", bg = "LightSkyBlue4",  width=tam)
        self.btn_expo["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_exponencial, "Exponencial")
        self.btn_quadra = Button(self.frm_buttons, text="Quadrática", bg = "LightSkyBlue4",  width=tam)
        self.btn_quadra["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_quadrada, "Quadrática")
        self.btn_cube = Button(self.frm_buttons, text="Cúbica", bg = "LightSkyBlue4",  width=tam)
        self.btn_cube["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_cubica, "Cúbica")
        self.btn_racio = Button(self.frm_buttons, text="Racional", bg = "LightSkyBlue4",  width=tam)
        self.btn_racio["command"] = partial(self.curve_plot, px, err_x, py, err_y, Fit_racional, "Racional")
        #==========================

        self.frm_graphic.pack(side=TOP)
        self.frm_buttons.pack(side=BOTTOM)

        self.btn_linear.grid(row=3,column=0)
        self.btn_expo.grid(row=3,column=1)
        self.btn_quadra.grid(row=3,column=2)
        self.btn_cube.grid(row=3,column=3)
        self.btn_racio.grid(row=3,column=4)

        self.btn_return.grid(row=5, column=0)
        self.btn_plot.grid(row=5, column=1)

        #======================================================
        #=Código para desenhar o gráfico no frame da janela
        #
        #=Primeira linha cria a figura onde o plot será feito
        self.fig = Figure(figsize=(7,5))
        
        #=Não sei bem o que o add_subplot faz ainda, mas parece que é algum tipo
        #=de "preparação" pro plot ser feito em uma variável
        self.grafico = self.fig.add_subplot(111)
        #=função simples para plotar as duas variáveis. "bo" é o tipo de "linha"
        self.grafico.plot(px, py, "bo")        

        self.grafico.set_xlabel('x', labelpad=5)
        self.grafico.set_ylabel('y', labelpad=5)
        
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
    def curve_plot(self, px, err_x, py, err_y, Funcao, f_nome):
        funct = Funcao( px, py, err_x, err_y)        
        popt, pcov, qui_quadrado = funct.gerar_qui_quadrado()

        #versão original
        #x_teste = range(int(px.min()),int(px.max())+1)


        #pra trocar pra versão float, basta comentar a linha abaixo
        x_teste = range(int(floor(px.min())),int(ceil(px.max())+1))

        '''
        x_teste = []
        d0 = px.min()

        while d0 < px.max():
            x_teste.append(d0)
            d0 += 1
        x_teste.append(px.max())

        '''
        self.limpar_grafico()
        
        def gerar_legenda():
            legenda = ""
            for coef, err_coef, letra in zip(popt, pcov, ['A','B','C','D']):
                legenda += letra + f" = {coef:.2f} +/- {err_coef:.2f}\n"
            legenda += r'$\chi^2$/ndof ='
            legenda += f"{qui_quadrado:.2f}"
            return legenda
        
        self.fig = Figure(figsize=(7,5))
        self.grafico = self.fig.add_subplot(111)
        self.grafico.plot(x_teste, funct.funcao(popt, x_teste), "k", 
                    label = gerar_legenda())
        
        self.grafico.errorbar(px, py, yerr=array(err_y), fmt='o')
        self.grafico.legend(fontsize='x-small')
        
        self.grafico.set_xlabel('x', labelpad=5)
        self.grafico.set_ylabel('y', labelpad=5)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frm_graphic)
        self.canvas.get_tk_widget().pack()
        self.canvas.draw()

        self.resultados(popt, pcov, qui_quadrado, f_nome)

    #==========================================================================
    def salvar_imagem(self):
        filename = filedialog.asksaveasfilename()
        self.fig.savefig(filename)

    #==========================================================================
    def resultados(self, popt, pcov, qui_quadrado, f_nome):
        top_res = Toplevel(bd=10)
        top_res.resizable(False, False)
        top_res.title("Resultados: " + f_nome)
        top_res.configure(background="azure2")

        txt_a_value = Entry(top_res)
        txt_a_value.insert(0, popt[0])
        txt_a_value.config(state='readonly')
        Label(top_res, text="A: ", bg = "azure2").grid(row=0, column=0)
        txt_a_value.grid(row=0, column=1)

        txt_a_error = Entry(top_res)
        txt_a_error.insert(0, pcov[0])
        txt_a_error.config(state='readonly')
        Label(top_res, text="+/-", bg = "azure2").grid(row=0, column=2)
        txt_a_error.grid(row=0, column=3)

        txt_b_value = Entry(top_res)
        txt_b_value.insert(0, popt[1])
        txt_b_value.config(state='readonly')
        Label(top_res, text="B: ", bg = "azure2").grid(row=1, column=0)
        txt_b_value.grid(row=1, column=1)

        txt_b_error = Entry(top_res)
        txt_b_error.insert(0, pcov[1])
        txt_b_error.config(state='readonly')
        Label(top_res, text="+/-", bg = "azure2").grid(row=1, column=2)
        txt_b_error.grid(row=1, column=3)
        
        if(len(popt) > 2):
            txt_c_value = Entry(top_res)
            txt_c_value.insert(0, popt[2])
            txt_c_value.config(state='readonly')
            Label(top_res, text="C: ", bg = "azure2").grid(row=2, column=0)
            txt_c_value.grid(row=2, column=1)

            txt_c_error = Entry(top_res)
            txt_c_error.insert(0, pcov[2])
            txt_c_error.config(state='readonly')
            Label(top_res, text="+/-", bg = "azure2").grid(row=2, column=2)
            txt_c_error.grid(row=2, column=3)
        
            if(len(popt)>3):
                txt_d_value=Entry(top_res)
                txt_d_value.insert(0, popt[3])
                txt_d_value.config(state='readonly')
                Label(top_res, text="D: ", bg = "azure2").grid(row=3, column=0)
                txt_d_value.grid(row=3, column=1)

                txt_d_error=Entry(top_res)
                txt_d_error.insert(0, pcov[3])
                txt_d_error.config(state='readonly')
                Label(top_res, text="+/-", bg = "azure2").grid(row=3, column=2)
                txt_d_error.grid(row=3, column=3)

        txt_q_entry = Entry(top_res)
        txt_q_entry.insert(0, round(qui_quadrado, 4))
        txt_q_entry.config(state='readonly')
        Label(top_res, text="x²/ndof: ", bg = "azure2").grid(row=4, column=0)
        
        txt_q_entry.grid(row=4, column=1)


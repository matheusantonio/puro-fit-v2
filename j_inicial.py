# import tkinter as tk
from tkinter import Frame, Label, Button, TOP, BOTTOM
# from tkinter import ttk
#======================================
from j_pontos import TelaPontos

#==================================================================
#=Tela inicial do programa, onde é selecionada a opção de
#=criar um novo ajuste ou de verificar os ajustes salvos.
#==================================================================
class TelaInicial():

    #==================================================================
    def __init__(self, janela):
        janela.title("Puro Fit")
        self.janela = janela
        self.janela.configure(background="azure2")
        self.janela.geometry("300x300+400+200")

        #=Criação e posicionamento de elementos da tela
        self.frm_upper = Frame(janela, bg="azure2")
        self.frm_down = Frame(janela, bg="azure2")

        self.lb_title = Label(self.frm_upper, text="Furo Pit", font=('arial','30'), fg = "midnight blue", bg = "azure2")
        self.btn_plotar = Button(self.frm_down, text="Novo ajuste", command=self.proxJanelaNovo, bg = "LightSkyBlue4")
        self.btn_sair = Button(self.frm_down, text="Sair", command=self.janela.destroy, bg = "LightSkyBlue4")

        self.ocupar = Label(self.frm_upper, width = 37, height = 3, bg = "azure2")
        self.ocupar2 = Label(self.frm_upper, width = 37, height = 2, bg = "azure2")

        self.ocupar.grid()
        self.lb_title.grid()
        self.ocupar2.grid()

        self.frm_upper.grid()
        self.frm_down.grid()

        self.lb_title.grid()
        self.btn_plotar.pack(side=TOP)
        self.btn_sair.pack(side=BOTTOM)

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

        self.ocupar.grid()
        self.lb_title.grid()
        self.ocupar2.grid()

        self.btn_plotar.pack(side=TOP)
        self.btn_sair.pack(side=BOTTOM)

    #==================================================================
    #= Caso seja necessário sair dessa janela, os objetos devem ser apagados.
    def limparJanela(self):

        self.lb_title.grid_forget()
        self.btn_plotar.pack_forget()
        self.btn_sair.pack_forget()

        self.ocupar.grid_forget()
        self.ocupar2.grid_forget()
        
        self.frm_upper.grid_forget()
        self.frm_down.grid_forget()
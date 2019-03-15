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
        self.janela.geometry("325x300+400+200")

        #=Criação e posicionamento de elementos da tela
        self.frm_upper = Frame(janela, bg="azure2")
        self.frm_down = Frame(janela, bg="azure2")

        tam=10
        self.lb_title = Label(self.frm_upper, text="Puro Fit", font=('arial','30'), fg = "midnight blue", bg = "azure2")
        self.btn_plotar = Button(self.frm_down, text="Novo ajuste", command=self.proxJanelaNovo, bg = "LightSkyBlue4", width = tam)
        self.btn_sair = Button(self.frm_down, text="Sair", command=self.janela.destroy, bg = "LightSkyBlue4", width = tam)

        self.ocupar = Label(self.frm_upper, width = 37, height = 3, bg = "azure2")
        self.ocupar2 = Label(self.frm_upper, width = 37, height = 3, bg = "azure2")

        self.ocupar.pack(side = TOP)
        self.lb_title.pack(side = TOP)
        self.ocupar2.pack(side = TOP)

        self.frm_upper.pack(side = TOP)
        self.frm_down.pack(side = TOP)

        self.lb_title.pack(side = TOP)
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
        self.frm_upper.pack(side = TOP)
        self.frm_down.pack(side = TOP)

        self.ocupar.pack(side = TOP)
        self.lb_title.pack(side = TOP)
        self.ocupar2.pack(side = TOP)

        self.btn_plotar.pack(side=TOP)
        self.btn_sair.pack(side=BOTTOM)

    #==================================================================
    #= Caso seja necessário sair dessa janela, os objetos devem ser apagados.
    def limparJanela(self):

        self.lb_title.pack_forget()
        self.btn_plotar.pack_forget()
        self.btn_sair.pack_forget()

        self.ocupar.pack_forget()
        self.ocupar2.pack_forget()
        
        self.frm_upper.pack_forget()
        self.frm_down.pack_forget()
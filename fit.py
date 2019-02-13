import numpy as np 
from scipy.optimize import curve_fit

class Fit_curve:
    def __init__(self,horizontal, vertical, erro_h,erro_v):
        self.xdata = horizontal #atribui valores ao x
        self.ydata = vertical #atribui valores ao y
        self.erro_x = erro_h #atribui erro ao x
        self.erro_y = erro_v #atribui erro ao y
    
    def existe_erro(self):
        for i in range(self.erro_x.size):
            if self.erro_x[i] != 0:
                return True
        return False



class Fit_linear(Fit_curve):
    def __init__(self, horizontal, vertical, erro_h, erro_v):
        super().__init__(horizontal, vertical, erro_h, erro_v) #super para a classe Fit_curve
        
    def funcao(self,variavel,coef_angular,coef_linear): #função que retorna o resultaoo da função matematica linear
        return variavel*coef_angular + coef_linear #retorna f(x) onde f(x) = a*x + b

    def obter_coeficientes(self):
        if self.existe_erro():
            return curve_fit(self.funcao,self.xdata,self.ydata,[1,1],self.erro_y,True) #para o caso onde não existe erro em x
        else:
            return curve_fit(self.funcao,self.xdata,self.ydata) #para o caso onde nao existe erro em x
            



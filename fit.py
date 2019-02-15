import numpy as np 
from scipy.odr import ODR, Model, Data, RealData

#class scipy.odr.ODR(data, model, beta0=None, delta0=None, ifixb=None, ifixx=None,
#job=None, iprint=None, errfile=None, rptfile=None, ndigit=None, taufac=None, sstol=None, 
#partol=None, maxit=None, stpb=None, stpd=None, sclb=None, scld=None, work=None, iwork=None)

#data: instancia do tipo data. data recebe dois parâmetros(x,y) e retorna um objeto do tipo data
#model: instancia da classe Model. Recebe a função que será usada na aproximação de curva



class Fit_curve:
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):
        self.xdata = recebe_x
        self.ydata = recebe_y
        self.x_erro = recebe_x_erro
        self.y_erro = recebe_y_erro
        self.data=0
        self.model=0
    
    def gerar_qui_quadrado(self,vetor):
        odr = ODR(self.data,self.model,vetor)
        odr.set_job(fit_type = 2)
        resultado = odr.run()
        return resultado.beta,resultado.sd_beta

class Fit_linear(Fit_curve):
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):
        super(). __init__(recebe_x,recebe_y,recebe_x_erro,recebe_y_erro)
        if recebe_y_erro.all() != 0 and recebe_x_erro.all() != 0:
            self.data = RealData(self.xdata,self.ydata,self.x_erro,self.y_erro)
        else:
            self.data = RealData(self.xdata,self.ydata)

        self.model = Model(self.funcao)

    def funcao(self,parametros,x):
        return parametros[0]*x + parametros[1]

    def gerar_qui_quadrado(self):
        return super().gerar_qui_quadrado(np.array([1,1]))


class Fit_exponencial(Fit_curve):
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):
        super().__init__(recebe_x,recebe_y,recebe_x_erro,recebe_y_erro)
        if recebe_y_erro.all() != 0 and recebe_x_erro.all() != 0:
            self.data = RealData(self.xdata,self.ydata,self.x_erro,self.y_erro)
        else:
            self.data = RealData(self.xdata,self.ydata)

        self.model = Model(self.funcao)
    
    def funcao(self,parametros,x):
        return parametros[1]*np.exp(parametros[0]*x)
    
    def gerar_qui_quadrado(self):
        return super().gerar_qui_quadrado(np.array([1,1]))
    
    

'''
def func(parametros, x):
    return parametros[0]*x + parametros[1]

x = np.arange(1,11)
y = func([1,0],x)
#x = np.linspace(1,5,10)
#y = func([1,0],x)
#x += np.random.normal(scale=0.1, size=10)
#y += np.random.normal(scale=0.1, size=10)
erro_x = np.zeros(10)
erro_y = np.zeros(10)
#erro_x = np.random.normal(scale=0.1,size=10)
#erro_y = np.random.normal(scale=0.1,size=10)
data = RealData(x,y)#,erro_x,erro_y)
model = Model(func)
odr = ODR(data,model,[1,1])
odr.set_job(fit_type = 2)
resultado = odr.run()
print(resultado.beta)
print(resultado.sd_beta)
print("fim")
'''



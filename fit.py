import numpy as np 
from scipy.odr import ODR, Model, Data, RealData
from scipy.stats import chisquare
from scipy.optimize import curve_fit
#class scipy.odr.ODR(data, model, beta0=None, delta0=None, ifixb=None, ifixx=None,
#job=None, iprint=None, errfile=None, rptfile=None, ndigit=None, taufac=None, sstol=None, 
#partol=None, maxit=None, stpb=None, stpd=None, sclb=None, scld=None, work=None, iwork=None)

#data: instancia do tipo data. data recebe dois parâmetros(x,y) e retorna um objeto do tipo data
#model: instancia da classe Model. Recebe a função que será usada na aproximação de curva



class Fit_curve:
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):#construtor geral das classes
        for i in range(recebe_x.size):#verifica se x está em ordem crescente
            for j in range(i+1,recebe_x.size):
                if recebe_x[i]>recebe_x[j]:
                    recebe_x[i],recebe_x[j] = recebe_x[j],recebe_x[i]
                    recebe_y[i],recebe_y[j] = recebe_y[j],recebe_y[i]
                    recebe_x_erro[i],recebe_x_erro[j]=recebe_x_erro[j],recebe_x_erro[i]
                    recebe_y_erro[i],recebe_y_erro[j]=recebe_y_erro[j],recebe_y_erro[i]


        
        #coloca os valores em suas devidas variáveis locais
        self.xdata = recebe_x
        self.ydata = recebe_y
        self.x_erro = recebe_x_erro
        self.y_erro = recebe_y_erro
        self.model = 0
        self.data = RealData(self.xdata,self.ydata,self.x_erro,self.y_erro)
     
    
    def gerar_qui_quadrado(self,vetor,funcao,funcao2):#gera o qui quadrado
        if self.x_erro.all() != 0 and self.y_erro.all() != 0:
            odr = ODR(self.data,self.model,vetor)#cria classe do tipo "Ortogonal Distance Regression"
            odr.set_job(fit_type = 2)#No tipo 2 a classe odr faz qui quadrado
            resultado = odr.run() #gera o qui quadrado, retorna um tipo retorna uma classe output
            esperado = funcao(resultado.beta, self.xdata) #recebe os valores esperados pela aproximação
            qui_quadrado = chisquare(self.ydata,esperado) #gera o qui quadrado
            return resultado.beta,resultado.sd_beta,qui_quadrado[1] #retorna os valores da aproximação e seus erros

        else:
            if self.y_erro.any() != 0:
                resultado, erro = curve_fit(funcao2,self.xdata,self.ydata,vetor,self.y_erro,absolute_sigma = False)#chamada de função com erro em y
            else:
                resultado, erro = curve_fit(funcao2,self.xdata,self.ydata)#chamada de função seme erro
            erro = (np.diagonal(erro))**0.5#a raiz quadrada da diagonal principal da matriz de covariancia é o erro de cada variavel
            esperado = funcao(resultado, self.xdata) #recebe os valores esperados pela aproximação
            qui_quadrado = chisquare(self.ydata,esperado) #gera o qui quadrado, que retorna um vetor com 2 casas
            return resultado,erro,qui_quadrado[1] #retorna o resultado do qui quadrado, os erros das variáveis e a confiabilidade
        
#====================================================

class Fit_linear(Fit_curve):
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):
        super(). __init__(recebe_x,recebe_y,recebe_x_erro,recebe_y_erro)#chama o construtor da classe Fit_curve
        self.model = Model(self.funcao)#cria uma classe Model com a função linear

    def funcao(self,parametros,x):
        return parametros[0]*x + parametros[1] #retorna A*X + B

    def funcao2(self,x,a,b):
        return a*x + b #mesma função, parametros trocados. a função odr só aceita o primeiro método e a função fit_curve só aceita os segundo

    def gerar_qui_quadrado(self):
        return super().gerar_qui_quadrado(np.array([1,1]),self.funcao, self.funcao2)#retorna o qui quadrado da classe Fit_curve com o vetor ajustado para função linear

#====================================================

class Fit_exponencial(Fit_curve):
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):#construtor da classe
        super().__init__(recebe_x,recebe_y,recebe_x_erro,recebe_y_erro)#chama o construtor da classe Fit_curve
        self.model = Model(self.funcao) #cria uma classe model com a função Exponencial
    
    def funcao(self,parametros,x):
        return parametros[1]*np.exp(parametros[0]*x) # retorna B*e^(A*X)
    
    def funcao2(self,x,a,b):#mesma função, parametros trocados. a função odr só aceita o primeiro método e a função fit_curve só aceita os segundo
        return b*np.exp(a*x)
    
    def gerar_qui_quadrado(self):
        return super().gerar_qui_quadrado(np.array([1,1]),self.funcao,self.funcao2)#retorna o qui quadrado da classe Fit_curve com o vetor ajustado para função exponencial

#====================================================

class Fit_quadrada(Fit_curve):
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):#construtor da classe
        super().__init__(recebe_x,recebe_y,recebe_x_erro,recebe_y_erro)#chama o construtor da classe Fit_curve
        self.model = Model(self.funcao) #cria uma classe model com a função quadratica
    
    def funcao(self,parametros,x):
        return parametros[0]*np.power(x,2) + parametros[1]*x + parametros[2]#retorna A*X² + B*X + C

    def funcao2(self,x,a,b,c):#mesma função, parametros trocados. a função odr só aceita o primeiro método e a função fit_curve só aceita os segundo
        return a*np.power(x,2)+b*x + c

    def gerar_qui_quadrado(self):
        return super().gerar_qui_quadrado(np.array([1,1,1]),self.funcao,self.funcao2)#retorna o qui quadrado da classe Fit_curve com o vetor ajustado para função quadratica

#====================================================

class Fit_cubica(Fit_curve):
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):#construtor da classe
        super().__init__(recebe_x,recebe_y,recebe_x_erro,recebe_y_erro)#chama o construtor da classe Fit_curve
        self.model = Model(self.funcao) #cria uma classe model com a função cúbica

    def funcao(self,parametros,x):
        return parametros[0]*np.power(x,3) + parametros[1]*np.power(x,2) + parametros[2]*x + parametros[3]#retorna A*X³ + B*X² + C*X + D
    
    def funcao2(self,x,a,b,c,d):#mesma função, parametros trocados. a função odr só aceita o primeiro método e a função fit_curve só aceita os segundo
        return a*np.power(x,3) + b*np.power(x,2) + c*x + d

    def gerar_qui_quadrado(self):
        return super().gerar_qui_quadrado(np.array([1,1,1,1]),self.funcao,self.funcao2)#retorna o qui quadrado da classe Fit_curve com o vetor ajustado para função cúbica

#====================================================

class Fit_racional(Fit_curve):
    def __init__(self,recebe_x,recebe_y,recebe_x_erro,recebe_y_erro):#construtor da classe
        super().__init__(recebe_x,recebe_y,recebe_x_erro,recebe_y_erro)#chama o construtor da classe Fit_curve
        self.model = Model(self.funcao) #cria uma classe model com a função racional
    
    def funcao(self,parametros,x):#retorna A/(X+B)
        return parametros[0]/(parametros[1]+x)
    
    def funcao2(self,x,a,b):#mesma função, parametros trocados. a função odr só aceita o primeiro método e a função fit_curve só aceita os segundo
        return a/(x+b)
    
    def gerar_qui_quadrado(self):
        return super().gerar_qui_quadrado(np.array([1,1]),self.funcao,self.funcao2)#retorna o qui quadrado da classe Fit_curve com o vetor ajustado para função racional

#====================================================

#func = Fit_linear(np.array([173,168,188,158,161,193,163,178,183]),np.array([69,70,81,61,63,79,71,73,79]),np.zeros(9),np.zeros(9))
#[173,168,188,158,161,193,163,178,183]
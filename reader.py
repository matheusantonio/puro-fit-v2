from pandas import read_csv
from numpy import array, sqrt

def tratarRaizNegativa(num):
    return sqrt(abs(num))

def ler_csv(caminho):
    #= Cria um dataframe lido a partir do csv
    df = read_csv(caminho, names=['x','y', 'err_x', 'err_y'])
    df['err_x'].fillna(0, inplace=True)
    df['err_y'].fillna(df['y'].apply(tratarRaizNegativa), inplace=True)

    #= Separa as colunas do dataframe em arrays
    try:
        x = array(df['x'], dtype=float)
        y = array(df['y'], dtype=float)
        err_x = array(df['err_x'], dtype=float)
        err_y = array(df['err_y'], dtype=float)
    except ValueError:
        raise ValueError

    return x, y, err_x, err_y

def ler_excel(texto):
    x = []
    y = []
    err_x = []
    err_y = []
    #= troca as vírgulas por pontos no texto e separa em várias
    #= strings referente às linhas
    texto = texto.replace(',', '.')
    texto = texto.split('\n')
    
    #= Para cada linha no texto, separa os valores e os coloca nas
    #= listas correspondentes
    try:
        for i in texto:
            valor = i.split()
            if(len(valor) != 0):
                x.append(float(valor[0]))
                y.append(float(valor[1]))
                
                try:
                    err_x.append(float(valor[2]))
                except IndexError:
                    err_x.append(0)
                
                try:
                    err_y.append(float(valor[3]))
                except IndexError:
                    err_y.append(tratarRaizNegativa(y[-1]))

    except ValueError:
        raise ValueError

    return (array(x, dtype=float),
    array(y, dtype=float),
    array(err_x, dtype=float),
    array(err_y, dtype=float))

def validar_pontos(pontos_erros):

    x = []
    y = []
    err_x = []
    err_y = []

    #= Recebe os widgets de texto, troca as vírgulas por pontos,
    #= retira seu valor transformado em float e adicina às listas
    #= correspondentes
    try:
        for i in range(0, len(pontos_erros), 4):
            x.append(float(pontos_erros[i].get().replace(',','.')))
            y.append(float(pontos_erros[i+1].get().replace(',','.')))
            
            sx = pontos_erros[i+2].get()
            if(sx == ""):
                sx = "0"
            err_x.append(float(sx.replace(',','.')))

            sy = pontos_erros[i+3].get()
            if(sy == ""):
                sy = str(tratarRaizNegativa(y[-1]))

            err_y.append(float(sy.replace(',','.')))

    except ValueError:
        raise ValueError

    return (array(x, dtype=float),
    array(y, dtype=float),
    array(err_x, dtype=float),
    array(err_y, dtype=float))
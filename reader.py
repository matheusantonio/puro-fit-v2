from pandas import read_csv
import numpy as np

#Padrão:
#X - erro x - y - erro y
def ler_csv(caminho):
    df = read_csv(caminho, names=['x','err_x', 'y', 'err_y'])
    
    try:
        x = np.array(df['x'])
        y = np.array(df['y'])
        err_x = np.array(df['err_x'])
        err_y = np.array(df['err_y'])
    
    except ValueError:
        x=[0]
        y=[0]
        err_x=[0]
        err_y=[0]

    return x, y, err_x, err_y


def ler_excel(texto):
    x = []
    y = []
    err_x = []
    err_y = []
    texto = texto.replace(',', '.')
    l1 = texto.split('\n')
    try:
        for i in l1:
            l2 = i.split()
            if(len(l2) != 0):
                x.append(float(l2[0]))
                y.append(float(l2[2]))
                err_x.append(float(l2[1]))
                err_y.append(float(l2[3]))
    except ValueError:
        x=[0]
        y=[0]
        err_x=[0]
        err_y=[0]

    return x, y, err_x, err_y
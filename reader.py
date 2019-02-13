from pandas import read_csv

#Padrão:
#X - erro x - y - erro y
def ler_csv(caminho):
    df = read_csv(caminho, names=['x','err_x', 'y', 'err_y'])
    
    x = df['x']
    y = df['y']
    err_x = df['err_x']
    err_y = df['err_y']
    
    return x, y, err_x, err_y

def ler_excel(texto):
    x = []
    y = []
    err_x = []
    err_y = []
    l1 = texto.split('\n')
    for i in l1:
        l2 = i.split()
        if(len(l2) != 0):
            x.append(l2[0])
            y.append(l2[2])
            err_x.append(l2[1])
            err_y.append(l2[3])
    return x, y, err_x, err_y


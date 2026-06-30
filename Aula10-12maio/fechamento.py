import cv2
import numpy as np

imagem = cv2.imread("draw2.png")

def deixaCinza(imag):
    if len(imag.shape) < 3:
        return imag

    cinzas = np.zeros((imag.shape[0], imag.shape[1]), dtype = np.uint8)
    for i in range (imag.shape[0]):
        for j in range (imag.shape[1]):
            cinzas[i][j] = (imag[i][j].sum()//3)

    return cinzas

cinza = deixaCinza(imagem)

def deixaPretoBranco(cinza):
    pretoBranco = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
    for i in range (imagem.shape[0]):
        for j in range (imagem.shape[1]):
            if (cinza[i][j] /2) > 100:
                pretoBranco[i][j] = 255
            else:
                pretoBranco[i][j] = 0
    return pretoBranco

preto_branco = deixaPretoBranco(cinza)

def dilatacao3x3(preto_branco):   
    altura, largura = preto_branco.shape
    dilatada = np.zeros((altura, largura), dtype=np.uint8)   
    
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):        
            vizinhanca = preto_branco[i-5 : i+6, j-5 : j+6]
    
            if np.any(vizinhanca == 255):
                dilatada[i, j] = 255
            else:
                dilatada[i, j] = 0
                
    return dilatada

dilatada = dilatacao3x3(preto_branco)

def bordaPreta(cinza):
    borda = np.zeros(((imagem.shape[0]+2), (imagem.shape[1]+2)), dtype = np.uint8)
    for i in range (imagem.shape[0]):
        for j in range (imagem.shape[1]):
            borda[i+1][j+1] = cinza[i][j]
    cv2.imshow("Borda Preta", borda)
    return borda

def erosao(cinza):

    borda = bordaPreta(cinza)

    operador1 = [
        [1,0,1],
        [0,1,0],
        [1,0,1]
    ]

    for i in range (3):
        for j in range (3):
            operador1[i][j] = ((i+j)%2)
    print('Operador 1 =')
    print(operador1)
    print('')

    transformada1 = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
    for i in range ((imagem.shape[0])):
        for j in range ((imagem.shape[1])):
            m = n = 0
            aux1 = ((borda[i-1][j-1]) * (operador1[m][n]))
            aux2 = ((borda[i-1][j]) * (operador1[m][n+1]))
            aux3 = ((borda[i-1][j+1]) * (operador1[m][n+2]))
            aux4 = ((borda[i][j-1]) * (operador1[m+1][n]))
            aux5 = ((borda[i][j]) * (operador1[m+1][n+1]))
            aux6 = ((borda[i][j+1]) * (operador1[m+1][n+2]))
            aux7 = ((borda[i+1][j-1]) * (operador1[m+2][n]))
            aux8 = ((borda[i+1][j]) * (operador1[m+2][n+1]))
            aux9 = ((borda[i+1][j+1]) * (operador1[m+2][n+2]))
            transformada1 [i][j] = aux1 + aux2 + aux3 + aux4 + aux5 + aux6 + aux7 + aux8 + aux9
    return transformada1

fechamento =  erosao(dilatada)

cv2.imshow("dilatada", dilatada)
cv2.imshow("fechamento", fechamento)

cv2.waitKey(0)
cv2.destroyAllWindows()
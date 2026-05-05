import cv2
import numpy as np

imagem = cv2.imread("moedas.png")

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
            if ((cinza[i][j])/2) > 100:
                pretoBranco[i][j] = 255
            else:
                pretoBranco[i][j] = 0
    return pretoBranco

preto_branco = deixaPretoBranco(cinza)

def dilatacao3x3(preto_branco):
    # Obtém as dimensões da imagem
    altura, largura = preto_branco.shape
    # Cria uma imagem de saída preta (zeros)
    dilatada = np.zeros((altura, largura), dtype=np.uint8)
    
    # Percorre a imagem desconsiderando as bordas para a máscara 3x3
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # Recorta a vizinhança 3x3 em torno do pixel (i, j)
            vizinhanca = preto_branco[i-1 : i+2, j-1 : j+2]
            
            # Se houver qualquer pixel branco (255) na vizinhança, o central vira branco
            if np.any(vizinhanca == 255):
                dilatada[i, j] = 255
            else:
                dilatada[i, j] = 0
                
    return dilatada

def dilatacao5x3(preto_branco):
    altura, largura = preto_branco.shape

    dilatada = np.zeros((altura, largura), dtype=np.uint8)

    for i in range(2, altura - 2):
        for j in range(1, largura - 1):
            vizinhanca = preto_branco[i-2 : i+3, j-2 : j+2]

            if np.any(vizinhanca == 255):
                dilatada[i, j] = 255
            else:
                dilatada[i, j] = 0
    return dilatada

dilatada_1 = dilatacao3x3(preto_branco)

dilatada_2 = dilatacao5x3(preto_branco)

cv2.imshow("Imagem cinza", cinza)
cv2.imshow("Preto e Branco", preto_branco)
cv2.imshow("Dilatada mask 3x3", dilatada_1)
cv2.imshow("Dilatada mask 5x3", dilatada_2)

cv2.waitKey(0)
cv2.destroyAllWindows()
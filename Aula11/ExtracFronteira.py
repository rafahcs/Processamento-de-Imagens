#contorno_A = imag_A - ( A erosao B)
# , onde B é o elemento estruturante 3x3 (quadrado ou cruz)

import cv2
import numpy as np

imagem = cv2.imread("draw2.png")

def deixaCinza(imag):
    if len(imag.shape) < 3:
        return imag
    cinzas = np.zeros((imag.shape[0], imag.shape[1]), dtype=np.uint8)
    for i in range(imag.shape[0]):
        for j in range(imag.shape[1]):
            cinzas[i][j] = int(imag[i][j].sum() / 3)
    return cinzas

def deixaPretoBranco(cinza):
    pretoBranco = np.zeros((cinza.shape[0], cinza.shape[1]), dtype=np.uint8)
    for i in range(cinza.shape[0]):
        for j in range(cinza.shape[1]):
            # se maior que 127, branco (255), senão preto (0)
            if cinza[i][j] > 127:
                pretoBranco[i][j] = 255
            else:
                pretoBranco[i][j] = 0
    return pretoBranco

def erosao(img_binaria):
    altura, largura = img_binaria.shape
    img_erodida = np.zeros((altura, largura), dtype=np.uint8)
    
    # Elemento estruturante 3x3 
    
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            # Verifica se todos os pixels na vizinhança 3x3 são brancos
            vizinhança = img_binaria[i-1:i+2, j-1:j+2]
            if np.all(vizinhança == 255):
                img_erodida[i][j] = 255
            else:
                img_erodida[i][j] = 0
    return img_erodida

def extrai_contorno(img_original, img_erodida):
    altura, largura = img_original.shape
    img_contorno = np.zeros((altura, largura), dtype=np.uint8)
    
    # Operação: Contorno = Imagem Original - Imagem Erodida
    for i in range(altura):
        for j in range(largura):
            # Subtração manual pixel a pixel
            resultado = int(img_original[i][j]) - int(img_erodida[i][j])
            # Garante que não existam valores negativos (clip entre 0 e 255)
            if resultado < 0:
                img_contorno[i][j] = 0
            else:
                img_contorno[i][j] = np.uint8(resultado)
    return img_contorno


cinza = deixaCinza(imagem)
preto_branco = deixaPretoBranco(cinza)

# 1. Realiza a Erosão (A erosao B)
img_erodida = erosao(preto_branco)

# 2. Realiza a extração do contorno (A - (A erosao B))
contorno = extrai_contorno(preto_branco, img_erodida)

# Resultados
cv2.imshow("Original PB", preto_branco)
cv2.imshow("Erosao", img_erodida)
cv2.imshow("Contorno", contorno)

cv2.waitKey(0)
cv2.destroyAllWindows()
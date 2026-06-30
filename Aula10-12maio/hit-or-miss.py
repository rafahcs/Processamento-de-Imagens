import cv2
import numpy as np

imagem = cv2.imread("draw.png")

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

def hit_miss(img, limiar=127):

    # Cria imagem de saída vazia
    binaria = np.zeros_like(img, dtype=np.uint8)

    # Percorre pixel por pixel
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):

            # Se pixel >= limiar → branco
            if img[i, j] >= limiar:
                binaria[i, j] = 1
            else:
                binaria[i, j] = 0

    return binaria

A = hit_miss(preto_branco, 127)

# Pixels do objeto
B1 = np.array([
    [0, 0, 0],
    [0, 1, 0],
    [1, 1, 1]
], dtype=np.uint8)

# Pixels do fundo
B2 = np.array([
    [1, 1, 1],
    [0, 0, 0],
    [0, 0, 0]
], dtype=np.uint8)

A_comp = 1 - A

erode1 = cv2.erode(A, B1)
erode2 = cv2.erode(A_comp, B2)

hitmiss = cv2.bitwise_and(erode1, erode2)

cv2.imshow("Original", imagem)
cv2.imshow("Binaria Manual", A * 255)
cv2.imshow("Hit-or-Miss", hitmiss * 255)

cv2.waitKey(0)
cv2.destroyAllWindows()

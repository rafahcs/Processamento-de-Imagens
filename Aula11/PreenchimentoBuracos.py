# X_k = (X_k-1 dilatacao B) intersec A^c , k = 1,2,3,...
# X_0 é simplesmente um ponto dentro da fronteira
# B é o elemento estruturante
# A^c é o complemento de A
# Aplicar a equação até que X_k seja igual a X_k-1
# Unir resultado com a fronteira original

import cv2
import numpy as np

imagem = cv2.imread("foto.png")

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
            if cinza[i][j] < 200: 
                pretoBranco[i][j] = 255
            else:
                pretoBranco[i][j] = 0
    return pretoBranco

def dilatacao3x3(img_binaria):
    altura, largura = img_binaria.shape
    dilatada = np.zeros((altura, largura), dtype=np.uint8)
    for i in range(1, altura - 1):
        for j in range(1, largura - 1):
            vizinhanca = img_binaria[i-1:i+2, j-1:j+2]
            if np.any(vizinhanca == 255):
                dilatada[i, j] = 255
    return dilatada

def preencher_buracos(imagem_A, semente_x, semente_y):
    # Obter A^c (Complemento de A)
    # Onde era 0 vira 255, onde era 255 vira 0
    complemento_A = np.zeros_like(imagem_A)
    for i in range(imagem_A.shape[0]):
        for j in range(imagem_A.shape[1]):
            if imagem_A[i, j] == 0:
                complemento_A[i, j] = 255
            else:
                complemento_A[i, j] = 0

    # X_0: Imagem preta com apenas um ponto branco na semente
    X_k_anterior = np.zeros_like(imagem_A)
    X_k_anterior[semente_y, semente_x] = 255
    
    while True:
        # Dilatação: (X_{k-1} + B)
        dilatada = dilatacao3x3(X_k_anterior)
        
        # Interseção dilatada com A^c
        X_k_atual = np.zeros_like(imagem_A)
        for i in range(imagem_A.shape[0]):
            for j in range(imagem_A.shape[1]):
                if dilatada[i, j] == 255 and complemento_A[i, j] == 255:
                    X_k_atual[i, j] = 255
        
        # Critério de parada: X_k == X_{k-1}
        if np.array_equal(X_k_atual, X_k_anterior):
            break
        
        X_k_anterior = X_k_atual.copy()

    # 3. Unir resultado com a fronteira original: X_k ∪ A
    resultado_final = np.zeros_like(imagem_A)
    for i in range(imagem_A.shape[0]):
        for j in range(imagem_A.shape[1]):
            if X_k_atual[i, j] == 255 or imagem_A[i, j] == 255:
                resultado_final[i, j] = 255
                
    return resultado_final

# --- Execução ---
cinzas = deixaCinza(imagem)
A = deixaPretoBranco(cinzas)

# Definindo uma semente (ponto dentro do buraco da imagem foto.png)
# Baseado na grade, o ponto (x=3, y=6) está dentro do buraco inferior.
ponto_x, ponto_y = 3, 6 

resultado = preencher_buracos(A, ponto_x, ponto_y)

cv2.imshow("Original (A)", imagem)
cv2.imshow("Buracos Preenchidos", resultado)
cv2.waitKey(0)
cv2.destroyAllWindows()
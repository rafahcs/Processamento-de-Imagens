import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

def deixaCinza(imagem):
    if len(imagem.shape) < 3:
        return imagem

    cinzas = np.mean(imagem, axis=2).astype(np.uint8)
    return cinzas

def convolucao_roberts(imagem, mask):
    altura, largura = imagem.shape
    saida = np.zeros((altura, largura), dtype=np.float32)

    # percorre a máscara 2x2
    for i in range(altura - 1):
        for j in range(largura - 1):
            # Recorta a janela 
            sub_matriz = imagem[i:i+2, j:j+2]
            
            # Multiplicação elemento a elemento e soma
            valor_final = np.sum(sub_matriz * mask)
            saida[i, j] = valor_final

    return saida

def filtro_roberts(cinza):
    
    mask_x = np.array([
        [1,  0],
        [0, -1]
    ], dtype=np.float32)
    
    mask_y = np.array([
        [0,  1],
        [-1, 0]
    ], dtype=np.float32)

    # convolução para direções vertical e horizontal
    grad_x = convolucao_roberts(cinza, mask_x)
    grad_y = convolucao_roberts(cinza, mask_y)

    # magnitude do gradiente
    magnitude = np.sqrt(grad_x**2 + grad_y**2)

    # normalização
    saida = np.clip(magnitude, 0, 255).astype(np.uint8)
    return saida

cinza = deixaCinza(imagem)
result = filtro_roberts(cinza)

cv2.namedWindow("Imagem cinza", cv2.WINDOW_NORMAL)
cv2.namedWindow("Filtro de Roberts", cv2.WINDOW_NORMAL)

cv2.imshow("Imagem cinza", cinza)
cv2.imshow("Filtro de Roberts", result)
cv2.waitKey(0)
cv2.destroyAllWindows()
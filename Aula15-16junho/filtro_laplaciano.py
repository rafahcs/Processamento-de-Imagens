import cv2
import numpy as np

foto = "foto.png"

# máscaras
Z_L1 = np.array([
    [ 0, -1,  0],
    [-1,  4, -1],
    [ 0, -1,  0]
], dtype=np.float32)

Z_L2 = np.array([
    [-1, -1, -1],
    [-1,  8, -1],
    [-1, -1, -1]
], dtype=np.float32)

Z_L3 = np.array([
    [ 1, -2,  1],
    [-2,  4, -2],
    [ 1, -2,  1]
], dtype=np.float32)

def aplicar_filtro(imagem, kernel):
    alt_img, larg_img = imagem.shape
    alt_k, larg_k = kernel.shape
    
    pad_h = alt_k // 2
    pad_w = larg_k // 2
    
    # imagem com bordas com 0
    imagem_pad = np.pad(imagem, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    
    saida = np.zeros_like(imagem, dtype=np.float32)
    
    # convolução 
    for i in range(alt_img):
        for j in range(larg_img):
            # Extrai a janela da imagem
            regiao = imagem_pad[i:i+alt_k, j:j+larg_k]
            
            valor_filtrado = np.sum(regiao * kernel)
            saida[i, j] = valor_filtrado
            
    saida = np.absolute(saida)
    saida = np.clip(saida, 0, 255)
    
    return saida.astype(np.uint8)

# Carrega imagem em tons de cinza 
def deixa_cinza(imagem):
    if imagem is None:
        return None
    if len(imagem.shape) < 3:
        return imagem

    cinzas = np.zeros((imagem.shape[0], imagem.shape[1]), dtype=np.uint8)
    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            cinzas[i][j] = int(imagem[i][j].sum() / 3)
    return cinzas
imagem_original = cv2.imread(foto)
imagem_cinza = deixa_cinza(imagem_original)

if imagem_cinza is None:
    print("Erro: Não foi possível carregar a imagem. Verifique o caminho.")
else:
    # filtros aplicados
    resultado_L1 = aplicar_filtro(imagem_cinza, Z_L1)
    resultado_L2 = aplicar_filtro(imagem_cinza, Z_L2)
    resultado_L3 = aplicar_filtro(imagem_cinza, Z_L3)

    # imagens
    cv2.imshow('Imagem Original', imagem_cinza)
    cv2.imshow('Laplaciano Z_L1 (4 vizinhos)', resultado_L1)
    cv2.imshow('Laplaciano Z_L2 (8 vizinhos)', resultado_L2)
    cv2.imshow('Laplaciano Z_L3', resultado_L3)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
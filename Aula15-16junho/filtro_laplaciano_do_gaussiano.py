import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

# a imagem em tons de cinza
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
img = deixa_cinza(imagem)

if img is None:
    print("Erro ao carregar a imagem. Verifique o caminho.")
    exit()

# máscara de Laplaciano do Gaussiano (LoG) 
mascara = np.array([
    [0,  1,  1,   2,   2,   2,  1,  1, 0],
    [1,  2,  4,   5,   5,   5,  4,  2, 1],
    [1,  4,  5,   3,   0,   3,  5,  4, 1],
    [2,  5,  3, -12, -24, -12,  3,  5, 2],
    [2,  5,  0, -24, -40, -24,  0,  5, 2],
    [2,  5,  3, -12, -24, -12,  3,  5, 2],
    [1,  4,  5,   3,   0,   3,  5,  4, 1],
    [1,  2,  4,   5,   5,   5,  4,  2, 1],
    [0,  1,  1,   2,   2,   2,  1,  1, 0]
], dtype=np.float32)

h, w = img.shape
m_h, m_w = mascara.shape

pad_h, pad_w = m_h // 2, m_w // 2

img_padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)

img_filtrada = np.zeros((h, w), dtype=np.float32)

# Aplicacao da máscara
for i in range(h):
    for j in range(w):
        # Extrai a janela da imagem correspondente ao tamanho da máscara
        regiao = img_padded[i:i+m_h, j:j+m_w]
        
        img_filtrada[i, j] = np.sum(regiao * mascara)

img_filtrada = np.abs(img_filtrada)
img_filtrada = np.clip(img_filtrada, 0, 255).astype(np.uint8)

# imagens
cv2.imshow('Imagem Original', imagem)
cv2.imshow('Filtro Laplaciano do Gaussiano (9x9)', img_filtrada)

cv2.waitKey(0)
cv2.destroyAllWindows()
import cv2
import numpy as np

foto = "cristo.jpg"
imagem = cv2.imread(foto)

mask = np.ones((3,3), dtype=np.int32) / 9.0

def escolheMask(cinza):
    print("Escolha qual mascara:")
    print("1, 2 ou 3")
    escolha = input()

    if escolha == 1:
        mask1 = np.ones((3,3), dtype=np.int32) / 9.0
        return convolucao(cinza, mask1)
    elif escolha == 2:
        mask2 = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]) / 9
        return convolucao(cinza, mask2)
    else:
        mask3 = np.array([
            [0, 1, 0],
            [1, -4, 1],
            [0, 1, 0]
        ], dtype = np.int32)
        return convolucao(cinza, mask3)

def deixaCinza (imagem):
    if len(imagem.shape) < 3:
        return imagem

    cinzas = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
    for i in range (imagem.shape[0]):
        for j in range (imagem.shape[1]):
            cinzas[i][j] = (imagem[i][j].sum()//3)

    return cinzas

def convolucao(imagem, mask):
    altura, largura = imagem.shape
    m_alt, m_larg = mask.shape 
    
    saida = np.zeros((altura, largura), dtype = np.float32)

    offset_h = m_alt // 2
    offset_w = m_larg // 2

    for i in range(offset_h, altura - offset_h):
        for j in range(offset_w, largura - offset_w):
            # Recorta o pedaço da imagem que a máscara está sobrepondo
            sub_matriz = imagem[
                i - offset_h : i + offset_h + 1, 
                j - offset_w : j + offset_w + 1
            ]
            
            # Multiplica cada pixel pelo peso da máscara e soma tudo
            valor_final = np.sum(sub_matriz * mask)
            
            # Atribui o resultado ao pixel central na saída
            saida[i, j] = valor_final

            # Normaliza para o intervalo 0-255 e converte de volta para uint8
    saida = np.clip(saida, 0, 256).astype(np.uint8)
    return saida
        
cinza = deixaCinza(imagem)
result = escolheMask(cinza)

cv2.namedWindow("Imagem cinza", cv2.WINDOW_NORMAL)
cv2.namedWindow("convolucao", cv2.WINDOW_NORMAL)

cv2.imshow("Imagem cinza", cinza)
cv2.imshow("convolucao", result)
cv2.waitKey(0)
cv2.destroyAllWindows()

import cv2
import numpy as np

# 1. Carregar a imagem em tons de cinza
foto = "foto.png"
imagem = cv2.imread(foto)

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
else:
    # Converter para float64 para evitar estouro de memória (overflow) nos cálculos
    img_float = img.astype(np.float64)
    h, w = img_float.shape

    # 2. Definir as máscaras do operador de Prewitt (3x3)
    # Máscara Horizontal (detecta bordas verticais - variação em X)
    gx_mask = np.array([[-1, 0, 1],
                        [-1, 0, 1],
                        [-1, 0, 1]])

    # Máscara Vertical (detecta bordas horizontais - variação em Y)
    gy_mask = np.array([[-1, -1, -1],
                        [ 0,  0,  0],
                        [ 1,  1,  1]])

    # 3. Criar matrizes de saída com zeros
    img_gx = np.zeros_like(img_float)
    img_gy = np.zeros_like(img_float)

    # 4. Aplicar a convolução manual (ignorando as bordas de 1 pixel)
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            # Extrair a região 3x3 da imagem ao redor do pixel atual
            regiao = img_float[i-1:i+2, j-1:j+2]
            
            # Aplicar a multiplicação ponto a ponto e somar os resultados
            img_gx[i, j] = np.sum(regiao * gx_mask)
            img_gy[i, j] = np.sum(regiao * gy_mask)

    # 5. Processar os resultados (Valor absoluto e conversão para 8-bit)
    img_gx_abs = np.clip(np.abs(img_gx), 0, 255).astype(np.uint8)
    img_gy_abs = np.clip(np.abs(img_gy), 0, 255).astype(np.uint8)

    # 6. Resultado da soma dos sentidos vertical e horizontal (Magnitude do Gradiente)
    # Uma aproximação comum e eficiente é a soma dos valores absolutos
    img_soma = np.clip(np.abs(img_gx) + np.abs(img_gy), 0, 255).astype(np.uint8)

    # 7. Exibir os resultados utilizando apenas imread e imshow do OpenCV
    cv2.imshow('1. Imagem Original', img)
    cv2.imshow('2. Contorno Horizontal (Gx)', img_gx_abs)
    cv2.imshow('3. Contorno Vertical (Gy)', img_gy_abs)
    cv2.imshow('4. Soma dos Sentidos (Magnitude)', img_soma)

    # Aguarda uma tecla ser pressionada para fechar as janelas
    cv2.waitKey(0)
    cv2.destroyAllWindows()
import cv2
import numpy as np

# 1. Carregar a imagem em tons de cinza
foto = "foto.png"

# 1. Definir as máscaras (kernels) de acordo com as imagens fornecidas
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

def aplicar_filtro_manual(imagem, kernel):
    # Obter as dimensões da imagem e do kernel
    alt_img, larg_img = imagem.shape
    alt_k, larg_k = kernel.shape
    
    # Calcular o preenchimento (padding) necessário para manter o tamanho original
    pad_h = alt_k // 2
    pad_w = larg_k // 2
    
    # Criar uma imagem com bordas preenchidas com zeros (Zero Padding)
    imagem_pad = np.pad(imagem, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    
    # Criar a matriz de saída preenchida com zeros (usando float para evitar estouro de 8-bits)
    saida = np.zeros_like(imagem, dtype=np.float32)
    
    # Realizar a convolução pixel a pixel
    for i in range(alt_img):
        for j in range(larg_img):
            # Extrair a região de interesse (janela) da imagem com padding
            regiao = imagem_pad[i:i+alt_k, j:j+larg_k]
            # Multiplicar elemento a elemento e somar os resultados
            valor_filtrado = np.sum(regiao * kernel)
            saida[i, j] = valor_filtrado
            
    # O Laplaciano calcula derivadas, gerando valores negativos. 
    # Pegamos o valor absoluto e limitamos o intervalo entre 0 e 255.
    saida = np.absolute(saida)
    saida = np.clip(saida, 0, 255)
    
    return saida.astype(np.uint8)

# --- Fluxo Principal ---

# 2. Carregar a imagem em tons de cinza (0 no segundo parâmetro força a escala de cinza)
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
    # 3. Aplicar cada um dos filtros
    resultado_L1 = aplicar_filtro_manual(imagem_cinza, Z_L1)
    resultado_L2 = aplicar_filtro_manual(imagem_cinza, Z_L2)
    resultado_L3 = aplicar_filtro_manual(imagem_cinza, Z_L3)

    # 4. Exibir os resultados utilizando apenas cv2.imshow
    cv2.imshow('Imagem Original', imagem_cinza)
    cv2.imshow('Laplaciano Z_L1 (4 vizinhos)', resultado_L1)
    cv2.imshow('Laplaciano Z_L2 (8 vizinhos)', resultado_L2)
    cv2.imshow('Laplaciano Z_L3', resultado_L3)

    # Aguardar qualquer tecla ser pressionada para fechar as janelas
    cv2.waitKey(0)
    cv2.destroyAllWindows()
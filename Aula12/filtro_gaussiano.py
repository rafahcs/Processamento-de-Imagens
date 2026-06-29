import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

def convolucao_2d(imagem, mascara, divisor):
    # Obtém as dimensões da imagem e da máscara
    alt_img, larg_img = imagem.shape
    tam_masc = mascara.shape[0]
    deslocamento = tam_masc // 2
    
    # Cria uma imagem de saída preenchida com zeros
    imagem_filtrada = np.zeros((alt_img, larg_img), dtype=np.uint8)
    
    # Aplica a convolução pixel a pixel (ignorando as bordas para simplificação)
    for i in range(deslocamento, alt_img - deslocamento):
        for j in range(deslocamento, larg_img - deslocamento):
            # Extrai a região de interesse (janela) da imagem
            janela = imagem[i - deslocamento : i + deslocamento + 1, 
                            j - deslocamento : j + deslocamento + 1]
            
            # Multiplica elemento a elemento e soma os valores
            soma = np.sum(janela * mascara)
            
            # Divide pelo fator de normalização correspondente e garante que fique entre 0 e 255
            valor_final = soma / divisor
            imagem_filtrada[i, j] = np.clip(valor_final, 0, 255)
            
    return imagem_filtrada

# 1. Carregar a imagem em tons de cinza
# Substitua 'sua_imagem.jpg' pelo caminho correto da sua imagem
def deixaCinza(imag):
    if len(imag.shape) < 3:
        return imag
    cinzas = np.zeros((imag.shape[0], imag.shape[1]), dtype=np.uint8)
    for i in range(imag.shape[0]):
        for j in range(imag.shape[1]):
            cinzas[i][j] = int(imag[i][j].sum() / 3)
    return cinzas
img_cinza = deixaCinza(imagem)

if img_cinza is None:
    print("Erro: Não foi possível carregar a imagem. Verifique o caminho.")
else:
    # 2. Definir as máscaras conforme as imagens fornecidas
    
    # Máscara 3x3 (Soma dos elementos = 16)
    mascara_3x3 = np.array([[1, 2, 1],
                            [2, 4, 2],
                            [1, 2, 1]], dtype=np.float32)
    divisor_3x3 = 16.0

    # Máscara 5x5 (Soma dos elementos = 273)
    mascara_5x5 = np.array([[1,  4,  7,  4, 1],
                            [4, 16, 26, 16, 4],
                            [7, 26, 41, 26, 7],
                            [4, 16, 26, 16, 4],
                            [1,  4,  7,  4, 1]], dtype=np.float32)
    divisor_5x5 = 273.0

    # 3. Aplicar os filtros
    print("Aplicando o filtro Gaussiano 3x3...")
    resultado_3x3 = convolucao_2d(img_cinza, mascara_3x3, divisor_3x3)

    print("Aplicando o filtro Gaussiano 5x5...")
    resultado_5x5 = convolucao_2d(img_cinza, mascara_5x5, divisor_5x5)

    # 4. Exibir os resultados utilizando apenas cv2.imshow
    cv2.imshow('Imagem Original (Cinza)', img_cinza)
    cv2.imshow('Filtro Gaussiano 3x3', resultado_3x3)
    cv2.imshow('Filtro Gaussiano 5x5', resultado_5x5)

    # Aguarda qualquer tecla para fechar as janelas
    cv2.waitKey(0)
    cv2.destroyAllWindows()
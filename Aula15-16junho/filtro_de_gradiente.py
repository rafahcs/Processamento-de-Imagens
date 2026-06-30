import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

def aplicar_convolucao(imagem, mascara):
    """
    Aplica uma máscara (kernel) a uma imagem 2D usando convolução manual.
    """
    lin_img, col_img = imagem.shape
    lin_mask, col_mask = mascara.shape
    
    # Calcula o preenchimento (padding) necessário para manter o tamanho da imagem
    pad_lin = lin_mask // 2
    pad_col = col_mask // 2
    
    # Cria uma imagem com padding de zeros
    img_pad = np.zeros((lin_img + 2 * pad_lin, col_img + 2 * pad_col))
    
    # Para máscara 2x2, o padding ideal na direita/base precisa ser ajustado
    if lin_mask == 2 and col_mask == 2:
        img_pad = np.zeros((lin_img + 1, col_img + 1))
        img_pad[0:lin_img, 0:col_img] = imagem
    else:
        img_pad[pad_lin:pad_lin + lin_img, pad_col:pad_col + col_img] = imagem
    
    # Imagem de saída
    resultado = np.zeros_like(imagem, dtype=float)
    
    # Aplica a máscara deslizando-a sobre a imagem
    for i in range(lin_img):
        for j in range(col_img):
            regiao = img_pad[i : i + lin_mask, j : j + col_mask]
            resultado[i, j] = np.sum(regiao * mascara)
            
    return resultado

def calcular_magnitude(gx, gy):
    """
    Calcula a magnitude do gradiente combinando as respostas em X e Y.
    """
    magnitude = np.sqrt(gx**2 + gy**2)
    # Normaliza para o intervalo 0-255 e converte para inteiro de 8 bits
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    return magnitude

# 1. Carregar a imagem em tons de cinza
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
    print("Erro: Imagem não encontrada. Verifique o caminho.")
else:
    # Converter a imagem original para float para evitar perda de dados nos cálculos
    img_float = img_cinza.astype(float)

    # DEFINIÇÃO DAS MÁSCARAS
    
    # Máscaras 2x2 (Primeira imagem)
    Gx_2x2 = np.array([[1, -1], 
                       [0,  0]])
    
    Gy_2x2 = np.array([[ 1,  0], 
                       [-1,  0]])

    # Máscaras 3x3 (Segunda imagem - Filtro de Prewitt)
    Gx_3x3 = np.array([[-1, -1, -1], 
                       [ 0,  0,  0], 
                       [ 1,  1,  1]])
    
    Gy_3x3 = np.array([[-1,  0,  1], 
                       [-1,  0,  1], 
                       [-1,  0,  1]])

    # APLICAÇÃO DOS FILTROS
    
    print("Aplicando filtros 2x2...")
    res_x_2x2 = aplicar_convolucao(img_float, Gx_2x2)
    res_y_2x2 = aplicar_convolucao(img_float, Gy_2x2)
    gradiente_2x2 = calcular_magnitude(res_x_2x2, res_y_2x2)

    print("Aplicando filtros 3x3...")
    res_x_3x3 = aplicar_convolucao(img_float, Gx_3x3)
    res_y_3x3 = aplicar_convolucao(img_float, Gy_3x3)
    gradiente_3x3 = calcular_magnitude(res_x_3x3, res_y_3x3)

    # EXIBIÇÃO DOS RESULTADOS
    
    cv2.imshow("Imagem Original", img_cinza)
    cv2.imshow("Gradiente 2x2", gradiente_2x2)
    cv2.imshow("Gradiente 3x3", gradiente_3x3)

    # Funções necessárias para manter as janelas do imshow abertas
    cv2.waitKey(0)
    cv2.destroyAllWindows()
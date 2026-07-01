import numpy as np
import cv2

foto = "foto.png"

def criar_kernel_derivada_gaussiana(sigma, tamanho_kernel=None):
    
    #Convolução da imagem com G'(x)
    if tamanho_kernel is None:
        tamanho_kernel = int(2 * np.ceil(3 * sigma) + 1)
    
    if tamanho_kernel % 2 == 0:
        tamanho_kernel += 1
        
    raio = tamanho_kernel // 2
    x = np.arange(-raio, raio + 1)
    
    termo_constante = 1.0 / np.sqrt(2 * np.pi * (sigma**3))
    gauss_deriv_1d = (-x * termo_constante) * np.exp(-(x**2) / (2 * (sigma**2)))
    
    # suavização perpendicular
    gauss_1d = (1.0 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-(x**2) / (2 * (sigma**2)))
    
    # operadores bidimensionais 
    kernel_x = np.outer(gauss_1d, gauss_deriv_1d) # Derivada em X, Suavização em Y
    kernel_y = np.outer(gauss_deriv_1d, gauss_1d) # Suavização em X, Derivada em Y
    
    return kernel_x, kernel_y

def convolucao(imagem, kernel):
    img_h, img_w = imagem.shape
    k_h, k_w = kernel.shape
    
    pad_h = k_h // 2
    pad_w = k_w // 2
    
    # tratamento de bordas externas com 0
    imagem_padded = np.pad(imagem, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)
    imagem_filtrada = np.zeros_like(imagem, dtype=np.float64)
    
    for i in range(img_h):
        for j in range(img_w):
            regiao = imagem_padded[i:i+k_h, j:j+k_w]
            imagem_filtrada[i, j] = np.sum(regiao * kernel)
            
    return imagem_filtrada

def filtro_canny_customizado(imagem, sigma=1.4, limiar_baixo=20, limiar_alto=50):
    img = cv2.imread(imagem)
    if img is None:
        print("Erro: Não foi possível carregar a imagem.")
        return
    
    # conversão em tons de cinza
    if len(img.shape) == 3:
        cinza = 0.299 * img[:, :, 2] + 0.587 * img[:, :, 1] + 0.114 * img[:, :, 0]
    else:
        cinza = img.copy()
        
    cinza = cinza.astype(np.float64)
    
    # operadores das imagens
    kernel_x, kernel_y = criar_kernel_derivada_gaussiana(sigma)
    
    # extração dos gradientes 
    Ix = convolucao(cinza, kernel_x)
    Iy = convolucao(cinza, kernel_y)
    
    # magnitude e ângulo do gradiente
    magnitude = np.hypot(Ix, Iy)
    magnitude = (magnitude / magnitude.max()) * 255 # Normalizando para faixa visível
    angulo = np.arctan2(Iy, Ix) * 180 / np.pi
    angulo[angulo < 0] += 180
    
    # Afinamento das bordas
    h, w = cinza.shape
    supremido = np.zeros((h, w), dtype=np.float64)
    
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            ang = angulo[i, j]
            
            if (0 <= ang < 22.5) or (157.5 <= ang <= 180):
                v1, v2 = magnitude[i, j+1], magnitude[i, j-1]
            elif (22.5 <= ang < 67.5):
                v1, v2 = magnitude[i+1, j-1], magnitude[i-1, j+1]
            elif (67.5 <= ang < 112.5):
                v1, v2 = magnitude[i+1, j], magnitude[i-1, j]
            else:
                v1, v2 = magnitude[i-1, j-1], magnitude[i+1, j+1]
                
            if (magnitude[i, j] >= v1) and (magnitude[i, j] >= v2):
                supremido[i, j] = magnitude[i, j]
                
    # Limiarização 
    bordas = np.zeros((h, w), dtype=np.uint8)
    FORTE = 255
    FRACO = 50
    
    forte_i, forte_j = np.where(supremido >= limiar_alto)
    fraco_i, fraco_j = np.where((supremido >= limiar_baixo) & (supremido < limiar_alto))
    
    bordas[forte_i, forte_j] = FORTE
    bordas[fraco_i, fraco_j] = FRACO
    
    # Rastreamento de Borda por Conectividade 8-vizinhos
    for i in range(1, h - 1):
        for j in range(1, w - 1):
            if bordas[i, j] == FRACO:
                if np.any(bordas[i-1:i+2, j-1:j+2] == FORTE):
                    bordas[i, j] = FORTE
                else:
                    bordas[i, j] = 0
                    
    # imagens
    cv2.imshow("Imagem Original", img)
    cv2.imshow("Bordas (Filtro Canny Customizado)", bordas)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    filtro_canny_customizado(foto, sigma=1.4, limiar_baixo=20, limiar_alto=50)
import numpy as np
import cv2

foto = "foto.png"
imagem_original = cv2.imread(foto)

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

def filtro_passa_baixa_media(imagem, tamanho_kernel=3):
    h, w = imagem.shape
    offset = tamanho_kernel // 2
    imagem_borrada = np.zeros_like(imagem, dtype=np.float32)
    
    # tratamento das bordas como 0
    imagem_pad = np.pad(imagem, offset, mode='constant', constant_values=0)
    
    # Convolução
    for i in range(h):
        for j in range(w):
            # Extrai a região de interesse (janela)
            regiao = imagem_pad[i:i+tamanho_kernel, j:j+tamanho_kernel]
            # Calcula a média
            imagem_borrada[i, j] = np.mean(regiao)
            
    return imagem_borrada

def aplicar_alto_reforco(caminho_imagem, A):
    # Carrega a imagem em tons de cinza 
    original = deixa_cinza(caminho_imagem)
    
    if original is None:
        print("Erro ao carregar a imagem. Verifique o caminho.")
        return
    
    # Converte para float32 para evitar estouro de canal 
    original_f = original.astype(np.float32)
    
    # Aplicação filtro Passa-Baixa 
    passa_baixa = filtro_passa_baixa_media(original_f, tamanho_kernel=3)
    
    # Aplicação filtro Passa-Alta
    passa_alta = original_f - passa_baixa
    
    # Alto-reforço
    regra1 = (A * original_f) - passa_baixa
    regra2 = ((A - 1) * original_f) + (original_f - passa_baixa)
    regra3 = ((A - 1) * original_f) + passa_alta
    
    # Normalização
    resultados = []
    for img in [regra1, regra2, regra3]:
        img_clipada = np.clip(img, 0, 255)
        resultados.append(img_clipada.astype(np.uint8))
        
    # imagens
    cv2.imshow("Original", original)
    cv2.imshow("(A * Orig) - PB", resultados[0])
    cv2.imshow("(A-1)*Orig + (Orig-PB)", resultados[1])
    cv2.imshow("(A-1)*Orig + PA", resultados[2])
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Execução
aplicar_alto_reforco(imagem_original, A=1.5)
import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

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
    print("Erro ao carregar a imagem. Verifique o caminho!")
else:
    # Pegar as dimensões da imagem original
    altura_img, largura_img = img_cinza.shape

    # 2. Definir o kernel (h) - Exemplo: Filtro de Média (Borramento) 3x3
    # Cada posição do filtro h[i, j] terá peso 1/9
    kernel = [
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9],
        [1/9, 1/9, 1/9]
    ]
    
    # Dimensões do kernel (n x m)
    n = len(kernel)
    m = len(kernel[0])

    # Deslocamentos para centralizar o kernel no pixel atual
    offset_x = n // 2
    offset_y = m // 2

    # 3. Criar uma imagem de saída preenchida com zeros
    imagem_filtrada = []
    for _ in range(altura_img):
        imagem_filtrada.append([0] * largura_img)

    # 4. Implementar a Convolução Espacial (Equação 2)
    # Varre todos os pixels da imagem original (desconsiderando as bordas para evitar erros de índice)
    for x in range(offset_x, altura_img - offset_x):
        for y in range(offset_y, largura_img - offset_y):
            
            soma_convolucao = 0.0
            
            # Somatórios da equação: i de 1 a n, j de 1 a m
            for i in range(n):
                for j in range(m):
                    # Coordenadas do pixel vizinho na imagem original f[x - (i - offset), y - (j - offset)]
                    # Ajustado para mapear corretamente o centro da máscara
                    pixel_x = x - (i - offset_x)
                    pixel_y = y - (j - offset_y)
                    
                    valor_pixel = img_cinza[pixel_x, pixel_y]
                    peso_kernel = kernel[i][j]
                    
                    soma_convolucao += valor_pixel * peso_kernel
            
            # Garantir que o valor está no intervalo válido de pixels [0, 255]
            if soma_convolucao < 0:
                soma_convolucao = 0
            elif soma_convolucao > 255:
                soma_convolucao = 255
                
            imagem_filtrada[x][y] = int(soma_convolucao)

    # Convertendo a lista Python de volta para o formato de matriz que o OpenCV entende (uint8)
    import numpy as np
    imagem_final = np.array(imagem_filtrada, dtype=np.uint8)

    # 5. Exibir os resultados utilizando o OpenCV
    cv2.imshow("Imagem Original", img_cinza)
    cv2.imshow("Imagem Filtrada (Convolucao)", imagem_final)
    
    # Aguarda uma tecla ser pressionada para fechar as janelas
    cv2.waitKey(0)
    cv2.destroyAllWindows()
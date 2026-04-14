import cv2
import numpy as np 
import matplotlib.pyplot as plt

imagem = cv2.imread("moedas.png")


def deixaCinza (imagem):
    if len(imagem.shape) < 3:
        return imagem

    cinzas = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
    for i in range (imagem.shape[0]):
        for j in range (imagem.shape[1]):
            cinzas[i][j] = (imagem[i][j].sum()//3)

    return cinzas

def criaHistograma (IMG):
    histCinza = [0]*256
    for i in range (IMG.shape[0]):
        for j in range (IMG.shape[1]):
            histCinza[IMG[i][j]] = histCinza[IMG[i][j]] + 1
    pixel = [0]*256
    for i in range (256):
        pixel[i]=i
    plt.xlabel('ID do Pixel (0 a 255)')
    plt.ylabel('Quantidade')
    plt.title('Histograma dos Pixels da Imagem')
    plt.bar(pixel, histCinza, color='gray')
    plt.show()

mask = np.array([
            [1, 1, 1],
            [1, 1, 1],
            [1, 1, 1]
        ]) / 9

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

#adiciona uma borda preta de 1 px na imagem
def bordaPreta(cinza):
    borda = np.zeros(((imagem.shape[0]+2), (imagem.shape[1]+2)), dtype = np.uint8)
    for i in range (imagem.shape[0]):
        for j in range (imagem.shape[1]):
            borda[i+1][j+1] = cinza[i][j]
    cv2.imshow("Borda Preta", borda)
    return borda

def erosao(cinza):

    borda = bordaPreta(cinza)

    operador1 = [
        [1,0,1],
        [0,1,0],
        [1,0,1]
    ]

    for i in range (3):
        for j in range (3):
            operador1[i][j] = ((i+j)%2)
    print('Operador 1 =')
    print(operador1)
    print('')

    transformada1 = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
    for i in range ((imagem.shape[0])):
        for j in range ((imagem.shape[1])):
            m = n = 0
            aux1 = ((borda[i-1][j-1]) * (operador1[m][n]))
            aux2 = ((borda[i-1][j]) * (operador1[m][n+1]))
            aux3 = ((borda[i-1][j+1]) * (operador1[m][n+2]))
            aux4 = ((borda[i][j-1]) * (operador1[m+1][n]))
            aux5 = ((borda[i][j]) * (operador1[m+1][n+1]))
            aux6 = ((borda[i][j+1]) * (operador1[m+1][n+2]))
            aux7 = ((borda[i+1][j-1]) * (operador1[m+2][n]))
            aux8 = ((borda[i+1][j]) * (operador1[m+2][n+1]))
            aux9 = ((borda[i+1][j+1]) * (operador1[m+2][n+2]))
            transformada1 [i][j] = aux1 + aux2 + aux3 + aux4 + aux5 + aux6 + aux7 + aux8 + aux9
    return transformada1

def erosao2(cinza):   
    borda = bordaPreta(cinza)

    operador2 = [
        [1,0,1],
        [0,4,0],
        [1,0,1]
    ]
    print('Operador 2 =')
    print(operador2)
    print('')

    transformada2 = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
    for i in range ((imagem.shape[0])):
        for j in range ((imagem.shape[1])):
            m = n = 0
            aux1 = ((borda[i-1][j-1]) * (operador2[m][n]))
            aux2 = ((borda[i-1][j]) * (operador2[m][n+1]))
            aux3 = ((borda[i-1][j+1]) * (operador2[m][n+2]))
            aux4 = ((borda[i][j-1]) * (operador2[m+1][n]))
            aux5 = ((borda[i][j]) * (operador2[m+1][n+1]))
            aux6 = ((borda[i][j+1]) * (operador2[m+1][n+2]))
            aux7 = ((borda[i+1][j-1]) * (operador2[m+2][n]))
            aux8 = ((borda[i+1][j]) * (operador2[m+2][n+1]))
            aux9 = ((borda[i+1][j+1]) * (operador2[m+2][n+2]))
            auxF = (aux1 + aux2 + aux3 + aux4 + aux5 + aux6 + aux7 + aux8 + aux9)
            if auxF < 0:
                auxF = 0
            if auxF > 255:
                auxF = 255
            transformada2 [i][j] = auxF
    return transformada2

cinza = deixaCinza(imagem)
histograma = criaHistograma(cinza)
convoc = convolucao(cinza, mask)
ero1 = erosao(cinza)
ero2 = erosao2(cinza)

cv2.namedWindow("Imagem cinza", cv2.WINDOW_NORMAL)
cv2.namedWindow("convolucao", cv2.WINDOW_NORMAL)

cv2.imshow("Imagem cinza", cinza)
cv2.imshow("Imagem convolucao", convoc)
cv2.imshow("Erosao 1", ero1)
cv2.imshow("Erosao 2", ero2)

#Operadores morfologicos de erosao prontos

kernel = np.ones((5,5), np.uint8)
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
#kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
#kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))

erosion =  cv2.erode(cinza, kernel, iterations = 1)
cv2.imshow("erosao", erosion)

cv2.waitKey(0)
cv2.destroyAllWindows()


import cv2
import numpy
import matplotlib.pyplot as plt
foto = 'entrada2.jpg'
imagem = cv2.imread(foto)

###################################

def deixaCinza (IMG):
    cinzas = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
    for i in range (imagem.shape[0]):
        for j in range (imagem.shape[1]):
            cinzas[i][j] = (IMG[i][j].sum()//3)
    cv2.imshow('Imagem em Tons de Cinza', cinzas)
    cv2.waitKey(0)
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

###################################
###################################

def normalizacao (IMG):
    normalizada = [0]*256
    for i in range (256):
        normalizada[i] = (criaHistograma(IMG))/((IMG.shape[0])*(IMG.shape[1]))
    pixel = [0]*256
    for i in range (256):
        pixel[i]=i
    plt.xlabel('Tom de Cinza')
    plt.ylabel('Quantidade')
    plt.title('Histograma de Tons de Cinza Normalizado')
    plt.bar(pixel, normalizada, color='gray')
    plt.show()
    return normalizada

###################################
###################################

def acumulacao (NRML):
    acumulada = [0]*256
    for i in range (256):
        if i == 0:
            acumulada[i] = NRML[i]
        else:
            acumulada[i] = NRML[i] + acumulada[i-1]
    pixel = [0]*256
    for i in range (256):
        pixel[i]=i
    plt.xlabel('Tom de Cinza')
    plt.ylabel('Quantidade')
    plt.title('Histograma Normalizado Acumulado')
    plt.bar(pixel, acumulada, color='gray')
    plt.show()
    return acumulada

###################################
###################################

def mapeamento (ACML):
    mapa = [0]*256
    for i in range (256):
        mapa[i] = round(ACML[i]*255)
    return mapa

###################################
###################################

def equalizacao (IMG, MPMT):
    equalizada = numpy.zeros((IMG.shape[0], IMG.shape[1]), dtype = numpy.uint8)
    for i in range (IMG.shape[0]):
        for j in range (IMG.shape[1]):
            equalizada[i][j] = MPMT[IMG[i][j]]
    criaHistograma(equalizada)
    cv2.imshow('Imagem Equalizada', equalizada)
    cv2.waitKey(0)

###################################
###################################

imgCinza = deixaCinza(imagem)
criaHistograma(imgCinza)
imgEqualizada = equalizacao(imgCinza,mapeamento(acumulacao(normalizacao(imgCinza))))
cv2.imwrite("saida2-iEqualizada.jpg",imgEqualizada)

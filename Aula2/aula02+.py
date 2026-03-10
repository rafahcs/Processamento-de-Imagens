# -*- coding: utf-8 -*-

import cv2
import numpy
import matplotlib.pyplot as plt
foto = 'foto.jpg'
imagem = cv2.imread(foto)


def extraiAzul (IMG):
    azul = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
    azul[:,:] = IMG[:,:,0]  #[linhas (altura), colunas (largura), canais('profundidade')]
    cv2.imshow("Canal Azul",azul)
    cv2.waitKey(0)
    return azul

def extraiVerde (IMG):
    verde = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
    verde[:,:] = IMG[:,:,1]
    cv2.imshow("Canal Verde",verde)
    cv2.waitKey(0)
    return verde

def extraiVermelho (IMG):
    vermelho = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
    vermelho [:,:] = IMG[:,:,2]
    cv2.imshow("Canal Vermelho",vermelho)
    cv2.waitKey(0)
    return vermelho


def deixaCinza (IMG):
    cinzas = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
    for i in range (imagem.shape[0]):
        for j in range (imagem.shape[1]):
            cinzas[i][j] = (IMG[i][j].sum()//3)
    cv2.imshow('Imagem em Tons de Cinza', cinzas)
    cv2.waitKey(0)
    return cinzas

def separaCor (IMG):
    separada = IMG
    for i in range (IMG.shape[0]):
        for j in range (IMG.shape[1]):
            if ((separada[i][j]<=130) or (separada[i][j]>=160)):
                separada[i][j] = 255
    cv2.imshow('Imagem Cinza com Tom Separado', separada)
    cv2.waitKey(0)
    return separada

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


imgCinza = deixaCinza(imagem)
criaHistograma(imgCinza)
canalAzul = extraiAzul(imagem)
criaHistograma(canalAzul)
canalVerde = extraiVerde(imagem)
criaHistograma(canalVerde)
canalVermelho = extraiVermelho(imagem)
criaHistograma(canalVermelho)
imgSeparada = separaCor(imgCinza)
cv2.imwrite("saida1-iSeparada.jpg",imgSeparada)

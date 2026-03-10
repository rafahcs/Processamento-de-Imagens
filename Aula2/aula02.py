# -*- coding: utf-8 -*-

import cv2
import numpy
import matplotlib.pyplot as plt
foto = 'foto.jpg'
imagem = cv2.imread(foto)

###

#cria uma imagem (matriz) e preenche seus pixels com tons de cinza
#cada tom de cinz equivale à média dos tres canais daquele pixel
cinzas = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        cinzas[i][j] = (imagem[i][j].sum()//3)
"""
cv2.imshow("Tons de Cinza", cinzas)
cv2.waitKey(0)
cv2.imwrite("im_cinza.jpg", cinzas)
"""

###

#cria um array com 256 casas, contando os 256 tons de cinza
#preenche ele casa a casa somando +1 sempre que aquele tom de cinza for encontrado (0 a 255)
histCinza = [0]*256
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        histCinza[cinzas[i][j]]+=1

#cria o eixo x e nomeia o eixo x e y
pixel = [0]*256
for i in range (256):
    pixel[i]=i
plt.xlabel('Tom de Cinza')
plt.ylabel('Quantidade')

#nomeia e plota o histograma
plt.title('Histograma de Tons de Cinza')
plt.bar(pixel, histCinza, color='gray')
plt.show()

###

#criando histogramas pros outros canais
canalAzul = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype = numpy.uint8)
canalVerde = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype = numpy.uint8)
canalVermelho = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype = numpy.uint8)

canalAzul[:,:,0] = imagem[:,:,0]
canalVerde[:,:,1] = imagem[:,:,1]
canalVermelho[:,:,2] = imagem[:,:,2]

histAzul = [0]*256
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        histAzul[canalAzul[i][j][0]]+=1
pixel = [0]*256
for i in range (256):
    pixel[i]=i
plt.xlabel('Tom de Azul')
plt.ylabel('Quantidade')
plt.title('Histograma de Tons de Azul')
plt.bar(pixel, histAzul, color='blue')
plt.show()

histVerde = [0]*256
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        histVerde[canalVerde[i][j][1]]+=1
pixel = [0]*256
for i in range (256):
    pixel[i]=i
plt.xlabel('Tom de Verde')
plt.ylabel('Quantidade')
plt.title('Histograma de Tons de Verde')
plt.bar(pixel, histVerde, color='green')
plt.show()

histVermelho = [0]*256
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        histVermelho[canalVermelho[i][j][2]]+=1
pixel = [0]*256
for i in range (256):
    pixel[i]=i
plt.xlabel('Tom de Vermelho')
plt.ylabel('Quantidade')
plt.title('Histograma de Tons de Vermelho')
plt.bar(pixel, histVermelho, color='red')
plt.show()

###

separadas = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        separadas[i][j] = cinzas[i][j]


for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        if ((separadas[i][j]<=130) or (separadas[i][j]>=160)):
            separadas[i][j] = 255

#cria um array com 256 casas, contando os 256 tons de cinza
#preenche ele casa a casa somando +1 sempre que aquele tom de cinza for encontrado (0 a 255)
histSepara = [0]*256
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        histSepara[separadas[i][j]]+=1

#cria o eixo x e nomeia o eixo x e y
pixelN = [0]*256
for i in range (256):
    pixelN[i]=i
plt.xlabel('Tom de Cinza')
plt.ylabel('Quantidade')

#nomeia e plota o histograma
plt.title('Histograma de Tons de Cinza 2')
plt.bar(pixelN, histSepara, color='gray')
plt.show()


cv2.imshow("Imagem Real",imagem)
cv2.imshow("Tons de Cinza", cinzas)
cv2.imshow("Cores Separadas", separadas)
cv2.waitKey(0)
cv2.imwrite("im_separada.jpg", separadas)

import cv2
import numpy
import matplotlib.pyplot as plt
foto = 'entrada2.jpg'
imagem = cv2.imread(foto)

###################################

#cria uma imagem (matriz) e preenche seus pixels com tons de cinza
#cada tom de cinza equivale à média dos tres canais daquele pixel
contrtCinzas = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        contrtCinzas[i][j] = (imagem[i][j].sum()//3)

cv2.imshow("Tons de Cinza", contrtCinzas)

histCinza = [0]*256
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        histCinza[contrtCinzas[i][j]]+=1

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

###################################
###################################

normaliza = [0]*256
for i in range (256):
    normaliza[i] = (histCinza[i])/((imagem.shape[0])*(imagem.shape[1]))

#cria o eixo x e nomeia o eixo x e y
pixel = [0]*256
for i in range (256):
    pixel[i]=i
plt.xlabel('Tom de Cinza')
plt.ylabel('Quantidade')

#nomeia e plota o histograma
plt.title('Histograma de Tons de Cinza Normalizado')
plt.bar(pixel, normaliza, color='gray')
plt.show()

###################################
###################################

acumula = [0]*256
for i in range (256):
    if i == 0:
        acumula[i] = normaliza[i]
    else:
        acumula[i] = normaliza[i] + acumula[i-1]
        
#print(acumula)

#cria o eixo x e nomeia o eixo x e y
pixel = [0]*256
for i in range (256):
    pixel[i]=i
plt.xlabel('Tom de Cinza')
plt.ylabel('Quantidade')

#nomeia e plota o histograma
plt.title('Histograma Normalizado Acumulado')
plt.bar(pixel, acumula, color='gray')
plt.show()

###################################
###################################

mapeamento = [0]*256
for i in range (256):
    mapeamento[i] = round(acumula[i]*255)

equaliza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype = numpy.uint8)
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        equaliza[i][j] = mapeamento[contrtCinzas[i][j]]
cv2.imshow("Mapeamento", equaliza)

#cria o eixo x e nomeia o eixo x e y
histEqlz = [0]*256
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        histEqlz[equaliza[i][j]]+=1
pixel = [0]*256
for i in range (256):
    pixel[i]=i
plt.xlabel('Tom de Cinza')
plt.ylabel('Quantidade')
plt.title('Histograma Equalizado')
plt.bar(pixel, histEqlz, color='gray')
plt.show()

###################################
###################################

cv2.waitKey(0)
cv2.imwrite("im_equzlizada.jpg", equaliza)

import numpy as np
import cv2
import matplotlib.pyplot as plt

foto = "foto.jpg"
imagem = cv2.imread(foto)

cinzas = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        cinzas[i][j] = (imagem[i][j].sum() // 3)

cv2.imshow("imagem tons de cinza", cinzas)
cv2.waitKey(0)

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

def curva_expansao(imagem):
    img_dest = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
    r1 = 64
    r2 = 192

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            r = imagem[i][j]
            if r <= r1:
                s = 0
            elif  r1<= r <= r2: 
                s = 255*((r-r1) / (r2-r1))
            else:
                s = 255
            img_dest[i][j] = s
    return img_dest

img = curva_expansao(cinzas)
cv2.imshow("imagem expandida", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

histExpandido = [0]*256

for i in range(imagem.shape[0]):
    for j in range(imagem.shape[1]):
        histExpandido[img[i][j]] += 1 

pixel = [0]*256
for i in range (256):
    pixel[i]=i
plt.xlabel('Tom de Cinza')
plt.ylabel('Quantidade')

plt.title("Histograma imagem expandida")
plt.bar(pixel, histExpandido, color='gray')
plt.show()



import numpy as np
import cv2 
import matplotlib.pyplot as plt

foto = 'foto.jpg'
imagem = cv2.imread(foto)

cinzas = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        cinzas[i][j] = (imagem[i][j].sum() // 3)

#cv2.imshow("titulo", cinzas)
#cv2.waitKey(0)

def curvas_ton(imagem):
    img_dest = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            r = int(imagem[i][j])
            s = 2*r

            if s > 255:
                s = 255

            img_dest[i][j] = s
    
    return img_dest

img_dest = curvas_ton(cinzas)

cv2.imshow("Original", cinzas)
cv2.imshow("f(r) = 2r", img_dest)
cv2.waitKey(0)
cv2.destroyAllWindows()

r = np.arange(256)
s = np.clip(2*r, 0, 255)

plt.title("")
plt.xlabel("Origem")
plt.xlim(0, 255)
plt.ylabel("Destino")
plt.ylim(0, 255)
plt.plot(r, s, color='blue')
plt.grid(True)

plt.show()



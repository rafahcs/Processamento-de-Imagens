import numpy as np
import cv2 
import matplotlib.pyplot as plt

foto = 'foto.jpg'
imagem = cv2.imread(foto)

cinzas = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)
for i in range (imagem.shape[0]):
    for j in range (imagem.shape[1]):
        cinzas[i][j] = (imagem[i][j].sum() // 3)

def curva_parabolica(imagem):
    img_dest = np.zeros((imagem.shape[0], imagem.shape[1]), dtype = np.uint8)

    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            r = int(imagem[i][j])
            s = ((1/256)*r)**2 * 255

            if s > 255:
                s = 255

            img_dest[i][j] = int(s)

    return img_dest

img = curva_parabolica(cinzas)

cv2.imshow("cinza", cinzas)
cv2.imshow("parabolica", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

r = np.arange(256)
s = np.clip((((1/256)*r)**2)*255, 0, 255)

plt.title("")
plt.xlabel("Origem")
plt.xlim(0, 255)
plt.ylabel("Destino")
plt.ylim(0, 255)
plt.plot(r, s, color='blue')
plt.grid(True)

plt.show()


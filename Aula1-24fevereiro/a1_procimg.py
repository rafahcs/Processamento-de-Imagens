import cv2  #no vscode a função imshow é cv2.imshow()
import numpy

nomeImagem = 'foto.jpg'

imagem = cv2.imread(nomeImagem)
if imagem is None:
    raise FileNotFoundError(f"Não foi possível abrir a imagem: {nomeImagem}")

print('Largura em pixels:', end="")
print(imagem.shape[1])

print('Altura img:', end="")
print(imagem.shape[0])

print('Qtde de canais:', end="")
print(imagem.shape[2])

cv2.imshow("Original", imagem)
(b, g, r) = imagem[0, 0]

canalBlue = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype=numpy.uint8)
canalGreen = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype=numpy.uint8)
canalRed = numpy.zeros((imagem.shape[0], imagem.shape[1], imagem.shape[2]), dtype=numpy.uint8)

canalBlue[:,:,0] = imagem[:,:,0]
canalGreen[:,:,1] = imagem[:,:,1]
canalRed[:,:,2] = imagem[:,:,2]

cv2.imshow("canal Blue", canalBlue)
cv2.imshow("canal Green", canalGreen)
cv2.imshow("canal Red", canalRed)

canalCinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)

for i in range(imagem.shape[0]):
  for j in range(imagem.shape[1]):
    canalCinza[i][j] = (imagem[i][j].sum()//3)

cv2.waitKey(0)

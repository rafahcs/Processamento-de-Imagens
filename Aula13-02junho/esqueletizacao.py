nomeImagem = 'draw2.png'

import cv2
import numpy
import math
import matplotlib.pyplot as plt

imagem = cv2.imread(nomeImagem)

cinza = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
preto_branco = numpy.zeros((imagem.shape[0], imagem.shape[1]), dtype=numpy.uint8)
histograma = numpy.zeros(256, dtype=int)

divisor = 80

for i in range(0, imagem.shape[0]):
  for j in range(0, imagem.shape[1]):
    cor = (imagem[i][j].sum()) // 3
    cinza[i, j] = cor
    histograma[cor] += 1
    if cor > divisor:
      preto_branco[i, j] = 255

def masc(num):
  return numpy.ones((num, num), dtype=int)

def erosao(img, mask, procura_preto = False):
  margem_inicio = math.floor(len(mask) / 2)
  margem_final = len(mask) - margem_inicio - 1
  cinza_convolucionada = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)
  qtdProcurada = numpy.count_nonzero(mask == 1)

  for i in range(margem_inicio, img.shape[0] - margem_final):
    for j in range(margem_inicio, img.shape[1] - margem_final):
      qtd_Encontrada = 0

      for a in range(0, len(mask)):
        for b in range(0, len(mask[0])):
          if procura_preto:
            if img[i + a - margem_inicio, j + b - margem_inicio] == 0 and mask[a][b] == 1:
              qtd_Encontrada += 1
          else:
            if img[i + a - margem_inicio, j + b - margem_inicio] / 255 == 1 and mask[a][b] == 1:
              qtd_Encontrada += 1

    
      if qtd_Encontrada == qtdProcurada: # Fit
        cinza_convolucionada[i, j] = 0 if procura_preto else 255
      else:
        cinza_convolucionada[i, j] = 255 if procura_preto else 0

  return cinza_convolucionada

def erosaoQtd(qtd, img, mask, procura_preto = False):
  img_Recursiva = erosao(img, mask, procura_preto)
  for i in range(qtd - 1):
    img_Recursiva = erosao(img_Recursiva, mask, procura_preto)
  return img_Recursiva

def dilatar(img, mask, procura_preto = False):
  margem_inicio = math.floor(len(mask) / 2)
  margem_final = len(mask) - margem_inicio - 1
  cinza_convolucionada = numpy.zeros((img.shape[0], img.shape[1]), dtype=numpy.uint8)

  for i in range(margem_inicio, img.shape[0] - margem_final):
    for j in range(margem_inicio, img.shape[1] - margem_final):
      encontrou = False
      
      a = 0
      while a < len(mask) and not encontrou:
        b = 0
        while b < len(mask[0]) and not encontrou:
          if procura_preto:
            if mask[a][b] == 1 and img[i + a - margem_inicio, j + b - margem_inicio] == 0:
              encontrou = True
          else:
            if mask[a][b] == 1 and img[i + a - margem_inicio, j + b - margem_inicio] / 255 == 1:
              encontrou = True
          b += 1
        a += 1
    
      if encontrou:
        cinza_convolucionada[i, j] = 0 if procura_preto else 255
      else:
        cinza_convolucionada[i, j] = 255 if procura_preto else 0

  return cinza_convolucionada

def dilatarQtd(qtd, img, mask, procura_preto = False):
  img_Recursiva = dilatar(img, mask, procura_preto)
  for i in range(qtd - 1):
    img_Recursiva = dilatar(img_Recursiva, mask, procura_preto)
  return img_Recursiva

def abertura(img, mask, procura_preto = False):
  return dilatar(erosao(img, mask, procura_preto), mask, procura_preto)

def intersecao(img1, img2, procura_preto = False):
  img_Intersecao = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      if img1[i][j] == img2[i][j]:
        img_Intersecao[i, j] = img1[i][j]
      else:
        img_Intersecao[i, j] = (255 if procura_preto else 0)
  return img_Intersecao

def diferenca(img1, img2, procura_preto = False):
  img1_Subtraida = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      if procura_preto:
        if img1[i][j] == 0 and img2[i][j] == 255:
          img1_Subtraida[i, j] = 0
        else:
          img1_Subtraida[i, j] = 255
      else:
        if img1[i][j] == 255 and img2[i][j] == 0:
          img1_Subtraida[i, j] = 255
        else:
          img1_Subtraida[i, j] = 0
  return img1_Subtraida

def unir(img1, img2, procura_preto = False):
  img_Unida = numpy.zeros((img1.shape[0], img1.shape[1]), dtype=numpy.uint8)
  for i in range(0, img1.shape[0]):
    for j in range(0, img1.shape[1]):
      if procura_preto:
        if img1[i][j] == 0 or img2[i][j] == 0:
          img_Unida[i, j] = 0
        else:
          img_Unida[i, j] = 255
      else:
        if img1[i][j] == 255 or img2[i][j] == 255:
          img_Unida[i, j] = 255
        else:
          img_Unida[i, j] = 0
  return img_Unida

def resize(img):
  return cv2.resize(img, (img.shape[1], img.shape[0]), interpolation=cv2.INTER_AREA)

mask = numpy.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]])

def esqueletizar(img, procura_preto = False):
  img_Vazia = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (255 if procura_preto else 0)
  img_Esqueleto = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (255 if procura_preto else 0)
  img_Erodida = img.copy()
  img_Aberta = numpy.ones((img.shape[0], img.shape[1]), dtype=numpy.uint8) * (0 if procura_preto else 255)

  while not numpy.array_equal(img_Aberta, img_Vazia):
    img_Aberta = abertura(img_Erodida, mask, procura_preto)
    imgDiferenca = diferenca(img_Erodida, img_Aberta, procura_preto)
    img_Esqueleto = unir(img_Esqueleto, imgDiferenca, procura_preto)
    img_Erodida = erosao(img_Erodida, mask, procura_preto)

  return img_Esqueleto

cv2.imshow("Tons de Cinza", resize(cinza))
cv2.imshow("Preto e Branco", resize(preto_branco))

img_Esqueleto = esqueletizar(preto_branco, False)
cv2.imshow("Esqueleto", resize(img_Esqueleto))
img_Esqueletizada = diferenca(preto_branco, img_Esqueleto, False)
cv2.imshow("Esqueletizado", resize(img_Esqueletizada))

pixel = list(range(256))
fig, ((x0y0)) = plt.subplots(1, 1, sharex=True)
subplots = [x0y0]
histogramas = [histograma]
labels = ["Histograma"]

for i in range(len(histogramas)):
  subplots[i].bar(pixel, histogramas[i], color='black', width = 1)
  subplots[i].set_xlabel("Cor")
  subplots[i].set_ylabel("Quantidade")
  subplots[i].set_title(labels[i])

fig.tight_layout()
#plt.show()

cv2.waitKey(0)
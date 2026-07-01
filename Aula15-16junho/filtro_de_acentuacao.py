import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

# Transforma a imagem em tons de cinza
def deixaCinza(imag):
    if len(imag.shape) < 3:
        return imag
    cinzas = np.zeros((imag.shape[0], imag.shape[1]), dtype=np.uint8)
    for i in range(imag.shape[0]):
        for j in range(imag.shape[1]):
            cinzas[i][j] = int(imag[i][j].sum() / 3)
    return cinzas
img_cinza = deixaCinza(imagem)

if img_cinza is None:
    print("Erro ao carregar a imagem. Verifique o caminho!")
else:
    M, N = img_cinza.shape

    # Transformada de Fourier
    f = np.fft.fft2(img_cinza)
    fshift = np.fft.fftshift(f)  # Centraliza a frequência no meio da imagem

    # máscara do Filtro de Acentuação
    D0 = 30     #frequeência do corte
    H = np.zeros((M, N), dtype=np.float32)

    cy, cx = M // 2, N // 2

    for u in range(M):
        for v in range(N):
            # distância D(u, v) até a origem centralizada
            D = np.sqrt((u - cy) ** 2 + (v - cx) ** 2)

            # Relações do filtro passa-altas: 1 se D > D0, 0 se D <= D0
            if D > D0:
                H[u, v] = 1.0
            else:
                H[u, v] = 0.0

    # Aplicação do filtro no domínio da frequência
    fshift_filtrado = fshift * H

    # Transformada de Fourier inversa
    f_ishift = np.fft.ifftshift(fshift_filtrado)
    img_back = np.fft.ifft2(f_ishift)
    img_filtrada = np.abs(img_back)

    # Normalização
    img_filtrada = cv2.normalize(
        img_filtrada, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
    )

    # imagens
    cv2.imshow("Imagem Original", img_cinza)
    cv2.imshow("Filtro de Acentuacao (Passa-Altas)", img_filtrada)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

# 1. Carregar a imagem em tons de cinza usando apenas o imread do OpenCV
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
    # 2. Obter as dimensões da imagem
    M, N = img_cinza.shape

    # 3. Aplicar a Transformada de Fourier Bidimensional (FFT) usando Numpy
    f = np.fft.fft2(img_cinza)
    fshift = np.fft.fftshift(f)  # Centraliza a frequência (0,0) no meio da imagem

    # 4. Criar a máscara do Filtro Passa-Altas Ideal (Acentuação)
    # Definir a frequência de corte D0 (ajuste esse valor para mudar o resultado)
    D0 = 30
    H = np.zeros((M, N), dtype=np.float32)

    # Centro do plano de frequências
    cy, cx = M // 2, N // 2

    for u in range(M):
        for v in range(N):
            # Calcular a distância D(u, v) até a origem centralizada
            D = np.sqrt((u - cy) ** 2 + (v - cx) ** 2)

            # Relação do filtro passa-altas: 1 se D > D0, 0 se D <= D0
            if D > D0:
                H[u, v] = 1.0
            else:
                H[u, v] = 0.0

    # 5. Aplicar o filtro no domínio da frequência
    fshift_filtrado = fshift * H

    # 6. Reverter a Transformada de Fourier (FFT Inversa)
    f_ishift = np.fft.ifftshift(fshift_filtrado)
    img_back = np.fft.ifft2(f_ishift)
    img_filtrada = np.abs(img_back)

    # 7. Normalizar o resultado para o intervalo [0, 255] de forma a exibir corretamente
    img_filtrada = cv2.normalize(
        img_filtrada, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
    )

    # Soma opcional: Para acentuar os detalhes na imagem original (Nitidez/Sharpening)
    # img_acentuada = cv2.addWeighted(img, 1.0, img_filtrada, 0.5, 0)

    # 8. Exibir as imagens utilizando apenas o imshow do OpenCV
    cv2.imshow("Imagem Original", img_cinza)
    cv2.imshow("Filtro de Acentuacao (Passa-Altas)", img_filtrada)

    # Aguarda uma tecla ser pressionada para fechar as janelas
    cv2.waitKey(0)
    cv2.destroyAllWindows()
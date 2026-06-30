import cv2
import numpy as np

foto = "foto2.png"
imagem = cv2.imread(foto)

# 1. Carregar a imagem em tons de cinza
def deixaCinza(imag):
    if len(imag.shape) < 3:
        return imag
    cinzas = np.zeros((imag.shape[0], imag.shape[1]), dtype=np.uint8)
    for i in range(imag.shape[0]):
        for j in range(imag.shape[1]):
            cinzas[i][j] = int(imag[i][j].sum() / 3)
    return cinzas
img_cinza = deixaCinza(imagem)

# 2. Converter a imagem para float32 e aplicar a DFT (Transformada Discreta de Fourier)
img_float = np.float32(img_cinza)
dft = cv2.dft(img_float, flags=cv2.DFT_COMPLEX_OUTPUT)

# 3. Centralizar as baixas frequências no meio da matriz (fftshift)
dft_shift = np.fft.fftshift(dft)

# 4. Obter as dimensões da imagem e determinar o centro
rows, cols = img_cinza.shape
crow, ccol = rows // 2, cols // 2

# 5. Definir o raio de corte (r) do filtro passa-alta
r = 60 

# 6. Criar a máscara H(u,v) baseada nas novas equações fornecidas
# Inicializa com 1 (permite a passagem) e define 0 apenas dentro do raio r
mask = np.ones((rows, cols, 2), np.uint8)

for u in range(rows):
    for v in range(cols):
        # Translada a origem para o centro da imagem carregada
        dist_quadrado = (u - crow)**2 + (v - ccol)**2
        if dist_quadrado < r**2:
            mask[u, v] = 0  # H(u,v) = 0 se u^2 + v^2 < r^2

# 7. Aplicar a máscara no domínio da frequência (multiplicação ponto a ponto)
f_shift_filtrado = dft_shift * mask

# 8. Desfazer a centralização (Inverse fftshift)
f_filtrado = np.fft.ifftshift(f_shift_filtrado)

# 9. Aplicar a Transformada Inversa de Fourier (IDFT) para voltar ao domínio espacial
img_back = cv2.idft(f_filtrado)
img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])

# 10. Normalizar o resultado para exibição (escala de 0 a 255)
cv2.normalize(img_back, img_back, 0, 255, cv2.NORM_MINMAX)
img_final = np.uint8(img_back)

# 11. Exibir a imagem original e a imagem filtrada
cv2.imshow('Imagem Original', img_cinza)
cv2.imshow('Filtro Passa-Alta Realizado', img_final)

# Aguarda pressionar qualquer tecla para fechar as janelas
cv2.waitKey(0)
cv2.destroyAllWindows()
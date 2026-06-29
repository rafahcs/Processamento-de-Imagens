import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

def aplicar_filtro_media(imagem, tamanho_mascara):
    """Aplica um filtro de média manual em uma imagem em tons de cinza."""
    # Garante que a imagem está em formato float para evitar estouro de canal (overflow)
    img_float = imagem.astype(np.float32)

    # Recupera as dimensões da imagem
    altura, largura = img_float.shape

    # Cria uma imagem de saída preenchida com zeros
    img_filtrada = np.zeros_like(img_float)

    # Calcula o deslocamento (offset) a partir do centro da máscara
    offset = tamanho_mascara // 2

    # Cria uma borda (padding) ao redor da imagem para tratar os limites
    img_padded = np.pad(
        img_float, pad_width=offset, mode="constant", constant_values=0
    )

    # Define o divisor (número total de pixels na máscara)
    divisor = tamanho_mascara * tamanho_mascara

    # Varre a imagem pixel por pixel (desconsiderando o padding na iteração)
    for i in range(altura):
        for j in range(largura):
            # Extrai a região da imagem que corresponde à máscara
            regiao = img_padded[i : i + tamanho_mascara, j : j + tamanho_mascara]

            # Calcula a média dos pixels da região
            img_filtrada[i, j] = np.sum(regiao) / divisor

    # Converte de volta para o tipo de dado original de imagem (8-bit)
    return img_filtrada.astype(np.uint8)


# 1. Carregar a imagem em tons de cinza
# Substitua 'caminho_da_sua_imagem.jpg' pelo caminho correto no seu computador
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
    print(
        "Erro ao carregar a imagem. Verifique se o caminho do arquivo está correto."
    )
else:
    # 2. Aplicar o filtro para os tamanhos 3x3, 5x5 e 7x7
    img_3x3 = aplicar_filtro_media(img_cinza, 3)
    img_5x5 = aplicar_filtro_media(img_cinza, 5)
    img_7x7 = aplicar_filtro_media(img_cinza, 7)

    # 3. Exibir os resultados utilizando apenas o OpenCV
    cv2.imshow("Original (Cinza)", img_cinza)
    cv2.imshow("Filtro Media 3x3", img_3x3)
    cv2.imshow("Filtro Media 5x5", img_5x5)
    cv2.imshow("Filtro Media 7x7", img_7x7)

    # Aguarda o usuário pressionar qualquer tecla para fechar as janelas
    print("Pressione qualquer tecla nas janelas de imagem para fechar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
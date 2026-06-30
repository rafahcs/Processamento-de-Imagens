import cv2
import numpy as np

# 1. Carregar a imagem em tons de cinza
foto = "foto.png"
imagem = cv2.imread(foto)

# garante que a imagem seja lida em tons de cinza
def deixa_cinza(imagem):
    if imagem is None:
        return None
    if len(imagem.shape) < 3:
        return imagem

    cinzas = np.zeros((imagem.shape[0], imagem.shape[1]), dtype=np.uint8)
    for i in range(imagem.shape[0]):
        for j in range(imagem.shape[1]):
            cinzas[i][j] = int(imagem[i][j].sum() / 3)
    return cinzas
img = deixa_cinza(imagem)

# Verificar se a imagem foi carregada corretamente
if img is None:
    print("Erro ao carregar a imagem. Verifique o caminho.")
    exit()

# 2. Definir a máscara de Laplaciano do Gaussiano (LoG) 9x9 da imagem
mascara = np.array([
    [0,  1,  1,   2,   2,   2,  1,  1, 0],
    [1,  2,  4,   5,   5,   5,  4,  2, 1],
    [1,  4,  5,   3,   0,   3,  5,  4, 1],
    [2,  5,  3, -12, -24, -12,  3,  5, 2],
    [2,  5,  0, -24, -40, -24,  0,  5, 2],
    [2,  5,  3, -12, -24, -12,  3,  5, 2],
    [1,  4,  5,   3,   0,   3,  5,  4, 1],
    [1,  2,  4,   5,   5,   5,  4,  2, 1],
    [0,  1,  1,   2,   2,   2,  1,  1, 0]
], dtype=np.float32)

# 3. Processo de Convolução Manual
h, w = img.shape
m_h, m_w = mascara.shape

# Definir o tamanho do preenchimento (padding) nas bordas
pad_h, pad_w = m_h // 2, m_w // 2

# Criar uma imagem com padding de zeros nas bordas para tratar os limites
img_padded = np.pad(img, ((pad_h, pad_h), (pad_w, pad_w)), mode='constant', constant_values=0)

# Matriz para armazenar o resultado (usando float32 para evitar estouro de tipo uint8)
img_filtrada = np.zeros((h, w), dtype=np.float32)

# Loop pixel a pixel para aplicar a máscara
for i in range(h):
    for j in range(w):
        # Extrai a região da imagem (janela) correspondente ao tamanho da máscara
        regiao = img_padded[i:i+m_h, j:j+m_w]
        
        # Multiplicação elemento a elemento e soma dos resultados
        img_filtrada[i, j] = np.sum(regiao * mascara)

# Como o Laplaciano calcula bordas (derivadas segundas), ele gera valores negativos.
# Para visualização correta, tiramos o valor absoluto e limitamos o intervalo entre 0 e 255.
img_filtrada = np.abs(img_filtrada)
img_filtrada = np.clip(img_filtrada, 0, 255).astype(np.uint8)

# 4. Exibir os resultados utilizando apenas as funções permitidas do OpenCV
cv2.imshow('Imagem Original', imagem)
cv2.imshow('Filtro Laplaciano do Gaussiano (9x9)', img_filtrada)

# Aguarda pressionar qualquer tecla para fechar as janelas
cv2.waitKey(0)
cv2.destroyAllWindows()
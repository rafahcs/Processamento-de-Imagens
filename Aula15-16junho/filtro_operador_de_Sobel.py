import cv2
import numpy as np

foto = "foto.png"
imagem = cv2.imread(foto)

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


def aplicar_filtro_sobel(imagem):
    if isinstance(imagem, str):
        imagem = cv2.imread(imagem)

    if imagem is None:
        print("Erro ao carregar a imagem. Verifique o caminho.")
        return

    imagem_cinza = deixa_cinza(imagem)

    # máscaras de Sobel
    Zh = np.array([[-1, -2, -1],
                   [ 0,  0,  0],
                   [ 1,  2,  1]])

    Zv = np.array([[-1,  0,  1],
                   [-2,  0,  2],
                   [-1,  0,  1]])

    linhas, colunas = imagem_cinza.shape

    # imagem com bordas preenchidas com zeros
    imagem_pad = np.pad(imagem_cinza, ((1, 1), (1, 1)), mode='constant', constant_values=0)

    # gradientes horizontais e verticais
    Gx = np.zeros((linhas, colunas), dtype=np.float32)
    Gy = np.zeros((linhas, colunas), dtype=np.float32)

    # convolução
    print("Aplicando o filtro de Sobel... (isso pode levar alguns segundos dependendo do tamanho da imagem)")
    for i in range(linhas):
        for j in range(colunas):
            # Extrai a vizinhança 3x3 ao redor do pixel atual
            regiao = imagem_pad[i:i+3, j:j+3]
            
            # Multiplicação elemento a elemento e soma
            Gx[i, j] = np.sum(regiao * Zh)
            Gy[i, j] = np.sum(regiao * Zv)

    # Calcula a magnitude do gradiente 
    magnitude = np.sqrt(Gx**2 + Gy**2)

    # Normalização
    magnitude = np.clip(magnitude, 0, 255).astype(np.uint8)
    
    Gx_vis = np.clip(np.abs(Gx), 0, 255).astype(np.uint8)
    Gy_vis = np.clip(np.abs(Gy), 0, 255).astype(np.uint8)

    # imagens
    cv2.imshow("Imagem Original", imagem if len(imagem.shape) == 3 else imagem_cinza)
    cv2.imshow("Sobel Horizontal (Zh)", Gx_vis)
    cv2.imshow("Sobel Vertical (Zv)", Gy_vis)
    cv2.imshow("Sobel Magnitude (Bordas Finais)", magnitude)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    aplicar_filtro_sobel(imagem)
import cv2
import matplotlib.pyplot as plt


def carregar_imagem(caminho):
    imagem = cv2.imread(caminho)
    if imagem is None:
        raise FileNotFoundError(f"Não foi possível carregar a imagem: {caminho}")
    return imagem


def converter_para_cinza(imagem):
    return cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)


def mostrar_imagem(imagem, titulo):
    plt.figure(figsize=(6, 6))
    plt.imshow(imagem, cmap="gray")
    plt.title(titulo)
    plt.axis("off")
    plt.show()


def mostrar_histograma(imagem, titulo):
    hist = cv2.calcHist([imagem], [0], None, [256], [0, 256]).flatten()

    plt.figure(figsize=(8, 4))
    plt.title(titulo)
    plt.xlabel("Tom de cinza")
    plt.ylabel("Quantidade de pixels")
    plt.bar(range(256), hist, color="gray")
    plt.xlim([0, 255])
    plt.tight_layout()
    plt.show()


def main():
    imagem_colorida = carregar_imagem("foto.jpg")
    imagem_cinza = converter_para_cinza(imagem_colorida)
    imagem_equalizada = cv2.equalizeHist(imagem_cinza)

    mostrar_imagem(imagem_cinza, "Imagem em tons de cinza")
    mostrar_imagem(imagem_equalizada, "Imagem equalizada")
    mostrar_histograma(imagem_cinza, "Histograma da imagem em tons de cinza")
    mostrar_histograma(imagem_equalizada, "Histograma da imagem equalizada")

    


if __name__ == "__main__":
    main()

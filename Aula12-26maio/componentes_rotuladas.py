import cv2
import numpy as np

class DisjointSet:
    """Estrutura Union-Find para gerenciar as equivalências de rótulos."""
    def __init__(self):
        self.parent = {}
    
    def find(self, i):
        if i not in self.parent:
            self.parent[i] = i
            return i
        if self.parent[i] == i:
            return i
        # Compressão de caminho (Path Compression) para eficiência O(1)
        self.parent[i] = self.find(self.parent[i])
        return self.parent[i]
    
    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)
        if root_i != root_j:
            # Aponta o maior rótulo para o menor para manter consistência
            if root_i < root_j:
                self.parent[root_j] = root_i
            else:
                self.parent[root_i] = root_j

def rotular_componentes_conectadas(imagem_binaria):
    """Implementação do algoritmo de duas passadas para 8-conectividade."""
    altura, largura = imagem_binaria.shape
    rotulos = np.zeros((altura, largura), dtype=np.int32)
    ds = DisjointSet()
    proximo_rotulo = 1
    
    # --- PRIMEIRA PASSADA: Varredura e Rotulação Inicial ---
    for y in range(altura):
        for x in range(grid_width := largura):
            if imagem_binaria[y, x] == 255:  # Pixel de primeiro plano (objeto)
                
                # Coleta os vizinhos da vizinhança-8 que já foram processados
                vizinhos = []
                if x > 0 and rotulos[y, x-1] > 0:                 # Esquerda
                    vizinhos.append(rotulos[y, x-1])
                if y > 0:
                    if x > 0 and rotulos[y-1, x-1] > 0:           # Cima-Esquerda
                        vizinhos.append(rotulos[y-1, x-1])
                    if rotulos[y-1, x] > 0:                       # Cima
                        vizinhos.append(rotulos[y-1, x])
                    if x < largura - 1 and rotulos[y-1, x+1] > 0: # Cima-Direita
                        vizinhos.append(rotulos[y-1, x+1])
                
                if not vizinhos:
                    # Nenhum vizinho rotulado: cria um novo rótulo
                    rotulos[y, x] = proximo_rotulo
                    ds.find(proximo_rotulo)
                    proximo_rotulo += 1
                else:
                    # Vizinhos encontrados: rotula com o menor deles e registra equivalências
                    menor_rotulo = min(vizinhos)
                    rotulos[y, x] = menor_rotulo
                    for v in vizinhos:
                        ds.union(menor_rotulo, v)
                        
    # --- SEGUNDA PASSADA: Resolução de Equivalências ---
    for y in range(altura):
        for x in range(largura):
            if rotulos[y, x] > 0:
                rotulos[y, x] = ds.find(rotulos[y, x])
                
    # --- NORMALIZAÇÃO: Torna os rótulos sequenciais (1, 2, 3...) ---
    rotulos_unicos = np.unique(rotulos)
    rotulos_unicos = rotulos_unicos[rotulos_unicos > 0]
    mapa_rotulos = {antigo: novo for novo, antigo in enumerate(rotulos_unicos, start=1)}
    
    rotulos_finais = np.zeros_like(rotulos)
    for antigo, novo in mapa_rotulos.items():
        rotulos_finais[rotulos == antigo] = novo
        
    return rotulos_finais, len(rotulos_unicos)

# 1. Carrega a imagem fornecida em tons de cinza
imagem_original = cv2.imread('components.png', cv2.IMREAD_GRAYSCALE)

if imagem_original is None:
    print("Erro: Não foi possível carregar a imagem. Verifique o caminho.")
else:
    # 2. Pré-processamento: Binarização (Limiarização) da imagem
    # Pixels acima de 127 viram 255 (branco), o restante vira 0 (preto)
    _, imagem_bin = cv2.threshold(imagem_original, 127, 255, cv2.THRESH_BINARY)
    
    # Inverte caso o fundo seja claro, pois o algoritmo busca objetos brancos (255)
    if np.sum(imagem_bin == 255) > np.sum(imagem_bin == 0):
        imagem_bin = cv2.bitwise_not(imagem_bin)

    # 3. Executa o algoritmo de rotulação implementado
    matriz_rotulos, total_componentes = rotular_componentes_conectadas(imagem_bin)
    print(f"Número de componentes conectadas encontradas: {total_componentes}")

    # 4. Criação de uma imagem colorida (RGB) para visualização dos resultados
    altura, largura = imagem_bin.shape
    imagem_colorida = np.zeros((altura, largura, 3), dtype=np.uint8)

    # Gera cores aleatórias fixas para cada componente
    np.random.seed(42)  # Semente fixa para manter as mesmas cores a cada execução
    cores = {0: [0, 0, 0]}  # Fundo permanece preto
    for i in range(1, total_componentes + 1):
        cores[i] = list(np.random.randint(50, 256, size=3, dtype=int))

    # Mapeia os rótulos para as cores geradas
    for y in range(altura):
        for x in range(largura):
            imagem_colorida[y, x] = cores[matriz_rotulos[y, x]]

    # 5. Exibe os resultados na tela usando apenas o OpenCV
    cv2.imshow("1. Imagem Original Binaria", imagem_bin)
    cv2.imshow("2. Componentes Rotuladas e Coloridas", imagem_colorida)
    
    print("Pressione qualquer tecla com as janelas abertas para fechar...")
    cv2.waitKey(0)
    cv2.destroyAllWindows()
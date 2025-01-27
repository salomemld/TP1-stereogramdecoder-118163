import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import pyvista as pv

def calcular_deslocamento_ncc(imagem):
    """
    Calcula o deslocamento periódico usando NCC e ignora deslocamentos iniciais irrelevantes.
    Retorna o deslocamento ideal e exibe um gráfico para análise visual.
    """
    altura, largura = imagem.shape
    max_deslocamento = largura // 4  # Limita o deslocamento a 1/4 da largura da imagem para otimizar o cálculo
    min_deslocamento = 10  # Ignora deslocamentos menores que 10 px para evitar resultados irrelevantes
    correlacoes = []

    # Cálculo do NCC para cada deslocamento possível
    for deslocamento in range(1, max_deslocamento):
        # Criação de uma versão deslocada da imagem
        imagem_deslocada = np.roll(imagem, deslocamento, axis=1)
        # Cálculo da correlação cruzada normalizada
        ncc = np.sum((imagem - np.mean(imagem)) * (imagem_deslocada - np.mean(imagem_deslocada))) / (
            np.std(imagem) * np.std(imagem_deslocada) * altura * largura
        )
        correlacoes.append(ncc)

    # Ignorar deslocamentos iniciais irrelevantes
    correlacoes = np.array(correlacoes[min_deslocamento - 1:])

    # Identificação do deslocamento com a maior correlação
    deslocamento_ideal = np.argmax(correlacoes) + min_deslocamento

    # Exibição do gráfico das correlações
    plt.figure()
    plt.plot(range(min_deslocamento, max_deslocamento), correlacoes, color="blue", label="Correlação NCC")
    plt.axvline(deslocamento_ideal, color="red", linestyle="--", label=f"Ideal: {deslocamento_ideal}px")
    plt.xlabel("Deslocamento (px)")
    plt.ylabel("Correlação NCC")
    plt.title("Correlação Cruzada Normalizada")
    plt.legend()
    plt.show()

    return deslocamento_ideal

def normalizar_imagem(imagem):
    """Normaliza uma imagem para o intervalo [0, 1]. Importante para cálculos aritméticos consistentes."""
    return imagem.astype(np.float32) / 255.0

def calcular_sobreposicao(imagem, imagem_deslocada):
    """
    Calcula a sobreposição entre a imagem original e a imagem deslocada.
    Destaca objetos em preto.
    """
    # Combinação das imagens, utilizando 'pesos' específicos para destacar diferenças
    sobreposta = cv2.addWeighted(imagem, 0.7, imagem_deslocada, 0.3, 0)
    objeto_em_preto = np.minimum(imagem, imagem_deslocada)
    return sobreposta - objeto_em_preto

def gerar_mapa_de_disparidade(imagem, deslocamento):
    """
    Gera um mapa de disparidade baseado no deslocamento calculado.
    O mapa indica a diferença de intensidade entre pixels deslocados.
    """
    altura, largura = imagem.shape
    mapa_de_disparidade = np.zeros_like(imagem, dtype=np.uint8)

    for y in range(altura):
        for x in range(largura - deslocamento):  # Evita acesso fora dos limites
            mapa_de_disparidade[y, x] = abs(int(imagem[y, x]) - int(imagem[y, x + deslocamento]))

    return mapa_de_disparidade

def exibir_mapa_de_disparidade(mapa_de_disparidade):
    """
    Exibe o mapa de disparidade gerado.
    """
    plt.figure()
    plt.imshow(mapa_de_disparidade, cmap="gray")  # Usa um colormap 'gray' para destacar disparidades
    plt.colorbar(label="Disparidade")
    plt.title("Mapa de Disparidade")
    plt.show()

def visualizar_sobreposicao_interativa(imagem, deslocamento_inicial):
    """
    Cria uma interface interativa para visualizar a sobreposição da imagem original com uma versão deslocada.
    """
    # Configuração da figura para a interface
    fig, ax = plt.subplots()
    plt.subplots_adjust(bottom=0.25)

    # Normalização da imagem
    imagem_normalizada = normalizar_imagem(imagem)

    # Configuração da sobreposição inicial
    imagem_deslocada = np.roll(imagem, deslocamento_inicial, axis=1)
    imagem_deslocada_normalizada = normalizar_imagem(imagem_deslocada)
    sobreposta = calcular_sobreposicao(imagem_normalizada, imagem_deslocada_normalizada)
    img_plot = ax.imshow(sobreposta, cmap="gray")
    ax.set_title("Visualização Interativa de Sobreposição")

    # Configuração do slider
    ax_slider = plt.axes([0.2, 0.1, 0.65, 0.03])
    slider = Slider(ax_slider, "Deslocamento", 1, imagem.shape[1] // 4, valinit=deslocamento_inicial, valstep=1)

    # Atualização da sobreposição quando o slider for movido
    def update(val):
        deslocamento = int(slider.val)
        imagem_deslocada = np.roll(imagem, deslocamento, axis=1)
        imagem_deslocada_normalizada = normalizar_imagem(imagem_deslocada)
        sobreposta = calcular_sobreposicao(imagem_normalizada, imagem_deslocada_normalizada)
        img_plot.set_data(sobreposta)
        fig.canvas.draw_idle()

    slider.on_changed(update)
    plt.show()

def gerar_nuvem_de_pontos(mapa_profundidade, limiar_inferior=10, limiar_superior=255):
    """
    Gera uma núvem de pontos filtrando os pixels com profundidade dentro de um intervalo.
    """
    altura, largura = mapa_profundidade.shape
    x, y = np.meshgrid(np.arange(0, largura), np.arange(0, altura))
    
    # Filtração dos pontos dentro do intervalo de profundidade
    mask = (mapa_profundidade >= limiar_inferior) & (mapa_profundidade <= limiar_superior)
    x = x[mask]
    y = y[mask]
    z = mapa_profundidade[mask]

    return x, y, z

def exibir_nuvem_de_pontos_pyvista(x, y, z):
    """
    Exibe a nuvem de pontos em 3D usando PyVista.
    """
    # Conversão para float para evitar avisos
    x = x.astype(np.float32)
    y = y.astype(np.float32)
    z = z.astype(np.float32)
    
    # Criação da nuvem de pontos
    pontos = np.column_stack((x, y, z))
    cloud = pv.PolyData(pontos)
    cloud["Profundidade"] = z
    
    # Configuração do visualizador
    plotter = pv.Plotter()
    plotter.add_mesh(cloud, scalars="Profundidade", cmap="viridis", point_size=2, render_points_as_spheres=True)
    plotter.add_axes()
    plotter.show_grid()
    plotter.show()

def carregar_imagem():
    """
    Solicita ao usuário o caminho da imagem e faz validações básicas.
    """
    while True:
        try:
            caminho_imagem = input("Insira o caminho completo para a imagem (ou digite 'sair' para encerrar): ")
            if caminho_imagem.lower() == 'sair':
                print("Programa encerrado.")
                exit(0)
            if not caminho_imagem.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
                print("O arquivo selecionado não é uma imagem válida. Por favor, insira uma imagem com extensão suportada.")
                continue
            imagem = cv2.imread(caminho_imagem, cv2.IMREAD_GRAYSCALE)
            if imagem is None:
                raise FileNotFoundError(f"Erro: A imagem no caminho '{caminho_imagem}' não foi encontrada ou não é válida.")
            return imagem  # Retorna a imagem se o carregamento foi bem-sucedido
        except FileNotFoundError as e:
            print(e)
            print("Por favor, tente novamente.")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")
            exit(1)

# Carregamento da imagem
imagem = carregar_imagem()

# Cálculo do deslocamento com NCC
deslocamento_ncc = calcular_deslocamento_ncc(imagem)
print(f"Deslocamento calculado com NCC: {deslocamento_ncc}px")

# Criação e exibição do mapa de disparidade
mapa_de_disparidade = gerar_mapa_de_disparidade(imagem, deslocamento_ncc)
exibir_mapa_de_disparidade(mapa_de_disparidade)

# Visualização da sobreposição interativa
visualizar_sobreposicao_interativa(imagem, deslocamento_ncc)

# Criação do mapa de profundidade (com limiar para remover o fundo)
limiar_disparidade = 50  # Ajustar se necessário
mapa_profundidade = gerar_mapa_de_disparidade(imagem, deslocamento_ncc)
x, y, z = gerar_nuvem_de_pontos(mapa_profundidade, limiar_inferior=limiar_disparidade)

# Exibição da núvem de pontos com PyVista
exibir_nuvem_de_pontos_pyvista(x, y, z)

print("Processamento concluído com sucesso!")
# TP1-StereogramDecoder-118163

Projeto de decodificação e codificação de estereogramas, criando imagens binárias 2D e reconstruções 3D.

## 🎯 **Objetivo**
Um estereograma é uma ilusão óptica que cria uma imagem tridimensional a partir de uma imagem bidimensional. Quando visualizado corretamente, o cérebro interpreta os padrões e cores na imagem para perceber profundidade e forma, revelando objetos 3D ocultos.

O objetivo deste projeto é:
- **Decodificar estereogramas:**
  - Extrair informações de profundidade e gerar mapas de disparidade.
  - Criar reconstruções tridimensionais (3D) das formas ocultas nos estereogramas.
- **Visualizar informações em 3D:**
  - Exibir nuvens de pontos 3D geradas a partir dos mapas de disparidade.

---

## 🚀 **Funcionalidades**
1. **Decodificação de estereogramas:**
   - Calcular deslocamentos de disparidade e gerar mapas de profundidade 2D a partir de imagens estereográficas.
   - Normalizar e processar imagens para análise de disparidades.
   
2. **Reconstrução 3D:**
   - Gerar nuvens de pontos 3D para visualizar formas ocultas nos estereogramas.

3. **Visualização interativa:**
   - Explorar imagens deslocadas e sobreposições de profundidade com controles interativos.
   - Exibir nuvens de pontos 3D com o PyVista para melhor análise.

---

## 📂 **Estrutura do Projeto**
- **`main.py`:** Arquivo principal contendo todas as funções para processamento e visualização.
- **`requirements.txt`:** Lista de dependências necessárias para o funcionamento do programa.
- **`Imagens/`:** Pasta com exemplos de imagens para teste.

---

## 🛠️ **Como Executar**
1. Clone o repositório:
   ```bash
   git clone <(https://github.com/salomemld/TP1-StereogramDecoder-118163.git)>
   cd TP1-StereogramDecoder-118163

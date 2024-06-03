import networkx as nx
import matplotlib.pyplot as plt


# Função para ler arestas de um arquivo
def ler_arestas_de_arquivo(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        edges = []
        for line in file:
            parts = line.strip().split()
            if len(parts) == 3:
                edges.append((int(parts[0]), int(parts[1]), int(parts[2])))
    return edges


# Função para desenhar o grafo com vértices destacados
def desenhar_grafo_com_vertices_destacados(G, pos, vertices_destacados):
    # Adicionar vértices ao grafo com cores diferentes
    node_colors = []
    for node in G.nodes():
        if node in vertices_destacados:
            node_colors.append('red')
        else:
            node_colors.append('skyblue')

    # Desenhar o grafo
    plt.figure(figsize=(15, 15))
    nx.draw(G, pos, with_labels=True, node_size=500, node_color=node_colors, font_size=10, font_weight='bold',
            edge_color='gray')

    # Desenhar as arestas com os pesos
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=8)

    # Mostrar a imagem do grafo
    plt.title("Grafo com Pesos nas Arestas")
    plt.show()


# Ler as arestas do arquivo
edges = ler_arestas_de_arquivo('instances/pmed1n.txt')

# Criar o grafo
G = nx.Graph()

# Adicionar arestas ao grafo
for edge in edges:
    G.add_edge(edge[0], edge[1], weight=edge[2])

# Definir a posição dos nós
pos = nx.spring_layout(G)

# Lista de vértices a serem destacados
vertices_destacados = [1, 17, 37, 49, 60, 70, 74, 82, 85, 87] # Exemplos de vértices a serem destacados em vermelho

# Desenhar o grafo com os vértices destacados
desenhar_grafo_com_vertices_destacados(G, pos, vertices_destacados)

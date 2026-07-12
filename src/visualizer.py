import networkx as nx
import matplotlib.pyplot as plt

def draw_attribution_graph(G: nx.DiGraph, target_drone: str, emitter: str, candidates: list, title: str = "Red de Comunicacion UAS"):
    """
    Genera y muestra la visualización topológica de la red UAS resaltando
    los roles de los nodos y el emisor primario identificado.
    """
    pos = nx.spring_layout(G, seed=42)
    plt.figure(figsize=(10, 6))

    # Definir paleta de colores según la función del nodo
    node_colors = []
    for node in G.nodes():
        if node == emitter:
            node_colors.append("#E63946")  # Rojo: Emisor Primario Identificado
        elif node == target_drone:
            node_colors.append("#1D3557")  # Azul Oscuro: Dron Interceptado
        elif node in candidates:
            node_colors.append("#F4A261")  # Naranja: Candidato secundario / Señuelo
        else:
            node_colors.append("#A8DADC")  # Azul Claro / Gris: Repetidores / Relays

    # Dibujar nodos y aristas
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2000, alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", font_color="black")
    nx.draw_networkx_edges(G, pos, edgelist=G.edges(), edge_color="#457B9D", arrowsize=20, width=2)

    plt.title(title, fontsize=14, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()
    return plt

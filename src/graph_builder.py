import networkx as nx
import random

def build_star_network():
    """Escenario A: Control directo punto a punto (Operador -> Dron)."""
    G = nx.DiGraph()
    G.add_edge("Operador_C1", "Dron_D1")
    return G
    
def build_relay_chain_network():
    """Escenario B: Cadena de repetidores (Operador -> Relay 1 -> Relay 2 -> Dron)."""
    G = nx.DiGraph()
    G.add_edge("Operador_C1", "Relay_R1")
    G.add_edge("Relay_R1", "Relay_R2")
    G.add_edge("Relay_R2", "Dron_D1")
    return G

def build_complex_mesh_network():
    """Escenario C: Red acíclica compleja con múltiples repetidores e interferencia."""
    G = nx.DiGraph()
    # Camino 1 principal del Operador real
    G.add_edge("Operador_Real_C1", "Relay_R1")
    G.add_edge("Relay_R1", "Relay_R2")
    G.add_edge("Relay_R2", "Dron_D1")
    
    # Camino 2 señuelo / alternativo más largo
    G.add_edge("Operador_Falso_C2", "Relay_R3")
    G.add_edge("Relay_R3", "Relay_R4")
    G.add_edge("Relay_R4", "Relay_R2") # Converge al mismo relay
    
    return G

def build_disconnected_network():
    """Caso Borde: Red desconectada o datos corruptos."""
    G = nx.DiGraph()
    G.add_node("Operador_C1")
    G.add_node("Dron_Aislado_D1")  # Sin aristas que los conecten
    return G

def build_layered_random_network(num_layers: int, nodes_per_layer: int, seed: int = 42):
    """
    Genera una red por capas de tamaño variable: un unico nodo raiz (Operador),
    capas intermedias de repetidores con conexiones aleatorias hacia la capa
    anterior, y un dron objetivo final. Usada para validar empiricamente la
    complejidad O(|V| + |E|) del algoritmo de atribucion sobre grafos de
    tamano creciente.
    """
    rng = random.Random(seed)
    G = nx.DiGraph()
    root = "Root_Operador"
    G.add_node(root)
    prev_layer = [root]

    for layer_idx in range(num_layers):
        current_layer = [f"L{layer_idx}_R{i}" for i in range(nodes_per_layer)]
        for node in current_layer:
            k = min(len(prev_layer), rng.randint(1, 2))
            parents = rng.sample(prev_layer, k=k)
            for p in parents:
                G.add_edge(p, node)
        prev_layer = current_layer

    target = "Dron_Target"
    for node in prev_layer:
        G.add_edge(node, target)

    return G, target

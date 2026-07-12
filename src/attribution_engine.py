import networkx as nx

def identify_primary_emitter(G: nx.DiGraph, target_drone: str):
    """
    Identifica el nodo operador origen (emisor primario) de un dron interceptado.
    
    Implementa el algoritmo de trazabilidad inversa sobre el Grafo Transpuesto G^T:
    1. Transpone el grafo G -> G^T.
    2. Encuentra los ancestros alcanzables desde target_drone mediante BFS.
    3. Filtra nodos con grado de entrada d^-(v) == 0 en el grafo original G.
    4. Resuelve ambigüedades mediante camino mínimo d(v, target_drone).
    
    Retorna:
        tuple: (nodo_origen_optimo, distancia_camino, lista_candidatos)
    """
    if target_drone not in G:
        raise ValueError(f"El dron {target_drone} no pertenece al grafo capturado.")

    # Paso 1: Obtener el Grafo Transpuesto G^T
    G_transposed = G.reverse(copy=True)

    # Paso 2: Calcular distancias inversas desde target_drone en G^T
    # Nota: d_G^T(target, v) == d_G(v, target)
    try:
        distances_from_target = nx.single_source_shortest_path_length(G_transposed, target_drone)
    except nx.NetworkXError:
        distances_from_target = {}

    # Paso 3: Filtrar ancestros alcanzables que tengan d_G^-(v) == 0 en el grafo original G
    candidatos = [
        node for node in distances_from_target
        if G.in_degree(node) == 0 and node != target_drone
    ]

    # Manejo de Caso Borde: Red desconectada o sin fuentes alcanzables
    if not candidatos:
        return None, float('inf'), []

    # Paso 4: Selección del origen óptimo (candidato con menor distancia hacia el dron)
    optimum_candidate = min(candidatos, key=lambda c: distances_from_target[c])
    shortest_distance = distances_from_target[optimum_candidate]

    return optimum_candidate, shortest_distance, candidatos

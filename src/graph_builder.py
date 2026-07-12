import networkx as nx

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

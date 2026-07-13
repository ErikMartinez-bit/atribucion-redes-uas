import pytest
from src.graph_builder import (
    build_star_network,
    build_relay_chain_network,
    build_complex_mesh_network,
    build_disconnected_network
)
from src.attribution_engine import identify_primary_emitter

def test_attribution_star_network():
    """Valida la detección directa en escenario punto a punto."""
    G = build_star_network()
    emitter, dist, candidates = identify_primary_emitter(G, "Dron_D1")
    assert emitter == "Operador_C1"
    assert dist == 1

def test_attribution_relay_chain():
    """Valida que los repetidores intermedios d^-(r) >= 1 sean descartados."""
    G = build_relay_chain_network()
    emitter, dist, candidates = identify_primary_emitter(G, "Dron_D1")
    assert emitter == "Operador_C1"
    assert dist == 3
    assert "Relay_R1" not in candidates
    assert "Relay_R2" not in candidates

def test_attribution_complex_mesh_tiebreak():
    """Valida el desempate por distancia mínima cuando existen múltiples candidatos."""
    G = build_complex_mesh_network()
    emitter, dist, candidates = identify_primary_emitter(G, "Dron_D1")
    assert emitter == "Operador_Real_C1"
    assert dist == 3
    assert "Operador_Falso_C2" in candidates
    assert len(candidates) == 2

def test_attribution_disconnected_network():
    """Valida el caso borde C_candidatos = vacio en red desconectada."""
    G = build_disconnected_network()
    emitter, dist, candidates = identify_primary_emitter(G, "Dron_Aislado_D1")
    assert emitter is None
    assert dist == float('inf')
    assert len(candidates) == 0

import networkx as nx
from parameters import NUM_CS, NUM_SOURCES, NUM_DESTINATIONS

def build_test_graph():
    G = nx.Graph()
    sources = [f"S{i}" for i in range(1, NUM_SOURCES + 1)]
    css = [f"CS{i}" for i in range(1, NUM_CS + 1)]
    dests = [f"D{i}" for i in range(1, NUM_DESTINATIONS + 1)]
    for node in sources + css + dests:
        G.add_node(node)
    
    edges = [
        ("S1", "CS1", 5), ("CS1", "CS2", 10), ("CS2", "CS4", 8), ("CS4", "CS5", 12), ("CS5", "D1", 6),
        ("S2", "CS1", 7), ("CS1", "CS3", 9), ("CS3", "CS4", 11), ("CS4", "CS6", 10), ("CS6", "D2", 5),
        ("S3", "CS2", 6), ("CS2", "CS4", 8), ("CS4", "CS7", 13), ("CS7", "D3", 7),
        ("S4", "CS3", 8), ("CS3", "CS5", 12), ("CS5", "CS8", 9), ("CS8", "D4", 6),
        ("S5", "CS4", 10), ("CS4", "CS6", 10), ("CS6", "D5", 8),
        ("S6", "CS5", 11), ("CS5", "CS7", 14), ("CS7", "D6", 5),
        ("CS1", "CS4", 15), ("CS2", "CS5", 14), ("CS3", "CS6", 16), ("CS6", "CS8", 12)
    ]
    for u, v, w in edges:
        G.add_edge(u, v, weight=w)
    return G

if __name__ == "__main__":
    G = build_test_graph()
    print(f"Graph ready → {len(G.nodes())} nodes, {len(G.edges())} edges")

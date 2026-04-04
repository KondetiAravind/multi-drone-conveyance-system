import networkx as nx
from graph_builder import build_test_graph
from parameters import OD_PAIRS

def compute_all_shortest_paths():
    G = build_test_graph()
    paths = {}
    for s, d in OD_PAIRS:
        path = nx.shortest_path(G, s, d, weight='weight')
        travel_time = nx.shortest_path_length(G, s, d, weight='weight')
        cs_visited = [node for node in path if 'CS' in node]
        paths[(s, d)] = {
            'path': path,
            'travel_time': travel_time,
            'cs_visited': cs_visited
        }
    return paths, G

if __name__ == "__main__":
    paths, G = compute_all_shortest_paths()
    print("Shortest-time paths computed for all OD pairs.")

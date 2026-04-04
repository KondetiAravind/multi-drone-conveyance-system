from graph_builder import build_test_graph
from parameters import TOTAL_LAMBDA, MU

G = build_test_graph()
print("=== PHASE 1 SUCCESS ===")
print(f"λ = {TOTAL_LAMBDA} | μ = {MU}")
print(f"Graph: {len(G.nodes())} nodes | {len(G.edges())} edges")
print("Web UI ready → run: streamlit run app.py")

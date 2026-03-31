import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import random
import simpy
import numpy as np
import zipfile
import io
from collections import defaultdict

st.set_page_config(page_title="Multi-Drone Conveyance System", layout="wide", initial_sidebar_state="expanded")

st.title("🛸 Multi-Drone Conveyance System Simulator")
st.subheader("Assessment of Waiting Time with Time-Based (Shortest-Time) Path Selection")

# Session state - START WITH EMPTY GRAPH
if 'G' not in st.session_state:
    st.session_state.G = nx.Graph()

if 'od_pairs' not in st.session_state:
    st.session_state.od_pairs = [(f"S{i}", f"D{i}") for i in range(1,7)]

# Sidebar - Node Addition & Controls
st.sidebar.header("Add Nodes")
col_add = st.sidebar.columns(3)
with col_add[0]:
    if st.button("➕ Add Source", use_container_width=True):
        next_s = max((int(n[1:]) for n in st.session_state.G.nodes() if n.startswith("S")), default=0) + 1
        st.session_state.G.add_node(f"S{next_s}")
        st.rerun()
with col_add[1]:
    if st.button("➕ Add CS", use_container_width=True):
        next_cs = max((int(n[2:]) for n in st.session_state.G.nodes() if n.startswith("CS")), default=0) + 1
        st.session_state.G.add_node(f"CS{next_cs}")
        st.rerun()
with col_add[2]:
    if st.button("➕ Add Destination", use_container_width=True):
        next_d = max((int(n[1:]) for n in st.session_state.G.nodes() if n.startswith("D")), default=0) + 1
        st.session_state.G.add_node(f"D{next_d}")
        st.rerun()

st.sidebar.header("Create Path")
u_list = sorted(list(st.session_state.G.nodes()))
v_list = sorted(list(st.session_state.G.nodes()))
if u_list:
    u_sel = st.sidebar.selectbox("From Node", u_list, key="from_sel")
    v_sel = st.sidebar.selectbox("To Node", [n for n in v_list if n != u_sel], key="to_sel")
    weight = st.sidebar.number_input("Travel Time (min)", min_value=1.0, value=10.0, key="w_sel")
    if st.sidebar.button("➤ Add Arrowed Connection", type="primary", use_container_width=True):
        if u_sel and v_sel:
            st.session_state.G.add_edge(u_sel, v_sel, weight=weight)
            st.sidebar.success(f"Added {u_sel} → {v_sel} ({weight} min)")
            st.rerun()

st.sidebar.header("Network Controls")
if st.sidebar.button("🔄 Load Minimal Default Network", use_container_width=True):
    st.session_state.G = nx.Graph()
    for i in range(1,7): st.session_state.G.add_node(f"S{i}")
    for i in range(1,9): st.session_state.G.add_node(f"CS{i}")
    for i in range(1,7): st.session_state.G.add_node(f"D{i}")
    default_edges = [
        ("S1","CS1",5),("CS1","CS2",10),("CS2","CS4",8),("CS4","CS5",12),("CS5","D1",6),
        ("S2","CS1",7),("CS1","CS3",9),("CS3","CS4",11),("CS4","CS6",10),("CS6","D2",5),
        ("S3","CS2",6),("CS2","CS4",8),("CS4","CS7",13),("CS7","D3",7),
        ("S4","CS3",8),("CS3","CS5",12),("CS5","CS8",9),("CS8","D4",6),
        ("S5","CS4",10),("CS4","CS6",10),("CS6","D5",8),
        ("S6","CS5",11),("CS5","CS7",14),("CS7","D6",5)
    ]
    for u,v,w in default_edges:
        st.session_state.G.add_edge(u, v, weight=w)
    st.rerun()

if st.sidebar.button("🗑️ Clear All (Empty Network)", use_container_width=True):
    st.session_state.G = nx.Graph()
    st.rerun()

# Final layered layout with alternating \ / stagger (no straight lines)
def get_layered_pos(G):
    pos = {}
    sources = sorted([n for n in G.nodes() if n.startswith('S')])
    css = sorted([n for n in G.nodes() if n.startswith('CS')])
    dests = sorted([n for n in G.nodes() if n.startswith('D')])
    
    random.seed(42)
    np.random.seed(42)
    
    # Sources - Left column with \ / alternating stagger
    for i, node in enumerate(sources):
        base_x = 0.12
        base_y = 0.95 - i * (0.85 / max(len(sources)-1, 1))
        offset_x = 0.06 if i % 2 == 0 else -0.06   # alternate left/right
        pos[node] = (base_x + offset_x, base_y)
    
    # Charging Stations - Middle with strong alternating stagger
    for i, node in enumerate(css):
        base_x = 0.50
        base_y = 0.95 - i * (0.85 / max(len(css)-1, 1))
        offset_x = 0.12 if i % 2 == 0 else -0.12   # strong \ / pattern
        pos[node] = (base_x + offset_x, base_y)
    
    # Destinations - Right column with \ / alternating stagger
    for i, node in enumerate(dests):
        base_x = 0.88
        base_y = 0.95 - i * (0.85 / max(len(dests)-1, 1))
        offset_x = 0.06 if i % 2 == 0 else -0.06
        pos[node] = (base_x + offset_x, base_y)
    
    return pos

# Main Visualization
st.header("Interactive Network")
fig_net, ax_net = plt.subplots(figsize=(18, 12))
G = st.session_state.G

if len(G.nodes()) == 0:
    ax_net.text(0.5, 0.5, "Network is empty.\nUse sidebar to add Sources, CS, Destinations\nand create paths.", 
                ha='center', va='center', fontsize=16, color='gray')
else:
    pos = get_layered_pos(G)
    
    node_colors = []
    for node in G.nodes():
        if node.startswith('S'): node_colors.append('#90EE90')
        elif node.startswith('CS'): node_colors.append('#87CEEB')
        elif node.startswith('D'): node_colors.append('#FF9999')
        else: node_colors.append('#D3D3D3')
    
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=2600, ax=ax_net)
    nx.draw_networkx_labels(G, pos, font_size=11, font_weight='bold', ax=ax_net)
    nx.draw_networkx_edges(G, pos, edge_color='#333333', width=2.8, 
                           connectionstyle="arc3,rad=0.18", ax=ax_net)
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u,v): f"{G[u][v]['weight']}" for u,v in G.edges()},
                                 font_size=9, font_color='darkblue', ax=ax_net)
    
    ax_net.set_title("Network Visualization (Sources LEFT | CS MIDDLE | Destinations RIGHT)")
    ax_net.set_xlim(-0.05, 1.05)
    ax_net.set_ylim(-0.05, 1.05)
    ax_net.axis('off')

st.pyplot(fig_net, use_container_width=True)

# Analysis Section
st.header("Run Analysis")
lambda_total = st.number_input("Total Drone Arrival Rate λ (drones/min)", value=5.0, step=0.1)
mu = st.number_input("Charging Service Rate μ (per station)", value=6.0, step=0.1)

st.subheader("OD Pairs (exactly 6 paths required)")
od_cols = st.columns(6)
for i in range(6):
    with od_cols[i]:
        s = st.text_input(f"S{i+1}", st.session_state.od_pairs[i][0], key=f"s_{i}")
        d = st.text_input(f"D{i+1}", st.session_state.od_pairs[i][1], key=f"d_{i}")
        st.session_state.od_pairs[i] = (s, d)

if st.button("🚀 Run Theoretical + Simulation Analysis", type="primary", use_container_width=True):
    G = st.session_state.G
    od_pairs = st.session_state.od_pairs
    
    paths = {}
    for s, d in od_pairs:
        try:
            path = nx.shortest_path(G, s, d, weight='weight')
            travel = nx.shortest_path_length(G, s, d, weight='weight')
            cs_list = [n for n in path if n.startswith('CS')]
            paths[(s,d)] = {'path': path, 'travel': travel, 'cs': cs_list}
        except:
            st.error(f"No path between {s} and {d}. Please connect the network properly.")
            st.stop()
    
    flow_per_od = lambda_total / len(od_pairs)
    
    lambda_k = defaultdict(float)
    for data in paths.values():
        for cs in data['cs']:
            lambda_k[cs] += flow_per_od
    
    theo_results = []
    for cs in sorted(lambda_k.keys()):
        rho = lambda_k[cs] / mu
        wq = rho / (mu * (1 - rho)) if rho < 0.999 else float('inf')
        theo_results.append({
            'Charging Station': cs,
            'Effective λ_k': round(lambda_k[cs], 3),
            'Utilization ρ': round(rho, 3),
            'Avg Waiting Time Wq (min)': round(wq, 3)
        })
    theo_df = pd.DataFrame(theo_results)
    
    class DroneSystem:
        def __init__(self, env, G, paths, mu):
            self.env = env
            self.G = G
            self.paths = paths
            self.mu = mu
            self.cs_servers = {cs: simpy.Resource(env, capacity=1) for cs in lambda_k.keys()}
            self.arrival_counts = {cs: 0 for cs in lambda_k.keys()}
            self.waiting_times = {cs: [] for cs in lambda_k.keys()}
            self.e2e = []
        
        def process(self, s, d):
            start = self.env.now
            data = self.paths[(s, d)]
            path = data['path']
            for i in range(len(path)-1):
                u, v = path[i], path[i+1]
                if v.startswith('CS'):
                    self.arrival_counts[v] += 1
                    arr = self.env.now
                    with self.cs_servers[v].request() as req:
                        yield req
                        wait = self.env.now - arr
                        self.waiting_times[v].append(wait)
                        yield self.env.timeout(random.expovariate(self.mu))
                yield self.env.timeout(self.G.edges[u,v]['weight'])
            self.e2e.append(self.env.now - start)
    
    env = simpy.Environment()
    system = DroneSystem(env, G, paths, mu)
    
    def source(s, d):
        while True:
            yield env.timeout(random.expovariate(flow_per_od))
            env.process(system.process(s, d))
    
    for s, d in od_pairs:
        env.process(source(s, d))
    
    env.run(until=3000)
    
    sim_df = pd.DataFrame({
        'Charging Station': list(system.arrival_counts.keys()),
        'Sim λ_k': [c / env.now for c in system.arrival_counts.values()],
        'Sim Wq (min)': [sum(w)/len(w) if w else 0 for w in system.waiting_times.values()]
    })
    
    comparison = pd.merge(theo_df, sim_df, on='Charging Station', how='left')
    
    st.session_state.comparison = comparison
    st.session_state.bottlenecks = comparison.nlargest(3, 'Utilization ρ')
    st.session_state.avg_e2e_theo = round(sum(
        data['travel'] + sum(comparison[comparison['Charging Station']==cs]['Avg Waiting Time Wq (min)'].values[0] + 1/mu 
                             for cs in data['cs']) * flow_per_od 
        for data in paths.values()) / lambda_total, 3)
    st.session_state.avg_e2e_sim = round(sum(system.e2e) / len(system.e2e), 3)
    st.session_state.fig_net = fig_net
    st.success("Analysis Completed Successfully")
    st.rerun()

# Results
if 'comparison' in st.session_state:
    st.header("Results")
    st.subheader("Bottleneck Charging Stations")
    st.dataframe(st.session_state.bottlenecks.style.highlight_max(axis=0, color='#FFCCCC'), use_container_width=True)
    
    st.subheader("Effective Arrival Rate, Utilization & Waiting Time")
    st.dataframe(st.session_state.comparison.round(3), use_container_width=True)
    
    st.subheader("Average End-to-End Delay per Drone")
    col1, col2 = st.columns(2)
    col1.metric("Theoretical", f"{st.session_state.avg_e2e_theo} minutes")
    col2.metric("Simulation", f"{st.session_state.avg_e2e_sim} minutes")
    
    # Bar graph with exact values (normal font, appropriate size)
    fig_bar, ax_bar = plt.subplots(figsize=(12, 5))
    df_plot = st.session_state.comparison.set_index('Charging Station')
    bars = df_plot[['Avg Waiting Time Wq (min)', 'Sim Wq (min)']].plot(kind='bar', ax=ax_bar)
    ax_bar.set_ylabel("Average Waiting Time (minutes)")
    ax_bar.set_title("Waiting Time Comparison – Bottleneck vs Non-Bottleneck")
    ax_bar.legend(title="Method")
    
    for container in ax_bar.containers:
        ax_bar.bar_label(container, fmt='%.3f', padding=3, fontsize=6.5)   # normal font, good size
    
    st.pyplot(fig_bar, use_container_width=True)
    
    # Download ZIP
    if st.button("📥 Download Complete Project Folder (ZIP)", type="primary", use_container_width=True):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            net_buf = io.BytesIO()
            st.session_state.fig_net.savefig(net_buf, format="png", dpi=300, bbox_inches='tight')
            net_buf.seek(0)
            zip_file.writestr("network_diagram.png", net_buf.read())
            
            bar_buf = io.BytesIO()
            fig_bar.savefig(bar_buf, format="png", dpi=300, bbox_inches='tight')
            bar_buf.seek(0)
            zip_file.writestr("waiting_time_bar_graph.png", bar_buf.read())
            
            csv_buf = st.session_state.comparison.to_csv(index=False).encode("utf-8")
            zip_file.writestr("results.csv", csv_buf)
        
        zip_buffer.seek(0)
        st.download_button(
            label="✅ Download drone_system_results.zip",
            data=zip_buffer,
            file_name="drone_system_results.zip",
            mime="application/zip",
            use_container_width=True
        )

st.caption("Team 8 Project • Final clean version")
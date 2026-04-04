# 🛸 Assessment of Waiting Time in a Multi-Drone Conveyance System
## with Time-Based (Shortest-Time) Path Selection

**TP-8 | Team 8**  
**Advanced Computer Networks Course**  
**Indian Institute of Technology Bhubaneswar**

This term project models a realistic **multi-drone conveyance system** where drones must visit multiple charging stations due to battery constraints. It evaluates the impact of **static shortest-time path routing** (Dijkstra on travel times only) on congestion, waiting time, and overall system performance using **M/M/1 queuing theory** and **discrete-event simulation (SimPy)**.

The system is delivered as a **fully interactive web application** that allows users to build any network topology, run analysis, visualize bottlenecks, and download complete results.

---

# 🚀 Live Demo

**Deployed Application (Streamlit Cloud)**  
👉 https://multi-drone-conveyance-system.streamlit.app/

---

# 📌 Project Objectives

- Quantify **waiting time** and **end-to-end delay** under shortest-time routing  
- Identify **bottleneck charging stations**  
- Compute **effective arrival rate (λ_k)** at each station  
- Compare **theoretical M/M/1 results** with **discrete-event simulation**  
- Provide a fully interactive network builder (no hard-coded topology)

---

# 🧠 System Features

- **Routing**: Shortest-time path using static edge weights (Dijkstra)  
- **Service**: FCFS at every charging station  
- **Queuing Model**: Independent M/M/1 queues  
- **Simulation**: Discrete-event simulation using SimPy  
- **Visualization**: Clean layered graph with curved edges and staggered nodes

**Key Insight**: Deterministic shortest-time routing leads to severe uneven load distribution even though every drone individually chooses the "fastest" path.

---

# 📊 Generated Outputs

- Identification of bottleneck charging stations  
- Effective arrival rate λ_k at each station  
- Average waiting time (bottleneck vs non-bottleneck)  
- Average end-to-end delay per drone (Theoretical + Simulated)  
- Downloadable ZIP containing network diagram, bar graph, and CSV results

---

# 🖥️ Web Application Features

- Start with **completely empty network**  
- One-click buttons to add Sources, Charging Stations, Destinations  
- Draw arrowed connections with travel time  
- **Load Minimal Default Network** button (realistic 6S + 8CS + 6D topology)  
- Real-time layered visualization (Sources left | CS middle | Destinations right)  
- One-click **Theoretical + Simulation Analysis**  
- Bar graph with exact values displayed on bars  
- Download complete project folder as ZIP

---

# 📂 Project Structure

```
multi-drone-conveyance-system/
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore file
├── README.md                   # This documentation
│
├── graph_builder.py            # Graph construction module
├── parameters.py               # Default parameters
├── shortest_path.py            # Shortest-time path computation
├── theoretical_analysis.py     # M/M/1 theoretical calculations
├── simulation.py               # SimPy discrete-event simulation
├── phase1_validate.py          # Phase 1 validation
├── phase2_run.py               # Phase 2 theoretical analysis
├── phase3_run.py               # Phase 3 simulation
│
└── assets/                     # Screenshots (optional)
```

---

# ⚙️ Local Setup

```bash
git clone https://github.com/KondetiAravind/multi-drone-conveyance-system.git
cd multi-drone-conveyance-system

python3 -m venv drone_env
source drone_env/bin/activate        # Windows: drone_env\Scripts\activate

pip install -r requirements.txt
```

---

# ▶️ Run Locally

```bash
streamlit run app.py
```

Open in browser: `http://localhost:8501`

---

# 🌐 Deployment Details

- **Platform**: Streamlit Community Cloud  
- **Repository**: https://github.com/KondetiAravind/multi-drone-conveyance-system  
- **Live URL**: https://multi-drone-conveyance-system.streamlit.app/  
- **Deployment**: Automatic on every push to `main`

---

# 🎯 Key Highlights

- Fully interactive network builder (add/remove nodes and edges)  
- Clean layered visualization with curved paths and staggered nodes  
- Theoretical vs Simulation comparison with high accuracy  
- Professional downloadable results (network diagram + bar graph + CSV)  
- Complete modular codebase for academic transparency

---

# 🧑‍🎓 Academic Context (Term Project – Advanced Computer Networks)

**Course**: Advanced Computer Networks (ACN)  
**Project Number**: TP-8  
**Mentor**: Satwik Mondal

This project demonstrates practical application of:

- Graph algorithms (shortest path)  
- Queuing theory (M/M/1)  
- Discrete-event simulation  
- Performance analysis of real-world drone delivery networks  
- Impact of deterministic routing on congestion

---

# 👥 Team 8

---

# 📜 License

This project is developed for **academic and educational purposes** as part of the Advanced Computer Networks course at IIT Bhubaneswar.

---
---

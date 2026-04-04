import simpy
import random
import pandas as pd
from graph_builder import build_test_graph
from parameters import TOTAL_LAMBDA, MU, OD_PAIRS
from shortest_path import compute_all_shortest_paths

class DroneSystem:
    def __init__(self, env):
        self.env = env
        self.G = build_test_graph()
        self.paths, _ = compute_all_shortest_paths()
        self.cs_servers = {cs: simpy.Resource(env, capacity=1) for cs in [f"CS{i}" for i in range(1,9)]}
        self.arrival_counts = {cs: 0 for cs in self.cs_servers}
        self.waiting_times = {cs: [] for cs in self.cs_servers}
        self.e2e_delays = []

    def drone_process(self, origin, dest):
        start_time = self.env.now
        data = self.paths[(origin, dest)]
        path = data['path']

        for i in range(len(path)-1):
            u = path[i]
            v = path[i+1]

            if 'CS' in v:
                self.arrival_counts[v] += 1
                arrival_ts = self.env.now
                with self.cs_servers[v].request() as req:
                    yield req
                    wait_time = self.env.now - arrival_ts
                    self.waiting_times[v].append(wait_time)
                    service_time = random.expovariate(MU)
                    yield self.env.timeout(service_time)

            # Travel
            travel_time = self.G.edges[u, v]['weight']
            yield self.env.timeout(travel_time)

        self.e2e_delays.append(self.env.now - start_time)

def run_simulation(num_drones=12000, replications=3):
    all_sim_dfs = []
    all_e2e = []

    for rep in range(replications):
        env = simpy.Environment()
        system = DroneSystem(env)

        flow_rate_per_pair = TOTAL_LAMBDA / len(OD_PAIRS)

        def source_process(s, d):
            while True:
                yield env.timeout(random.expovariate(flow_rate_per_pair))
                env.process(system.drone_process(s, d))

        for s, d in OD_PAIRS:
            env.process(source_process(s, d))

        env.run(until=3000)  # sufficient time for ~12000 drones

        # Stats
        sim_time = env.now
        sim_df = pd.DataFrame({
            'Charging Station': list(system.arrival_counts.keys()),
            'Sim λ_k': [count / sim_time for count in system.arrival_counts.values()],
            'Sim Avg Wq (min)': [sum(w)/len(w) if w else 0.0 for w in system.waiting_times.values()]
        })
        avg_e2e = sum(system.e2e_delays) / len(system.e2e_delays) if system.e2e_delays else 0
        all_sim_dfs.append(sim_df)
        all_e2e.append(avg_e2e)

    avg_sim_df = pd.concat(all_sim_dfs).groupby('Charging Station').mean().reset_index()
    avg_e2e = sum(all_e2e) / replications
    return avg_sim_df, round(avg_e2e, 3)

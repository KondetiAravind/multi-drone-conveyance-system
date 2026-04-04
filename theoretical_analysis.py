import pandas as pd
from parameters import TOTAL_LAMBDA, MU, OD_PAIRS
from shortest_path import compute_all_shortest_paths

def run_theoretical_analysis():
    paths, G = compute_all_shortest_paths()
    flow_per_od = TOTAL_LAMBDA / len(OD_PAIRS)
    
    # Effective arrival rate λ_k at each charging station
    lambda_k = {f"CS{i}": 0.0 for i in range(1, 9)}
    for (s, d), data in paths.items():
        for cs in data['cs_visited']:
            lambda_k[cs] += flow_per_od
    
    # M/M/1 metrics
    results = []
    for cs in lambda_k:
        rho = lambda_k[cs] / MU
        wq = rho / (MU * (1 - rho)) if rho < 0.999 else float('inf')
        results.append({
            'Charging Station': cs,
            'Effective λ_k': round(lambda_k[cs], 3),
            'Utilization ρ': round(rho, 3),
            'Avg Waiting Time Wq (min)': round(wq, 3)
        })
    
    df = pd.DataFrame(results)
    
    # Bottlenecks
    bottlenecks = df.nlargest(3, 'Utilization ρ')
    
    # Average end-to-end delay
    total_delay = 0.0
    for (s, d), data in paths.items():
        travel = data['travel_time']
        cs_delay = sum(df[df['Charging Station'] == cs]['Avg Waiting Time Wq (min)'].values[0] + 1/MU 
                      for cs in data['cs_visited'])
        total_delay += (travel + cs_delay) * flow_per_od
    avg_e2e = total_delay / TOTAL_LAMBDA
    
    return df, bottlenecks, round(avg_e2e, 3), paths

if __name__ == "__main__":
    df, bottlenecks, avg_e2e, paths = run_theoretical_analysis()
    print(df.to_string(index=False))
    print("\n=== BOTTLENECK CHARGING STATIONS ===")
    print(bottlenecks.to_string(index=False))
    print(f"\nAverage end-to-end delay per drone: {avg_e2e} minutes")

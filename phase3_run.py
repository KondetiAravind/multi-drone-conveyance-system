import pandas as pd
from simulation import run_simulation

print("=== PHASE 3: DISCRETE-EVENT SIMULATION STARTED ===")
print("Running corrected SimPy simulation...")

sim_df, sim_e2e = run_simulation()

theo_df = pd.read_csv('theoretical_results.csv')

comparison = pd.merge(theo_df[['Charging Station','Effective λ_k','Avg Waiting Time Wq (min)']], 
                      sim_df, on='Charging Station', how='left')
comparison = comparison.rename(columns={
    'Effective λ_k': 'Theo λ_k',
    'Avg Waiting Time Wq (min)': 'Theo Wq',
    'Sim λ_k': 'Sim λ_k',
    'Sim Avg Wq (min)': 'Sim Wq'
})

print("\n=== COMPARISON: Theoretical vs Simulation ===")
print(comparison[['Charging Station','Theo λ_k','Sim λ_k','Theo Wq','Sim Wq']].round(3).to_string(index=False))

print(f"\nAverage end-to-end delay (theoretical): 33.324 min")
print(f"Average end-to-end delay (simulation):   {sim_e2e} min")

comparison.to_csv('theo_vs_sim_comparison.csv', index=False)
print("\nComparison saved to theo_vs_sim_comparison.csv")
print("Phase 3 complete.")

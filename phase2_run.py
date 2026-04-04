from theoretical_analysis import run_theoretical_analysis
import pandas as pd

print("=== PHASE 2: THEORETICAL ANALYSIS STARTED ===")
df, bottlenecks, avg_e2e, paths = run_theoretical_analysis()

print("\nEffective Arrival Rates, Utilizations & Waiting Times:")
print(df.to_string(index=False))

print("\nBottleneck Stations (highest load due to shortest-time routing):")
print(bottlenecks.to_string(index=False))

print(f"\nAverage end-to-end delay per drone (theoretical): {avg_e2e} minutes")

# Save for later use (Phase 4)
df.to_csv('theoretical_results.csv', index=False)
bottlenecks.to_csv('bottlenecks.csv', index=False)
print("\n✅ Results saved: theoretical_results.csv and bottlenecks.csv")
print("Phase 2 complete. Reply 'Proceed to Phase 3' when ready.")

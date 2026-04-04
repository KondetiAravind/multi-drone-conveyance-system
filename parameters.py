TOTAL_LAMBDA = 5.0          # External drone arrival rate (drones/min, Poisson)
MU = 6.0                    # Charging service rate per station (drones/min)
NUM_CS = 8
NUM_SOURCES = 6
NUM_DESTINATIONS = 6
BATTERY_MAX_FLIGHT_TIME = 20  # minutes (assumption)

OD_PAIRS = [
    ("S1", "D1"), ("S2", "D2"), ("S3", "D3"),
    ("S4", "D4"), ("S5", "D5"), ("S6", "D6")
]
